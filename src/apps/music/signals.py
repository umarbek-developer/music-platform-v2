from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
import mutagen
from .models import Music, Playlist


@receiver(pre_save, sender=Music)
def update_music_duration(sender, instance, **kwargs):
    if instance.music_data:
        try:
            # Bulutli xotiralarda ham ishlashi uchun fayl obyektini ochamiz
            file = instance.music_data.open()
            audio = mutagen.File(file)
            
            if audio and audio.info:
                instance.duration = int(audio.info.length)
        except Exception as e:
            print(f"Davomiylikni hisoblashda xatolik yuz berdi: {e}")
        finally:
          
            instance.music_data.close()



@receiver(m2m_changed, sender=Music.playlist.through)
def update_playlist_music_count(sender, instance, action, pk_set, **kwargs):

    if action == "pre_clear":
        if isinstance(instance, Music):
            instance._affected_playlists = list(instance.playlist.all())
        else:
            instance._affected_playlists = [instance]

    elif action in ["post_add", "post_remove", "post_clear"]:
        if action == "post_clear":
            playlists = getattr(instance, '_affected_playlists', [])
        else:
            if isinstance(instance, Music):
                playlists = instance.playlist.all()
            else:
                playlists = [instance]

        for playlist in playlists:
            playlist.musics_count = playlist.music_set.count()
            playlist.save(update_fields=['musics_count'])