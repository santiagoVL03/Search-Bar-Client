from app.modules.spark_search.route import spark_search_bp
from app.modules.video.route import video_bp
from app.modules.search.route import search_bp
from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_bp
from app.db.db import db


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(spark_search_bp, url_prefix='/api/v1/spark_search')
        app.register_blueprint(video_bp, url_prefix='/api/v1/video')
        app.register_blueprint(search_bp, url_prefix='/api/v1/search')
        app.register_blueprint(main_bp, url_prefix='/api/v1/main')


def initialize_db(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger