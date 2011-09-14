from models import *
from mongoengine import *
class ELOScore(object):
	def __init__(self):
		self.connection = connect("wordrank")
		self.K_VALUE = 20
		self.WIN = 1
		self.LOSE = 0
		self.DRAW = 0.5
		
	def load_word_A(self,_word):
		self.wordA  = Word.objects.filter(word=_word).first()


        def load_word_B(self,_word):
                self.wordB  = Word.objects.filter(word=_word).first()
	
	def recalculate(self,winner):
		if (winner == 'A'):
			self.wordA.score = self.wordA.score + (self.K_VALUE * (self.WIN - self.calc_win_P(winner)))
			self.wordB.score = self.wordB.score - (self.K_VALUE * (self.WIN - self.calc_win_P(winner)))
		else:
			self.wordB.score = self.wordB.score + (self.K_VALUE * (self.WIN - self.calc_win_P(winner)))
			self.wordA.score = self.wordA.score - (self.K_VALUE * (self.WIN - self.calc_win_P(winner)))
		
	def calc_win_P(self,winner):
		score = 0
		if (winner=='A'):
			score = 1 / ( 10**(( self.wordA.score - self.wordB.score)/400)+1)
		else:
			score = 1 / ( 10**(( self.wordB.score - self.wordA.score)/400)+1)
		return score

	def store(self):
		self.wordA.save()
		self.wordB.save()

