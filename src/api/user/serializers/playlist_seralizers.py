from rest_framework.serializers import ModelSerializer
from apps.music.models import Playlist


class PlaylistListSeralizer(ModelSerializer):

    class Meta:
        model = Playlist
        fields = '__all__'


class PlaylistCreateSeralizer(ModelSerializer):

    class Meta:
        model = Playlist
        fields = '__all__'

