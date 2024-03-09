# DJANGO API

Two steps are needed to launch the project.


- *Change directory* 

- *Run the file docker-compose.yml*

<br>

The directory `django_api_test_files` only includes the files to test the API with Swagger and Postman. 

The directory `docker_compose` contains the full Django API project.

<br>

**All environment variables are included in the `.env` file**

<br><br>

# Run the project

### Change directory

```
$ cd docker_compose/django_api
```

<br>

### Run docker-compose.yml 

```
$ sudo docker compose up 
```




<br><br>

### Project structure
----

<br>

```

movies_admin
    ├── configs
    │   └── site.conf
    ├── data
    │   └── index.html
    ├── movies_admin
    │   ├── config
    │   ├── movies
    │   │   ├── api
    │   │   │   ├── __init__.py
    │   │   │   ├── urls.py
    │   │   │   └── v1
    │   │   │       ├── __init__.py
    │   │   │       ├── urls.py
    │   │   │       └── views.py
    │   │   ├── locale
    │   │   ├── migrations
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py
    │   │   └── views.py
    │   ├── uwsgi
    │   │     └── uwsgi.ini
    │   ├── db.sqlite
    │   ├── dclasses.py
    │   ├── Dockerfile
    │   ├── entrypoint.sh
    │   ├── load_data.py
    │   ├── manage.py
    │   ├── requirements.txt
    ├── .env
    ├── docker-compose.yml
    └── nginx.conf


```