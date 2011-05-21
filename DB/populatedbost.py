from findost.models import Film,Song,Artist,Show,Episode
import datetime
#'/home/silvain/WebTech/projet/database/populatedbost.py'

def find_and_add_film(l):
	i = 3
	temp = ''
	while (l[i] != '"' and i<len(l)-1):		
		temp = temp + l[i]
		i=i+1	
	if(i<len(l)-1):
		filmtitle = temp
		temp = ''
		i=i+3
		while(l[i] != ')' and l[i] != '/' and i<len(l)-1):
			temp = temp + l[i]
			i=i+1
		if(i<len(l)-1):
			date = temp
			lifilm = Film.objects.filter(title=filmtitle).filter(cameouton=int(date))
			if(lifilm):
				film = lifilm[0]
			else:
				print (filmtitle + ', ' + date)
				film = Film(title=filmtitle,cameouton=int(date))
				film.updatedon=datetime.datetime.now()
				film.save()
	return film	


def find_and_add_episode(l):
	i = 3
	temp = ''
	while (l[i] != '"' and i<len(l)-1):
		temp = temp + l[i]
		i=i+1	
	if(i<len(l)-1):
		showtitle = temp
		lishow = Show.objects.filter(title=showtitle)
		if(lishow):
			show = lishow[0]
		else:
			show = Show(title=showtitle)
			show.save()
		temp = ''
		i=i+3
		while(l[i] != ')' and l[i] != '/' and i<len(l)-1):
			temp = temp + l[i]
			i=i+1
		if(i<len(l)-1):
			year = int(temp)
			date = datetime.datetime(year,01,01)
			temp=''
			i = l.index('{') + 1
			while(l[i] != '(' and i<len(l)-1):
				temp = temp + l[i]
				i=i+1
			if(i<len(l)-1):
				eptitle = temp
				temp = ''
				i = l[i:].index('#') + 1 + i
				while(l[i] != '.' and i<len(l)-1):
					temp = temp + l[i]
					i=i+1
				if(i<len(l)-1):
					epseason = int(temp)
					temp = ''
					i = i+1
					while(l[i] != ')' and i<len(l)-1):
						temp = temp + l[i]
						i=i+1
					if(i<len(l)-1):
						epnum = int(temp)
						temp = ''
						liepisode = Episode.objects.filter(show__title=showtitle).filter(seasonnb=epseason).filter(number=epnum)
						if(liepisode):
							episode = liepisode[0]
						else:
							print (showtitle + " : " + eptitle + ', s' + str(epseason) + 'e' + str(epnum))
							episode = Episode(title=eptitle,cameouton=date,show=show,number=epnum,seasonnb=epseason)
							episode.updatedon=datetime.datetime.now()
							episode.save()
							if(epseason > show.nbseason):
								show.nbseason = epseason
								show.save()
	return episode	




f = open('/home/silvain/WebTech/projet/database/soundtracks.norme','r') #norme avec sed -r 's:# ([^"].*) (\([0-9]{4}):# "\1" \2:g' 
#f = open('/home/silvain/WebTech/projet/database/test','r')
l = f.readline()
for i in range(1205000): #saute les lignes du fichier deja en DB
	l=f.readline()
l=l.decode('iso-8859-1')
j = 0
i = 0
while(l):
	try:
		if(l[0] == '#' and l[2] == '"'):
			if('#' in l[1:]):
				obj=find_and_add_episode(l)
			else:
				obj=find_and_add_film(l)
			l = f.readline()
			l=l.decode('iso-8859-1')
		if(l[0]=='-'):
			i = 3
			temp = ''
			while(l[i] != '"' and i<len(l)-1):
				temp = temp + l[i]
				i = i+1
			if(i<len(l)-1):
				songtitle = temp
				#print ('title : ' + songtitle)
			l=f.readline()
			l=l.decode('iso-8859-1')
		else:
			if('Performed by' in l):
				i = 0
				temp = ''
				while(l[i] != "'" and i<len(l)-1):
					i=i+1
				i=i+1
				if(i<len(l)-1):
					while(l[i] != "'" and l[i] != '(' and i<len(l)-1):
						temp = temp +l[i]
						i=i+1
					songartist = temp	
			#		print ('   artist : ' + songartist)
					liartist = Artist.objects.filter(name=songartist)
					if(liartist):
						a = liartist[0]
					else :
						a = Artist(name=songartist)				
						a.save()
					lisong = Song.objects.filter(title= songtitle).filter(artist__name=a)
					if(lisong):
						s = lisong[0]
					else:
						s = Song(title=songtitle, artist = a)
						s.save()
						obj.songs.add(s)
						obj.updatedon=datetime.datetime.now()
						obj.save()
			l = f.readline()
			l=l.decode('iso-8859-1')
	except not KeyboardInterrupt:
		l = f.readline()
		l=l.decode('iso-8859-1')
f.close()

