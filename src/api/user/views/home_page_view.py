from rest_framework.generics import ListAPIView,\
    CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.user.serializers import music_seralizers
from api.user.serializers import playlist_seralizers
from rest_framework import status
from rest_framework.response import Response
from apps.music.models import Music, Playlist


class HomeTopMusicListApiView(ListAPIView):
    queryset = Music.objects.filter(is_public=True).order_by("-listen_count")
    serializer_class = music_seralizers.MusicListSeralizer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()[:5]
        return queryset



class HomeTopPlaylistListApiView(ListAPIView):
    queryset = Playlist.objects.filter(is_public=True).order_by("-saves_count")
    serializer_class = playlist_seralizers.PlaylistListSeralizer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()[:5]
        return queryset