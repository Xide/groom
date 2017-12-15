# Server store

This service keep an updated table of the current system state and
allow querying via an HTTP api.


TODO: lib silent connection errors, we need to find out how to define
      a maximal number of retries.


### HTTP API

| Endpoint | Description                                           | Method |
| -------- | ----------------------------------------------------- | ------ |
| /health  | Is the service alive ?                                | GET    |
| /ready   | TODO: need to respond 500 until table is provisionned | GET    |
| /        | Json object containing the active servers             | GET    |


### Kafka event

Events persisted:

- server.requested
- server.created
- server.spawned
- server.expired
- server.deleted


| field          | description                                 |
| -------------- | ------------------------------------------- |
| type           | the AMQP routing key of the message         |
| event.date_iso | Date at which this event entered the system |
| uid            | UUID attributed to the server on a `server.created` event   

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
