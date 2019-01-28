from rest_framework import serializers
from .models import Cinema, Screening

class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)   #allow_null = True

    class Meta:
        model = Cinema
        fields = ('name', 'city', 'movies')


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='name', queryset=Cinema.objects.all())
    movie = serializers.HyperlinkedRelatedField(view_name='movie-detail', read_only=True)

    class Meta:
        model = Screening
        fields = ('cinema', 'movie', 'date')


