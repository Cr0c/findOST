# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Comment'
        db.create_table('findost_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('postedby', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('postedon', self.gf('django.db.models.fields.DateTimeField')()),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['findost.Episode'])),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['findost.Film'])),
        ))
        db.send_create_signal('findost', ['Comment'])


    def backwards(self, orm):
        
        # Deleting model 'Comment'
        db.delete_table('findost_comment')


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
        'findost.comment': {
            'Meta': {'object_name': 'Comment'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['findost.Episode']"}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['findost.Film']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postedby': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'postedon': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'findost.episode': {
            'Meta': {'object_name': 'Episode'},
            'cameouton': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'reported': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'reportedby': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
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
            'reported': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'reportedby': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
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
            'reported': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'reportedby': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'songid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['findost']
