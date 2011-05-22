from findost.models import Song
import urllib2,string

#'/home/silvain/WebTech/GitRep/findOST/DB/findsongid.py'

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

def add_already_found_ids():

	file = open('/home/silvain/WebTech/GitRep/findOST/DB/ids','r')
	l = file.readline()
	l=l.decode('iso-8859-1')
	ind = 0
	last = 0
	stitle = ''
	sid = ''
	sartist = ''
	while(l):
		while(l[ind:ind+3] != '_|_'):
			stitle = stitle + l[ind]
			ind = ind + 1
		ind = ind + 3
		while(l[ind:ind+3] != '_|_'):
			sartist = sartist + l[ind]
			ind = ind + 1
		
		song = Song.objects.filter(title=stitle).get(artist__name=sartist)
		if(last<song.pk):			
			last = song.pk		
		if (song.songid < 0):
			ind = ind+3
			while(ind < len(l)):
	 			sid = sid + l[ind]
				ind = ind + 1
			song.songid = int(sid)
			song.save()
			
		l = file.readline()
		l=l.decode('iso-8859-1')
		ind = 0
		sartist = ''
		sid=''
		stitle = ''
	file.close()
	print 'all ids already found were successfully added to DB, up to '+ str(last)
	return last




#add_already_found_ids()

file = open('/home/silvain/WebTech/GitRep/findOST/DB/ids','a')
count = 0
keyind = 0
bad = 0
OK = 0
keys=['2f3763493ccbe8cec903a6235274b1a5','b3fa54409e286bd0192b9c2966767482']
try :
	for song in Song.objects.exclude(songid__gte = -1): 
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
		
		#print (title + " by, " + artist)
		request = "http://tinysong.com/b/"+ modtitle+"+"+modartist+"?format=json&key="+keys[keyind]
		Json=urllib2.urlopen(request).read()
		count = count + 1
		Json = Json.decode('utf-8')
		if (Json != '[]' and Json[0] == '{'):
			try:
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
					print(song.title + " /found : " + songtitle + "           OK   " + str(count))
					file.write(song.title + "_|_" + song.artist.name + "_|_" + songid + "\n")
					OK=OK+1
				else:
					print(song.title + " /found : " + songtitle + "  // not validated   " + str(count))
					song.songid=-1
					song.save()
					bad = bad+1
			except:
				if(keyind < len(keys)-1):
					keyind = keyind + 1
					print ("key used = " + str(keyind) + '( ' + keys[keyind] + ' )')
				else:
					file.close()
					print ('success ratio : ' + str(float(OK)/(OK+bad+1)))
					break
		else:
			song.songid=-1
			song.save()
			bad=bad+1		
			print(song.title + " not found : not validated")
	
except KeyboardInterrupt:
	file.close()
	print ('success ratio : ' + str(float(OK)/(OK+bad+1)))

except urllib2.HTTPError:
	file.close()
	print request
	print ('success ratio : ' + str(float(OK)/(OK+bad+1)))
