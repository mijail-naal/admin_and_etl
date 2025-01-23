# Service Admin Panel + API and ETL

### Project description

A content management service whit Django-based admin interface that allow to upload movies to server and receive them, and an
ETL (Extract-Transform-Load) process for uploading data about movies and related people to the Elasticsearch search engine. 

The project include the next fetures:
- Ready to launch in a production environment via Docker-Compose. (*) 
- At the beginning, all the data are transfered from SQLite3 to Postgres database with SQL through Python ("load_data" script) and fill the repository with movies information.
- A simple API developed with Django to provide a page-by-page list of movies and detailed view about a particular movie.
- ETL process to extract the data from Postgres database and load to Elasticsearch.
- The ETL implement a fault-tolerant process when the database crash.

<br>

Two steps are needed to launch the project:

- *Change the file `.env.sample` to `.env` and set the environment variables* 

- *Run docker-compose.yml*

<br>

The directory `django_api_test_files` only includes the files to test the API with Swagger and Postman. 

The directory `admin_etl` contains the full project (Django admin + API and ETL).

<br>


*All environment variables samples are included in the `.env.sample` file*

*Don't forget to set the environment variables before running the project!*


<br>

### Technologies used:

![Technologies used](https://skillicons.dev/icons?i=python,django,html,nginx,postgres,redis,elasticsearch,docker)

###### Python, django, HTML, Nginx, Postgres, Redis, Elasticsearch, Docker

<br><br>

###### (*) *Do not use this project for a real deployment*.

<br>

# Run the project


### 1. Set the environment variables 

```
- Change .env.samble file to .env
- Set the environment variables
```

### 2. Run docker-compose.yml 

```
$ sudo docker compose up 
```

<br>

### Project structure
----

<br>

```

admin_and_etl
    ├── admin_etl
    │   ├── django_api
    │   │   ├── configs
    │   │   │   └── site.conf
    │   │   ├── data
    │   │   │   └── index.html
    │   │   ├── movies_admin
    │   │   │   ├── config
    │   │   │   ├── movies
    │   │   │   │   ├── api
    │   │   │   │   │   ├── __init__.py
    │   │   │   │   │   ├── urls.py
    │   │   │   │   │   └── v1
    │   │   │   │   │       ├── __init__.py
    │   │   │   │   │       ├── urls.py
    │   │   │   │   │       └── views.py
    │   │   │   │   ├── locale
    │   │   │   │   ├── migrations
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── admin.py
    │   │   │   │   ├── apps.py
    │   │   │   │   ├── models.py
    │   │   │   │   └── views.py
    │   │   │   ├── uwsgi
    │   │   │   │     └── uwsgi.ini
    │   │   │   ├── db.sqlite
    │   │   │   ├── dclasses.py
    │   │   │   ├── Dockerfile
    │   │   │   ├── entrypoint.sh
    │   │   │   ├── load_data.py
    │   │   │   ├── manage.py
    │   │   │   ├── requirements.txt
    │   |   └── nginx.conf
    |   |
    │   └── etl
    |       ├── configs
    │       │   └── setting.py
    |       ├── index
    │       │   └── movieIndex.json
    |       ├── utils
    |       |   ├── elasticloader.py
    |       |   ├── etlqueries.py
    │       │   └── storage.py
    |       ├── Dockerfile
    |       ├── entrypoint.sh
    |       ├── etl_script.py
    |       └── requirements.txt
    |    
    ├── django_api_test_files
    ├── .env.sample
    ├── docker-compose.yml
    └── README.md


```