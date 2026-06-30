from rest_framework.generics import ListAPIView,\
    CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.user.serializers import music_seralizers
from api.user.serializers import playlist_seralizers
from rest_framework import status
from rest_framework.response import Response
from apps.music.models import Music, Playlist
from rest_framework.viewsets import ModelViewSet
from api.user.permissions import CustomPermission
from api.user.filters import MusicFilter


class TestApiViewset(ModelViewSet):
    serializer_class = music_seralizers.MusicListSeralizer
    queryset = Music.objects.all()
    permission_classes = [IsAuthenticated, CustomPermission]
    filterset_class = MusicFilter
    search_fields = ['name', 'author']
    ordering_fields = ['duration']

    app_label = "music"
    app_model = "music"
    # create(POST), Update(PUT, PATCH), Delete(DELETE), List(GET), Detail(GET)

    def list(self, request, *args, **kwargs):
        print(request.user)
        return super().list(request, *args, **kwargs)








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