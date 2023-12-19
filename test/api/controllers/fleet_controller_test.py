import unittest
from copy import copy

import six
from contexter import Contexter
from mock import MagicMock

from app.api.controllers.ImperialFleetController import ImperialFleetController
from app.api.controllers.SatelliteController import SatelliteController
from app.api.managers.ImperialFleetManager import ImperialFleetManager
from app.api.exceptions.errors import SatelliteValidationNotSuccess
from helpers.testHelper import build_patches


class ImperialControllerTest(unittest.TestCase):

    data = {
        "satellites": [
            {
                "name": "kenobi",
                "distance": 100.0,
                "message": ["este", "", "", "mensaje", ""],
            },
            {
                "name": "skywalker",
                "distance": 115.5,
                "message": ["", "es", "", "", "secreto"],
            },
            {"name": "sato", "distance": 142.7, "message": ["este", "", "un", "", ""]},
        ]
    }

    status = {
        "position": {
            "x": -100,
            "y": 75.5,
        },
        "message": "este es un mensaje secreto",
    }

    def get_patches(self, new_patches=None):
        imperial_fleet_manager_mock = ImperialFleetManager()
        imperial_fleet_manager_mock.create_new_status_fleet = MagicMock(return_value={})

        patches = {
            "app.api.controllers.ImperialFleetController.ImperialFleetManager": {
                "return_value": imperial_fleet_manager_mock
            },
        }

        if new_patches is not None:
            for key, value in six.iteritems(new_patches):
                patches[key] = value

        return build_patches(patches)

    def test_triangulate_position_fleet_success(self):
        patches = self.get_patches()
        new_data = copy(self.data)
        new_data["satellites"][1]["message"] = ["", "es", "", "", "secreto"]

        with Contexter(*patches):
            response = ImperialFleetController().triangulate_position_float(
                new_data["satellites"]
            )
            assert response["message"] == "este es un mensaje secreto "
            # TEST PARA OBTENER LA POSICION

    def test_triangulate_position_fleet_no_found(self):
        new_data = copy(self.data)
        new_data["satellites"][1]["message"] = ["un", "es", "", "", "secreto"]
        patches = self.get_patches()
        with Contexter(*patches):
            try:
                response = ImperialFleetController().triangulate_position_float(
                    new_data["satellites"]
                )
                assert False
            except SatelliteValidationNotSuccess as e:
                assert True
            except Exception as e:
                assert False

    def test_triangulate_position_fleet_error(self):
        with Contexter():
            try:
                response = ImperialFleetController().triangulate_position_float(
                    self.data["satellites"]
                )
                assert False
            except SatelliteValidationNotSuccess as e:
                assert False
            except Exception as e:
                assert True

    def test_setup_satellite_configuration_success(self):
        imperial_fleet_manager_mock = ImperialFleetManager()
        imperial_fleet_manager_mock.create_new_status_fleet = MagicMock(return_value={})

        satellite_controller_mock = SatelliteController()
        satellite_controller_mock.create_satellite_data = MagicMock(
            return_value=self.data["satellites"][0]
        )

        patches = {
            "app.api.controllers.ImperialFleetController.ImperialFleetManager": {
                "return_value": imperial_fleet_manager_mock
            },
            "app.api.controllers.ImperialFleetController.SatelliteController": {
                "return_value": satellite_controller_mock
            },
        }
        data = [self.data["satellites"][0]]
        with Contexter(*build_patches(patches)):
            response = ImperialFleetController().setup_satellite_configuration(data)
            assert isinstance(response, list)
            assert response[0]["name"] == "kenobi"
            assert response[0]["distance"] == 100.0
            assert isinstance(response[0]["message"], list)

    def test_setup_satellite_configuration_error(self):
        data = [self.data["satellites"][0]]
        with Contexter(*self.get_patches()):
            try:
                response = ImperialFleetController().setup_satellite_configuration(data)
                assert False
            except Exception as e:
                assert True

    def test_create_new_status_fleet_success(self):
        with Contexter(*self.get_patches()):
            try:
                ImperialFleetController().create_new_status_fleet(self.status)
                assert True
            except Exception as e:
                assert False

    def test_create_new_status_fleet_error(self):
        with Contexter():
            try:
                ImperialFleetController().create_new_status_fleet(self.status)
                assert False
            except Exception as e:
                assert True

