from quasarservice.app import db
from quasarservice.app.exceptions.errors import SatelliteNotFound
from quasarservice.app.models import Satellite


class SatelliteManager(object):
    def __init__(self, db_session=None):
        if not db_session:
            self.__db_session = db.session
        else:
            self.__db_session = db_session

    def get_satellites(self):
        try:
            return (
                self.__db_session.query(
                    Satellite.name,
                    Satellite.position,
                    Satellite.distance,
                    Satellite.message,
                )
                .filter(
                    Satellite.distance.isnot(None),
                    Satellite.message.isnot(None),
                )
                .all()
            )
        except Exception as e:
            raise e

    def get_satellite_by_filters(self, filters):
        try:
            db_query = self.__db_session.query(Satellite).filter_by(**filters)
            return db_query.first()

        except Exception as e:
            raise e

    def create_satellite(self, filters, new_values, autocommit=False):
        try:
            satellite = self.get_satellite_by_filters(filters)

            if satellite:
                self.update_satellite_by_filters(filters, new_values)
            else:
                satellite = Satellite(**new_values)
                self.__db_session.add(satellite)
            self.__db_session.commit() if autocommit else self.__db_session.flush()
            return satellite
        except Exception as e:
            self.__db_session.rollback()
            raise e

    def update_satellite_by_filters(self, filters, new_values, autocommit=False):
        try:
            satellite = self.get_satellite_by_filters(filters)
            if not satellite:
                raise SatelliteNotFound

            satellite_updated = (
                self.__db_session.query(Satellite)
                .filter_by(**filters)
                .update(new_values)
            )
            self.__db_session.commit() if autocommit else self.__db_session.flush()

            return satellite
        except SatelliteNotFound as e:
            raise e
        except Exception as e:
            self.__db_session.rollback()
            raise e
