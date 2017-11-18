"""RESTful api."""

from wsgiref.simple_server import make_server
import json
import falcon
from query import QueryManager


class StatusHandler:
    """List the history of all active instances lifecycle."""

    def __init__(self, qm):
        """Link the handler with QueryManager."""
        self.qm = qm

    def on_get(self, req, resp):
        """Process the current system state."""
        resp.body = json.dumps(self.qm.aggregate_state())
        resp.status = falcon.HTTP_OK


class InstanceStatusHandler:
    """List the history of a specific instance lifecycle."""

    def __init__(self, qm):
        """Link the handler with QueryManager."""
        self.qm = qm

    def on_get(self, req, resp, uid):
        """Process the current system state."""
        state = self.qm.aggregate_state()
        if state.get(uid) is not None:
            resp.body = json.dumps(state[uid])
            resp.status = falcon.HTTP_OK
        else:
            raise falcon.HTTPNotFound(
                title='Instance {} does not exist.'.format(uid)
            )


if __name__ == '__main__':
    from settings import MONGODB_URI, DB_NAME

    with QueryManager(MONGODB_URI, DB_NAME) as qm:
        api = falcon.API()
        api.add_route('/v1/status', StatusHandler(qm))
        api.add_route('/v1/status/{uid}', InstanceStatusHandler(qm))

        server = make_server('0.0.0.0', 5000, api)
        server.serve_forever()
