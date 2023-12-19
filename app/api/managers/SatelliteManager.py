from app import db
from app.api.exceptions.errors import SatelliteNotFound
from app.models import Satellite


class SatelliteManager(object):
    """
    Contains methods to access to data related to satellite model
    """
    def __init__(self, db_session=None):
        """
        Init SatelliteManager instance setting database session
        otherwise use the default db.session
        :param db_session: (Optional) SQLAlchemy session instance
        """
        if not db_session:
            self.__db_session = db.session
        else:
            self.__db_session = db_session

    def get_satellites(self):
        """
        Gets all satellites that have distance and position
        :return: Satellite object: corresponding to the filters.
        """
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
                    Satellite.position.isnot(None),
                )
                .all()
            )
        except Exception as e:
            raise e

    def get_satellite_by_filters(self, filters):
        """
        Get satellite by filters
        :param filters: filter data. Ie, {'name': "sato"}
        :return: Satellite object: corresponding to the filters.
        """
        try:
            satellite = self.__db_session.query(Satellite).filter_by(**filters)
            if not satellite:
                raise SatelliteNotFound

            return satellite.first()

        except SatelliteNotFound as e:
            raise e
        except Exception as e:
            raise e

    def create_satellite(self, filters, new_values, autocommit=False):
        """
        Get satellite by filters
        :param filters: filter data. Ie, {'name': "sato"}
        :param new_values: object data. Ie, {
          "distance": 100.0,
          "message": ["este", "", "", "mensaje", ""]
        }
        :param autocommit: flag to know if tha changes must be committed
        :return: Satellite object: new satellite with the new values.
        """
        try:
            satellite = self.get_satellite_by_filters(filters)

            if satellite:
                self.update_satellite_by_filters(filters, new_values)
            else:
                new_values.update(filters)
                satellite = Satellite(**new_values)
                self.__db_session.add(satellite)
            self.__db_session.commit() if autocommit else self.__db_session.flush()
            return satellite
        except Exception as e:
            self.__db_session.rollback()
            raise e

    def update_satellite_by_filters(self, filters, new_values, autocommit=False):
        """
        Update satellite by filters
        :param filters: filter data. Ie, {'name': "sato"}
        :param new_values: object data. Ie, {
          "distance": 100.0,
          "message": ["este", "", "", "mensaje", ""]
        }
        :param autocommit: flag to know if tha changes must be committed
        :return: Satellite object: satellite update with the new values.
        """
        try:
            satellite = self.get_satellite_by_filters(filters)
            if not satellite:
                raise SatelliteNotFound

            self.__db_session.query(Satellite).filter_by(**filters).update(new_values)
            self.__db_session.commit() if autocommit else self.__db_session.flush()

            satellite = self.get_satellite_by_filters(filters)

            return satellite
        except SatelliteNotFound as e:
            raise e
        except Exception as e:
            self.__db_session.rollback()
            raise e
