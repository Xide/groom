# Server store

This component will subscribe to rabbitMQ and persist events into MongoDB.
It allow querying over HTTP to get the current state of the system.

Events persisted:

- server.requested
- server.created
- server.spawned
- server.expired
- server.deleted

You can customize events persisted with the command container
environment variable AMQP_ROUTING_KEYS.

## Endpoints

### Data ingestion
The `command` module handle data ingestion of the AMQP messages, it persist
them in the `instances` collection of the Mongodb.

### Data access
The `query` module provide an HTTP api to retreive instances status.
The endpoints are:

| Endpoint         | description                                    |
| ---------------- | ---------------------------------------------- |
| /v1/status       | List the current state of all active instances |
| /v1/status/{uid} | State of the instance `{uid}`                  |

## Messages format

Store: send an AMQP payload on the exchange with one of the routing key `server.*` listed above. The data of the payload must be a valid JSON UTF-8 encoded in the format described below

Read: HTTP REST endpoint for aggregated state of the servers with a valid UUID attributed.

### MongoDB records

They are stored in the `instances` collection.
The common parts of instances records is:


| field          | description                                 |
| -------------- | ------------------------------------------- |
| type           | the AMQP routing key of the message         |
| event.date_iso | Date at which this event entered the system |
| uid            | UUID attributed to the server on a `server.created` event                                            |

Example:

```json
{
  "type": "server.expired",
  "event": {
    "date_iso": "2017-11-18T18:42:28.360740",
    "uid": "6c3000bd-48ae-49c2-9776-51098c25252a"
  }
}
```

## Deployment
TODO
