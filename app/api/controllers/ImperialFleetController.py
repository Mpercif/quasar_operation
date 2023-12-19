import json

from app.api.controllers.SatelliteController import SatelliteController
from app.api.managers.ImperialFleetManager import ImperialFleetManager
from app.api.exceptions.errors import SatelliteValidationNotSuccess
from helpers.locationAndMessageDecryptHelper import (
    LocationAndMessageDecryptHelper,
)


class ImperialFleetController(object):
    """
    Contains methods related to imperial fleet
    """
    def triangulate_position_float(self, fleet_information):
        """
        :param fleet_information: List containing satellite information.
        [
            {
                  "name": "kenobi",
                  "distance": 100.0,
                  "message": ["este", "", "", "mensaje", ""]
            },
            ...
        ]
        :return: Returns the x and y coordinates of the fleet together with the message
          {
            "position": {
              "x": -100,
              "y": 75.5,
            },
            "message": "este es un mensaje secreto"
          }
        """
        try:
            location_message_helper = LocationAndMessageDecryptHelper(fleet_information)
            message = self.get_message_encrypted(location_message_helper)
            position = self.get_location_fleet(location_message_helper)
            response = {"message": message, "position": position}
            self.create_new_status_fleet(response)

            return response

        except SatelliteValidationNotSuccess as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def setup_satellite_configuration(fleet_information):
        """
        Loops the information of each satellite and creates the satellite in the database.
        :param fleet_information: List containing satellite information.
        [
            {
              "name": "kenobi",
              "distance": 100.0,
              "message": ["este", "", "", "mensaje", ""]
            },
            ...
        ]
        :return:
        """
        try:
            new_fleet_info = []
            for satellite in fleet_information:
                new_satellite = SatelliteController().create_satellite_data(satellite)
                new_fleet_info.append(new_satellite)
            return new_fleet_info
        except Exception as e:
            raise e

    @staticmethod
    def get_message_encrypted(location_message_helper):
        """
        Calls get_message method to decrypt the message
        :param location_message_helper: LocationAndMessageDecryptHelper instance
        """
        return location_message_helper.get_message(
            location_message_helper.get_parameter_list("message")
        )

    @staticmethod
    def get_location_fleet(location_message_helper):
        """
        Calls get_message method to find position
        :param location_message_helper: LocationAndMessageDecryptHelper instance
        """
        return location_message_helper.get_location()

    @staticmethod
    def create_new_status_fleet(new_status):
        """
        Create new fleet status
        :param new_status: x and y coordinates of the fleet together with the message
          {
            "position": {
              "x": -100,
              "y": 75.5,
            },
            "message": "este es un mensaje secreto"
          }
        """
        try:
            new_value = {
                "message": new_status["message"],
                "position": json.dumps(new_status["position"])
            }
            ImperialFleetManager().create_new_status_fleet(new_value, True)
        except Exception as e:
            raise e
