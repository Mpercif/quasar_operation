import json

from flask_restful import Resource
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from quasarservice.app.api.controllers.JsonSchemaController import JsonSchemaController
from quasarservice.helpers.responseHelper import json_response


class Satellite(Resource):

    def post(self, satellite_info):
        try:
            data = json.loads(satellite_info)
            self.__validate_params(data)

        except ValidationError as e:
            return json_response({"message": e}, 400)
        except ValueError as e:
            return json_response({"message": e}, 400)
        except Exception as e:
            return json_response({"message": e}, 500)

    def get(self, satellite_name):
        pass

    def __validate_params(self, data):
        json_schema_controller = JsonSchemaController()
        schema = json_schema_controller.get_json_schema("satellite-info")
        validate(data, schema)
