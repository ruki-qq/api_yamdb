# api_yamdb

This project represents API for Yamdb.

## Description

YaMDb is a user review platform that gathers opinions on various works of art, including books, movies, and music.
Unlike other platforms, YaMDb doesn't store the actual content of the works; instead, it focuses on categorizing them
into genres such as "Books," "Movies," and "Music." Each work can be further labeled with predefined genres like "Fairy
Tale," "Rock," or "Arthouse." The system allows only administrators to add new works, categories, and genres.

Authenticated users can express their gratitude or discontent by leaving text reviews and assigning a numerical rating
ranging from one to ten, contributing to the work's overall rating. Users are limited to one review per work.
Additionally, users can engage in discussions by leaving comments on reviews. The platform ensures that only
authenticated users have the privilege to add reviews, comments, and ratings, maintaining the integrity of the feedback
system.

## Usage

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## How to fill DB

Use csv files and command ```python manage.py loaddb``` to fill database.

## Documentation

Go to http://localhost:8000/redoc/ endpoint to see API docs.

## Authors
- [Soslan Khutinaev](https://github.com/ruki-qq/api_yamdb)
- [Andrey Korolev](https://github.com/ankor2023)

## Tech Stack

- [Python](https://www.python.org//)
- [Django](https://www.djangoproject.com//) - [🐙](https://github.com/django/django) - Django is a high-level Python web framework.
- [Django REST Framework](https://www.django-rest-framework.org/) - [🐙](https://github.com/encode/django-rest-framework) - Django REST framework is a toolkit for building Web APIs.
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/) - [🐙](https://github.com/jpadilla/pyjwt) - A Python implementation of RFC 7519.
- [django-filter](https://django-filter.readthedocs.io/en/stable/) - [🐙](https://github.com/carltongibson/django-filter) - A reusable Django application allowing users to declaratively add dynamic QuerySet filtering from URL parameters.
- [pytest](https://docs.pytest.org/en/7.4.x/) - [🐙](https://github.com/pytest-dev/pytest) - A framework to write tests.
- [requests](https://requests.readthedocs.io/en/latest/) - [🐙](https://github.com/psf/requests) - A simple, yet elegant, HTTP library.

## Examples

### Request

GET /titles/

    curl -i -H 'Accept: application/json' http://localhost:8000/api/v1/titles/

### Response

    HTTP/1.1 200 OK
    Date: Mon, 04 Dec 2023 12:09:49 GMT
    Server: WSGIServer/0.2 CPython/3.9.18
    Content-Type: application/json
    Vary: Accept
    Allow: GET, POST
    X-Frame-Options: DENY
    Content-Length: 1006
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin

    {<data>}

### Request

GET /titles/{titles_id}/

    curl -i -H 'Accept: application/json' http://localhost:8000/api/v1/titles/3/

### Response

    HTTP/1.1 200 OK
    Date: Mon, 04 Dec 2023 12:09:49 GMT
    Server: WSGIServer/0.2 CPython/3.9.18
    Content-Type: application/json
    Vary: Accept
    Allow: GET, POST
    X-Frame-Options: DENY
    Content-Length: 1006
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin

    {
        "id":3,
        "category":{"name":"Фильм","slug":"movie"},
        "genre":[{"name":"Драма","slug":"drama"}],
        "rating":7,
        "name":"12 разгневанных мужчин",
        "year":1957,
        "description":""
    }

