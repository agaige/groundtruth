# requires pip install rq==0.12.0 redis==2.10.6

import os
import subprocess

import redis
from rq import Connection, Worker

REDIS_URL = r'redis://127.0.0.1:6379/0'
QUEUE = 'default'


def process_image(url):
    result = {
        'value': '',
        'status': 'failed',
    }
    # Work on image
    print('Processing image: %s' % url)

    env = os.environ.copy()
    env['INPUT_URL'] = url

    try:
        p = subprocess.run(
            ['touch', 'foo', '&&', 'pwd', '&&', '/bin/bash', 'script.sh'],
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=os.getcwd()
        )
    except subprocess.CalledProcessError as err:
        result['error'] = err
    else:
        result['status'] = 'success'
        result['returncode'] = p.returncode
        result['stdout'] = p.stdout.decode('utf-8')
        result['stderr'] = p.stderr.decode('utf-8')

    # Return result
    return result


def run_worker():
    redis_connection = redis.from_url(REDIS_URL)
    with Connection(redis_connection):
        worker = Worker(QUEUE)
        worker.work()


if __name__ == '__main__':
    run_worker()
