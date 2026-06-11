from rest_framework.serializers import ModelSerializer
from apps.users.models import Favouriteplaylist


class FavouriteplaylistListSeralizer(ModelSerializer):

    class Meta:
        model = Favouriteplaylist
        fields = '__all__'


class FavouriteplaylistCreateSeralizer(ModelSerializer):

    class Meta:
        model = Favouriteplaylist
        fields = '__all__'

