from rest_framework import serializers
from .models import Cinema

class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)   #allow_null = True

    class Meta:
        model = Cinema
        fields = ('name', 'city', 'movies')


