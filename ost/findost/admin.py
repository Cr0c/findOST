from findost.models import Film,Show,Actor,Song,Artist,Episode
from django.contrib import admin


class FilmAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Film, FilmAdmin)

class ShowAdmin(admin.ModelAdmin):
     search_fields = ['title']

admin.site.register(Show, ShowAdmin)

class ActorAdmin(admin.ModelAdmin):
     search_fields = ['name']

admin.site.register(Actor, ActorAdmin)

class SongAdmin(admin.ModelAdmin):
     search_fields = ['title']
     list_filter = ['reported']

admin.site.register(Song, SongAdmin)

class ArtistAdmin(admin.ModelAdmin):
     search_fields = ['name']

admin.site.register(Artist, ArtistAdmin)

class EpisodeAdmin(admin.ModelAdmin):
     search_fields = ['title']
     search_fields = ['number']

admin.site.register(Episode, EpisodeAdmin)
