import json
import logging
from typing import Any, Dict


class ElasticLoader:
    """Class to load data to Elasticseach."""
    def __init__(self, client: object) -> None:
        self.client = client

    def create_index(self, index: str) -> bool:
        """Method to create an index in Elasticsearch."""

        # Check if Elastichseach is working.
        if self.client.ping():
            logging.info(
                'Response received successfully. Elastichsearch is working.'
            )

            # If the index exists return True otherwise False.
            movies_index = self.client.indices.exists(index=index)

            if not movies_index:
                # Load the data to create the index.
                with open('movieIndex.json', 'r') as file:
                    data = file.read()
                    idx = json.loads(data)
                    settings = idx['settings']
                    mappings = idx['mappings']

                movies = self.client.indices.create(
                    index=index, settings=settings, mappings=mappings
                )
                if movies['acknowledged']:
                    logging.info(
                        f'The index {index} was successfully created.'
                    )
            else:
                logging.info(f'The index {index} already exists.')
            return True
        else:
            logging.warning(
                'The request could not be made. Elasticsearch is not working.'
            )
            return False

    def _check_doc_exists(self, index: str, id: str) -> bool:
        """
        Private method to check the existence of the
        document in Elastichsearch.

        Return True if exists, otherwise False.
        """
        check = self.client.exists(index=index, id=id)
        return check

    def add_film(self, index: str, data: Dict[str, Any]) -> Dict:
        """Method to create or update a film."""
        id = data['fw_id']
        rating = 0 if not data['rating'] else data['rating']
        title = data['title']
        description = data['description']

        if not self._check_doc_exists(index, id):
            resp = self.client.index(
                index=index,
                id=id,
                body={
                    "id": f"{id}",
                    "imdb_rating": f"{rating}",
                    "genres": [],
                    "title": f"{title}",
                    "description": f"{description}",
                    "directors_names": [],
                    "actors_names": [],
                    "writers_names": [],
                    "actors": [],
                    "writers": []
                },
            )
            return resp
        else:
            self.client.bulk(
                body=[
                    {
                        "update": {
                            "_id": f"{id}",
                            "_index": f"{index}",
                        }
                    },
                    {
                        "script": {
                            "source": "if (ctx._source.imdb_rating == params.rating) { ctx.op = 'noop' } else { ctx._source.imdb_rating = params.rating }",
                            "lang": "painless",
                            "params": {
                                "rating": f"{rating}",
                            }
                        }
                    },
                    {
                        "update": {
                            "_id": f"{id}",
                            "_index": f"{index}",
                        }
                    },
                    {
                        "script": {
                            "source": "if (ctx._source.title == params.title) { ctx.op = 'noop' } else { ctx._source.title = params.title }",
                            "lang": "painless",
                            "params": {
                                "title": f"{title}"
                            }
                        }
                    },
                    {
                        "update": {
                            "_id": f"{id}",
                            "_index": f"{index}",
                        }
                    },
                    {
                        "script": {
                            "source": "if (ctx._source.description == params.description) { ctx.op = 'noop' } else { ctx._source.description = params.description }",
                            "lang": "painless",
                            "params": {
                                "description": f"{description}"
                            }
                        }
                    },
                ],
            )
            return {"result": "updated"}

    def add_genre(self, index: str, id: str, genre: str) -> Dict:
        """Method to add genre if not exists."""
        self.client.update(
            index=index,
            id=id,
            body={
                "script": {
                    "source": "if (ctx._source.genres.contains(params.genre)) { ctx.op = 'noop' } else { ctx._source.genres.add(params.genre) }",
                    "lang": "painless",
                    "params": {
                        "genre": f"{genre}",
                    }
                }
            },
        )
        return {"result": "updated"}

    def add_director(self, index: str, id: str, name: str) -> None:
        """Asign the role of director to the document."""
        self.client.update(
            index=index,
            id=id,
            body={
                "script": {
                    "source": "if (ctx._source.directors_names.contains(params.name)) { ctx.op = 'noop' } else { ctx._source.directors_names.add(params.name) }",
                    "lang": "painless",
                    "params": {
                        "name": f"{name}"
                    }
                }
            },
        )

    def add_actor(self, index: str, data: Dict[str, Any]) -> None:
        """Asign the role of actor to the document."""
        person_id = data['id']
        name = data['full_name']
        id = data['fw_id']

        self.client.bulk(
            body=[
                {
                    "update": {
                        "_id": f"{id}",
                        "_index": f"{index}",
                    }
                },
                {
                    "script": {
                        "source": "if (ctx._source.actors.contains(params)) { ctx.op = 'noop' } else { ctx._source.actors.add(params) }",
                        "lang": "painless",
                        "params": {
                            "id": f"{person_id}",
                            "name": f"{name}"
                        }
                    }
                },
                {
                    "update": {
                        "_id": f"{id}",
                        "_index": f"{index}",
                    }
                },
                {
                    "script": {
                        "source": "if (ctx._source.actors_names.contains(params.name)) { ctx.op = 'noop' } else { ctx._source.actors_names.add(params.name) }",
                        "lang": "painless",
                        "params": {
                            "name": f"{name}"
                        }
                    }
                },
            ],
        )

    def add_writer(self, index: str, data: Dict[str, Any]) -> None:
        """Asign the role of writer to the document."""
        id=data['fw_id']
        person_id = data['id']
        name = data['full_name']

        self.client.bulk(
            body=[
                {
                    "update": {
                        "_id": f"{id}",
                        "_index": f"{index}",
                    }
                },
                {
                    "script": {
                        "source": "if (ctx._source.writers.contains(params)) { ctx.op = 'noop' } else { ctx._source.writers.add(params) }",
                        "lang": "painless",
                        "params": {
                            "id": f"{person_id}",
                            "name": f"{name}"
                        }
                    }
                },
                {
                    "update": {
                        "_id": f"{id}",
                        "_index": f"{index}",
                    }
                },
                {
                    "script": {
                        "source": "if (ctx._source.writers_names.contains(params.name)) { ctx.op = 'noop' } else { ctx._source.writers_names.add(params.name) }",
                        "lang": "painless",
                        "params": {
                            "name": f"{name}"
                        }
                    }
                },
            ],
        )

    def load_data(self, index: str, data: Dict[str, Any]) -> Dict:
        """Method to manage the data to load to Elasticsearch."""

        id = data['fw_id']
        role = data['role']
        genre = data['genre']
        name = data['full_name']

        self.add_genre(index, id, genre)
        if role == 'director':
            self.add_director(index, id, name)
        elif role == 'actor':
            self.add_actor(index, data)
        elif role == 'writer':
            self.add_writer(index, data)
        else:
            logging.error('Someting went wrong. Role does not exists.')

        return {"result": "updated"}
