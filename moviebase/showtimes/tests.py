from rest_framework.test import APITestCase
from .models import Cinema


#import client?

class CinemaTestCase(APITestCase):

    def setUp(self):
        print('Test_1_Cinemas')
        for i in range(5):
            Cinema.objects.create(name='Kino {}'.format(i))

    def _fake_cinema(self):
        new_cinema = {
            "name" : "Cinema X",
            "city" : "Katowice"
        }
        return new_cinema

    # def _create_new_cinema(self):
    #     new_cinema_json = self._fake_cinema()
    #     new_cinema_db = Cinema()
    #     new_cinema_db.name = new_cinema_json["name"]
    #     new_cinema_db.city = new_cinema_json["city"]
    #     new_cinema_db.save()



    def test_get_cinemas_list(self):
        response = self.client.get("/cinemas/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.count(), len(response.data))
        print(response.data)
        print(Cinema.objects.count())
        print('get')


    def test_get_cinema_detail(self):
        response = self.client.get("/cinemas/1/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Kino 0')
        print('detail')

    def test_add_cinema(self):
        cinemas_before = Cinema.objects.count()
        new_cinema = self._fake_cinema()
        response = self.client.post("/cinemas/", new_cinema, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cinema.objects.count(), cinemas_before + 1)
        print(response.data)
        print('add')
        for key, val in new_cinema.items():
            self.assertIn(key, response.data)
            if isinstance(val, list):
                # Compare contents regardless of their order
                self.assertCountEqual(response.data[key], val)
            else:
                self.assertEqual(response.data[key], val)






