import json

from app.api.controllers.SatelliteController import SatelliteController
from app.api.managers.ImperialFleetManager import ImperialFleetManager
from app.exceptions.errors import SatelliteValidationNotSuccess
from helpers.locationAndMessageDecryptHelper import (
    LocationAndMessageDecryptHelper,
)


class ImperialFleetController(object):
    def triangulate_position_float(self, fleet_information):
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
        return location_message_helper.get_message(
            location_message_helper.get_parameter_list("message")
        )

    @staticmethod
    def get_location_fleet(location_message_helper):
        return location_message_helper.get_location(
            location_message_helper.get_parameter_list("message")
        )

    @staticmethod
    def create_new_status_fleet(new_status):
        ImperialFleetManager().create_new_status_fleet(
            new_status["message"], json.dumps(new_status["position"])
        )
