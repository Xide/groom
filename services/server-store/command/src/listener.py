"""This module notify the system about servers update.

It listen on a rabbitMQ topic, and allow message .
"""

import pika
from functools import reduce


class AMQPConsumer:
    """Hook functions to AMQP messages.

    Implemented around `pika` using a blocking connection, it can only handle
    messages sequentially.

    Usage:

    def callback(channel, method_frame, header_frame, body):
        print('Received message: ', body)
        # Do stuff with message

    with AMQPConsumer(broker_uri, channel) as c:
        c.ioloop(callback)
    """

    def __init__(self, broker_uri, exchange, routing_keys):
        """Initialize consumer, does not connect.

        @param broker_uri: AMQP broker uri.
        @param exchange: the AMQP exchange to listen on.
        @param: routing_keys: keys to filter exchange messages.
        """
        self.broker_uri, self.exchange, self.routing_keys = \
            broker_uri, exchange, routing_keys

        self.connection, self.channel, self.consumer_tag = None, None, None
        self.connected = False

    def connect(self):
        """Connect to the rabbitMQ server using a basic blocking connection."""
        if not self.connected:
            try:
                self.connection = pika.BlockingConnection(
                    pika.URLParameters(self.broker_uri)
                )
                self.channel = self.connection.channel()

                self.channel.exchange_declare(
                    exchange=self.exchange,
                    exchange_type='topic'
                )
                self._queue_result = self.channel.queue_declare(
                    exclusive=True
                )
                self.queue = self._queue_result.method.queue

                list(map(
                    lambda key: self.channel.queue_bind(
                        self.queue,
                        self.exchange,
                        routing_key=key
                    ),
                    self.routing_keys
                ))

            except Exception as e:
                self.connection, self.channel, self.consumer_tag = \
                    None, None, None
                raise RuntimeError('Could not open AMQP connection') from e
            else:
                self.connected = True

    def __enter__(self):
        """Connect to the rabbitMQ broker."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure pending messages are requeued + close rabbitMQ connection."""
        print('QUIT AMQP')
        if self.connected:
            print('WAS CONNECTED')
            # Requeue pending messages
            if self.consumer_tag:
                self.channel.basic_cancel(self.consumer_tag)

            # Notify broker from disconnection
            self.channel.close()
            self.connection.close()

            # Cleanup references
            self.channel, self.connection = None, None
            self.connected = False
            print('OUT')

    def ioloop(
                self,
                callback,
                hooks=[]
            ):
        """Consumer main loop.

        @note: must be called inside a `with` block.

        @param callback: functor called to process the request.
        @param hooks: functors list called sequentially to preprocess request.
        """
        def _apply_hooks(hooks, payload):
            def _reduce_hook(payload, fn):
                return fn(*payload)
            return reduce(_reduce_hook, hooks, payload)

        def _io(channel, method_frame, header_frame, body):
            print('_IO')
            processed_payload = _apply_hooks(hooks, (
                channel, method_frame, header_frame, body
            ))
            callback(*processed_payload)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        self.consumer_tag = self.channel.basic_consume(_io, self.queue)
        self.channel.start_consuming()


if __name__ == '__main__':
    """Example usage for a basic consumer."""
    from settings import RABBITMQ_URI, AMQP_EXCHANGE, AMQP_ROUTING_KEYS

    def _callback(channel, method_frame, header_frame, body):
        print('=' * 50)
        print('={:48s}='.format('MESSAGE'))
        print('=' * 50)
        print('channel      : ', channel)
        print('method_frame : ', method_frame)
        print('header_frame :', header_frame)
        print('body         :', body)
        print('=' * 50)

    with AMQPConsumer(RABBITMQ_URI, AMQP_EXCHANGE, AMQP_ROUTING_KEYS) as c:
        print("""Starting to listen to AMQP messages.
- Broker URI      : {}
- Broker exchange : {}
- routing_keys    : {}
""".format(RABBITMQ_URI, AMQP_EXCHANGE, AMQP_ROUTING_KEYS))
        try:
            c.ioloop(_callback)
        except KeyboardInterrupt as e:
            print('\nShutting down.')
