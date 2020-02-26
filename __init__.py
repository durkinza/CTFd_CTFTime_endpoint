from flask import Blueprint
from flask_restplus import Api
from .routes import ctftime_namespace


def load(app):
    api = Blueprint("ctftime_api", __name__, url_prefix="/api/v1")
    CTFTime_API_v1 = Api(api, version="v1", doc=app.config.get("SWAGGER_UI"))
    CTFTime_API_v1.add_namespace(ctftime_namespace, "/ctftime")
    app.register_blueprint(api)
