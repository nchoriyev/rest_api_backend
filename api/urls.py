from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSetWeb, ArtistViewSetTelegram, AlbomViewSetWeb, AlbomViewSetTelegram, SongViewSetWeb, \
    SongViewSetTelegram

router = DefaultRouter()
router.register(r'artists-web', ArtistViewSetWeb, basename='artists-web')
router.register(r'artists-telegram', ArtistViewSetTelegram, basename='artists-telegram')
router.register(r'albom-web', AlbomViewSetWeb, basename='albom-web')
router.register(r'albom-telegram', AlbomViewSetTelegram, basename='albom-tele')
router.register(r'song-web', SongViewSetWeb, basename='song-web')
router.register(r'song-telegram', SongViewSetTelegram, basename='song-telegram')
urlpatterns = [
    path('', include(router.urls)),
]
