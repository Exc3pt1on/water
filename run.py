import RPi.GPIO as GPIO
import time
import json
from datetime import datetime
import threading
from flask import Flask, render_template, request
app = Flask(__name__)

out_pump = 38
in_sensor = 40
out_sensor = 36

GPIO.setmode(GPIO.BOARD)

GPIO.setup(out_pump, GPIO.OUT)
GPIO.setup(in_sensor, GPIO.IN)
GPIO.setup(out_sensor, GPIO.OUT)

log = []

with open('data.json') as f:
    data = json.load(f)

watering = data['watering_values']['watering_time'] #seconds
wait = data['watering_values']['wait_time'] #minutes

@app.route("/")
def function():
    return render_template("index.html", data = log)

@app.route("/<param>/<value>/")
def action(param, value):
    global watering
    global wait
    if  (param == "watering_time" or param == "wait_time") and (value.replace('.','',1).isdigit()):
        data['watering_values'][str(param)] = value

        with open('data.json', 'w') as f:
            json.dump(data, f)

        watering = data['watering_values']['watering_time'] #seconds
        wait = data['watering_values']['wait_time'] #minutes

    return render_template("index.html", data = log)


def thread_function():

    global log 

    while True:
        GPIO.output(out_sensor, GPIO.HIGH)
        time.sleep(1)
        if GPIO.input(in_sensor):
            #print("Too dry, watering for {} seconds...".format(watering))
            GPIO.output(out_pump, GPIO.HIGH)
            time.sleep(float(watering))
            GPIO.output(out_pump, GPIO.LOW)
            now = datetime.now()
            log.insert(0, now.strftime("%d/%m/%Y %H:%M:%S"))
            if len(log) > 5:
                log.pop()
        #else:
            #print("Wet enough")
        GPIO.output(out_sensor, GPIO.LOW)
        time.sleep(float(wait)*60)


if __name__ == "__main__":
    watering_sequence = threading.Thread(target=thread_function)
    watering_sequence.daemon = True
    watering_sequence.start()
    app.run(host='0.0.0.0', port=80, debug=True)
