from datetime import datetime

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    now = str(datetime.now())
    return 'Hello, World! Current Time: %s' % now


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
