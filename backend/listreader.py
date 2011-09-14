#!/usr/bin/env python
import os
import sys
sys.path.append('/home/tom/Projects')

os.environ['DJANGO_SETTINGS_MODULE'] = 'wordrank.settings'
import django

import time
import re
import pprint
from django.conf import settings
from models import *
from mongoengine import *
import random
connect('wordrank')

STOPWORDS  = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your',]

def saveData(status):
	tokens = status.lstrip().rstrip().split(' ')
	for t in tokens:
		if "@" in t:
			print "Username found %s" %t
			continue
		if t in STOPWORDS:
			print "Stopword found %s" %t
			continue
		if "http" in t:
			print "URL Found: %s" %t
			continue
		w = Word(word=t,random=random.random())	
		w.save()
	return True

if __name__ == "__main__":
	try:
		word_count =0
		reader = open(sys.argv[1])
		for line in reader:
			saveData(line)	
			word_count += 1
		print "All %d words processed" % word_count
	except:
		sys.exit()
