import time

import redis
from rq import Connection, Worker

REDIS_URL = r'redis://127.0.0.1:6379/0'
QUEUE = 'default'


def process_image(url):
    time.sleep(5)
    # TODO: Work on image
    print('Processing image: %s' % url)


def run_worker():
    redis_connection = redis.from_url(REDIS_URL)
    with Connection(redis_connection):
        worker = Worker(QUEUE)
        worker.work()


if __name__ == '__main__':
    run_worker()
