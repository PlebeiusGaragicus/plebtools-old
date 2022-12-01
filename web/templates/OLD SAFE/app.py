import os
import logging
import time
import json
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)
# app.app_context()
# app.register_blueprint(sse, url_prefix='/stream')

from .authproxy import AuthServiceProxy
from .tick_tock import wait_for_block
from . import tick_tock


###############
@app.route("/")
def index():

    # if os.getenv("NOT_IN_CONTAINER") == "1":
    #     rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(config.u, config.p))
    # else:
    #     rpc_connection = AuthServiceProxy("http://%s:%s@host.docker.internal:8332"%(config.u, config.p))
    # TODO - if error occurs, show to user and assist in trouble-shooting
    # bc = rpc_connection.getblockcount()
    # config.tip_height = bc

    #with app.app_context():
    # nbd = tick_tock.get_latest_block_details( rpc_con=rpc_connection )

    #return render_template("index.html", tip_height=nbd.height, difficulty=nbd.difficulty, block_time=nbd.block_time, time_now=nbd.time_now)
    return render_template("index.html")


###############
@app.route("/height")
def height():
    if os.getenv("NOT_IN_CONTAINER") == "1":
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(config.u, config.p))
    else:
        rpc_connection = AuthServiceProxy("http://%s:%s@host.docker.internal:8332"%(config.u, config.p))
    # TODO - if error occurs, show to user and assist in trouble-shooting

    config.best_hash = 0

    #with app.app_context():
    nbd = tick_tock.get_latest_block_details( rpc_con=rpc_connection )
    return render_template("height.html", height=nbd['height'])
    # return render_template("height.html")



#####################
# STEAM ENDPOINT... DON'T JUST PULL UP AND USE!
@app.route('/stream_ticktocknewblock')
def stream_clockface():
    def eventStream_clockface():
        with app.app_context():
            while True:
                # wait for source data to be available, then push it
                nbd = wait_for_block()
                yield 'data: {}\n\n'.format(nbd)
    return Response(eventStream_clockface(), mimetype="text/event-stream")




############################
# this is what the "client" listens to.. don't just pull up this page and see what happens!!! you'll be confused like I was at 19s!!!
@app.route('/stream_height')
def stream_height(): # the function that runs this 'URL'
    def respond_to_client():
        nh = wait_for_block()['height']
        _data = json.dumps({"color":"dick", "height":nh})
        yield f"id: 1\ndata: {_data}\nevent: update\n\n"

        # while True:
        #     global counter
        #     print(counter)
        #     counter += 1
        #     _data = json.dumps({"color":"dick", "height":counter})
        #     yield f"id: 1\ndata: {_data}\nevent: update\n\n"
        #     time.sleep(2)
    return Response(respond_to_client(), mimetype='text/event-stream')

    def eventStream_height(): # the 'generator' function that the javascript listens to for messages
        with app.app_context(): # I guess I need this?
            while True: # wait for source data to be available, then push it
                nbd = wait_for_block() # This is my own function that asks Bitcoin Core every second or so
                yield 'data: {}\n\n'.format(nbd['height']) # I ACT LIKE A GENERATOR
    return Response(eventStream_height(), mimetype="text/event-stream") # This Response (AKA GENERATOR) is returned to the Javascript EventSource


