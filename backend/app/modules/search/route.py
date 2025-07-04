from flask import Blueprint, make_response, jsonify, request
from .controller import SearchController

# THIS CONTROLLER WILL BE DEPRECATED IN THE FUTURE, IT IS JUST A DEMO FOR THE SEARCH FUNCTIONALITY
# It will be replaced by a more robust implementation in Spark for the search functionality.

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
    search_word = request.args.get('word')
    result=search_controller.index(search_word)
    return make_response(jsonify(data=result))
      