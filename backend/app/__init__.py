from flask import Flask, session
import os
from . import config
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
from cachelib.file import FileSystemCache
from datetime import datetime, timedelta
import time
import threading
import shutil



def create_app(test_config=None):
    # Create a flask application object.
    app = Flask(__name__)

    app.config.from_mapping(
        UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads'),
        DATABASE = os.path.join(app.instance_path, 'database.db'),
        VECTOR_STORE = os.path.join(app.instance_path, 'chroma'),
        SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir=os.path.join(app.instance_path, "sessions"))
    )

    active_sessions = {}
    lock = threading.Lock()

    def clear_expired_sessions():
        while True:
            time.sleep(10)
            print("Thread running")

            current_time = datetime.now()
            with lock:  # Acquire the lock before accessing the shared resource
                for session_id in list(active_sessions.keys()):
                    last_activity = active_sessions[session_id]
                    # print(session_id+ " : "+ str(last_activity))
                    if current_time - last_activity > timedelta(seconds=30):
                        print("removing session", end="\n\n")
                        
                        from .utils.chroma import remove_collection 
                        remove_collection(session_id, app.config["VECTOR_STORE"])  # Remove any collections from vector_store

                        # Remove any data associated with the session
                        try:
                            shutil.rmtree(os.path.join(app.instance_path,"uploads", session_id))
                        except FileNotFoundError:
                            pass 

                        app.session_interface.cache.delete(session_id)
                        del active_sessions[session_id] 

    threading.Thread(target=clear_expired_sessions, daemon=True).start()


    @app.before_request
    def track_session_activity():
        print("Hello",end="\n\n")
        session_id = session.get('session_id')
        if session_id:
            with lock:  # Acquire the lock before modifying the shared resource
                active_sessions[session_id] = datetime.now()


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


