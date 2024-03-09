from uuid import uuid4
from dataclasses import dataclass


@dataclass
class IdCreateUpdate:
    id: uuid4
    created_at: str
    updated_at: str


@dataclass
class IdFilmWorkCreate:
    id: uuid4
    film_work_id: uuid4
    created_at: str


@dataclass
class FilmWork(IdCreateUpdate):
    title: str
    description: str
    creation_date: None
    file_path: None
    rating: float
    type: str


@dataclass
class Genre(IdCreateUpdate):
    name: str
    description: str


@dataclass
class GenreFilmWork(IdFilmWorkCreate):
    genre_id: uuid4


@dataclass
class Person(IdCreateUpdate):
    full_name: str


@dataclass
class PersonFilmWork(IdFilmWorkCreate):
    person_id: uuid4
    role: str
