from rest_framework.generics import ListAPIView,\
    CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from api.user.serializers import music_seralizers
from rest_framework import status
from rest_framework.response import Response
from apps.music.models import Music


class MusicListApiView(ListAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicListSeralizer
    permission_classes = [IsAuthenticated]


class MusicCreateAPIView(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicCreateSeralizer
    permission_classes = [IsAuthenticated]


class MusicUpdateAPIView(UpdateAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicCreateSeralizer
    permission_classes = [IsAuthenticated]


class MusicRetrieveAPIView(RetrieveAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicListSeralizer
    permission_classes = [IsAuthenticated]


class MusicDestroyAPIView(DestroyAPIView):
    queryset = Music.objects.all()
    permission_classes = [IsAuthenticated]


