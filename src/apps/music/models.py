import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from mutagen.mp3 import MP3
from mutagen.wave import WAVE


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    saves_count = models.IntegerField(default=0)
    musics_count = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    

    def delete(self, *args, **kwargs):
        if self.picture and os.path.isfile(self.picture.path):
            os.remove(self.picture.path)

        if self.picture and os.path.isfile(self.picture.path):
            os.remove(self.picture.path)
            
        # 3. Asosiy o'chirish jarayonini bajarish
        super().delete(*args, **kwargs)
    


class Music(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(default=False)
    playlist = models.ManyToManyField(Playlist, blank=True, null=True)
    favouites_count = models.IntegerField(default=0)
    listen_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='pictures/', blank=True, null=True)
    lirics = models.TextField(default=0)
    source = models.CharField(max_length=255, blank=True, null=True)
    music_data = models.FileField(upload_to='musics/')

    def __str__(self):
        return f"{self.name}"
    
    def delete(self, *args, **kwargs):
        if self.picture and os.path.isfile(self.picture.path):
            os.remove(self.picture.path)

        if self.music_data and os.path.isfile(self.music_data.path):
            os.remove(self.music_data.path)
            
        # 3. Asosiy o'chirish jarayonini bajarish
        super().delete(*args, **kwargs)

@receiver(post_save, sender=Music)
def update_music_duration(sender, instance, created, **kwargs):
    if created and instance.music_data:
        try:
            # Fayl yo'lini olish
            file_path = instance.music_data.path
            
            # Fayl formatiga qarab aniqlash
            if file_path.endswith('.mp3'):
                audio = MP3(file_path)
            elif file_path.endswith('.wav'):
                audio = WAVE(file_path)
            else:
                return # Boshqa formatlar uchun qo'shimcha logic yozishingiz mumkin

            # Davomiylikni sekundda olish va saqlash
            instance.duration = int(audio.info.length)
            instance.save(update_fields=['duration'])
            
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
    