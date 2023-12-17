from quasarservice.app import db
from quasarservice.app.models import ImperialFleet


class ImperialFleetManager(object):
    def __init__(self, db_session=None):
        if not db_session:
            self.__db_session = db.session
        else:
            self.__db_session = db_session

    def create_new_status_fleet(self, message, position):
        try:
            new_status_fleet = ImperialFleet(message, position)
            self.__db_session.add(new_status_fleet)
            self.__db_session.commit()

            return new_status_fleet
        except Exception as e:
            self.__db_session.rollback()
            raise e
