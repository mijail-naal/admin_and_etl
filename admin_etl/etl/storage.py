from redis import Redis
from typing import Any, Dict


class RedisStorage:
    """Implementation of a repository using a Redis.
    Storage format: JSON
    """
    def __init__(self, redis_adapter: Redis) -> None:
        self.redis_adapter = redis_adapter

    def save_state(self, state: Dict[str, Any]) -> None:
        """Save the state to the repository."""
        name, value = [d for d in state.items()][0]
        self.redis_adapter.set(name, value)

    def retrieve_state(self, key: str) -> Dict[str, Any]:
        """Get the state from the repository."""
        if not self.redis_adapter.get(key):
            return {}
        return {key: self.redis_adapter.get(key)}


class State:
    """A class for working with states."""
    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Set the state for a specific key."""
        state = dict()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """Get the status for a specific key."""
        state = self.storage.retrieve_state(key)
        if not state:
            return None
        return state.get(key)
