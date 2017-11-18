"""This service persist events from rabbitMQ into mongoDB."""

from json import loads
from pymongo import MongoClient
from listener import AMQPConsumer
from settings import \
    RABBITMQ_URI, \
    AMQP_EXCHANGE, \
    AMQP_ROUTING_KEYS, \
    MONGODB_URI, \
    DB_NAME


class DBInserter:
    """Wrapper around pymongo.

    Usage:
    with DBInserter(datastore_uri, db) as db:
        db.insert(dict(type='some_type', message='hello world'))
    """

    def __init__(self, datastore_uri, db):
        """Initialize a connection with MongoDB."""
        self.db_name = db
        self.uri = datastore_uri
        self.client, self.db, self.servers = None, None, None

    def __enter__(self):
        """Connect to MongoDB."""
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        self.servers = self.db['instances']
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup MongoDB connection."""
        self.client.close()

    def insert(self, payload: dict):
        """Insert a formatted record in datastore."""
        return self.servers.insert_one(payload)


if __name__ == '__main__':
    def _verbose_hook(channel, method_frame, header_frame, body):
        print('=' * 50)
        print('={:48s}='.format('MESSAGE'))
        print('=' * 50)
        print('channel      : ', channel)
        print('method_frame : ', method_frame)
        print('header_frame :', header_frame)
        print('body         :', body)
        print('=' * 50)
        return channel, method_frame, header_frame, body

    with AMQPConsumer(RABBITMQ_URI, AMQP_EXCHANGE, AMQP_ROUTING_KEYS) as c:
        print("""Starting to listen to AMQP messages.
- Broker URI      : {}
- Broker exchange : {}
- routing_keys    : {}
""".format(RABBITMQ_URI, AMQP_EXCHANGE, AMQP_ROUTING_KEYS))
        with DBInserter(MONGODB_URI, DB_NAME) as db:

            def callback(channel, method_frame, header_frame, body):
                """Persist the message into MongoDB."""
                payload = {
                    'type': method_frame.routing_key,
                    'event': loads(body.decode('utf-8'))
                }
                print('Inserting event into db:', payload)
                print(db.insert(payload).acknowledged)

            try:
                c.ioloop(callback, hooks=[_verbose_hook])
            except KeyboardInterrupt as e:
                print('\nShutting down.')
