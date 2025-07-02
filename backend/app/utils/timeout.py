from flask import (session, g as globals)
from datetime import datetime

def time_out():
    difference = datetime.now() - session['created_at']
    if datetime.total_seconds()/60 > 30:
        session.clear()
        globals.clear()

def init_app(app):
    app.teardown_appcontext(time_out)
