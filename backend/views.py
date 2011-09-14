from django.template import Context, Template, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from wordrank.backend.models import *
from wordrank.backend.choosepair import *
from wordrank.backend.eloscore import *

def index(request):
	pc = PairChooser()
	return render_to_response('index.html',{'word_a':pc.getword(),'word_b':pc.getword()},context_instance=RequestContext(request))
	

def vote(request,word_a,word_b,winner):
	try:
		elo = ELOScore()
		elo.load_word_A(word_a)
		elo.load_word_B(word_b)
		elo.recalculate(winner)
		elo.store()
		return HttpResponseRedirect('/')
	except:
		return HttpResponseRedirect('/')

	
