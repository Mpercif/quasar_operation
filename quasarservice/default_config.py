import os

basedir = os.path.abspath(os.path.dirname(__file__))
APIDOCS_PATH = basedir + "/app/api/apidocs"
JSON_SCHEMA_PATH = basedir + "/app/api/json_schemas"
SECRET_KEY = "fdsjkEERkjkW1jk$5Jk%#12dsfdsadjk32"
SQLALCHEMY_DATABASE_URI = (
    os.environ.get("QS_DATABASE_URL") or "postgresql://postgres:testenv@localhost/mercadolibre"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False