from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("quasarservice.default_config")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:testenv@localhost/mercadolibre"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
