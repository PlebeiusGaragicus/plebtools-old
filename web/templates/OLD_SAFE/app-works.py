from flask import Flask, Response, render_template
import json
import time

counter = 99

app = Flask(__name__)

##############################
@app.route("/")
def render_index():
  return render_template("grass.html")

##############################
@app.route("/listen")
def listen():

  def respond_to_client():
    while True:
      global counter
      print(counter)
      counter += 1
      _data = json.dumps({"color":"dick", "counter":counter})
      yield f"id: 1\ndata: {_data}\nevent: online\n\n"
      time.sleep(0.5)
  return Response(respond_to_client(), mimetype='text/event-stream')
