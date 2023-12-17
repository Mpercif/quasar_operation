import json

from flask_restful import Resource
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from app.api.controllers.ImperialFleetController import (
    ImperialFleetController,
)
from app.api.controllers.JsonSchemaController import JsonSchemaController
from app.exceptions.errors import SatelliteValidationNotSuccess
from helpers.responseHelper import json_response


class ImperialFleet(Resource):
    def post(self, fleet_information):
        try:
            data = json.loads(fleet_information)
            self.__validate_params(data)
            satellites = ImperialFleetController().setup_satellite_configuration(
                data["satellites"]
            )
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
        schema = json_schema_controller.get_json_schema("satellite-triangulation")
        validate(data, schema)