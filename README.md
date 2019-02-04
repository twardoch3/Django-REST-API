# Django-REST-API
This project is a Django API application that allows to create, edit, update and delete cinemas, movies and screenings. It is built with Django REST framework.

### Requirements
Program requires Django and Django REST framework.

### Installing
Install requirements  with command:
```
pip install -r requirements.txt
```
### Running the program
Apply the migrations:
```
python manage.py migrate
```
Start a development Web server on the local machine with command:
```
python manage.py runserver
```
### Usage Examples:
Movies Endpoint (GET,POST):
```
http://127.0.0.1:8000/movies/
```
Screening Endpoint (GET,POST):
```
http://127.0.0.1:8000/screening/
```
Cinema detail Endpoint (GET, PUT, DELETE):
```
http://127.0.0.1:8000/cinemas/1/
```
Filter Screenings by Movie Title:
```
http://127.0.0.1:8000/screening/?movie__title=Film1
```
Run Tests:
```
python manage.py test showtimes
```

