import express from 'express'
import { tableInitializer } from './table'
import { loadConfig } from './config'

const initializeApiServer = (query) => {
  let app = express()

  app.get('/', (req, res) => {
    query()
    .then((state) => {
      res.send(state)
    })
  })

  app.get('/health', (res, req) => {
    res.sendStatus(200)
  })

  app.get('/ready', (res, req) => {
    res.sendStatus(200)
  })

  return app
}

tableInitializer()
.then(initializeApiServer)
.then((app) => {
  const config = loadConfig()

  app.listen(config.API_PORT)
})
