from flask import Blueprint, make_response, jsonify, request
from .controller import Spark_searchController


spark_search_bp = Blueprint('spark_search', __name__)
spark_search_controller = Spark_searchController()
@spark_search_bp.route('/', methods=['GET'])
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
    result=spark_search_controller.index(search_word)
    return make_response(jsonify(data=result))
      