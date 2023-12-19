import json

from app.api.managers.SatelliteManager import SatelliteManager
from app.api.exceptions.errors import (
    SatelliteNotFound,
    SatelliteValidationNotSuccess,
)


class SatelliteController(object):
    """
    Contains methods related to satellite
    """
    @staticmethod
    def update_satellite_data(satellite_data):
        """
        Update satellite information
        :param satellite_data: Object with satellite information
        {
          "name": "kenobi",
          "distance": 100.0,
          "message": ["este", "", "", "mensaje", ""]
        }
        :return: Returns the updated information of the formatted satellite.
        {
          "name": "kenobi",
          "distance": 100.0,
          "message": ["este", "", "", "mensaje", ""]
        }
        """
        try:
            satellite_manager = SatelliteManager()
            filters = {"name": satellite_data.pop("name")}
            new_data = {
                "distance": satellite_data["distance"],
                "message": json.dumps(satellite_data["message"]),
            }
            satellite_update = satellite_manager.update_satellite_by_filters(
                filters, new_data, True
            )
            satellite_format = SatelliteController().format_satellite_data(
                satellite_update
            )
            return satellite_format
        except SatelliteNotFound as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def create_satellite_data(satellite_data):
        """
        Create the satellite in the database.
        :param satellite_data: Object with satellite information
        {
          "name": "skywalker",
          "distance": 115.5,
          "message": ["", "es", "", "un", ""]
        }
        :return: Returns formatted information from the new satellite.
        {
          "name": "skywalker",
          "distance": 115.5,
          "message": ["", "es", "", "un", ""]
        }
        """
        try:
            satellite_manager = SatelliteManager()
            filters = {"name": satellite_data["name"]}
            new_data = {
                "distance": satellite_data["distance"],
                "message": json.dumps(satellite_data["message"]),
            }
            if satellite_data.get("position"):
                new_data.update({
                    "position": json.dumps(satellite_data["position"])
                })

            new_satellite = satellite_manager.create_satellite(
                filters, new_data, True
            )
            satellite_format = SatelliteController().format_satellite_data(
                new_satellite
            )
            return satellite_format
        except Exception as e:
            raise e

    @staticmethod
    def get_valid_satellites_data():
        """
        Obtains the valid satellites (those with position and distance) and returns them formatted.
        :return:
        [
            {
              "name": "kenobi",
              "distance": 100.0,
              "message": ["este", "", "", "mensaje", ""]
            },
            ...
        ]
        """
        try:
            satellite_manager = SatelliteManager()
            satellites = satellite_manager.get_satellites()
            satellite_data = []
            for satellite in satellites:
                satellite_format = SatelliteController().format_satellite_data(
                    satellite
                )
                satellite_data.append(satellite_format)

            return satellite_data

        except Exception as e:
            raise e

    def get_missing_satellites(self, satellite_info):
        """
        obtains the information of the other satellites and returns the information of the
        valid satellites together with the information sent by parameter
        :param satellite_info: Object with satellite information
        {
          "name": "skywalker",
          "distance": 115.5,
          "message": ["", "es", "", "un", ""]
        }
        :return:
        [
            {
              "name": "kenobi",
              "distance": 100.0,
              "message": ["este", "", "", "mensaje", ""]
            },
            {
              "name": "skywalker",
              "distance": 115.5,
              "message": ["", "es", "", "un", ""]
            }
            ...
        ]
        """
        try:
            current_satellite_name = satellite_info["name"]
            satellites = SatelliteController().get_valid_satellites_data()
            missing_satellites = list(
                filter(lambda x: x["name"] != current_satellite_name, satellites)
            )
            current_satellite = list(
                filter(lambda x: x["name"] == current_satellite_name, satellites)
            )

            if len(satellites) < 1:
                raise SatelliteValidationNotSuccess

            if not current_satellite:
                current_satellite = SatelliteController().get_satellite({"name": current_satellite_name})
            else:
                current_satellite = current_satellite[0]

            current_satellite.update(satellite_info)
            missing_satellites.append(current_satellite)

            return missing_satellites

        except SatelliteNotFound as e:
            raise e
        except SatelliteValidationNotSuccess as e:
            raise e
        except Exception as e:
            raise e

    def get_satellite(self, satellite_info):
        """
        Obtains the satellite using the filters
        :param satellite_info: Object with satellite information
        {
          "name": "skywalker",
          "distance": 115.5,
          "message": ["", "es", "", "un", ""]
        }
        :return:
        """
        try:
            satellite_manager = SatelliteManager()
            satellite = satellite_manager.get_satellite_by_filters(satellite_info)
            return SatelliteController().format_satellite_data(
                satellite
            )
        except SatelliteNotFound as e:
            raise e
        except Exception as e:
            raise e


    @staticmethod
    def format_satellite_data(satellite):
        """
        Formats a Satellite instance in Json format
        :param satellite: Satellite instance
        :return: Object formatted in json
        {
          "name": "skywalker",
          "distance": 115.5,
          "message": ["", "es", "", "un", ""],
          "position": [500, 600]
        }
        """
        return {
            "distance": satellite.distance,
            "message": json.loads(satellite.message) if satellite.message else [],
            "name": satellite.name,
            "position": json.loads(satellite.position) if satellite.position else [],
        }
