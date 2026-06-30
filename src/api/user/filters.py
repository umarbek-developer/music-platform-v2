import django_filters
from apps.music.models import Music


class MusicFilter(django_filters.FilterSet):
    # category = django_filters.CharFilter(field_name='category__title_uz', lookup_expr='icontains')
    # title = django_filters.CharFilter(field_name='title_uz', lookup_expr='icontains')

    class Meta:
        model = Music
        fields = ['name', 'author']