from django.db import models
from movielist.models import Movie
import datetime

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, through='Screening', related_name='movie_in_cinema')

    def __str__(self):
        return self.name + ' - ' + self.city

    @property
    def days30(self):
        dt = datetime.datetime.today()
        return self.movies.filter(screening__date__range=[dt, dt + datetime.timedelta(29)])


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.cinema.name +  ' - ' + self.movie.title + ' - ' + str(self.date)



