"""moviebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from movielist.views import MovieListView, MovieView
from showtimes.views import CinemaListView, CinemaView, ScreeningListView, ScreeningView, CinemaListView30daysMovies, CinemaListView30daysMoviesVersion2


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^movies/$', MovieListView.as_view(), name='movies-list'),
    url(r'^movies/(?P<pk>[0-9]+)/$', MovieView.as_view(), name='movie-detail'),


    url(r'^cinemas/$', CinemaListView.as_view(), name='cinemas-list'),
    url(r'^cinemas/(?P<pk>[0-9]+)/$', CinemaView.as_view(), name='cinema-detail'),

    url(r'^screening/$', ScreeningListView.as_view(), name='screening-list'),
    url(r'^screening/(?P<pk>[0-9]+)/$', ScreeningView.as_view(), name='screening-detail'),

    #zadanie dodatkowe
    url(r'^cinemas/30DaysMovies/$', CinemaListView30daysMovies.as_view(), name='cinemas-30days-movies'),
    #wersja 2
    url(r'^cinemas/30DaysMoviesVersion2/$', CinemaListView30daysMoviesVersion2.as_view(), name='cinemas-30days-movies-version2'),


]
