from django.shortcuts import render
from .models import Cinema, Screening
from .serializers import CinemaSerializer, ScreeningSerializer, Movies_30_days_Serializer
from rest_framework import generics
#usunac to potem
from movielist.models import Movie


class CinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer



class ScreeningView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer


class ScreeningListView(generics.ListCreateAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer


#dodatkowe
class CinemaListView30daysMovies(generics.ListAPIView):
    queryset = Cinema.objects.all()
    serializer_class = Movies_30_days_Serializer