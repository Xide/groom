"""Process env variable and secret import and expose them to the app."""

from envparse import Env

arguments = Env(
    MONGODB_URI=str
    # RABBITMQ_URI=str
)

MONGODB_URI = arguments('MONGODB_URI')

# RABBITMQ_URI = arguments('RABBITMQ_URI')
