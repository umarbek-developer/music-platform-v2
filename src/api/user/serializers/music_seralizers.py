from rest_framework.serializers import ModelSerializer
from apps.music.models import Music


class MusicListSeralizer(ModelSerializer):

    class Meta:
        model = Music
        fields = '__all__'


class MusicCreateSeralizer(ModelSerializer):

    class Meta:
        model = Music
        fields = '__all__'

