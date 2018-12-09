"""
Implement pessimistic lock using mongoengine.

"""
import time
from datetime import datetime
from mongoengine import connect
from mongoengine.queryset.visitor import Q
import contextlib

class MongoLockTimeout(Exception):
   pass

class MongoCollectionLocked(Exception):
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
    def __init__(self, client=None, dbname=None, poll=0.1):
        if client:
           self.client = client
        else:
           if dbname:
              self.dbname = dbname
           else:
              self.dbname = 'mongolocks' 

           self.client = 'db='+ self.dbname + ', username=' + '' + 'password=' + '' + 'host=localhost'
        
        self.poll = poll
        connect(self.client)

    @contextlib.contextmanager
    def __call__(self, owner, retries=5):
        if not self.lock(owner, retries):
           status = self._get_lockinfo(owner)
           raise MongoLockTimeout(
              u'timedout, lock owned by {owner}, since {ts}. Please try after sometime.'.format(
                 owner=status['owner'], ts=status['ts']
              )
           )
        try:
           yield
        finally:
           self.release(owner) 

    def lock(self, owner, retries):
        _retry_step = 1
        _now = datetime.utcnow()
        while True:
           try:
              if not self.isLocked():
                 data = Locks(
                    'ts': _now,
                    'owner': self.owner,
                    'locked': True
                 )
                 data.save()

                 return True
              else:
                 raise MongoCollectionLocked('Error: DB has a write lock by another user, retrying self..')

           except MongoCollectionLocked:
              if _retry_step == self.retries:
                 return False

              _retry_step+=1
              time.sleep(self.poll)

    def isLocked():
        status = Locks.objects(locked__exact=True).count()

        return True if status == 1 else False

    def _get_lockinfo(owner):

        return Locks.objects(owner__exact=owner)

    def release(owner):
        status = Locks.objects(owner__exact=owner).delete()

        return True if status == 1 else False
