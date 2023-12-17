from flask_cache import logger

from app.exceptions.errors import deserialize_json, JsonSchemaNotFound
from default_config import JSON_SCHEMA_PATH


class JsonSchemaController:
    def get_json_schema(self, name):
        try:
            file_path = "{}/{}.json".format(JSON_SCHEMA_PATH, name)

            with open(file_path) as data_file:
                return deserialize_json(data_file.read())

        except Exception as e:
            logger.error(
                "Error return JSON schema file with name: {}. Error detail: {}".format(
                    name, e
                )
            )
            raise JsonSchemaNotFound(
                "Error getting JSON schema file: {}.json".format(name)
            )
