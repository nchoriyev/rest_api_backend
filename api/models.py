from django.db import models

class Artist(models.Model):
    nick = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nick


class Albom(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.URLField(max_length=1000)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StatusChoice(models.TextChoices):
    DRAFT = 'df', 'Draft'
    PUBLISH = 'pb', 'Publish'

class Song(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.URLField(max_length=1000)
    listen = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=5, choices=StatusChoice.choices, default=StatusChoice.PUBLISH)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id",]
        indexes = [
            models.Index(fields=['id']),
        ]

    def df_to_pb(self):
        if self.status == 'df':
            self.status = 'pb'
            self.save()

    def pb_to_df(self):
        if self.status == 'pb':
            self.status = 'df'
            self.save()

    def __str__(self):
        return self.title


class SongsAlbom(models.Model):
    albom = models.ForeignKey(Albom, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
