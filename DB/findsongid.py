from findost.models import Song
import urllib2,string

<<<<<<< HEAD
#'/home/silvain/WebTech/GitRep/findOST/DB/findsongid.py'
=======
#'/home/silvain/WebTech/projet/database/findsongid.py'
>>>>>>> e05133186b77281ae9f83fa98c7b3dd7170c5c71

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

<<<<<<< HEAD
	file = open('/home/silvain/WebTech/GitRep/findOST/DB/ids','r')
=======
	file = open('/home/silvain/WebTech/projet/database/ids','r')
>>>>>>> e05133186b77281ae9f83fa98c7b3dd7170c5c71
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




<<<<<<< HEAD
#add_already_found_ids()

file = open('/home/silvain/WebTech/GitRep/findOST/DB/ids','a')
=======
add_already_found_ids()

file = open('/home/silvain/WebTech/projet/database/ids','a')
>>>>>>> e05133186b77281ae9f83fa98c7b3dd7170c5c71
count = 0
keyind = 0
bad = 0
OK = 0
<<<<<<< HEAD
keys=['2f3763493ccbe8cec903a6235274b1a5','b3fa54409e286bd0192b9c2966767482']
=======
keys=['a888f7983a569ac0292fd8a4e177b774','4415354c92f1f5a3c92066fba2b94579','841b3a6c329b5645ea9e527f6e8fdcaf','6b8d39f9278ec54499dec10a784c3393','d62189fbab0f00f85cb76f3576f56b73','93adbed3e691ff209b6ec1508a67710d','2f8c33f9ded5e3118f4f0cd8b0c2e706','f807f5032f9ad6d3ffb706b7b6184dca','92580438ed1663b83d78f67d17b3a970','9c8ea5f6e823c3dced9d10d3af8d61ea','e6efa3f13f67dda4228acb0692598301','da51a49efc8a7244ba5e97a54c6a46c7','5d2bc217bf1c27eb1bb2b405520078e9','5a431de624aa75a11728c72212254bba','6d27464324a693b12e0141869996e946','deac983270aafb75a72f11415e525c1c','84fa2204a23978d4a6622d53148edecc','10b59146490e593eb0dd044a606e5bd6','a44deadbfa2d32326f94e33a9fe69194','61c58a8df857c324204b56805ed3b05e','8021b78681805e8367e581637fb90a49','2d18f4a252baf64d46bfe76267e6c712','a271c09359d41a9bd882520eeba09343','53ea903fb3d05c1d4ae8c5e78e5fdccc','da9a3dbc0b2eb32580720991f761a5ad']
>>>>>>> e05133186b77281ae9f83fa98c7b3dd7170c5c71
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
<<<<<<< HEAD
					print ("key used = " + str(keyind) + '( ' + keys[keyind] + ' )')
=======
					print ("key used = " + str(keyind))
>>>>>>> e05133186b77281ae9f83fa98c7b3dd7170c5c71
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
