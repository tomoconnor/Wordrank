#!/usr/bin/env python
import os
import sys
import tweepy
import pickle
import StringIO
from amqplib import client_0_8 as amqp
from multiprocessing import Pool,Process
import simplejson
import pprint

pp = pprint.PrettyPrinter(indent=4)

pool = Pool(processes=4)

def obj_to_str(obj):
        o = StringIO.StringIO()
        p = pickle.Pickler(o)
        p.dump(obj)
        return o.getvalue()


def process_tweet(status):
	conn = amqp.Connection(host="localhost:5672", userid="spotifind", password="musicb0x", virtual_host="/spotifind", insist=False)
	chan = conn.channel()
	status.__dict__['_api'] = None
	status.user = status.user.screen_name
	status.author = [status.author.screen_name,status.author.id]
	#pp.pprint(status.__dict__)
	msg = amqp.Message(obj_to_str(status.__dict__))
	msg.properties["delivery_mode"] = 2
	chan.basic_publish(msg,exchange="dataxchange",routing_key="tweet")
	print "RMQ Send Event"
	chan.close()
	conn.close()

def callback(status):
	pool.apply_async(process_tweet,[status])

class StreamWatcherListener(tweepy.StreamListener):
	def on_status(self, status):
		print "0"
		if __name__ == '__main__':
			Process(target=process_tweet,args=(status,)).start()
			print "1"

		#print status.author.screen_name
		#print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
		return True

	def on_error(self, status_code):
        	print 'An error has occured! Status code = %s' % status_code
	        return True  # keep stream alive

	def on_timeout(self):
		print 'Snoozing Zzzzzz'


def main():
    # Prompt for login credentials and setup stream object
#auth = tweepy.BasicAuthHandler("dev_astound","F37ce5f1882%")
	username = 'dev_astound' 
	password = 'F37ce5f1882%'
	stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
	follow_list = []
	track_list = []

        #stream.filter(follow_list, track_list)
	stream.sample()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
	chan.close()
	conn.close()
