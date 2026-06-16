from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.user.views import music_views, playlist_views, favourite_music, favourite_playlist_views

router = DefaultRouter()
router.include_root_view = False

urlpatterns = [
    # music
    path('music/', music_views.MusicListApiView.as_view()),
    path('music/create/', music_views.MusicCreateAPIView.as_view()),
    path('music/detail/<int:pk>/', music_views.MusicRetrieveAPIView.as_view()),
    path('music/delete/<int:pk>/', music_views.MusicDestroyAPIView.as_view()),
    path('music/update/<int:pk>/', music_views.MusicUpdateAPIView.as_view()),

    # playlist
    path('playlist/', playlist_views.PlaylistListApiView.as_view()),
    path('playlist/create/', playlist_views.PlaylistCreateAPIView.as_view()),
    path('playlist/detail/<int:pk>/', playlist_views.PlaylistRetrieveAPIView.as_view()),
    path('playlist/delete/<int:pk>/', playlist_views.PlaylistDestroyAPIView.as_view()),
    path('playlist/update/<int:pk>/', playlist_views.PlaylistUpdateAPIView.as_view()),

    # user favourite
    path('favourite/', favourite_music.FavouriteListApiView.as_view()),
    path('favourite/create/', favourite_music.FavouriteCreateAPIView.as_view()),
    path('favourite/delete/<int:pk>/', favourite_music.FavouriteDestroyAPIView.as_view()),

    # user favourite playlist
    path('favourite-playlist/', favourite_playlist_views.FavouriteplaylistListApiView.as_view()),
    path('favourite-playlist/create/', favourite_playlist_views.FavouriteplaylistCreateAPIView.as_view()),
    path('favourite-playlist/delete/<int:pk>/', favourite_playlist_views.FavouriteplaylistDestroyAPIView.as_view()),


    # path('', include(router.urls)),
    # path('restaurant/', RestaurantViewset.as_view({'get': 'list','post':'create'}), name='restaurant-detail'),
]
