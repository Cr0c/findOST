from django.shortcuts import get_object_or_404, render_to_response
from findost.models import Film, Show, Episode, Song, Artist,Actor
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import urllib2,string,datetime



def contains_or_is_contained(str1, str2):
  return (str1.find(str2) > -1 or str2.find(str1) > -1)

def cleaned(str):
	notspace = True
	cstr = ''
	for c in str:
		if (c not in string.letters and c not in string.digits):			
			if(notspace):
				cstr = cstr + " "
				notspace = False

		elif(notspace or c != " "):
			cstr = cstr + c
			notspace = True
	return cstr.upper()

def home(request):
	lastfilms = Film.objects.order_by('-updatedon')[:5]
	lastepisodes = Episode.objects.order_by('-updatedon')[:5]
	isauth = request.user.is_authenticated()
	path = request.path
	if isauth:
		message="You are logged in as " + request.user.username
	else:
		message="You are not logged in"
	return render_to_response('findost/home.html', {'lastfilms': lastfilms, 'lastepisodes': lastepisodes, 'message': message, 'isauth': isauth, 'path' : path}, context_instance=RequestContext(request))

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
	elif(len(username) > 12):
		error = "Your username is too long! (12 characters maximum)"
		return render_to_response('findost/subform.html', {'error': error}, context_instance=RequestContext(request))
	elif(len(passwd) < 6):
		error = "Your password is too short! (6 charatcers minimum)"
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
	if(isauth):
		message = "Logged in as " + request.user.username
	else:
		message = "You are not logged in"
	if(kind == 'film' or kind == 'show'):
		return render_to_response('findost/search.html', {'kind' : kind, 'isauth':isauth, 'path' : path, 'message':message}, context_instance=RequestContext(request))
	else:
		raise Http404

def find_results_set(query):
	querywords = []
	temp = ''
	for c in (query + ' '):
		if(c == ' ' and temp != ''):
			querywords.append(temp)
			temp = ''
		else:
			temp = temp + c
	results_setMovie = Film.objects.all()
	results_setShow = Show.objects.all()
	for w in querywords:
		results_setMovie = results_setMovie.filter(title__contains=w)
		results_setShow = results_setShow.filter(title__contains=w)
	results_setMovie = Film.objects.filter(title__contains=query).update(results_setMovie)
	results_setShow = Show.objects.filter(title__contains=query).update(results_setShow)
	return results_setMovie[0:20], results_setShow[0:20]


def results(request):
	if request.is_ajax():
		query = request.GET.get('query')
		results_setMovie, results_setShow= find_results_set(query)
		return render_to_response('findost/results.html',{'results_setMovie' : results_setMovie, 'results_setShow' : results_setShow}, context_instance=RequestContext(request))
	else:
		raise Http404

def showdetails(request,id):
	path = request.path
	isauth = request.user.is_authenticated()
	if(isauth):
		message = "Logged in as " + request.user.username
	else:
		meggae = ''
	show = get_object_or_404(Show,pk = id)
	nbseason = range(1, show.nbseason+1)
	return render_to_response('findost/showdetails.html',{'show' : show, 'nbseason' : nbseason, 'isauth':isauth, 'path' : path, 'message':message})

def loadepisodes(request,id):
	if(request.is_ajax()):
		season = request.GET.get('season')
		show = get_object_or_404(Show, pk = id)
		episodes = show.episode_set.all().filter(seasonnb = int(season)).order_by('number')
		return render_to_response('findost/episodelist.html',{'episodes' : episodes})
		
def details(request,kind,id):
	path = request.path
	isauth = request.user.is_authenticated()
	if(isauth):
		message = "Logged in as " + request.user.username
	else:
		message =''
	if(kind == 'film'):
		obj = get_object_or_404(Film, pk = id)
	if(kind == 'episode'):
		obj = get_object_or_404(Episode, pk = id)
	return render_to_response('findost/details.html', {'obj' : obj, 'isauth':isauth, 'path' : path, 'message':message})

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
		
