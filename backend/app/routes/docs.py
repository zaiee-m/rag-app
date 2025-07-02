from flask import (
    request, 
    jsonify, 
    session,
    redirect,
    url_for,
    Blueprint,
    current_app,
    send_from_directory,
    g as globals
)

import os
from dotenv import load_dotenv
import asyncio
from werkzeug.utils import secure_filename

from ..database import get_db

bp = Blueprint('docs', __name__, url_prefix='/docs')

@bp.route("/search")
def search():
    libray = request.args.get("name")

    db = get_db()

    rows = db.execute(
        "SELECT * FROM libraries WHERE name LIKE ?",
        (libray+"%",)
    ).fetchall()
    

    if not rows:
        return jsonify({'error': 'Item not found'}), 404
    else:
        results = [dict(row) for row in rows]
        return jsonify(results)


@bp.route("/serve")
def serve():
    filename = request.args.get('filename')
    return send_from_directory(os.path.join(current_app.instance_path , f"{filename}.txt"))


@bp.route("/chat", methods=["POST"])
def chat():
    from ..utils.query import augment_query

    if 'session_id' not in session:
        from . import general
        general.create_session()

    if 'vector_store' not in globals:
        return jsonify({'error':'Either upload your own documentation or select one from available documentations.'}), 404

    if request.method == "POST":
        request_data = request.get_json() 

        if request_data is None:
            return jsonify({"error": "Invalid JSON in request body"}), 400

        query = request_data.get("query")
        library = request_data.get("library")
        
        if not query:
            return jsonify({"error": "Query parameter is missing or empty"}), 400
        if not library:
            return jsonify({"error": "Library parameter is missing or empty"}), 400

        try:
            response = augment_query(query, globals['vector_store'])
            return jsonify({
                "text": response,
                "query": query
            }), 200
        except ValueError as E:
            return 404



@bp.route('/upload', methods=["POST"])
def upload():

    if 'session_id' not in session:
        from . import  general
        general.create_session()

    if request.method == 'POST':
        # Only accept a single file input
        if not request.files or len(request.files)>1:
            return jsonify({'error': "Upload only a single file."}), 400

        file_key = list(request.files)[0]
        file = request.files[file_key]

        if not file or file.name == '':
            return jsonify({'error':'No file selected'}), 400
        
        if file.mimetype not in current_app.config['ALLOWED_TYPES']:
            return jsonify({'error':'currently only pdf and txt files supported'}), 400
        
        if not os.path.exists(f'{current_app.instance_path}/uploads'):
            os.mkdir(f'{current_app.instance_path}/uploads')
        
        path = os.path.join(current_app.config['UPLOAD_FOLDER'] ,f'{session["session_id"]}', secure_filename(file.filename))
        file.save(path)
    
        from ..utils.vector_store import load_vector_store
        load_dotenv(os.path.join(current_app.root_path, ".."))
        async def _load():
            session['vector_store'] = await load_vector_store (
                    file_path=path, 
                    chroma_path=current_app.config['VECTOR_STORE'], 
                    collection_name=session['session_id'],
                    api_key=os.getenv("GENAI_API_KEY")
                )
        asyncio.run(_load())

        return jsonify({'message':f'current session is {session['session_id']}'}),200

    
@bp.route('/test', methods=["GET", "POST"])
def test():
    if 'session_id' in session:
        return jsonify({'message':f'current session is {session['session_id']}'}),200
    else:
        return jsonify({'message':'No session'}),200
        


        










