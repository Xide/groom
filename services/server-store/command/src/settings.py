"""Process env variable and secret import and expose them to the app."""

import os
from envparse import Env

arguments = Env(
    MONGODB_URI=str,
    DB_NAME=str,
    RABBITMQ_URI=str,
    AMQP_EXCHANGE=str,
    AMQP_ROUTING_KEYS=list,
    AMQP_CREDENTIALS_DIR=str
)

MONGODB_URI = arguments('MONGODB_URI')
DB_NAME = arguments('DB_NAME', default='groom')
RABBITMQ_URI = arguments('RABBITMQ_URI')
AMQP_EXCHANGE = arguments('AMQP_EXCHANGE', default='groom')
AMQP_ROUTING_KEYS = arguments('AMQP_ROUTING_KEYS')
AMQP_CREDENTIALS_DIR = arguments('AMQP_CREDENTIALS_DIR', default=None)
AMQP_USERNAME, AMQP_PASSWORD = None, None


def _read_file(f):
    with open(f, 'r') as fp:
        return fp.read()


if AMQP_CREDENTIALS_DIR is not None:
    AMQP_USERNAME = _read_file(os.path.join(AMQP_CREDENTIALS_DIR, 'username'))
    AMQP_PASSWORD = _read_file(os.path.join(AMQP_CREDENTIALS_DIR, 'password'))
