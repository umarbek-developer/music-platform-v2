from rest_framework.serializers import ModelSerializer
from apps.users.models import Favourite


class FavouriteListSeralizer(ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'


class FavouriteCreateSeralizer(ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'

