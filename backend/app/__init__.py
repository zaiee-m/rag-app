from ctypes import util
from flask import Flask, session
import os
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
from cachelib.file import FileSystemCache
from datetime import datetime, timedelta
import time
import shutil
import threading

def create_app(test_config=None):
    # Create a flask application object.
    app = Flask(__name__)

    app.config.from_mapping(
        UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads'),
        DATABASE = os.path.join(app.instance_path, 'database.db'),
        VECTOR_STORE = os.path.join(app.instance_path, 'chroma'),
        SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir=os.path.join(app.instance_path, "sessions"))
    )

    from .config import Config

    # Load the configuration.
    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object(Config)

    Session(app)
    CORS(app)

    if not load_dotenv(os.path.join(app.root_path, "..", "varibles.env")):
        raise ValueError("Invalid env file")

    app.config["API_KEY"] = os.getenv("GENAI_API_KEY")

    # Create relevent directores if they don't exist
    # If instance folder doesn't exists it is also created by os.makedirs()
    try:
        os.makedirs(os.path.join(app.instance_path, 'uploads'))
    except OSError:
        pass

    try:
        os.makedirs(os.path.join(app.instance_path, 'data'))
    except OSError:
        pass

    # Initialse the database within the Flask app.
    # Now flask --app <app path> init_db command is available to initianlise the database
    # from the schema.sql fise
    # Also app.teardown_context() has excess to the close_db function to close the
    # database after the request has been processed.
    from . import database
    database.init_app(app)


    # A clean-up function that runs in a thread paralled to the main thread.
    # It checks for timed-out sessions intervally independent of
    # wether the server is currently handling any request or not.
    # After identifying a session, it deletes the session and any data
    # (chroma collection or uploaded fiels) relevent to that particular session.

    from .utils.global_variables import active_sessions, lock

    # Checks for timed-out sessions and deletes them.
    def clear_expired_sessions():
        while True:
            time.sleep(60)
            current_time = datetime.now()

            # Acquire the lock before accessing the shared resource
            with lock:
                for session_id in list(active_sessions.keys()):
                    last_activity = active_sessions[session_id]

                    # Check if the session has timed-out
                    # Threshold for deleting data is set higher than treshold for session expiration
                    # because we don't ever want to be in a situation where the user is trying to
                    # access deleted data.
                    if current_time - last_activity > timedelta(minutes=35):
                        # Remove any collections from vector_store tied to timed-out session
                        from .utils.chroma import remove_collection
                        remove_collection(session_id, app.config["VECTOR_STORE"])

                        # Remove any data associated with the session
                        try:
                            shutil.rmtree(os.path.join(app.instance_path,"uploads", session_id))
                        except FileNotFoundError:
                            pass

                        del active_sessions[session_id]

    # Initialise and run the thread.
    threading.Thread(target=clear_expired_sessions, daemon=True).start()

    # Functions to be run before a request is processed.
    @app.before_request
    def track_session_activity():
        session_id = session.get('session_id')

        # If the user has a valid session, set the last-accessed as now.
        # Else do nothing. The user is redirected to "/create-session" via some other path
        # that we need not be concerned here.
        if session_id:
            # Acquire the lock before modifying the shared resource.
            with lock:
                # Update the time at which session was last accessed.
                active_sessions[session_id] = datetime.now()

    # Register the blueprints
    from .routes import general, docs
    app.register_blueprint(general.bp)
    app.register_blueprint(docs.bp)

    # Return the current instane of the Flask app object the app.run() can be called upon
    # inside of a run.py file or else via the flask --app <app path> run command.
    return app
