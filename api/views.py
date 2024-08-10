from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ArtistSerializerWeb, ArtistSerializerTelegram, AlbomSerializerWeb, AlbomSerializerTelegram, \
    SongSerializerWeb, SongSerializerTelegram
from .models import Artist, Albom, Song, SongsAlbom

class ArtistViewSetWeb(viewsets.ModelViewSet):
    serializer_class = ArtistSerializerWeb

    def get_queryset(self):
        return Artist.objects.all()

class AlbomViewSetWeb(viewsets.ModelViewSet):
    serializer_class = AlbomSerializerWeb

    def get_queryset(self):
        return Albom.objects.all()

class SongViewSetWeb(viewsets.ModelViewSet):
    serializer_class = SongSerializerWeb

    def get_queryset(self):
        return Song.objects.all()

#telegram
class ArtistViewSetTelegram(viewsets.ModelViewSet):
    serializer_class = ArtistSerializerTelegram

    def get_queryset(self):
        return Artist.objects.all()

class AlbomViewSetTelegram(viewsets.ModelViewSet):
    serializer_class = AlbomSerializerTelegram

    def get_queryset(self):
        return Albom.objects.all()


class SongViewSetTelegram(viewsets.ModelViewSet):
    serializer_class = SongSerializerTelegram

    def get_queryset(self):
        return Song.objects.all()


