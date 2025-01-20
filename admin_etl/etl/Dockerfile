FROM python:3.12-slim

ARG USERNAME=Reinhardt
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
     && apt-get update \
     && apt-get install -y sudo \
     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
     && chmod 0440 /etc/sudoers.d/$USERNAME

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  pip install --upgrade pip \
     && chown -R $USERNAME:$USERNAME /opt/app

COPY etl/requirements.txt requirements.txt
RUN  pip install -r requirements.txt

COPY pg_database/ .
COPY etl/ .

# EXPOSE 8000
USER $USERNAME

RUN  sudo chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]