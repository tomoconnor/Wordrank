from mongoengine import *
class Word(Document):
	word = StringField(max_length=255,required=True)
	random = FloatField()
	score = IntField(default=1600)

class UserWord(EmbeddedDocument):
	r_word = ReferenceField(Word)
	winner = BooleanField()

class User(Document):
	y_chromosome = BooleanField()
	number_ranked = IntField(default=0)
	words_ranked = ListField(EmbeddedDocumentField(UserWord))
