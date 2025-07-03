import os
from flask import current_app

class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = 'cachelib'
    SESSION_SERIALIZATION_FORMAT = 'json'
    PERMANENT_SESSION_LIFETIME = 300
    ALLOWED_TYPES = [
        'application/pdf',
        'text/plain'
    ]
