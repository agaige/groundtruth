import redis
from rq import Queue, Connection
from flask import (Blueprint, render_template, jsonify, request,
                   current_app)

groundtruth = Blueprint('main', __name__, )


@groundtruth.route('/', methods=['GET'])
def home():
    return render_template('main/home.html')


@groundtruth.route('/tasks', methods=['GET', 'POST'])
def run_task():
    image_url = request.form['url']
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.enqueue('__main__.process_image', image_url, timeout=120)
    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }
    return jsonify(response_object), 202


@groundtruth.route('/tasks/<task_id>', methods=['GET'])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response_object = {'status': 'error'}
    return jsonify(response_object)
