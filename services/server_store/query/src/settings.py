"""Process env variable and secret import and expose them to the app."""

from envparse import Env

arguments = Env(
    MONGODB_URI=str,
    DB_NAME=str
)

MONGODB_URI = arguments('MONGODB_URI')
DB_NAME = arguments('DB_NAME', default='groom')
