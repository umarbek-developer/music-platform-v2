from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    saves_count = models.IntegerField(default=1)
    musics_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
    

class Music(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(default=False)
    playlist = models.ManyToManyField(Playlist, blank=True, null=True)
    favouites_count = models.IntegerField(default=1)
    listen_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='pictures/', blank=True, null=True)
    lirics = models.TextField(default=0)
    source = models.CharField(max_length=255, blank=True, null=True)
    music_data = models.FileField(upload_to='musics/')

    def __str__(self):
        return f"{self.name}"