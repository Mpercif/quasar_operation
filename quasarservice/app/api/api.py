from flask_restful import Api

from quasarservice.app import app
from quasarservice.app.api.resources.ImperialFleet import ImperialFleet
from quasarservice.app.api.resources.Satellite import Satellite

api = Api(app)

api.add_resource(
    ImperialFleet, "/topsecret/<string:satellite_triangulation>", endpoint="Satellite-triangulation"
)

api.add_resource(Satellite, "/topsecret_split/<string:satellite_name>", endpoint="Satellite-info")

if __name__ == "__main__":
    app.run()
