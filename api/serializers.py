from rest_framework import serializers
from .models import Artist, Albom, Song, SongsAlbom


# telegram
class ArtistSerializerTelegram(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('nick', 'first_name', 'last_name')


class AlbomSerializerTelegram(serializers.ModelSerializer):
    class Meta:
        model = Albom
        fields = ('title', 'description', 'artist')


class SongSerializerTelegram(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('title', 'description', 'artist', 'listen')


class SongsAlbomSerializerTelegram(serializers.ModelSerializer):
    class Meta:
        model = SongsAlbom
        fields = ('id', 'songs', 'albom')


# web
class ArtistSerializerWeb(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'first_name', 'last_name', 'nick', 'image')


class AlbomSerializerWeb(serializers.ModelSerializer):
    class Meta:
        model = Albom
        fields = ('id', 'title', 'artist', 'image', 'description')


class SongSerializerWeb(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'description', 'image', 'artist', 'listen', 'status')


class SongsAlbomSerializerWeb(serializers.ModelSerializer):
    class Meta:
        model = SongsAlbom
        fields = ('id', 'songs', 'albom')
