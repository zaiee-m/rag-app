
class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = 'cachelib'
    SESSION_SERIALIZATION_FORMAT = 'json'
    PERMANENT_SESSION_LIFETIME = 60
    ALLOWED_TYPES = [
        'application/pdf',
        'text/plain'
    ]
