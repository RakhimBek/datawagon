"""Settings for Backup Cloud Storage

"""
from starlette.config import Config

config = Config('.env')

PROJECT_NAME = 'wishfulmap'
API_VERSION = '1.0'
API_PREFIX = '/api'
DEBUG = config('DEBUG', cast=bool, default=True)

HOST = config('HOST', cast=str, default='0.0.0.0')
PORT = config('PORT', cast=int, default=8080)