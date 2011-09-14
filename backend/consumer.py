#!/usr/bin/env python
import os
import sys
sys.path.append('/home/tom/Projects')

os.environ['DJANGO_SETTINGS_MODULE'] = 'wordrank.settings'
import django

import time
import tweepy
import re
import pprint
from django.conf import settings
from models import *
from multiprocessing import Pool,Process

from amqplib import client_0_8 as amqp
import pickle
import StringIO
from mongoengine import *

connect('wordrank')

STOPWORDS  = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your',]
def repost(msg):
        msg.properties["delivery_mode"] = 2
        chan.basic_publish(msg,exchange="failxchange",routing_key="failedtweet")

def str_to_obj(magic):
        inp = StringIO.StringIO(magic)
        upk = pickle.Unpickler(inp)
        return upk.load()

def saveData(status):
	tokens = status['text'].split(' ')
	for t in tokens:
		if "@" in t:
			continue
		if t in STOPWORDS:
			continue
		if "http" in t:
			continue
		print t	
		w = Word(word=t)	
		w.save()
		print "Data Saved!"
	return True

def recv_callback(msg):
	print "RMQ Received"
	try:
		saveData(str_to_obj(msg.body))	
	except:
		try:
			print "trying again..."
			saveData(str_to_obj(msg.body))
		except Exception, e:
			print "Something wrong, not saved"
			print e
			sys.exit()
def mainloop():
	try:
		conn = amqp.Connection(host="localhost:5672", userid="spotifind", password="musicb0x", virtual_host="/spotifind", insist=False)
		chan = conn.channel()

		chan.queue_declare(queue="tweets", durable=True, exclusive=False, auto_delete=False)
		chan.queue_declare(queue="failedtweets", durable=True, exclusive=False, auto_delete=False)
		chan.exchange_declare(exchange="dataxchange", type="direct", durable=True, auto_delete=False,)

		chan.exchange_declare(exchange="failxchange", type="direct", durable=True, auto_delete=False,)

		chan.queue_bind(queue="tweets", exchange="dataxchange", routing_key="tweet")
		chan.queue_bind(queue="failedtweets", exchange="failxchange", routing_key="failedtweet")

		chan.basic_consume(queue='tweets', no_ack=True, callback=recv_callback, consumer_tag="tweet")
		while True:
			chan.wait()
		chan.basic_cancel("tweet")
	except KeyboardInterrupt:
		print '\nGoodbye!'
		chan.close()
		conn.close()
	except:
		sys.exit()
if __name__ == "__main__":
	try:
		mainloop()
	except:
		sys.exit()
