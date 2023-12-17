import json

from app.api.managers.SatelliteManager import SatelliteManager
from app.exceptions.errors import (
    SatelliteNotFound,
    SatelliteValidationNotSuccess,
)


class SatelliteController(object):
    @staticmethod
    def update_satellite_data(satellite_data):
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
        try:
            satellite_manager = SatelliteManager()
            filters = {"name": satellite_data["name"]}
            new_satellite = satellite_manager.create_satellite(
                filters, satellite_data, True
            )
            satellite_format = SatelliteController().format_satellite_data(
                new_satellite
            )
            return satellite_format
        except Exception as e:
            raise e

    @staticmethod
    def get_valid_satellites_data():
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
        try:
            satellite_manager = SatelliteManager()
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
                satellite = satellite_manager.get_satellite_by_filters(
                    {"name": current_satellite_name}
                )
                current_satellite = SatelliteController().format_satellite_data(
                    satellite
                )
            else:
                current_satellite = current_satellite[0]

            current_satellite.update(satellite_info)
            missing_satellites.append(current_satellite)

            return missing_satellites

        except SatelliteValidationNotSuccess as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def format_satellite_data(satellite):
        return {
            "distance": satellite.distance,
            "message": json.loads(satellite.message) if satellite.message else [],
            "name": satellite.name,
            "position": json.loads(satellite.position) if satellite.position else [],
        }
