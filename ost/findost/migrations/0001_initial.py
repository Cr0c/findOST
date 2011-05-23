# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Actor'
        db.create_table('findost_actor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('findost', ['Actor'])

        # Adding model 'Artist'
        db.create_table('findost_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('findost', ['Artist'])

        # Adding model 'Song'
        db.create_table('findost_song', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['findost.Artist'], null=True)),
            ('album', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('cameouton', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('songid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('postedby', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal('findost', ['Song'])

        # Adding model 'Film'
        db.create_table('findost_film', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('otitle', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('producer', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('composer', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('imageurl', self.gf('django.db.models.fields.CharField')(max_length=110, null=True)),
            ('trailerurl', self.gf('django.db.models.fields.CharField')(max_length=110, null=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('cameouton', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('genre', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('updatedon', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('findost', ['Film'])

        # Adding M2M table for field mainactors on 'Film'
        db.create_table('findost_film_mainactors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('film', models.ForeignKey(orm['findost.film'], null=False)),
            ('actor', models.ForeignKey(orm['findost.actor'], null=False))
        ))
        db.create_unique('findost_film_mainactors', ['film_id', 'actor_id'])

        # Adding M2M table for field songs on 'Film'
        db.create_table('findost_film_songs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('film', models.ForeignKey(orm['findost.film'], null=False)),
            ('song', models.ForeignKey(orm['findost.song'], null=False))
        ))
        db.create_unique('findost_film_songs', ['film_id', 'song_id'])

        # Adding model 'Show'
        db.create_table('findost_show', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('otitle', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('imageurl', self.gf('django.db.models.fields.CharField')(max_length=110, null=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('genre', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('nbseason', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('startingyear', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('findost', ['Show'])

        # Adding M2M table for field mainactors on 'Show'
        db.create_table('findost_show_mainactors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('show', models.ForeignKey(orm['findost.show'], null=False)),
            ('actor', models.ForeignKey(orm['findost.actor'], null=False))
        ))
        db.create_unique('findost_show_mainactors', ['show_id', 'actor_id'])

        # Adding model 'Episode'
        db.create_table('findost_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('show', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['findost.Show'])),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('seasonnb', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('cameouton', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updatedon', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('findost', ['Episode'])

        # Adding M2M table for field songs on 'Episode'
        db.create_table('findost_episode_songs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('episode', models.ForeignKey(orm['findost.episode'], null=False)),
            ('song', models.ForeignKey(orm['findost.song'], null=False))
        ))
        db.create_unique('findost_episode_songs', ['episode_id', 'song_id'])


    def backwards(self, orm):
        
        # Deleting model 'Actor'
        db.delete_table('findost_actor')

        # Deleting model 'Artist'
        db.delete_table('findost_artist')

        # Deleting model 'Song'
        db.delete_table('findost_song')

        # Deleting model 'Film'
        db.delete_table('findost_film')

        # Removing M2M table for field mainactors on 'Film'
        db.delete_table('findost_film_mainactors')

        # Removing M2M table for field songs on 'Film'
        db.delete_table('findost_film_songs')

        # Deleting model 'Show'
        db.delete_table('findost_show')

        # Removing M2M table for field mainactors on 'Show'
        db.delete_table('findost_show_mainactors')

        # Deleting model 'Episode'
        db.delete_table('findost_episode')

        # Removing M2M table for field songs on 'Episode'
        db.delete_table('findost_episode_songs')


    models = {
        'findost.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'findost.artist': {
            'Meta': {'object_name': 'Artist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'findost.episode': {
            'Meta': {'object_name': 'Episode'},
            'cameouton': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'seasonnb': ('django.db.models.fields.IntegerField', [], {}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['findost.Show']"}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['findost.Song']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {})
        },
        'findost.film': {
            'Meta': {'object_name': 'Film'},
            'cameouton': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'composer': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageurl': ('django.db.models.fields.CharField', [], {'max_length': '110', 'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'mainactors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['findost.Actor']", 'symmetrical': 'False'}),
            'otitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['findost.Song']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trailerurl': ('django.db.models.fields.CharField', [], {'max_length': '110', 'null': 'True'}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {})
        },
        'findost.show': {
            'Meta': {'object_name': 'Show'},
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageurl': ('django.db.models.fields.CharField', [], {'max_length': '110', 'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'mainactors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['findost.Actor']", 'symmetrical': 'False'}),
            'nbseason': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'otitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'startingyear': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'findost.song': {
            'Meta': {'object_name': 'Song'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['findost.Artist']", 'null': 'True'}),
            'cameouton': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'postedby': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'songid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['findost']
