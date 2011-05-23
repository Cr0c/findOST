from django.db import models

# Create your models here.

class Actor(models.Model):
	name = models.CharField(max_length = 30)

	def __unicode__(self):
		return self.name

class Artist(models.Model):
	name = models.CharField(max_length = 30)

	def __unicode__(self):
		return self.name

class Song(models.Model):
	title = models.CharField(max_length = 100)
	artist = models.ForeignKey(Artist)
	artist.null = True
	album = models.CharField(max_length = 50)
	album.null = True
	cameouton = models.IntegerField()
	cameouton.null = True
	songid = models.IntegerField()
	songid.null = True
	length = models.IntegerField()
	length.null = True
	postedby = models.CharField(max_length = 30)
	postedby.null = True
	reported = models.NullBooleanField()
	reported.null = True
	reportedby = models.CharField(max_length = 15)
	reportedby.null = True

	def __unicode__(self):
		return self.title



class Film(models.Model):
	title = models.CharField(max_length = 100)
	otitle = models.CharField(max_length = 100)
	otitle.null = True
	director = models.CharField(max_length = 30)
	director.null = True
	producer = models.CharField(max_length = 30)
	producer.null = True
	mainactors = models.ManyToManyField(Actor)
	composer = models.CharField(max_length = 30)
	composer.null = True
	imageurl = models.CharField(max_length = 110)
	imageurl.null = True
	trailerurl = models.CharField(max_length = 110)
	trailerurl.null = True
	language = models.CharField(max_length = 30)
	language.null = True
	cameouton = models.IntegerField()
	cameouton.null = True
	length = models.IntegerField()
	length.null = True
	genre = models.CharField(max_length = 30)
	genre.null = True
	songs = models.ManyToManyField(Song)
	updatedon= models.DateTimeField()
	reported = models.CharField(max_length = 15)
	reported.null = True
	reportedby = models.CharField(max_length = 15)
	reportedby.null = True	

	def __unicode__(self):
		return self.title



class Show(models.Model):
	title = models.CharField(max_length = 100)
	otitle = models.CharField(max_length = 100)
	otitle.null = True
	mainactors = models.ManyToManyField(Actor)
	imageurl = models.CharField(max_length = 110)
	imageurl.null = True
	language = models.CharField(max_length = 30)
	language.null = True
	genre = models.CharField(max_length = 30)
	genre.null = True
	status = models.NullBooleanField()
	status.null = True
	nbseason = models.IntegerField()
	nbseason.null = True
	startingyear = models.IntegerField()
	startingyear.null = True

	def __unicode__(self):
		return self.title



class Episode(models.Model):
	show = models.ForeignKey(Show)
	length = models.IntegerField()
	length.null = True
	number = models.IntegerField()
	seasonnb = models.IntegerField()
	title = models.CharField(max_length = 100)
	title.null = True
	director = models.CharField(max_length = 30)
	director.null = True
	cameouton = models.DateTimeField('came out on')
	cameouton.null = True
	songs = models.ManyToManyField(Song)
	updatedon= models.DateTimeField()
	reported = models.CharField(max_length = 15)
	reported.null = True
	reportedby = models.CharField(max_length = 15)
	reportedby.null = True
	

	def __unicode__(self):
		return ('season ' + str(self.seasonnb) + ' episode ' + str(self.number) + ' : ' + self.title)

