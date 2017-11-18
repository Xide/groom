"""Handle the state aggregation into a single dict for querying."""

from functools import reduce
from pymongo import MongoClient


def without_key(d: dict, key):
    """Duplicate a dict and remove a key in the returned one."""
    new_d = d.copy()
    new_d.pop(key)
    return new_d


class QueryManager:
    """Manage the interaction with the datastore to fetch state."""

    def __init__(self, datastore_uri: str, db_name: str):
        """Instanciate the connection with MongoDB.

        @param datastore_uri: MongoDB URI containing the server datas.
        @param db_name: Mongodb database name.
        """
        self.db_name = db_name
        self.client = MongoClient(datastore_uri)
        self.db = self.client[db_name]
        self.servers = self.db['instances']

    def __enter__(self):
        """Use this object like so.

        with QueryManager(datastore_uri, db_name) as qm:
            # do stuff
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup MongoDB connection."""
        self.client.close()

    def aggregate_state(self):
        """Collect the full mongodb history and process current state."""
        def _aggregate_one(x, y):
            """Event stream reducer."""
            # Cleanup non serializable mongodb internal id
            y = without_key(y, '_id')

            # Server creation logic
            if y['type'] == 'server.created':
                # Side effect: clear any potential previous server with
                # the same UUID
                x[y['event']['uid']] = [y]
                return x

            # Event aggregation
            if y['event'].get('uid'):
                if y['event']['uid'] in x:
                    if y['type'] == 'server.expired':
                        # Server deletion
                        return without_key(x, y['event']['uid'])
                    else:
                        # history aggregation
                        x[y['event']['uid']] += [y]
                        return x
                # Payload with a undeclared UID (no server.created event)
                raise RuntimeError(
                    'Expected server.created, but got {}'.format(y)
                )
            # Event without UID are not treated
            return x

        return reduce(_aggregate_one, self.servers.find(), {})


if __name__ == '__main__':
    from settings import MONGODB_URI, DB_NAME

    with QueryManager(MONGODB_URI, DB_NAME) as qm:
        print(qm.aggregate_state())
