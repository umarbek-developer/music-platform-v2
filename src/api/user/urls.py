from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.user.views import music_views

router = DefaultRouter()
router.include_root_view = False

urlpatterns = [
    # music
    path('music/', music_views.MusicListApiView.as_view()),
    path('music/create/', music_views.MusicCreateAPIView.as_view()),
    path('music/detail/<int:pk>/', music_views.MusicRetrieveAPIView.as_view()),
    path('music/detail/<int:pk>/', music_views.MusicDestroyAPIView.as_view()),
    path('music/detail/<int:pk>/', music_views.MusicUpdateAPIView.as_view()),




    # path('', include(router.urls)),
    # path('restaurant/', RestaurantViewset.as_view({'get': 'list','post':'create'}), name='restaurant-detail'),
]
