from django.shortcuts import get_object_or_404, render_to_response
from findost.models import Film, Show, Episode, Song, Artist,Actor,Comment
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
		message="Logged in as " + request.user.username
	else:
		message="You are not logged in"
	return render_to_response('findost/home.html', {'lastfilms': lastfilms, 'lastepisodes': lastepisodes, 'message': message, 'isauth': isauth, 'path' : path}, context_instance=RequestContext(request))

def showlogin(request):
	if(request.is_ajax() and request.method == 'GET'):
		path = request.GET['path']
		return render_to_response('findost/loginform.html', {'path': path}, context_instance=RequestContext(request))
	else:
		raise Http404
	
def log_in(request):
	if(request.method == 'POST'):
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
	else:		
		raise Http404

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/home')
	
def showsubscribe(request):
	return render_to_response('findost/subform.html', context_instance=RequestContext(request))


def subscribe(request):
	if(request.method == 'POST'):
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
	else:
		raise Http404

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
	if(results_setMovie.filter(title__contains=query)):
		results_setMovie = results_setMovie.filter(title__contains=query)
	else:
		for w in querywords:
			results_setMovie = results_setMovie.filter(title__contains=w)
	
	if(results_setShow.filter(title__contains=query)):
		results_setShow = results_setShow.filter(title__contains=query)
	else:
		for w in querywords:
			results_setShow = results_setShow.filter(title__contains=w)
	return results_setMovie.order_by('title')[0:20], results_setShow.order_by('title')[0:20]


def results(request):
	if (request.is_ajax() and request.method == 'GET'):
		isauth = request.user.is_authenticated()
		query = request.GET.get('query')
		results_setMovie, results_setShow= find_results_set(query)
		return render_to_response('findost/results.html',{'results_setMovie' : results_setMovie, 'results_setShow' : results_setShow, 'isauth' : isauth, 'newtitle' : query}, context_instance=RequestContext(request))
	else:
		raise Http404

def showdetails(request,id):
	path = request.path
	isauth = request.user.is_authenticated()
	if(isauth):
		user = request.user.username
		message = "Logged in as " + user
	else:
		message = 'You are not logged in'
		user = None
	show = get_object_or_404(Show,pk = id)
	nbseason = range(1, show.nbseason+1)
	return render_to_response('findost/showdetails.html',{'show' : show, 'nbseason' : nbseason, 'isauth':isauth, 'user':user, 'path' : path, 'message':message},context_instance=RequestContext(request))

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
		user = request.user.username
		message = "Logged in as " + user
	else:
		message ='You are not logged in'
		user = None
	if(kind == 'film'):
		obj = get_object_or_404(Film, pk = id)
	if(kind == 'episode'):
		obj = get_object_or_404(Episode, pk = id)
	comments = obj.comment_set.order_by('-postedon')
	return render_to_response('findost/details.html', {'comments' : comments, 'obj' : obj, 'isauth':isauth, 'user':user, 'path' : path, 'message':message},context_instance=RequestContext(request))

def edit(request,kind,id):
	newtitle = request.GET.get('title')
	isauth = request.user.is_authenticated()
	if(isauth):
		message = "Logged in as " + request.user.username
		if(kind == 'film'):
			if(id != '0'):
				obj = get_object_or_404(Film, pk = id)
				message2 ="Edit movie"
			else:
				obj=Film(title=newtitle, updatedon=datetime.datetime.now())
				obj.save()
				message2 = "Fill in the information of the movie you want to add"
			return render_to_response('findost/editfilmform.html', {'id' : id, 'message2' : message2, 'message' : message, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))	
		if(kind == 'episode'):
			if(id != '0'):
				obj = get_object_or_404(Episode, pk = id)
				message2="Edit episode"
			else:
				obj=Episode(number=1,seasonnb=1)
				s = Show(title=newtitle)
				s.save()
				obj.show = s
				obj.updatedon=datetime.datetime.now()
				obj.save()
				message2 = "Fill in the information of the show you want to add"
			return render_to_response('findost/editepisodeform.html', {'id' : id, 'message':message, 'message2' : message2, 'obj' : obj, 'isauth' : isauth},context_instance=RequestContext(request))
	else:
		raise Http404

def cancel(request,kind,id):
	isauth = request.user.is_authenticated()
	if(isauth and id == '0' and request.method == 'POST'):
		objid=request.POST['objid']
		if(kind == 'episode'):
			obj = get_object_or_404(Episode, pk = objid)
			obj.show.delete()
		if(kind == 'film'):
			obj = get_object_or_404(Film, pk = objid)
		obj.delete()
		return HttpResponseRedirect('/home')
	else:
		raise Http404		

