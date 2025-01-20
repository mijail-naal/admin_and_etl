import uuid

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Film(BaseModel):
    fw_id: uuid.UUID
    title: str
    description: str | None
    rating: float    # | None
    # Updated_at is converted into string
    # with the TO_CHAR postgres function.
    updated_at: str  # | datetime


class FilmPersonGenre(Film):
    type: str
    # person_updated_at and genre_updated_at
    # also are converted into string from the
    # query to the database.
    person_updated_at: str  # | datetime
    genre_updated_at: str   # | datetime
    role: str
    id: uuid.UUID
    full_name: str
    genre: str


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    dbname: str = Field(..., alias='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='redis_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    host: str = ...
    port: int = ...
    db: int = ...
    decode_responses: str = Field(..., alias='REDIS_DECODE')


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='elasticsearch_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    endpoint: str
    index: str
    seconds: str = Field(..., alias='SCHEDULER_SECONDS')


postgres_database = PostgresSettings()
redis_database = RedisSettings()
elastic_settings = ElasticSettings()
