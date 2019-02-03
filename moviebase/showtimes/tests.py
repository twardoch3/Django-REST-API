from rest_framework.test import APITestCase
from random import randint, sample
from .models import Cinema, Screening
from movielist.models import Person, Movie
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone


class Faker_Temp_Data():

    faker = Faker("pl_PL")
    dt = timezone.make_aware(datetime.today(), timezone.get_current_timezone())

    def _fake_data_db(self):
        for _ in range(randint(5,10)):
            Person.objects.create(name=self.faker.name())
        for _ in range(randint(5,9)):
            self._create_fake_movie()
        for _ in range(randint(2,7)):
            nc = Cinema.objects.create(name='kino ' + self.faker.word() + self.faker.word(), city=self.faker.city())
            # nazwy kin nie powinny sie powtarzac
            movies = sample(list(Movie.objects.all()), randint(1,5))
            for m in movies:
                Screening.objects.create(cinema=nc, movie=m, date=self.dt + timedelta(randint(1,5)))
        # no movies
        Cinema.objects.create(name='kino ' + self.faker.word(), city=self.faker.city())


    def _random_movie(self):
        movies = Movie.objects.all()
        return movies[randint(0, len(movies) - 1)]

    def _random_cinema(self):
        cinemas = Cinema.objects.all()
        return cinemas[randint(0, len(cinemas) - 1)]


    def _random_person(self):
        """Return a random Person object from db."""
        people = Person.objects.all()
        return people[randint(0, len(people) - 1)]

    def _find_person_by_name(self, name):
        """Return the first `Person` object that matches `name`."""
        return Person.objects.filter(name=name).first()

    def _fake_movie_data(self):
        """Generate a dict of movie data
        The format is compatible with serializers (`Person` relations
        represented by names).
        """
        movie_data = {
            "title": "{} {}".format(self.faker.job(), self.faker.first_name()),
            "description": self.faker.sentence(),
            "year": int(self.faker.year()),
            "director": self._random_person().name,
        }
        people = Person.objects.all()
        actors = sample(list(people), randint(1, len(people)))
        actor_names = [a.name for a in actors]
        movie_data["actors"] = actor_names
        #print(movie_data["title"])
        return movie_data

    def _create_fake_movie(self):
        """Generate new fake movie and save to database."""
        movie_data = self._fake_movie_data()
        movie_data["director"] = self._find_person_by_name(movie_data["director"])
        actors = movie_data["actors"]
        del movie_data["actors"]
        new_movie = Movie.objects.create(**movie_data)
        for actor in actors:
            new_movie.actors.add(self._find_person_by_name(actor))
        #return new_movie


    def _fake_cinema(self):
        new_cinema = {
            "name" : "Kino WWW",
            "city" : "Katowice"
        }

        return new_cinema

    def _fake_screening(self):
        new_screening = {
            'date': '2019-02-10T14:33:02Z',
            'movie': 'http://testserver/movies/{}/'.format(self._random_movie().pk)
        }

        new_screening['cinema'] = self._random_cinema().name

        return new_screening


class CinemaTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fake_data = Faker_Temp_Data()

    def setUp(self):
        print('Test_Cinemas')
        CinemaTestCase.fake_data._fake_data_db()  #self albo CinemaTestCase
        #print(Person.objects.all())
        #print(Movie.objects.all())


    def test_get_cinemas_list(self):
        response = self.client.get("/cinemas/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.count(), len(response.data))
        print(Cinema.objects.count())
        print('get')


    def test_get_cinema_detail(self):
        c1 = Cinema.objects.get(pk=1)
        response = self.client.get("/cinemas/1/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], c1.name)
        self.assertEqual(response.data['city'], c1.city)
        print('detail')


    def test_add_cinema(self):
        cinemas_before = Cinema.objects.count()
        new_cinema = self.fake_data._fake_cinema()  #albo nazwa klasy
        response = self.client.post("/cinemas/", new_cinema, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cinema.objects.count(), cinemas_before + 1)
        for key, val in new_cinema.items():
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], val)
        print(response.data)
        print(new_cinema)
        print('add')

    def test_delete_cinema(self):
        response = self.client.delete("/cinemas/1/", {}, format='json')
        self.assertEqual(response.status_code, 204)
        cinema_ids = [cinema.pk for cinema in Cinema.objects.all()]
        self.assertNotIn(1, cinema_ids)
        print('delete')


    def test_update_cinema(self):
        response = self.client.get("/cinemas/1/", {}, format='json')
        cinema_data = response.data
        new_city = 'NYC'
        cinema_data['city'] = new_city
        response = self.client.patch("/cinemas/1/", cinema_data, format='json')
        self.assertEqual(response.status_code, 200)
        cinema_obj = Cinema.objects.get(id=1)
        self.assertEqual(cinema_obj.city, new_city)
        print('update')
        print(cinema_obj.movies.all())

    def test_non_existing_cinema_404(self):
        response = self.client.get("/cinemas/1000/", {}, format='json')
        self.assertEqual(response.status_code, 404)
        print('404')

    @classmethod
    def tearDownClass(cls):
        print('Cinema testing finished')


class ScreeningTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fake_data = Faker_Temp_Data()

    def setUp(self):
        print('Test_Screening')
        ScreeningTestCase.fake_data._fake_data_db()  # self albo CinemaTestCase
        print('m=', Movie.objects.all().count())
        #print(Screening.objects.all()[:3])
        print('s=', Screening.objects.all().count())
        print('c=', Cinema.objects.all().count())
        print(Cinema.objects.all())

    def test_get_screening_list(self):
        response = self.client.get("/screening/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Screening.objects.count(), len(response.data))
        print('get')


    def test_get_screening_detail(self):
        s1 = Screening.objects.get(pk=1)
        response = self.client.get("/screening/1/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['cinema'], s1.cinema.name)
        self.assertEqual(response.data['movie'][-2], str(s1.movie.pk))
        dt = response.data['date'][:-1].replace('T', ' ')
        self.assertIn(dt, str(s1.date))
        print(response.data)
        print('dt=',dt)
        print('detail')

    def test_add_screening(self):
        screening_before = Screening.objects.count()
        new_screening = self.fake_data._fake_screening()
        response = self.client.post("/screening/", new_screening, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Screening.objects.count(), screening_before + 1)
        for key, val in new_screening.items():
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], val)
        print(response.data)
        print(new_screening)
        print('add')

    def test_update_screening(self):
        response = self.client.get("/screening/1/", {}, format='json')
        screening_data = response.data
        print(screening_data)
        new_cinema = self.fake_data._random_cinema().name
        print(new_cinema)
        screening_data['cinema'] = new_cinema
        response = self.client.patch("/screening/1/", screening_data, format='json')
        self.assertEqual(response.status_code, 200)
        screening_obj = Screening.objects.get(id=1)
        self.assertEqual(screening_obj.cinema.name, new_cinema)
        print('update')
        print(screening_obj)


    def test_non_existing_screening_404(self):
        response = self.client.get("/screening/1000/", {}, format='json')
        self.assertEqual(response.status_code, 404)
        print('404')


    def test_delete_screening(self):
        response = self.client.delete("/screening/1/", {}, format='json')
        self.assertEqual(response.status_code, 204)
        screening_ids = [screening.pk for screening in Screening.objects.all()]
        self.assertNotIn(1, screening_ids)
        print('delete')

    @classmethod
    def tearDownClass(cls):
        print('Screening testing finished')