def checktrack(request,kind,gid,id):
	isauth = request.user.is_authenticated()
	if(isauth):
		user = request.user.username
	else:
		user=None

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
		if(artist == 'Unknown'):
			modartist = ''
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
		return render_to_response('findost/checktrackok.html',{'id':gid, 'song': song, 'user':user, 'isauth':isauth})
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
			return savechangesfilm(request,kind,id)
		if(kind == 'episode'):
			return savechangesepisode(request,kind,id)
	else:
		raise Http404

def savechangesepisode(request,kind,id):
	isauth = request.user.is_authenticated()
	showtitle=''
	number = ''
	seasonnb= ''
	if(isauth and request.method == 'POST'):
		message="You are logged in as " + request.user.username
		objid=request.POST['objid']
		obj = get_object_or_404(Episode, pk = int(objid))
		obj.show.mainactors.clear()
		obj.songs.clear()	
	
		data = request.POST	
		songartists = {}
		songtitles = {}
			
		for key in data:
			value = data[key]
			if(key != 'imageurl'):
				value = normalize(value)
			for field in obj._meta.fields:
				if(key == field.name and value):
					obj.__setattr__(field.name , value)
			

			if(key=='showstatus' and value):
				if(value == 'True'):
					obj.show.status=True
				else:
					obj.show.status=False		
				if(key.startswith('actor') and value):
					if(Actor.objects.filter(name=value)):
						actor = Actor.objects.filter(name=value)[0]
					else:
						actor = Actor(name = value)
					actor.save()
					obj.show.mainactors.add(actor)
	
			for field in obj.show._meta.fields:	
				if(key == field.name and value):
					obj.show.__setattr__(field.name , value)	





			if(key=='number'):
				number=value
			if(key=='seasonnb'):
				seasonnb=value
			if(key=='showtitle' and value):
				obj.show.title=value
				showtitle = value


			if(key.startswith('songtitle') and value):
				songtitles[key[9:]] = value
			if(key.startswith('songartist')):
				songartists[key[10:]] = value	

		for key in songtitles:
			title = songtitles[key]
			if (songartists[key]):
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
			
			else:
				if(Song.objects.filter(title=title)):
					song=Song.objects.filter(title=title)[0]
				else:
					artist = Artist.objects.filter(name='Unknown')[0]
					song = Song(title=title,artist=artist,postedby=request.user.username)
					song.save()
			
			obj.songs.add(song)
		
		
			

		if(showtitle and number and seasonnb):
			if(Show.objects.filter(title=showtitle)):
				show = Show.objects.filter(title=showtitle)[0]
			else:
				show = obj.show	
			
			if(not show.nbseason or int(show.nbseason) < int(obj.seasonnb)):
				show.nbseason = obj.seasonnb
			else:
				show.nbseason = obj.seasonnb
			if(show.episode_set.filter(number=number).filter(seasonnb=seasonnb)):
				obj2 = show.episode_set.filter(number=number).filter(seasonnb=seasonnb)[0]
				if(obj.id == obj2.id):
					obj.show.save()
					obj.updatedon=datetime.datetime.now()	
					obj.save()
					return HttpResponseRedirect('/findost/' + kind + '/details/' + str(obj.id)) 	
				else:
					if(id == '0'):
						obj.show.delete()					
						obj.delete()
						obj = obj2
						message2 = "the episode you want to update is already in database : add your changes here"
						return render_to_response('findost/editepisodeform.html', {'message' : message , 'message2' : message2, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))	
					else:
						obj = obj2
						message2 = "the episode you want to update is already in database : add your changes here"
						return render_to_response('findost/editepisodeform.html', {'message' : message , 'message2' : message2, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))								
			else:
				print str(obj.show.id)				
				showtemp = obj.show
				obj.show = show
				if(Show.objects.filter(title=showtitle)):
					showtemp.delete()
				print str(obj.show.id)				
				obj.show.save()
				obj.updatedon=datetime.datetime.now()
				obj.save()
				return HttpResponseRedirect('/findost/' + kind + '/details/' + str(obj.id)) 
		
		else:
			if( not showtitle):
				message2="please fill in the Show title"
			elif (not number):
				message2="please fill in the Episode number"
			else:
				message2="please fill in the Episode Season number"						
			return render_to_response('findost/editepisodeform.html', {'message' : message, 'message2' : message2, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))	
	else:
		raise Http404	

