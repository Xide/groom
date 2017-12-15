import { KafkaStreams } from "kafka-streams"
import { loadConfig, loadKafkaConfig, kafkaLogger } from "./config"
import util from "util"
import createLogger from "debug"

const log = createLogger("server-store:table")

/*
** This module Encapsulate the creation and update of a
** Kafka KTable. It returns a function that can be used to query
** the current state of the table.
*/


/*
** Prepare the table by ingesting the stream history over
** all the historical data
** @params table: the `KafkaStreams.KTable` instance to provision
*/

const ingestHistoricData = (table) => {
  // log("Ingesting historical data")
  // Not implemented atm :'(
  // TODO: Implement in underlying library.
  // ktable.consumeUntilLatestOffset()
  // log("KTable initialized")
  return table
}

/*
** Parsing utilities
*/

const gcDeletedServers = (payload) => {
  switch (payload.type) {
    case "server.deleted": return null
    default: return payload
  }
}

const parseMessageToKv = (message) => {
  const payload = JSON.parse(message.value)

  return {
    key: payload.uid,
    value: gcDeletedServers(payload)
  }
}

const filterNullValues = (dct) => {
  return Object
    .keys(dct)
    .filter((k) => { return dct[k] != null })
    .reduce((res, k) => { return { ...res, [k]: dct[k] } }, {})
}

/*
** Encapsulate side effects and update logic.
** it schedule the state update and return the query function
*/

const stateMonad = (initialState, ms) => {
  let state = initialState

  /*
  ** Update logic, we use a fixed time window for events pulling
  ** as the `consumeUntilLatestOffset` function is not yet implemented
  ** in the kafka-stream library.
  */
  const updateState = () => {
    state = state.consumeUntilMs(ms)
    // queue a recursive call
    setTimeout(updateState, ms)

    // Debug messages
    // state.getTable()
    // .then(
    //   (res) => {log('TABLE: ' + util.inspect(filterNullValues(res)))},
    //   (err)   => {log('ERR:   ' + err)}
    // )
  }

  setTimeout(updateState, 0)

  /*
  ** Getter logic
  ** The `status` field of the returned dict can be one
  ** of `ok`/`ko`
  */

  const queryTable = () => {
    return state
      .getTable()
      .then(
        (res) => { return { status: 'ok', table: filterNullValues(res) } },
        (err) => {
          log("Error: Could not get KTable status: " + err)
          return { status: 'ko', message: err }
        }
      )
  }

  log("KTable initialized")
  return queryTable
}

/*
** Load kafka client, ingest historic data and return
** a promise that resolve to the table getter function.
** Can reject if the underlying library fail to
** connect to kafka.
** NOTE: ATM, the library never throw if it can't connect to broker,
** But only if the broker is starting while trying to connect ¯\_(ツ)_/¯
*/

export const tableInitializer = (updateInterval = 1000) => {
  const config = loadConfig()
  const kafkaConfig = loadKafkaConfig()
  const factory = new KafkaStreams(kafkaConfig)
  const ktable = factory.getKTable("server", parseMessageToKv)

  if (config.KAFKA_DEBUG) {
    ktable.forEach(message => kafkaLogger('[message]' + util.inspect(message)))
  }

  log("Starting KTable building")
  return ktable.start()
    .then(() => {
        log("Starting Ktable ingestion")
        const consolidatedTable = ingestHistoricData(ktable)
        const storeGetter = stateMonad(consolidatedTable, updateInterval)
        return storeGetter
      })
}
