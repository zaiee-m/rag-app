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

    if 'collection_name' not in session:
        return jsonify({'error':'Either upload your own documentation or select one from available documentations.'}), 404

    from ..utils.chroma import get_client
    client = get_client(
        gen_api_key=current_app.config["API_KEY"],
        collection_name=session["collection_name"],
        chroma_path=current_app.config["VECTOR_STORE"]
    )
    
    if request.method == "POST":
        query = request.form.get("query")
        
        if not query:
            return jsonify({"error": "Query parameter is missing or empty"}), 400

        try:
            response = augment_query(query, client)
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
        
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], session["session_id"])):
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], session["session_id"]))
        
        path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            f'{session["session_id"]}', 
            secure_filename(file.filename)
        )
        file.save(path)
    
        from ..utils.vector_store import load_vector_store
        try:
            async def _load():
                await load_vector_store (
                        file_path=path, 
                        chroma_path=current_app.config['VECTOR_STORE'], 
                        collection_name=session['session_id'],
                        api_key=current_app.config["API_KEY"]
                    )
            asyncio.run(_load())
            session['collection_name'] = session['session_id']
        except Exception as e:
            raise e
        
        return jsonify({'message':f'current session is {session['session_id']}'}),200

    
@bp.route('/test', methods=["GET", "POST"])
def test():
    if 'session_id' in session:
        return jsonify({'message':f'current session is {session['session_id']}'}),200
    else:
        from . import  general
        general.create_session()
        return jsonify({'message':f"Session didn't exist : New session created {session['session_id']}"}),200
    

        


        










