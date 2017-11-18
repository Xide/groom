"""Process env variable and secret import and expose them to the app."""

from envparse import Env

arguments = Env(
    MONGODB_URI=str,
    DB_NAME=str,
    RABBITMQ_URI=str,
    AMQP_EXCHANGE=str,
    AMQP_ROUTING_KEYS=list
)

MONGODB_URI = arguments('MONGODB_URI')
DB_NAME = arguments('DB_NAME', default='groom')
RABBITMQ_URI = arguments('RABBITMQ_URI')
AMQP_EXCHANGE = arguments('AMQP_EXCHANGE', default='groom')
AMQP_ROUTING_KEYS = arguments('AMQP_ROUTING_KEYS')
