from uuid import uuid4


if __name__ == '__main__':
    print('use groom;')

    for y in range(100000):
        uid = str(uuid4())
        for x in range(2):
            print("db.instances.insert({'type': '%s', 'uid': '%s'});" % (
                'serverScheduled' if not x % 2 else 'serverCanceled',
                uid
            ))
