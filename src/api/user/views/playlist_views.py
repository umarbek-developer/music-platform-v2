from rest_framework.generics import ListAPIView,\
    CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.user.serializers import playlist_seralizers
from rest_framework import status
from rest_framework.response import Response
from apps.music.models import Playlist
from django.contrib.auth.models import AnonymousUser



class PlaylistListApiView(ListAPIView):
    queryset = Playlist.objects.filter(is_public=True)
    serializer_class = playlist_seralizers.PlaylistListSeralizer
    permission_classes = [AllowAny]
    is_mine = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.is_mine and type(self.request.user) != AnonymousUser:
            queryset = Playlist.objects.filter(author=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        self.is_mine = request.GET.get("is_mine", False)
        return super().list(request, *args, **kwargs)
    


class PlaylistCreateAPIView(CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = playlist_seralizers.PlaylistCreateSeralizer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        data._mutable = True
        data['author'] = request.user.id
        ser = self.serializer_class(data=data)
        if ser.is_valid(raise_exception=True):
            ser.save()
        return Response({
            "msg": "Playlist created successfully",
            "data": ser.data
        }, status=status.HTTP_201_CREATED)


class PlaylistUpdateAPIView(UpdateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = playlist_seralizers.PlaylistCreateSeralizer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        try:
            request.data.pop("author")
        except: pass
        instance = self.get_object()
        if request.user == instance.author:
            request.data._mutable = True
            request.data['author'] = request.user.id
            ser = self.serializer_class(instance, data=request.data)
            if ser.is_valid(raise_exception=True):
                ser.save()
            return Response({
                "message": "ok",
                "data": ser.data
            },status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PlaylistRetrieveAPIView(RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = playlist_seralizers.PlaylistListSeralizer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if type(self.request.user) != AnonymousUser and self.request.user == instance.author:
            return super().retrieve(request, *args, **kwargs)
        elif instance.is_public:
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)


class PlaylistDestroyAPIView(DestroyAPIView):
    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            status_code = status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)
    