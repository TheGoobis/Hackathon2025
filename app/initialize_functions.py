from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main as main_blueprint


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main_blueprint)

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger