from django.db import models
from movielist.models import Movie

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, through='Screening', related_name='movie_in_cinema')


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema,on_delete=models.CASCADE)
    date = models.DateTimeField()


