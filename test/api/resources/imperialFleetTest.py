import json
import unittest


import six
from contexter import Contexter
from mock import MagicMock

from app import app
from app.api import api
from app.api.controllers.ImperialFleetController import ImperialFleetController
from helpers.testHelper import build_patches


class ImperialTestResource(unittest.TestCase):

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
    endpoint_url = "/topsecret/{}".format(json.dumps(data))

    def get_patches(self, new_patches=None):

        imperial_fleet_controller_mock = ImperialFleetController()

        imperial_fleet_controller_mock.setup_satellite_configuration = MagicMock(
            return_value=self.data["satellites"],
        )
        imperial_fleet_controller_mock.triangulate_position_float = MagicMock(
            return_value={
                "position": {"x": -500, "y": 200},
                "message": "este es un mensaje secreto",
            },
        )

        patches = {
            "app.api.resources.ImperialFleet.ImperialFleetController": {
                "return_value": imperial_fleet_controller_mock
            }
        }

        if new_patches is not None:
            for key, value in six.iteritems(new_patches):
                patches[key] = value

        return build_patches(patches)

    def test_topsecret_endpoint_success(self):
        patches = self.get_patches()
        with Contexter(*patches):
            client = app.test_client()
            res = client.post(self.endpoint_url)
            response = json.loads(res.data)
            assert res.status_code == 200
            assert response["message"] == "este es un mensaje secreto"
            assert response["position"]["x"] == -500
            assert response["position"]["y"] == 200

    def test_topsecret_endpoint_no_success(self):
        new_data = self.data
        new_data["satellites"][1]["message"] = ["un", "es", "", "", "secreto"]
        endpoint_url = "/topsecret/{}".format(json.dumps(new_data))

        imperial_fleet_controller_mock = ImperialFleetController()
        imperial_fleet_controller_mock.setup_satellite_configuration = MagicMock(
            return_value=self.data["satellites"],
        )
        patches = {
            "app.api.resources.ImperialFleet.ImperialFleetController": {
                "return_value": imperial_fleet_controller_mock
            }
        }
        with Contexter(*build_patches(patches)):
            client = app.test_client()
            res = client.post(endpoint_url)
            assert res.status_code == 404
            assert res.status == "404 NOT FOUND"

    def test_topsecret_endpoint_invalid_structure_data(self):
        new_data = ["un", "es", "", "", "secreto"]
        endpoint_url = "/topsecret/{}".format(json.dumps(new_data))

        with Contexter():
            client = app.test_client()
            res = client.post(endpoint_url)
            assert res.status_code == 400
            assert "is not of type u'object'" in res.data

    def test_topsecret_endpoint_value_error_except(self):
        endpoint_url = "/topsecret/{}".format(self.data)
        with Contexter():
            client = app.test_client()
            res = client.post(endpoint_url)
            assert res.status_code == 400
            assert res.status == "400 BAD REQUEST"

    def test_topsecret_endpoint_server_error(self):
        with Contexter():
            client = app.test_client()
            res = client.post(self.endpoint_url)
            assert res.status_code == 500
