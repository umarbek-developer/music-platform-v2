from rest_framework.generics import ListAPIView,\
    CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from api.user.serializers import userfavourite_seralizers
from rest_framework import status
from rest_framework.response import Response
from apps.users.models import Favourite


class FavouriteListApiView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = userfavourite_seralizers.FavouriteListSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class FavouriteCreateAPIView(CreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = userfavourite_seralizers.FavouriteCreateSeralizer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Copy into a plain dict so this works for both JSON and multipart
        # bodies. (request.data is a dict for JSON, which has no _mutable, and
        # an immutable QueryDict for multipart — the old code broke on both.)
        data = {key: request.data.get(key) for key in request.data}
        data['user'] = request.user.id
        ser = self.serializer_class(data=data)
        ser.user = request.user
        if ser.is_valid(raise_exception=True):
            ser.save()
        return Response({
            "msg": "Favourite added successfully",
            "data": ser.data
        }, status=status.HTTP_201_CREATED)



class FavouriteDestroyAPIView(DestroyAPIView):
    queryset = Favourite.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            instance.delete()
            status_code = status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)