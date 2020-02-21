from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('iindexx.html')

if __name__ == '__main__':
    app.run()




"""#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
    # serve index template
    return render_template('iindexx.html', name='Joe')

# getting the json containing the list of cars that was posted to the receiver endpoint
#                                                         ^ this was done in doWork() in iindexx.html
# 'POST' defines how this page can be accessed
#       - 'GET' is the default value for the methods parameter
#       - look up "http request methods" for more info
@app.route('/receiver', methods = ['POST'])
def worker():
    # read json + reply
    data = request.get_json()
    result = ''

    for item in data:
        # loop over every row
        result += str(item['make']) + '\n'

    return result

if __name__ == '__main__':
    # run!
    app.run()
"""
