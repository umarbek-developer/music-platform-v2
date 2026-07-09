from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
import mutagen
from .models import Music, Playlist


@receiver(pre_save, sender=Music)
def update_music_duration(sender, instance, **kwargs):
    if instance.music_data:
        try:
            # Read metadata from the uploaded file object (works for cloud
            # storage too, where .path is unavailable).
            instance.music_data.open()
            audio = mutagen.File(instance.music_data)

            if audio and audio.info:
                instance.duration = int(audio.info.length)
        except Exception as e:
            print(f"Davomiylikni hisoblashda xatolik yuz berdi: {e}")
        finally:
            # CRITICAL: rewind but DO NOT close. This pre_save signal runs
            # before Django's FileField writes the file to storage; closing
            # the uploaded file here causes the subsequent storage write to
            # fail with "ValueError: I/O operation on closed file", which
            # surfaced as an HTTP 500 on every upload.
            try:
                instance.music_data.seek(0)
            except Exception:
                pass



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