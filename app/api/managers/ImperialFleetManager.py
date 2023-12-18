from app import db
from app.models import ImperialFleet


class ImperialFleetManager(object):
    """
    Contains methods to access to data related to imperial_fleet model
    """
    def __init__(self, db_session=None):
        """
        Init ImperialFleetManager instance setting database session
        otherwise use the default db.session
        :param db_session: (Optional) SQLAlchemy session instance
        """
        if not db_session:
            self.__db_session = db.session
        else:
            self.__db_session = db_session

    def create_new_status_fleet(self, message, position, autocommit=False):
        """
        Create a new fleet status
        :param message: message of the fleet. "este es un mensaje secreto"
        :param position: x and y coordinates of the fleet. '"position": { "x": -100, "y": 75.5}'
        :param autocommit: flag to know if tha changes must be committed
        """
        try:
            new_status_fleet = ImperialFleet(message, position)
            self.__db_session.add(new_status_fleet)
            self.__db_session.commit() if autocommit else self.__db_session.flush()

            return new_status_fleet
        except Exception as e:
            self.__db_session.rollback()
            raise e
