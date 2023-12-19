import json
import unittest
from copy import copy

import six
from contexter import Contexter
from mock import MagicMock

from app import app
from app.api import api
from app.api.controllers.SatelliteController import SatelliteController
from app.api.managers.SatelliteManager import SatelliteManager
from helpers.testHelper import build_patches


class SatelliteGetTestResource(unittest.TestCase):

    data = {
        "data": json.dumps(
            {
                "distance": 100.0,
                "message": ["este", "", "", "mensaje", ""],
            }
        )
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
        satellite_controller_mock.update_satellite_data = MagicMock(return_value={})

        patches = {
            "app.api.resources.Satellite.SatelliteController": {
                "return_value": satellite_controller_mock
            },
        }

        if new_patches is not None:
            for key, value in six.iteritems(new_patches):
                patches[key] = value

        return build_patches(patches)

    def test_topsecret_split_post_success(self):
        patches = self.get_patches()

        with Contexter(*patches):
            client = app.test_client()
            res = client.post(self.endpoint_url, query_string=self.data)

            assert res.status_code == 200
            assert res.data == "Satellite data have been updated"

    def test_topsecret_split_post_no_found(self):
        satellite_manager_mock = SatelliteManager()
        satellite_manager_mock.get_satellite_by_filters = MagicMock(return_value=None)

        patches = {
            "app.api.controllers.SatelliteController.SatelliteManager": {
                "return_value": satellite_manager_mock
            },
        }

        with Contexter(*build_patches(patches)):
            client = app.test_client()
            res = client.post(self.endpoint_url, query_string=self.data)
            assert res.status_code == 404
            assert res.status == "404 NOT FOUND"

    def test_topsecret_endpoint_post_invalid_structure_data(self):
        new_data = copy(self.data)
        new_data["data"] = json.dumps(["test", "error"])

        with Contexter():
            client = app.test_client()
            res = client.post(self.endpoint_url, query_string=new_data)
            assert res.status_code == 400
            assert "is not of type u'object'" in res.data

    def test_topsecret_endpoint_post_value_error_except(self):
        new_data = copy(self.data)
        new_data["data"] = ["test", "error"]
        with Contexter():
            client = app.test_client()
            res = client.post(self.endpoint_url, query_string=new_data)
            assert res.status_code == 400
            assert res.status == "400 BAD REQUEST"

    def test_topsecret_endpoint_post_server_error(self):
        with Contexter():
            client = app.test_client()
            res = client.post(self.endpoint_url, query_string={})
            assert res.status_code == 500
