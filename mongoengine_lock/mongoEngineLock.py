"""
Implement pessimistic lock using mongoengine.

"""
import os
from datetime import datetime, timedelta
from mongoengine import *
import contextlib

class LockTimeout(Exception):
   pass

class Locks(Document):
    ts = DateTimeField(default=datetime.utcnow(), required=True, unique=True)
    locked = BooleanField(default=False, required=True)
    owner = StringField(required=True)
    meta = {
       'collection': 'mongoengine.lock',
       'indexes': [
           {
               'fields': ['ts'],
               'expireAfterSeconds': 10
           },
           {
               'fields': ['owner'],
               'unique': False
           }
       ]
    }

class mongoEngineLock(object):
    def __init__(self, client=None, dbname='mongoenginelocks', poll=0.1):
        if client:
           self.client = client
        else:
           self.client = 'db='+ dbname + ', username=' + '' + 'password=' + '' + 'host=localhost'
        
        self.poll = poll
        connect(client)

    @contextlib.contextmanager
    def __call__(self, owner, retries=5):
        if not self.lock(owner, retries):
           status = self._get_lockinfo(owner)
           raise LockTimeout(
              u'timedout, lock owned by {owner}, since {ts}. Please try after sometime.'.format(
                 owner=status['owner'], ts=status['ts']
              )
           )
        try:
           yield
        finally:
           self.release(owner) 

    def lock(self, owner, retries):
        _retry_step = 0
        _now = datetime.utcnow()
        while True:
           if not locked_by(owner):
              data = Locks(
                 'ts': now,
                 'owner': owner,
                 'locked': True
              )
              data.save()

              return True

           if _retry_step == self.retries:
              return False

           _retry_step+=1
           time.sleep(self.poll)

    def locked_by(owner):
        status = Locks.objects(owner__exact=owner).count()

        return True if status == 1 else False

    def _get_lockinfo(owner):

        return Locks.objects(owner__exact=owner)

    def release(owner):
        status = Locks.objects(owner__exact=owner).delete()

        return True if status == 1 else False
