#!/usr/bin/python3
"""Script that starts flask application web application
    aplication listen on 0.0.0.0 port 5000
    Route:
            / and /hbnb
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """function that is called at the root url '/'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """function that is called at '/hbnb' path url"""
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
