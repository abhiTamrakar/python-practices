from __future__ import division
from flask import Flask, flash, redirect, render_template, request, session, abort
import memcache
import logging
from random import randint

app = Flask(__name__)
 
@app.route("/")
def index():
    return "Index!"

@app.route("/stats")
def get_statics():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    keytext =[ "test1", "test2", "test3", "test4", "test5", "test6" ]
    quotes = [ "DevOps is not about Automation",
               "DevOps is not about CI/CD",
	       "DevOps is created to add scalability and HA to the environment",
	       "DevOps has an advantage with Automation",
	       "Automation and CI/CD adds value to DevOps as tools" ]
    randomNumber = randint(0,len(quotes)-1)
    quote = quotes[randomNumber]
    randomNumber2 = randint(0,len(keytext)-1)
    keyed = keytext[randomNumber2]
    this_quote = mc.get(keyed)
    if not this_quote:
        this_quote = quote
        set_it = mc.set(keyed, this_quote, time=360)
        if not set_it:
                logging.error('Memcache set failed.')
    stats = mc.get_stats()
    get_data = stats[0]
    data = get_data[1]
    ghits = '{}'.format(data['get_hits'])
    gmisses = '{}'.format(data['get_misses'])
    gmiss = int(gmisses)
    ghit = int(ghits)
    total_gets = ghit + gmiss
    percentage_miss = round(gmiss / total_gets * 100, 2)
    
    return render_template(
        'test.html',**locals())

if __name__ == "__main__":
    app.run()
