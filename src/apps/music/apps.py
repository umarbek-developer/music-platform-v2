from django.apps import AppConfig


class MusicConfig(AppConfig):
    name = 'apps.music'


    def ready(self):
        import apps.music.signals
