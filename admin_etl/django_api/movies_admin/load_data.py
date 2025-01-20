import os
import sqlite3
import psycopg2
import logging

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import closing
from dataclasses import dataclass, fields, astuple
from dclasses import FilmWork, Genre, GenreFilmWork, \
                                Person, PersonFilmWork


load_dotenv()
logging.basicConfig(
    filename='load_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s. %(message)s - %(filename)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


class SQLiteExtractor:
    def __init__(self, conection: sqlite3.Connection):
        self.connection = conection

    def extract_movies(self, table: str):
        query = f'SELECT * FROM {table};'
        q_count = f'SELECT count(*) FROM {table};'
        size = 20  # Change the size to fetch more or less rows
        part = 0
        try:
            with self.connection as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                total = cursor.execute(q_count).fetchone()[0]
                times = total // size + 1
                if total % size == 0:
                    times = total // size
                res = cursor.execute(query)
                for _ in range(times):
                    data = res.fetchmany(size)
                    yield data
                    if data:
                        part += 1
        except sqlite3.DatabaseError as err:
            logging.warning(
                f'The query "{query}" returned the following error. {err}'
            )
        finally:
            cursor.close()

        if part != 0:
            logging.info(f'Table "{table}" copied in {part} parts of {size} rows.')
        else:
            logging.warning(f'The table "{table}" could not be copied.')


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data: list, table: str, data_class: dataclass):
        rows = [data_class(**result) for result in data]
        column_names = [field.name for field in fields(rows[0])]
        column_names_str = ','.join(column_names)
        col_count = ', '.join(['%s'] * len(column_names))

        with self.pg_conn as conn:
            cursor = conn.cursor()

            bind_values = ','.join(cursor.mogrify(
                f"({col_count})", astuple(row)
            ).decode('utf-8') for row in rows)

            query = (
                f'INSERT INTO content.{table} ({column_names_str}) VALUES {bind_values} '
                f' ON CONFLICT (id) DO NOTHING'
            )
            try:
                cursor.execute(query)
            except psycopg2.DatabaseError as err:
                logging.warning(f'The following error occurred. {err}')


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    tables = ['film_work', 'genre', 'genre_film_work', 'person',
              'person_film_work']
    data_classes = [FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork]

    for idx in range(len(tables)):
        data = sqlite_extractor.extract_movies(tables[idx])
        if data:
            for obj_rows_list in data:
                if obj_rows_list:
                    postgres_saver.save_all_data(obj_rows_list,
                                                 tables[idx],
                                                 data_classes[idx])
        else:
            logging.warning(f"Check if the table '{tables[idx]}' exists.")


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432)
    }

    with closing(sqlite3.connect(os.environ.get('SQLITE_DB'))) as sqlite_conn, \
         closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
