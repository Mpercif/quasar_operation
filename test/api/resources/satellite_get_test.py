import json
import unittest
from copy import copy

import six
from contexter import Contexter
from mock import MagicMock

from app import app
from app.api import api
from app.api.controllers.ImperialFleetController import ImperialFleetController
from app.api.controllers.SatelliteController import SatelliteController
from helpers.testHelper import build_patches


class SatelliteGetResourceTest(unittest.TestCase):

    data = {
        "distance": 100.0,
        "message": ["este", "", "", "mensaje", ""],
    }

    data_missing = [
        {
            "name": "skywalker",
            "distance": 115.5,
            "message": ["", "es", "", "", "secreto"],
        },
        {
            "name": "kenobi",
            "distance": 100.0,
            "message": ["este", "", "", "mensaje", ""],
        },
        {"name": "sato", "distance": 142.7, "message": ["este", "", "un", "", ""]},
    ]

    endpoint_url = "/topsecret_split/kenobi"

    def get_patches(self, new_patches=None):

        satellite_controller_mock = SatelliteController()
        imperial_fleet_controller_mock = ImperialFleetController()

        satellite_controller_mock.get_missing_satellites = MagicMock(
            return_value=self.data_missing
        )
        imperial_fleet_controller_mock.triangulate_position_float = MagicMock(
            return_value={
                "position": {"x": -500, "y": 200},
                "message": "este es un mensaje secreto",
            },
        )

        patches = {
            "app.api.resources.Satellite.SatelliteController": {
                "return_value": satellite_controller_mock
            },
            "app.api.resources.Satellite.ImperialFleetController": {
                "return_value": imperial_fleet_controller_mock
            },
        }

        if new_patches is not None:
            for key, value in six.iteritems(new_patches):
                patches[key] = value

        return build_patches(patches)

    def test_topsecret_split_get_success(self):
        patches = self.get_patches()

        with Contexter(*patches):
            client = app.test_client()
            res = client.get(self.endpoint_url, data=json.dumps(self.data))
            response = json.loads(res.data)

            assert res.status_code == 200
            assert response["message"] == "este es un mensaje secreto"
            assert response["position"]["x"] == -500
            assert response["position"]["y"] == 200

    def test_topsecret_split_get_no_success(self):
        new_data_missing = self.data_missing
        new_data_missing[1]["message"] = ["un", "es", "", "", "secreto"]

        satellite_controller_mock = SatelliteController()
        satellite_controller_mock.get_missing_satellites = MagicMock(
            return_value=new_data_missing
        )

        patches = {
            "app.api.resources.Satellite.SatelliteController": {
                "return_value": satellite_controller_mock
            },
        }
        with Contexter(*build_patches(patches)):
            client = app.test_client()
            res = client.get(self.endpoint_url, data=json.dumps(self.data))
            assert res.status_code == 404
            assert res.status == "404 NOT FOUND"

    def test_topsecret_endpoint_get_invalid_structure_data(self):
        new_data = ["test", "error"]

        with Contexter():
            client = app.test_client()
            res = client.get(self.endpoint_url, data=json.dumps(new_data))
            assert res.status_code == 400
            assert "is not of type u'object'" in res.data

    def test_topsecret_endpoint_get_value_error_except(self):
        new_data = {
            "distance": None,
            "message": ["este", "", "", "mensaje", ""],
        }
        with Contexter():
            client = app.test_client()
            res = client.get(self.endpoint_url, data=json.dumps(new_data))
            assert res.status_code == 400
            assert res.status == "400 BAD REQUEST"

    def test_topsecret_endpoint_get_server_error(self):
        new_data = {
            "data": json.dumps(
                {
                    "distance": 100.0,
                    "message": ["este", "", "", "mensaje", ""],
                }
            )
        }
        with Contexter():
            client = app.test_client()
            res = client.get(self.endpoint_url, data=json.dumps(self.data))
            assert res.status_code == 500
