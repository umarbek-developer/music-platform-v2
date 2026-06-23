from rest_framework.generics import ListAPIView,\
    CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.user.serializers import music_seralizers
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from apps.music.models import Music


class MusicListApiView(ListAPIView):
    queryset = Music.objects.filter(is_public=True)
    serializer_class = music_seralizers.MusicListSeralizer
    permission_classes = [AllowAny]
    is_mine = False
    playlist = None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.is_mine and type(self.request.user) != AnonymousUser:
            queryset =  Music.objects.filter(author=self.request.user)
        if self.playlist:
            try: playlist = list(map(lambda d: int(d), self.playlist.split(",")))
            except: return []
            queryset = queryset.filter(playlist__id__in=playlist).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        self.is_mine =  request.GET.get("is_mine", False)
        self.playlist = request.GET.get("playlist", False)
        return super().list(request, *args, **kwargs)


class MusicCreateAPIView(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicCreateSeralizer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        data._mutable = True
        data['author'] = request.user.id
        ser = self.serializer_class(data=data)
        if ser.is_valid(raise_exception=True):
            ser.save()
        return Response({
            "msg": "Music created successfully",
            "data": ser.data 
        }, status=status.HTTP_201_CREATED)


class MusicUpdateAPIView(UpdateAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicUpdateSeralizer
    permission_classes = [IsAuthenticated]


    def partial_update(self, request, *args, **kwargs):
        try:
            request.data.pop("author")
        except: pass
        instance = self.get_object()
        if request.user == instance.author:
            request.data._mutable = True
            request.data['author'] = request.user.id
            ser = self.serializer_class(instance, data=request.data, partial=True)
            if ser.is_valid(raise_exception=True):
                ser.save()
            return Response({
                "message": "ok",
                "data": ser.data
            },status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class MusicRetrieveAPIView(RetrieveAPIView):
    queryset = Music.objects.all()
    serializer_class = music_seralizers.MusicListSeralizer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if type(self.request.user) != AnonymousUser and self.request.user == instance.author:
            return super().retrieve(request, *args, **kwargs)
        elif instance.is_public:
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)


class MusicDestroyAPIView(DestroyAPIView):
    queryset = Music.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            instance.delete()
            status_code = status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)