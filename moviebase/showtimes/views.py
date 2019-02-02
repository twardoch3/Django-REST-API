from django.shortcuts import render
from .models import Cinema, Screening
from .serializers import CinemaSerializer, ScreeningSerializer, Movies_30_days_Serializer, Movies_30_days_SerializerVersion2
from rest_framework import generics, filters



class CinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('city','name')



class ScreeningView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer


class ScreeningListView(generics.ListCreateAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
    filter_fields = ('movie__title', 'cinema__city')


#dodatkowe
class CinemaListView30daysMovies(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = Movies_30_days_Serializer

class CinemaListView30daysMoviesVersion2(generics.ListAPIView):
    queryset = Cinema.objects.all()
    serializer_class = Movies_30_days_SerializerVersion2