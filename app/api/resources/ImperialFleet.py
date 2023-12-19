import json

from flasgger import swag_from
from flask_restful import Resource
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from app.api.controllers.ImperialFleetController import (
    ImperialFleetController,
)
from app.api.controllers.JsonSchemaController import JsonSchemaController
from app.api.exceptions.errors import SatelliteValidationNotSuccess
from default_config import APIDOCS_PATH
from helpers.responseHelper import json_response


class ImperialFleet(Resource):
    """
    Imperial Fleet API endpoints
    """
    @swag_from(APIDOCS_PATH + "/satellite-triangulation.yml")
    def post(self, fleet_information):
        """
        Update and look up the x and y coordinates of the imperial fleet along with the encrypted message.
        :param fleet_information: Object containing satellite information
        {
            "satellites": [
                {
                      "name": "kenobi",
                      "distance": 100.0,
                      "message": ["este", "", "", "mensaje", ""]
                },
                ...
            ]
        }
        :return: Returns the x and y position of the fleet together with the message
          {
            "position": {
              "x": -100,
              "y": 75.5,
            },
            "message": "este es un mensaje secreto"
          }
        """
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
        """
        Validates the structure of the parameters sent
        :param data: Object containing satellite information
        {
            "satellites": [
                {
                      "name": "kenobi",
                      "distance": 100.0,
                      "message": ["este", "", "", "mensaje", ""]
                },
                ...
            ]
        }
        """
        json_schema_controller = JsonSchemaController()
        schema = json_schema_controller.get_json_schema("satellite-triangulation")
        validate(data, schema)
