from models import *
from mongoengine import *
import random

class PairChooser(object):
	def __init__(self):
		connect('wordrank')
	def getword(self):
		random.seed()
		return random.choice(Word.objects(random__gte=random.random())).word
	def getpair(self):
		random.seed()
		return (self.getword(),self.getword())

