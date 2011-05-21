from django.shortcuts import get_object_or_404, render_to_response
from findost.models import Film, Show, Episode, Song
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout



def home(request):
	lastfilms = Film.objects.order_by('-updatedon')[:5]
	lastepisodes = Episode.objects.order_by('-updatedon')[:5]
	isauth = request.user.is_authenticated()
	path = request.path
	if isauth:
		message="Bonjour " + request.user.username
	else:
		message="You are not logged in"
	return render_to_response('findost/home.html', {'lastfilms': lastfilms, 'lastepisodes': lastepisodes, 'message': message, 'isauth': isauth, 'path' : path})

def showlogin(request):
	path = request.GET['path']
	if(request.is_ajax()):
		return render_to_response('findost/loginform.html', {'path': path}, context_instance=RequestContext(request))
	
def log_in(request):
	username=request.POST['username']
	passwd = request.POST['passwd']
	path = request.POST['path']
	#verifier qu'il n'y a pas de caracteres speciaux

	user = authenticate(username=username,password=passwd)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(path)
		else:
			pass
			# Return a 'disabled account' error message
	else:
		return render_to_response('findost/loginerror.html', {'path' : path}, context_instance=RequestContext(request))		
	

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/home')
	
def showsubscribe(request):
	return render_to_response('findost/subform.html', context_instance=RequestContext(request))


def subscribe(request):
	username=request.POST['username']
	passwd = request.POST['passwd']
	confpasswd=request.POST['confpasswd']
	mail = request.POST['mail']
	#verifier qu'il n'y a pas de caracteres speciaux
	mailalreadyused = User.objects.filter(email__exact=mail)
	namealreadyused = User.objects.filter(email__exact=username)
	if(mailalreadyused):
		error = 'this mail address is already used by another user'
		return render_to_response('findost/subform.html', {'error': error}, context_instance=RequestContext(request))
	elif(namealreadyused):
		error = 'this username is already used'
		return render_to_response('findost/subform.html', {'error': error}, context_instance=RequestContext(request))
	elif(passwd != confpasswd):
		error = "you didn't type twice the same password"
		return render_to_response('findost/subform.html', {'error': error}, context_instance=RequestContext(request))
	else:
		User.objects.create_user(username,mail,passwd)
		user = authenticate(username=username,password=passwd)
		login(request, user)
		return HttpResponseRedirect('/home')

def search(request,kind):
	path = request.path
	isauth = request.user.is_authenticated()
	if(kind == 'film' or kind == 'show'):
		return render_to_response('findost/search.html', {'kind' : kind, 'isauth':isauth, 'path' : path}, context_instance=RequestContext(request))
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
	path = request.path
	isauth = request.user.is_authenticated()
	show = get_object_or_404(Show,pk = id)
	nbseason = range(1, show.nbseason+1)
	return render_to_response('findost/showdetails.html',{'show' : show, 'nbseason' : nbseason, 'isauth':isauth, 'path' : path})

def loadepisodes(request,id):
	if(request.is_ajax()):
		season = request.GET.get('season')
		show = get_object_or_404(Show, pk = id)
		episodes = show.episode_set.all().filter(seasonnb = int(season)).order_by('number')
		return render_to_response('findost/episodelist.html',{'episodes' : episodes})
		
def details(request,kind,id):
	path = request.path
	isauth = request.user.is_authenticated()
	if(kind == 'film'):
		obj = get_object_or_404(Film, pk = id)
	if(kind == 'episode'):
		obj = get_object_or_404(Episode, pk = id)
	return render_to_response('findost/details.html', {'obj' : obj, 'isauth':isauth, 'path' : path})

def edit(request,kind,id):
	isauth = request.user.is_authenticated()
	if(isauth):
		if(kind == 'film'):
			obj = get_object_or_404(Film, pk = id)	
		if(kind == 'episode'):
			obj = get_object_or_404(Episode, pk = id)
		return render_to_response('findost/editform.html', {'obj' : obj}, context_instance=RequestContext(request))
	else:
		raise Http404

def savechanges(request,kind,id):
	if(kind == 'film'):
		obj = get_object_or_404(Film, pk = id)	
	if(kind == 'episode'):
		obj = get_object_or_404(Episode, pk = id)
	data = request.POST
	for key,value in data:
		if(key='title' and value):
			obj.title = value
		if(key='otitle' and value):
			obj.otitle = value
		if(key='director' and value):
			obj.director = value
	raise Http404		
		
		
	


	

