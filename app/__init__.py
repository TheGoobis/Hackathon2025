from flask import Flask
from app.config.config import get_config_by_name
from app.initialize_functions import initialize_route, initialize_swagger

def create_app(config=None) -> Flask:
    app = Flask(__name__)

    if config:
        app.config.from_object(get_config_by_name(config))


    initialize_route(app)
    initialize_swagger(app)

    return app
