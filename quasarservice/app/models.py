from sqlalchemy import Sequence

from quasarservice.app import db


class ImperialFleet(db.Model):
    __tablename__ = "imperial_fleet"

    id = db.Column(db.Integer, Sequence("imperial_fleet_id_seq"), primary_key=True)
    position = db.Column(db.String(100), unique=True, nullable=False)
    message = db.Column(db.String(300), unique=True, nullable=False)

    def __init__(self, position, message):
        self.position = position
        self.message = message

class Satellite(db.Model):
    __tablename__ = "satellite"

    id = db.Column(db.Integer, Sequence("satellite_id_seq"), primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    distance = db.Column(db.Float(), nullable=True)
    message = db.Column(db.String(300), nullable=True)

    def __init__(self, name, position, distance, message):
        self.name = name
        self.position = position
        self.distance = distance
        self.message = message
