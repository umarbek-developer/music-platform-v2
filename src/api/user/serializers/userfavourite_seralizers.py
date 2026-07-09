from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from apps.users.models import Favourite
from api.user.serializers.music_seralizers import MusicListSeralizer


class FavouriteListSeralizer(ModelSerializer):
    # Nest the full track so the client can render the favourites list
    # without an extra request per item.
    music = MusicListSeralizer(read_only=True)

    class Meta:
        model = Favourite
        fields = '__all__'


class FavouriteCreateSeralizer(ModelSerializer):
    user = None

    class Meta:
        model = Favourite
        fields = '__all__'

    def validate_music(self, music):
        favourite = Favourite.objects.filter(user=self.user, music=music)
        if favourite.exists():
            raise ValidationError("This music aleady exists in your favourite list.")
        elif not music.is_public:
            raise ValidationError("You can't add this music to your favourites.")
        return music 


