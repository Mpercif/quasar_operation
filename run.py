from flasgger import Swagger
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager, Server, Shell

from app import app, db
from app.api.resources.ImperialFleet import ImperialFleet
from app.api.resources.Satellite import Satellite
from default_config import APIDOCS_PATH

app.config["SWAGGER"] = {
    "description": "Quasar Operation Service API Docs",
    "version": "0.1.1",
}

swagger = Swagger(app, template_file=APIDOCS_PATH + "/base.yml")
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
    ImperialFleet, "/topsecret/<string:fleet_information>", endpoint="Satellite-triangulation"
)

api.add_resource(Satellite, "/topsecret_split/<string:satellite_name>", endpoint="Satellite-info")


if __name__ == "__main__":
    manager.run()
