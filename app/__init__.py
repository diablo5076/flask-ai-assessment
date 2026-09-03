from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.db import check_database_connection
from app.services import initialize_prompt

load_dotenv()


def create_app():
    app = Flask(__name__)

    CORS(app)

    check_database_connection()
    initialize_prompt()

    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app