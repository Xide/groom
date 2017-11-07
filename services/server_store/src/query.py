"""Handle the state aggregation into a single dict for querying."""




from settings import MONGODB_URI

MONGODB_CLIENT = MongoClient(MONGODB_URI)

def without_key(d, key):
    new_d = d.copy()
    new_d.pop(key)
    return new_d

def aggregate_state():

    def aggregate_one(x, y):
        """Event stream reducer."""
        if y['instance_id'] in x:
            if y['type'] == 'SERVER_DOWN':
                return without_key(x, y['instance_id'])
            raise RuntimeError(
                'Illegal command, expected SERVER_DOWN, but got {}'.format(y)
            )
        else:
            if y['type'] == 'SERVER_UP':
                x[y['instance_id']] = y
                return x
            raise RuntimeError(
                'Illegal command, expected SERVER_UP, but got {}'.format(y)
            )

    db = MONGODB_CLIENT['groom']
    collection = db['instances']


    for event in collection.find():


if __name__ == '__main__':
    print(aggregate_state())
