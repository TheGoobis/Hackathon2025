from flask import Blueprint, make_response, jsonify
from .controller import MainController


main_bp = Blueprint('main', __name__)
main_controller = MainController()
@main_bp.route('/', methods=['GET'])
def index():
    return "<h1>Welcome to the Wildlife Sightings Visualizer!</h1>"
      