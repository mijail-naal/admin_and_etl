# DJANGO API

Three steps are needed to launch the project.

- *Change to directory docker_compose/django_api* 

- *Change the file `.env.sample` to `.env` and set the environment variables* 

- *Run the docker-compose.yml*

<br>

The directory `django_api_test_files` only includes the files to test the API with Swagger and Postman. 

The directory `docker_compose` contains the full Django API project.

<br>

**All environment variables samples are included in the `.env.sample` file**

**Don't forget to set the environment variables before running the project!**

<br><br>

> [!NOTE]  
> **Комментарии для ревьюера**  
> 
> Спасибо большое за ревью!  
> Я согласен с вашим замечанием и понимаю, что никогда не следует отправлять конфиденциальные данные или сохранять их в репозитории, в любом случае я оставил в комментариях важные значения для проекта, в файле .env.sample, для его правильного функционирования. Конечно, я понимаю, что в реальном проекте лучше не давать никаких подсказок.  
>
> Спасибо за ваше внимание!

<br>

# Run the project

### 1. Change directory

```
$ cd docker_compose/django_api
```

<br>

### 2. Set the environment variables 

```
- Change .env.samble file to .env
- Set the environment variables
```

<br>

### 3. Run the docker-compose.yml 

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