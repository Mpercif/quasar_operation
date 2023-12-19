import json

from flasgger import swag_from
from flask import request
from flask_restful import Resource
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from app.api.controllers.ImperialFleetController import ImperialFleetController
from app.api.controllers.JsonSchemaController import JsonSchemaController
from app.api.controllers.SatelliteController import SatelliteController
from app.api.exceptions.errors import (
    SatelliteValidationNotSuccess,
    SatelliteNotFound,
)
from default_config import APIDOCS_PATH
from helpers.responseHelper import json_response


class Satellite(Resource):
    """
    Satellite API endpoints
    """
    @swag_from(APIDOCS_PATH + "/satellite-update.yml")
    def post(self, satellite_name):
        """
        Update the x and y coordinates and encrypted message of the satellite
        :param satellite_name: Name of the satellite to be updated
        :return: Successful update message. Ie, Satellite data have been updated.
        """
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

    @swag_from(APIDOCS_PATH + "/satellite-position.yml")
    def get(self, satellite_name):
        """
        Look up the x and y coordinates of the imperial fleet with new satellite information
        :param satellite_name: Name of the satellite.
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
            data = json.loads(request.args.get("data"))
            self.__validate_params(data)
            data.update({"name": satellite_name})
            satellites = SatelliteController().get_missing_satellites(data)
            response = ImperialFleetController().triangulate_position_float(satellites)

            return response
        except SatelliteValidationNotSuccess as e:
            return json_response({"message": e}, e.code)
        except SatelliteNotFound as e:
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
              "distance": 100.0,
              "message": ["este", "", "", "mensaje", ""]
            }
        """
        json_schema_controller = JsonSchemaController()
        schema = json_schema_controller.get_json_schema("satellite-info")
        validate(data, schema)