def savechangesfilm(request,kind,id):
	isauth = request.user.is_authenticated()
	if(isauth and request.method == 'POST'):
		message="You are logged in as " + request.user.username
		objid=request.POST['objid']
		obj = get_object_or_404(Film, pk = int(objid))
		obj.mainactors.clear()
		obj.songs.clear()	
		
		data = request.POST
		songartists = {}
		songtitles = {}
		title=''
		yearout=''	
		for key in data:
			value = data[key]
			if(key != 'trailerurl' and key != 'imageurl'):
				value = normalize(value)
			for field in obj._meta.fields:
				if(key == field.name and value):					
					obj.__setattr__(field.name , value)
				if(key.startswith('actor') and value):
					if(Actor.objects.filter(name=value)):
						actor = Actor.objects.filter(name=value)[0]
					else:
						actor = Actor(name = value)
					actor.save()	
					obj.mainactors.add(actor)
			if(key=='title'):
				title=value
			if(key=='yearout'):
				yearout=value	
			
			if(key.startswith('songtitle') and value):
				songtitles[key[9:]] = value
			if(key.startswith('songartist')):
				songartists[key[10:]] = value		

		for key in songtitles:
			title = songtitles[key]
			if (songartists[key]):
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
			
			else:
				if(Song.objects.filter(title=title)):
					song=Song.objects.filter(title=title)[0]
				else:
					artist = Artist.objects.filter(name='Unknown')[0]
					song = Song(title=title,artist=artist,postedby=request.user.username)
					song.save()
			
			obj.songs.add(song)

		if(title and yearout):
			if(Film.objects.filter(title=title).filter(cameouton=yearout)):
				obj2 = Film.objects.filter(title=title).filter(cameouton=yearout)[0]
				if(obj.id == obj2.id):
					obj.updatedon=datetime.datetime.now()	
					obj.cameouton=int(yearout)
					obj.save()
					return HttpResponseRedirect('/findost/' + kind + '/details/' + str(obj.id)) 	
				else:
					if(id == '0'):					
						obj.delete()
						obj = obj2
						message2 = "the movie you want to update is already in database : add your changes here"
						return render_to_response('findost/editfilmform.html', {'message' : message , 'message2' : message2, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))	
					else:
						obj = obj2
						message2 = "the movie you want to update is already in database : add your changes here"
						return render_to_response('findost/editfilmform.html', {'message' : message , 'message2' : message2, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))								
			else:
				obj.updatedon=datetime.datetime.now()		
				obj.cameouton=int(yearout)
				obj.save()
				return HttpResponseRedirect('/findost/' + kind + '/details/' + str(obj.id)) 
		else:
			if(title):
				message2="please fill in the released year"
			else:
				message2="please fill in the title"	
			return render_to_response('findost/editfilmform.html', {'message' : message, 'message2' : message2, 'obj' : obj, 'isauth' : isauth}, context_instance=RequestContext(request))	
	else:
		raise Http404

def report(request,kind,id,sid):
	if(request.user.is_authenticated()):
		reportedby = request.user.username
		song = get_object_or_404(Song, pk = sid)
		if(not song.reported):
			song.reported=True
			song.reportedby = reportedby
			song.save()
		return HttpResponseRedirect('/findost/' + kind + '/details/' + id + '#info' + sid)
	else: 
		raise Http404

def unreport(request,kind,id,sid):
	if(request.user.is_authenticated()):
		song = get_object_or_404(Song, pk = sid)
		if(song.reportedby == request.user.username):
			song.reported=False
			song.reportedby = None
			song.save()
		return HttpResponseRedirect('/findost/' + kind + '/details/' + id + '#info' + sid)
	else: 
		raise Http404
	
def comment(request,kind,id):
	if(request.user.is_authenticated() and request.method == 'POST'):
		title = request.POST['title']
		body = request.POST['body']
		if (title and body):
			lastcomment = Comment.objects.order_by('-postedon')[0]
			if (lastcomment.title != title or lastcomment.body != body or lastcomment.postedby != request.user.username):
				c = Comment(title=title,body=body,postedby=request.user.username,postedon=datetime.datetime.now())
				if(kind == 'film'):
					film = get_object_or_404(Film, pk = id)
					c.film = film
				if(kind == 'episode'):
					episode = get_object_or_404(Episode, pk = id)
					c.episode = episode
				c.save()
			return HttpResponseRedirect('/findost/' + kind + '/details/' + id + '#showcomments')
		else :
			raise Http404
	else:
		raise Http404	
