import json

from flask import request
from flask_restful import Resource
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from app.api.controllers.ImperialFleetController import ImperialFleetController
from app.api.controllers.JsonSchemaController import JsonSchemaController
from app.api.controllers.SatelliteController import SatelliteController
from app.exceptions.errors import (
    SatelliteValidationNotSuccess,
    SatelliteNotFound,
)
from helpers.responseHelper import json_response


class Satellite(Resource):
    def post(self, satellite_name):
        try:
            data = json.loads(request.args.get("data"))
            self.__validate_params(data)
            data.update({"name": satellite_name})
            SatelliteController().update_satellite_data(data)

            return json_response({"message": "Satellite data have been updated"})
        except SatelliteNotFound as e:
            return json_response({"message": e.message}, e.code)
        except ValidationError as e:
            return json_response({"message": e}, 400)
        except ValueError as e:
            return json_response({"message": e}, 400)
        except Exception as e:
            return json_response({"message": e}, 500)

    def get(self, satellite_name):
        try:
            data = json.loads(request.args.get("data"))
            self.__validate_params(data)
            data.update({"name": satellite_name})
            satellites = SatelliteController().get_missing_satellites(data)
            response = ImperialFleetController().triangulate_position_float(satellites)

            return response
        except SatelliteValidationNotSuccess as e:
            return json_response({"message": e}, e.code)
        except ValidationError as e:
            return json_response({"message": e}, 400)
        except ValueError as e:
            return json_response({"message": e}, 400)
        except Exception as e:
            return json_response({"message": e}, 500)

    def __validate_params(self, data):
        json_schema_controller = JsonSchemaController()
        schema = json_schema_controller.get_json_schema("satellite-info")
        validate(data, schema)
