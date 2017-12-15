import { str, port, bool, num, cleanEnv } from "envalid"
import createLogger from "debug"


function loadConfigGetter (environ) {
  const env = cleanEnv(environ, {
    API_PORT:                   port({ default: 3000 }),
    KAFKA_HOST:                 str(),
    KAFKA_DEBUG:                bool({ default: false }),
    KAFKA_TOPIC:                str(),
    KAFKA_GROUP_ID:             str(),
    KAFKA_CLIENT_NAME:          str(),
    KAFKA_FETCH_INTERVAL_MS:    num({ default: 1000 }),
    KAFKA_WORKER_PER_PARTITION: num({ default: 1 })
  })

  return () => {
    return env
  }
}


export const loadConfig = loadConfigGetter(process.env)

export const kafkaLogger = createLogger("server-store:kafka-streams")

export const loadKafkaConfig = () => {
  const env = loadConfig()
  return {
      kafkaHost: env.KAFKA_HOST,
      logger: {
        debug: msg => kafkaLogger('[debug]' + msg),
        info: msg => kafkaLogger('[info]' + msg),
        warn: msg => kafkaLogger('[warn]' + msg),
        error: msg => kafkaLogger('[error]' + msg)
      },
      groupId: env.KAFKA_GROUP_ID,
      clientName: env.KAFKA_CLIENT_NAME,
      workerPerPartition: env.KAFKA_WORKER_PER_PARTITION,
      options: {
          sessionTimeout: 8000,
          protocol: ["roundrobin"],
          fromOffset: "earliest", //latest
          fetchMaxBytes: 1024 * 100,
          fetchMinBytes: 1,
          fetchMaxWaitMs: 10,
          heartbeatInterval: 250,
          retryMinTimeout: 250,
          autoCommit: true,
          autoCommitIntervalMs: 1000,
          requireAcks: 1,
          ackTimeoutMs: 100,
          partitionerType: 3
      }
  }

}
