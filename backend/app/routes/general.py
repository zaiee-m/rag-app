from datetime import datetime
from flask import (Blueprint, request, jsonify, session, g as globals)
import secrets
import json

bp = Blueprint('general', __name__)

@bp.route('/set-library', methods=["POST"])
def set_library():
    if 'session_id' not in session:
        create_session()

    library  = None
    if request.method == "POST":
        library = request.form.get("library")

        if not library:
            return jsonify({"error": "Library parameter is missing or empty"}), 400

        from ..database import get_db

        path = get_db().execute(
            'SELECT documentation_file_uri FROM docs '
            'WHERE name=?',
            (library,)
        ).fetchall()

        if not path:
            return jsonify({'message':'Library not found.'}), 404

        session['collection_name'] = session['session_id']

        return jsonify({'message':'library sucessfully selected.'}), 200

def create_session():
    if 'session-id' not in session:
        session['session_id'] = secrets.token_hex()

        from ..utils.global_variables import active_sessions, lock
        with lock:
            active_sessions[session['session_id']] = datetime.now()


@bp.route('/create-session', methods=["GET", "POST"])
def create_session_route():
    create_session()
    return jsonify({'message':'session set sucessfully'}), 200