def checktrack(request,kind,gid,id):
	if(request.is_ajax()):
		file = open('../DB/ids','a')
		song = get_object_or_404(Song, pk = id)
		modtitle = ''
		modartist = ''	
		title = song.title.encode('iso-8859-1')
		for c in title:
			if(c == " "):modtitle = modtitle + "+"
			if(c == "%"):modtitle = modtitle + "+percent+"				
			else: modtitle = modtitle + c	
		artist = song.artist.name.encode('iso-8859-1')
		for c in artist:
			if(c == " "): modartist = modartist + "+"
			if(c == "%"): modartist = modartist + "+percent+"
			else: modartist = modartist + c
		request = "http://tinysong.com/s/"+ modtitle+"+"+modartist+"?format=json&limit=5&key=b3fa54409e286bd0192b9c2966767482"
		Json=urllib2.urlopen(request).read()
		i=0
		while(i<5):
			if (Json != '[]' and Json[1] == '{'):
				ind = Json.index("SongID") + 8
				songid = ''
				while (Json[ind] != ","):
					songid = songid + Json[ind]
					ind = ind+1
				ind = Json.index("SongName") + 11
				songtitle = ''
				while (Json[ind] != '"'):
					songtitle = songtitle + Json[ind]
					ind = ind + 1
				if (contains_or_is_contained(cleaned(song.title),cleaned(songtitle))):
					song.songid = int(songid)
					song.save()
					file.write(song.title + "_|_" + song.artist.name + "_|_" + songid + "\n")
					i=6
				else:
					while(Json[ind] != '}'):
						ind =ind+1
					ind=ind+1
					Json=Json[ind:]
					if(Json[0] == ','):
						i=i+1
					else:
						i=5
			else:
				i=5
		if(i==5):
			song.songid=-1
			song.save()
		file.close()
		return render_to_response('findost/checktrackok.html',{'songid':song.songid})
	else:
		raise Http404

def normalize(string):
	words = []
	temp = ''
	for c in (string + ' '):
		if(c == ' ' and temp != ''):
			words.append(temp)
			temp = ''
		elif (c != ' '):
			temp = temp + c
	normstr = ''	
	for word in words:
		word = word[0].upper() + word[1:].lower()
		normstr = normstr +  ' ' + word
	return normstr[1:]	

def savechanges(request,kind,id):
	isauth = request.user.is_authenticated()
	if(isauth):			
		if(kind == 'film'):
			obj = get_object_or_404(Film, pk = id)	
			obj.mainactors.clear()
		if(kind == 'episode'):
			obj = get_object_or_404(Episode, pk = id)
			obj.show.mainactors.clear()
		
		obj.songs.clear()	

		data = request.POST
		songartists = {}
		songtitles = {}

		for key in data:
			value = data[key]
			value = normalize(value)
			print('key : ' + key + ' /value : ' + value)
			for field in obj._meta.fields:
				if(key == field.name and value):
					obj.__setattr__(field.name , value)
				if(key.startswith('actor') and value):
					if(Actor.objects.filter(name=value)):
						actor = Actor.objects.filter(name=value)[0]
					else:
						actor = Actor(name = value)
						actor.save()
					if(kind == 'film'):
						obj.mainactors.add(actor)
					if(kind == 'episode'):
						obj.show.mainactors.add(actor)
			if(key=='yearout' and value):
				obj.cameouton=datetime.datetime(int(value),1,1)
			if(key.startswith('songtitle') and value):
				songtitles[key[9:]] = value
			if(key.startswith('songartist') and value):
				songartists[key[10:]] = value
			
		for key in songtitles:
			title = songtitles[key]
			artistname = songartists[key]
			if(Artist.objects.filter(name=artistname)):
				artist = Artist.objects.get(name=artistname)
			else:
				artist = Artist(name=artistname)
				artist.save()
			if(Song.objects.filter(title=title).filter(artist = artist)):
				song=Song.objects.filter(title=title).filter(artist = artist)[0]
			else:
				song = Song(title=title,artist=artist,postedby=request.user.username)
				song.save()
			
			obj.songs.add(song)
			obj.updatedon=datetime.datetime.now()
		obj.save()
		return HttpResponseRedirect('/findost/' + kind + '/details/' + id) 
	else:
		raise Http404		
		
	


	

