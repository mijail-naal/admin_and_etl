import sys
import psycopg2
import logging
import sched
import time
import signal
import backoff
import redis
import storage

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import closing
from typing import Dict, List
from pydantic import ValidationError
from redis import Redis
from elasticsearch import Elasticsearch
from elasticloader import ElasticLoader
from etlqueries import FILM, PERSON, GENRE, PERSON_FILM, \
                       GENRE_FILM, FILM_PERSON_GENRE
from config import Film, FilmPersonGenre, postgres_database, \
                   redis_database, elastic_settings


load_dotenv()
logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s. %(message)s - %(filename)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


def signal_handler(signal, frame) -> None:
    logging.error('The program was stopped. Hasta la vista!')
    sys.exit(1)


class PostgresExtractor:
    """Provides an interface for working with the Postgres database."""

    def __init__(self, pg_conn: _connection) -> None:
        self.pg_conn = pg_conn
        self.film_query = FILM
        self.person_query = PERSON
        self.genre_query = GENRE
        self.person_film_query = PERSON_FILM
        self.genre_film_query = GENRE_FILM
        self.film_person_genre_query = FILM_PERSON_GENRE

    def _extract_data(self, query: str, data: str | tuple) -> List:
        """Method to interact and retrieve the data from the database."""
        with self.pg_conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (data,))
            data = cursor.fetchall()
        return data

    def updated_films(self, state: str) -> List:
        """Check for all the updated films."""
        if not state:
            # Asign a default value if state is None
            state = '2021-06-15'
        data = self._extract_data(self.film_query, state)
        return data

    def updated_persons(self, state: str) -> List | None:
        """
        Check for all the updated person and,
        if any, extract all the related data.
        """
        if not state:
            # Asign a default value if state is None
            state = '2021-06-15'

        data = self._extract_data(self.person_query, state)

        if data:
            person_ids = tuple([i['id'] for i in data])
            person_films = self._extract_data(self.person_film_query,
                                              person_ids)

            if person_films:
                person_film_ids = tuple([i['id'] for i in person_films])
                person_query = self.film_person_genre_query
                person_query += 'ORDER BY person_updated_at'
                all_person_info = self._extract_data(person_query,
                                                     person_film_ids)
                return all_person_info
        return None

    def updated_genres(self, state: str) -> List | None:
        """
        Check for all the updated genre and,
        if any, extract all the related data.
        """
        if not state:
            # Asign a default value if state is None
            state = '2021-06-15'

        data = self._extract_data(self.genre_query, state)

        if data:
            genre_ids = [i['id'] for i in data]
            if len(genre_ids) == 1:
                genre_ids.append(genre_ids[0])
            genre_films = self._extract_data(self.genre_film_query,
                                             tuple(genre_ids))
            if genre_films:
                genre_films_ids = [i['id'] for i in genre_films]
                genre_query = self.film_person_genre_query
                genre_query += 'ORDER BY genre_updated_at'
                all_genre_info = self._extract_data(genre_query,
                                                    tuple(genre_films_ids))
                return all_genre_info
        return None


def backoff_hadler(details: Dict) -> None:
    """Backoff event handler logging function"""
    logging.warning(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target.__name__} with args {args[0]} and {args[1]}"
        .format(**details)
    )


@backoff.on_exception(backoff.expo,
                      redis.exceptions.ConnectionError,
                      on_backoff=backoff_hadler)
@backoff.on_exception(backoff.expo,
                      psycopg2.OperationalError,
                      on_backoff=backoff_hadler)
def main(index: str, sc: sched.scheduler, seconds: int) -> None:
    """The main method of loading data from Postgres to Elasticsearch."""

    # Get the lasts states from Redis .
    films_state = redis_storage.get_state("last_updated_film")
    person_state = redis_storage.get_state("last_updated_person")
    genre_state = redis_storage.get_state("last_updated_genre")

    # This section extracts all the updated data from Postgres database.
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        extractor = PostgresExtractor(pg_conn)
        films = extractor.updated_films(films_state)
        persons = extractor.updated_persons(person_state)
        genres = extractor.updated_genres(genre_state)

    # This section loads all the data from Postgres to Elasticsearch.
    if films:
        for data in films:
            try:
                Film(**data)
            except ValidationError as e:
                logging.error(f'Film {data["fw_id"]} exit with: {e}')
            resp = es.add_film(index, data)
            if resp['result'] == 'updated' or resp['result'] == 'created':
                redis_storage.set_state('last_updated_film', data['updated_at'])
    if persons:
        for data in persons:
            try:
                FilmPersonGenre(**data)
            except ValidationError as e:
                logging.error(f'Person {data["fw_id"]} exit with: {e}')
            resp = es.load_data(index, data)
            if resp['result'] == 'updated':
                last_person_updated = data['person_updated_at']
                redis_storage.set_state('last_updated_person', last_person_updated)
    if genres:
        for data in genres:
            try:
                FilmPersonGenre(**data)
            except ValidationError as e:
                logging.error(f'Genre {data["fw_id"]} exit with: {e}')
            resp = es.load_data(index, data)
            if resp['result'] == 'updated':
                last_genre_updated = data['genre_updated_at']
                redis_storage.set_state('last_updated_genre', last_genre_updated)

    if not films and not persons and not genres:
        logging.info('No data to load. Setting the seconds to 10.')
        seconds = 10

    sc.enter(seconds, 1, main, (index, sc, seconds))
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    dsl = postgres_database.model_dump()

    s = sched.scheduler(time.time, time.sleep)

    redis_adapter = Redis(**redis_database.model_dump())
    redis_storage = storage.State(storage.RedisStorage(redis_adapter))

    # Elasticsearch variables and configurations.
    endpoint, index, seconds = elastic_settings.model_dump().values()
    client = Elasticsearch(endpoint)
    es = ElasticLoader(client)
    create_index = es.create_index(index)

    if not create_index:
        logging.warning(f'The index {index} was not created.')
        sys.exit(1)

    s.enter(int(seconds), 1, main, (index, s, int(seconds)))
    s.run()
    