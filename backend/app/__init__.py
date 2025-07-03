from flask import Flask
import os
from . import config
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv


def create_app(test_config=None):
    # Create a flask application object.
    app = Flask(__name__)

    app.config.from_mapping(
        UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads'),
        DATABASE = os.path.join(app.instance_path, 'database.db'),
        VECTOR_STORE = os.path.join(app.instance_path, 'chroma'),
        SESSION_FILE_DIR= os.path.join(app.instance_path, 'sessions')
    )

    # Load the configuration.
    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object(config.Config)

    Session(app)
    CORS(app)

    if not load_dotenv(os.path.join(app.root_path, "..", "varibles.env")):
        raise ValueError("Invalid env file")
    
    app.config["API_KEY"] = os.getenv("GENAI_API_KEY")

    try:
        os.makedirs(os.path.join(app.instance_path, 'uploads'))
    except OSError:
        pass

    try:
        os.makedirs(os.path.join(app.instance_path, 'data'))
    except OSError:
        pass
    
    from . import database
    database.init_app(app)

    from .routes import general, docs
    app.register_blueprint(general.bp)
    app.register_blueprint(docs.bp)

    return app


