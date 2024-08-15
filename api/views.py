from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import ArtistSerializerWeb, ArtistSerializerTelegram, AlbomSerializerWeb, AlbomSerializerTelegram, \
    SongSerializerWeb, SongSerializerTelegram
from .models import Artist, Albom, Song, SongsAlbom
from rest_framework import permissions
from rest_framework import authentication

class ArtistViewSetWeb(viewsets.ModelViewSet):
    serializer_class = ArtistSerializerWeb

    def get_queryset(self):
        return Artist.objects.all()

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        # Assuming we have a field 'popularity' in Artist model
        artists = self.get_queryset().order_by("-popularity")[:3]
        serializer = ArtistSerializerTelegram(artists, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def with_no_albums(self, request, *args, **kwargs):
        artists = self.get_queryset().filter(albom__isnull=True)
        serializer = ArtistSerializerTelegram(artists, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def activate_all(self, request, *args, **kwargs):
        artists = self.get_queryset()
        for artist in artists:
            artist.is_active = True
            artist.save()
        return Response(data={"message": "all artists activated"})

    @action(detail=False, methods=["GET"])
    def deactivate_all(self, request, *args, **kwargs):
        artists = self.get_queryset()
        for artist in artists:
            artist.is_active = False
            artist.save()
        return Response(data={"message": "all artists deactivated"})

    @action(detail=True, methods=["GET"])
    def activate(self, request, *args, **kwargs):
        artist = self.get_object()
        artist.is_active = True
        artist.save()
        return Response(data={"message": "artist activated"})

    @action(detail=True, methods=["GET"])
    def deactivate(self, request, *args, **kwargs):
        artist = self.get_object()
        artist.is_active = False
        artist.save()
        return Response(data={"message": "artist deactivated"})

class AlbomViewSetWeb(viewsets.ModelViewSet):
    serializer_class = AlbomSerializerWeb

    def get_queryset(self):
        return Albom.objects.all()

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        # Assuming we have a field 'popularity' in Albom model
        alboms = self.get_queryset().order_by("-popularity")[:3]
        serializer = AlbomSerializerTelegram(alboms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def with_no_songs(self, request, *args, **kwargs):
        alboms = self.get_queryset().filter(song__isnull=True)
        serializer = AlbomSerializerTelegram(alboms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def release_all(self, request, *args, **kwargs):
        alboms = self.get_queryset()
        for albom in alboms:
            albom.is_released = True
            albom.save()
        return Response(data={"message": "all albums released"})

    @action(detail=False, methods=["GET"])
    def unrelease_all(self, request, *args, **kwargs):
        alboms = self.get_queryset()
        for albom in alboms:
            albom.is_released = False
            albom.save()
        return Response(data={"message": "all albums unreleased"})

    @action(detail=True, methods=["GET"])
    def release(self, request, *args, **kwargs):
        albom = self.get_object()
        albom.is_released = True
        albom.save()
        return Response(data={"message": "album released"})

    @action(detail=True, methods=["GET"])
    def unrelease(self, request, *args, **kwargs):
        albom = self.get_object()
        albom.is_released = False
        albom.save()
        return Response(data={"message": "album unreleased"})

class SongViewSetWeb(viewsets.ModelViewSet):
    serializer_class = SongSerializerWeb

    def get_queryset(self):
        return Song.objects.filter(status='pb')

    @action(detail=True, methods=["GET", ])
    def listen(self, request, *args, **kwargs):
        song = self.get_object()
        song.listen += 1
        song.save()
        return Response(data={"listened": song.listen})

    @action(detail=False, methods=["GET",])
    def top(self, request, *args, **kwargs):
        songs = self.get_queryset().order_by("listen")[:3]
        serializer = SongSerializerWeb(songs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET", ])
    def null_listen(self, request, *args, **kwargs):
        songs = self.get_queryset().filter(listen=0)
        serializer = SongSerializerWeb(songs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET", ])
    def all_listen(self, request, *args, **kwargs):
        songs = self.get_queryset()
        for song in songs:
            song.listen += 1
            song.save()
        return Response(data={"message": "all music listened"})

    @action(detail=False, methods=["GET",])
    def to_draft(self, request, *args, **kwargs):
        songs = self.get_queryset()
        for song in songs:
            song.pb_to_df()
        return Response(data={"message": "all data changes to draft"})

    @action(detail=False, methods=["GET", ])
    def to_publish(self, request, *args, **kwargs):
        songs = Song.objects.all()
        for song in songs:
            song.df_to_pb()
        return Response(data={"message": "all data changes to publish"})

    @action(detail=True, methods=["GET", ])
    def to_publish_d(self, request, *args, **kwargs):
        song = self.get_object()
        song.df_to_pb()
        return Response(data={"message": "data changes to publish"})

    @action(detail=True, methods=["GET", ])
    def to_draft_d(self, request, *args, **kwargs):
        song = Song.objects.get(id=id)
        song.pb_to_df()
        return Response(data={"message": "data changes to draft"})

#telegram
class ArtistViewSetTelegram(viewsets.ModelViewSet):
    serializer_class = ArtistSerializerTelegram

    def get_queryset(self):
        return Artist.objects.all()

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        # Assuming we have a field 'popularity' in Artist model
        artists = self.get_queryset().order_by("-popularity")[:3]
        serializer = ArtistSerializerTelegram(artists, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def with_no_albums(self, request, *args, **kwargs):
        artists = self.get_queryset().filter(albom__isnull=True)
        serializer = ArtistSerializerTelegram(artists, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def activate_all(self, request, *args, **kwargs):
        artists = self.get_queryset()
        for artist in artists:
            artist.is_active = True
            artist.save()
        return Response(data={"message": "all artists activated"})

    @action(detail=False, methods=["GET"])
    def deactivate_all(self, request, *args, **kwargs):
        artists = self.get_queryset()
        for artist in artists:
            artist.is_active = False
            artist.save()
        return Response(data={"message": "all artists deactivated"})

    @action(detail=True, methods=["GET"])
    def activate(self, request, *args, **kwargs):
        artist = self.get_object()
        artist.is_active = True
        artist.save()
        return Response(data={"message": "artist activated"})

    @action(detail=True, methods=["GET"])
    def deactivate(self, request, *args, **kwargs):
        artist = self.get_object()
        artist.is_active = False
        artist.save()
        return Response(data={"message": "artist deactivated"})


class AlbomViewSetTelegram(viewsets.ModelViewSet):
    serializer_class = AlbomSerializerTelegram

    def get_queryset(self):
        return Albom.objects.all()

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        # Assuming we have a field 'popularity' in Albom model
        alboms = self.get_queryset().order_by("-popularity")[:3]
        serializer = AlbomSerializerTelegram(alboms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def with_no_songs(self, request, *args, **kwargs):
        alboms = self.get_queryset().filter(song__isnull=True)
        serializer = AlbomSerializerTelegram(alboms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def release_all(self, request, *args, **kwargs):
        alboms = self.get_queryset()
        for albom in alboms:
            albom.is_released = True
            albom.save()
        return Response(data={"message": "all albums released"})

    @action(detail=False, methods=["GET"])
    def unrelease_all(self, request, *args, **kwargs):
        alboms = self.get_queryset()
        for albom in alboms:
            albom.is_released = False
            albom.save()
        return Response(data={"message": "all albums unreleased"})

    @action(detail=True, methods=["GET"])
    def release(self, request, *args, **kwargs):
        albom = self.get_object()
        albom.is_released = True
        albom.save()
        return Response(data={"message": "album released"})

    @action(detail=True, methods=["GET"])
    def unrelease(self, request, *args, **kwargs):
        albom = self.get_object()
        albom.is_released = False
        albom.save()
        return Response(data={"message": "album unreleased"})



class SongViewSetTelegram(viewsets.ModelViewSet):
    serializer_class = SongSerializerTelegram

    def get_queryset(self):
        return Song.objects.all()

    @action(detail=True, methods=["GET"])
    def listen(self, request, *args, **kwargs):
        song = self.get_object()
        song.listen += 1
        song.save()
        return Response(data={"listened": song.listen})

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        songs = self.get_queryset().order_by("-listen")[:3]
        serializer = SongSerializerTelegram(songs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def null_listen(self, request, *args, **kwargs):
        songs = self.get_queryset().filter(listen=0)
        serializer = SongSerializerTelegram(songs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def all_listen(self, request, *args, **kwargs):
        songs = self.get_queryset()
        for song in songs:
            song.listen += 1
            song.save()
        return Response(data={"message": "all music listened"})

    @action(detail=False, methods=["GET"])
    def to_draft(self, request, *args, **kwargs):
        songs = self.get_queryset()
        for song in songs:
            song.pb_to_df()
        return Response(data={"message": "all data changes to draft"})

    @action(detail=False, methods=["GET"])
    def to_publish(self, request, *args, **kwargs):
        songs = Song.objects.all()
        for song in songs:
            song.df_to_pb()
        return Response(data={"message": "all data changes to publish"})

    @action(detail=True, methods=["GET"])
    def to_publish_d(self, request, *args, **kwargs):
        song = self.get_object()
        song.df_to_pb()
        return Response(data={"message": "data changes to publish"})

    @action(detail=True, methods=["GET"])
    def to_draft_d(self, request, *args, **kwargs):
        song = self.get_object()
        song.pb_to_df()
        return Response(data={"message": "data changes to draft"})



