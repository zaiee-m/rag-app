import os
from flask import current_app

class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = 'cachelib'
    SESSION_SERIALIZATION_FORMAT = 'json'
    ALLOWED_TYPES = [
        'application/pdf',
        'text/plain'
    ]
