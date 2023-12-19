import json
import unittest
from copy import copy

import six
from contexter import Contexter
from mock import MagicMock

from app.api.controllers.SatelliteController import SatelliteController
from app.api.managers.SatelliteManager import SatelliteManager
from app.api.exceptions.errors import SatelliteNotFound
from helpers.testHelper import build_patches

class SatelliteDbMock():
    def __init__(self):
        self.id = 1
        self.name = "kenobi"
        self.position = "[100, -100]"
        self.distance = 100.5
        self.message = json.dumps(["este", "", "", "mensaje", ""])


class FleetControllerTest(unittest.TestCase):
    satellite_data = {
        "name": "kenobi",
        "distance": 100.5,
        "message": ["este", "", "", "mensaje", ""]
    }

    def get_patches(self, new_patches=None):
        satellite_manager_mock = SatelliteManager()
        satellite_db_mock = SatelliteDbMock()
        satellite_manager_mock.get_satellite_by_filters = MagicMock(return_value=satellite_db_mock)
        satellite_manager_mock.create_satellite = MagicMock(return_value=satellite_db_mock)
        satellite_manager_mock.update_satellite_by_filters = MagicMock(return_value=satellite_db_mock)
        satellite_manager_mock.get_satellites = MagicMock(return_value=[satellite_db_mock, satellite_db_mock, satellite_db_mock])
        patches = {
            "app.api.controllers.SatelliteController.SatelliteManager": {
                "return_value": satellite_manager_mock
            },
        }

        if new_patches is not None:
            for key, value in six.iteritems(new_patches):
                patches[key] = value

        return build_patches(patches)

    def test_update_satellite_data_success(self):
        satellite_data = copy(self.satellite_data)
        patches = self.get_patches()
        with Contexter(*patches):
            response = SatelliteController().update_satellite_data(satellite_data)
            assert isinstance(response["message"], list)
            assert response["distance"] == self.satellite_data["distance"]
            assert response["name"] == "kenobi"
            assert isinstance(response["position"], list)

    def test_update_satellite_data_no_success(self):
        satellite_manager_mock = SatelliteManager()
        satellite_manager_mock.get_satellite_by_filters = MagicMock(return_value=None)
        satellite_data = copy(self.satellite_data)

        patches = {
            "app.api.controllers.SatelliteController.SatelliteManager": {
                "return_value": satellite_manager_mock
            },
        }

        with Contexter(*build_patches(patches)):
            try:
                response = SatelliteController().update_satellite_data(satellite_data)
                assert False
            except SatelliteNotFound as e:
                assert True
            except Exception as e:
                assert False

    def test_update_satellite_data_error(self):
        new_patches = {}
        satellite_data = copy(self.satellite_data)
        with Contexter(*build_patches(new_patches)):
            try:
                response = SatelliteController().update_satellite_data(satellite_data)
                assert False
            except SatelliteNotFound as e:
                assert False
            except Exception as e:
                assert True

    def test_create_satellite_data_satellite_found(self):
        satellite_data = copy(self.satellite_data)
        patches = self.get_patches()
        with Contexter(*patches):
            response = SatelliteController().create_satellite_data(satellite_data)
            assert isinstance(response["message"], list)
            assert response["distance"] == self.satellite_data["distance"]
            assert response["name"] == "kenobi"
            assert isinstance(response["position"], list)

    def test_create_satellite_data_satellite_error(self):
        with Contexter():
            try:
                response = SatelliteController().create_satellite_data(self.satellite_data)
                assert False
            except Exception as e:
                assert True

    def test_get_valid_satellites_data_success(self):
        patches = self.get_patches()
        with Contexter(*patches):
            response = SatelliteController().get_valid_satellites_data()
            assert isinstance(response, list)
            assert isinstance(response[0]["message"], list)
            assert response[0]["distance"] == self.satellite_data["distance"]
            assert response[0]["name"] == "kenobi"
            assert isinstance(response[0]["position"], list)

    def test_get_valid_satellites_data_error(self):

        with Contexter():
            try:
                response = SatelliteController().get_valid_satellites_data()
                assert False
            except Exception as e:
                assert True

    def test_get_satellite_success(self):
        patches = self.get_patches()
        with Contexter(*patches):
            response = SatelliteController().get_satellite(self.satellite_data)
            assert isinstance(response["message"], list)
            assert response["distance"] == self.satellite_data["distance"]
            assert response["name"] == "kenobi"
            assert isinstance(response["position"], list)

    def test_get_satellite_error(self):
        with Contexter():
            try:
                response = SatelliteController().get_satellite(self.satellite_data)
                assert False
            except Exception as e:
                assert True
