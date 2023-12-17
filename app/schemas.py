from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from app.models import ImperialFleet, Satellite


class ImperialFleetSchema(ModelSchema):
    class Meta:
        model = ImperialFleet

    id = fields.Method("get_imperial_float_id", dump_only=True)
    position = fields.Method("get_imperial_float_position", dump_only=True)
    message = fields.Method("get_imperial_float_message", dump_only=True)

    def get_imperial_float_id(self, imperial_float):
        return imperial_float.id

    def get_imperial_float_position(self, imperial_float):
        return imperial_float.position

    def get_imperial_float_message(self, imperial_float):
        return imperial_float.message


class SatelliteSchema(ModelSchema):
    class Meta:
        model = Satellite

    id = fields.Method("get_satellite_id", dump_only=True)
    position = fields.Method("get_satellite_position", dump_only=True)
    distance = fields.Method("get_satellite_distance", dump_only=True)
    message = fields.Method("get_satellite_message", dump_only=True)

    def get_satellite_id(self, satellite):
        return satellite.id

    def get_satellite_position(self, satellite):
        return satellite.position

    def get_satellite_distance(self, satellite):
        return satellite.distance

    def get_satellite_message(self, satellite):
        return satellite.message
