# server-store command service

## Docker image configuration

| Environment variable | description                                                    |
| -------------------- | -------------------------------------------------------------- |
| MONGODB_URI          | the datastore address, format `mongodb://hostname:port`        |
| DB_NAME              | MongoDB database name, default: groom                          |
| RABBITMQ_URI         | Address of the rabbitMQ broker, format: `amqp://hostname:5672` |
| AMQP_EXCHANGE        | Exchange to bind on, default: groom                            |
| AMQP_ROUTING_KEYS    | Comma separated list of events type to persist (see server store readme)                                                               |
