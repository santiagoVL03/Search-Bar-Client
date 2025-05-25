from flask import Blueprint, make_response, jsonify
from .controller import SearchController


search_bp = Blueprint('search', __name__)
search_controller = SearchController()
@search_bp.route('/', methods=['GET'])
def index():
    """ Example endpoint with simple greeting.
    ---
    tags:
      - Example API
    responses:
      200:
        description: A simple greeting
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello World!"
    """
    result=search_controller.index()
    return make_response(jsonify(data=result))
      