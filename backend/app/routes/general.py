from flask import (Blueprint, request, jsonify, session, g as globals)
import secrets
from datetime import datetime

bp = Blueprint('general', __name__)

@bp.route('/set_library', methods=["POST"])
def set_library():
    if 'session_id' not in session:
        create_session()
    
    if request.method == "POST":
        library = request.form.get("library")
        if not library:
            return jsonify({"error": "Library parameter is missing or empty"}), 400
        
    from ..utils.vector_store import load_vector_store
    from ..database import get_db
    path = get_db().execute(
        'SELECT documentation_file_uri FROM docs'
        'WHERE name=?',
        (library,)
    ).fetchall()

    if not path:
        return 404
    
    globals['vector_store'] = load_vector_store(path, session['session_id'])
    return 200
        


        
def create_session():
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex()
        session['created_at'] = datetime.now()

@bp.route('/create_session', methods=["GET", "POST"])
def create_session_route():
    create_session()
    return jsonify({'message':'session set sucessfully'}), 200
