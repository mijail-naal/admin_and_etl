FROM python:3.12-slim

ARG USERNAME=Reinhardt
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  apt-get update \
     && apt-get install -y gettext \
     && apt-get install -y gcc \
     && apt-get install -y sudo \
     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
     && chmod 0440 /etc/sudoers.d/$USERNAME

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt \
     && chown -R $USERNAME:$USERNAME /opt/app /opt/app/static /var/www/static \
     /var/www/media /opt/app/media /opt/app/movies/locale/en/LC_MESSAGES \
     /opt/app/movies/locale/ru/LC_MESSAGES

COPY . .

EXPOSE 8000

USER $USERNAME

RUN sudo chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]