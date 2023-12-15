from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager, Server, Shell

from quasarservice.app import app, db
from quasarservice.app.api.resources.ImperialFleet import ImperialFleet
from quasarservice.app.api.resources.Satellite import Satellite

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command(
    "runserver", Server(port=5000, use_debugger=False, use_reloader=True, threaded=True)
)

api = Api(app)

api.add_resource(
    ImperialFleet, "/topsecret/<string:satellite_triangulation>", endpoint="Satellite-triangulation"
)

api.add_resource(Satellite, "/topsecret_split/<string:satellite_name>", endpoint="Satellite-info")


if __name__ == "__main__":
    manager.run()
