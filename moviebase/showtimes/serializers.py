from rest_framework import serializers
from .models import Cinema, Screening
from movielist.models import Movie
import datetime


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
        dt = datetime.datetime.today()
        return [m.title for m in obj.movies.filter(screening__date__range=[dt, dt + datetime.timedelta(29)])]



