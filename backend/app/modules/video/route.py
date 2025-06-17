from flask import Blueprint, make_response, jsonify, send_file
from .controller import VideoController


video_bp = Blueprint('video', __name__)
video_controller = VideoController()
@video_bp.route('/<video_file>', methods=['GET'])
def index(video_file):
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
    result=video_controller.index(video_file=video_file)
    if result['status'] == 'error':
      return make_response(jsonify(data=result), 404)
    
    video_path = result.get('path')
    
    if not video_path:
      return make_response(jsonify(data={"error": "Video path not found"}), 404)
      
    return send_file(video_path, mimetype='video/mp4', as_attachment=False)