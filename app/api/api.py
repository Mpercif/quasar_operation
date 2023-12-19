#!flask/bin/python

from flask_restful import Api

from app import app
from app.api.resources.ImperialFleet import ImperialFleet
from app.api.resources.Satellite import Satellite

api = Api(app)

api.add_resource(
    ImperialFleet, "/topsecret/<string:fleet_information>", endpoint="Satellite-triangulation"
)

api.add_resource(Satellite, "/topsecret_split/<string:satellite_name>", endpoint="Satellite-info")

if __name__ == "__main__":
    app.run()
