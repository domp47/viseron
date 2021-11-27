"""Database Config."""
from voluptuous import Required, Schema

SCHEMA = Schema({Required("type"): str})


class DatabaseConfig:
    """Database config."""

    schema = SCHEMA

    def __init__(self, database):
        self.__type = database["type"]

    @property
    def type(self):
        """Return Database Type."""
        return self.__type
