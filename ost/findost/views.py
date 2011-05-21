from django.shortcuts import get_object_or_404, render_to_response
from findost.models import Film, Show, Episode, Song
from django.template import RequestContext
from django.http import Http404,HttpResponseRedirect


def home(request):
	lastfilms = Film.objects.order_by('-updatedon')[:5]
	lastepisodes = Episode.objects.order_by('-updatedon')[:5]
	if request.user.is_authenticated():
		message="bonjour" + request.user.username
	else:
		message="You are not logged in"
	return render_to_response('findost/home.html', {'lastfilms': lastfilms, 'lastepisodes': lastepisodes, 'message':message})

def showlogin(request):
	if(request.is_ajax()):
		return render_to_response('findost/loginform.html')
	
def login(request):
	username=request.POST['username']
	passwd = request.POST['passwd']
	#verifier qu'il n'y a pas de caracteres speciaux

	user = authenticate(username=username,password=passwd)
	if user is not None:
		if user.is_active:
			login(request, user)
		else:
			pass
			# Return a 'disabled account' error message
	return HttpResponseRedirect('/home')
	
def showsubscribe(request):
	return render_to_response('findost/subform.html')

def subscribe(request):
	username=request.POST['username']
	passwd = request.POST['passwd']
	confpasswd=request.POST['confpasswd']
	mail = request.POST['mail']
	#verifier qu'il n'y a pas de caracteres speciaux
	mailalreadyused = User.objects.filter(email__exact=mail)
	if(mailalreadyused):
		error = 'this mail address is already used by another user'
		return render_to_response('findost/subscribe.html', {'error': error})
	elif(passwd != confpasswd):
		error = "you didn't type twice the same password"
		return render_to_response('findost/subscribe.html', {'error': error})
	else:
		user = User.objects.create_user(username,mail,passwd)
		login(request, user)
		return HttpResponseRedirect('/home')

def search(request,kind):
	if(kind == 'film' or kind == 'show'):
		return render_to_response('findost/search.html', {'kind' : kind}, context_instance=RequestContext(request))
	else:
		raise Http404

def find_results_set(kind,query):
	querywords = []
	temp = ''
	for c in (query + ' '):
		if(c == ' ' and temp != ''):
			querywords.append(temp)
			temp = ''
		else:
			temp = temp + c
	if(kind == 'film'):
		results_set = Film.objects.all()
	if(kind == 'show'):
		results_set = Show.objects.all()
	for w in querywords:
			results_set = results_set.filter(title__contains=w)
	return results_set.order_by('title')[0:20]	


def results(request,kind):
	if((kind == 'film' or kind == 'show') and request.is_ajax()):
		query = request.GET.get('query')
		results_set = find_results_set(kind,query)
		return render_to_response('findost/results.html',{'results_set' : results_set, 'kind' : kind}, context_instance=RequestContext(request))
	else:
		raise Http404

def showdetails(request,id):
	show = get_object_or_404(Show,pk = id)
	nbseason = range(1, show.nbseason+1)
	return render_to_response('findost/showdetails.html',{'show' : show, 'nbseason' : nbseason})

def loadepisodes(request,id):
	if(request.is_ajax()):
		season = request.GET.get('season')
		show = get_object_or_404(Show, pk = id)
		episodes = show.episode_set.all().filter(seasonnb = int(season)).order_by('number')
		return render_to_response('findost/episodelist.html',{'episodes' : episodes})
		
def details(request,kind,id):
	if(kind == 'film'):
		obj = get_object_or_404(Film, pk = id)
	if(kind == 'episode'):
		obj = get_object_or_404(Episode, pk = id)
	return render_to_response('findost/details.html', {'obj' : obj})
