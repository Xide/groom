# Server store

This component will subscribe to rabbitMQ and persist `SERVER_UP` and `SERVER_DOWN`
messages. it will allow querying over HTTP to get the current state of the system.
