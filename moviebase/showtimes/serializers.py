from rest_framework import serializers
from .models import Cinema, Screening
from movielist.models import Movie
import datetime
from django.utils import timezone


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)

    class Meta:
        model = Cinema
        fields = ('name', 'city', 'movies')


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='name', queryset=Cinema.objects.all())
    movie = serializers.HyperlinkedRelatedField(view_name='movie-detail', queryset=Movie.objects.all())

    class Meta:
        model = Screening
        fields = ('date', 'cinema', 'movie')


#zad dodatkowe
class Movies_30_days_Serializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = ['name', 'city', 'movies']

    def get_movies(self, obj):
        dt = timezone.make_aware(datetime.datetime.today(), timezone.get_current_timezone())
        return [m.title for m in obj.movies.filter(screening__date__range=[dt, dt + datetime.timedelta(29)])]


#version 2
class Movies_30_days_SerializerVersion2(serializers.ModelSerializer):
    #days30 = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)
    days30 = serializers.SlugRelatedField(many=True, slug_field='title', read_only=True)

    class Meta:
        model = Cinema
        fields = ('name', 'city', 'days30')



