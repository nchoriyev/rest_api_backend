from django.contrib import admin
from .models import Albom, Artist, Song

admin.site.register([Albom, Artist, Song])
