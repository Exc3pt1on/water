import RPi.GPIO as GPIO
import time

out_pump = 40
in_sensor = 36
out_sensor = 38

GPIO.setmode(GPIO.BOARD)

GPIO.setup(out_pump, GPIO.OUT)
GPIO.setup(in_sensor, GPIO.IN)
GPIO.setup(out_sensor, GPIO.OUT)

watering = 2 #seconds
wait = 0.2 #minutes


while True:
    GPIO.output(out_sensor, GPIO.HIGH)
    time.sleep(1)
    if GPIO.input(in_sensor):
        print("Too dry, watering for {} seconds...".format(watering))
        GPIO.output(out_pump, GPIO.HIGH)
        time.sleep(watering)
        GPIO.output(out_pump, GPIO.LOW)
    else:
        print("Wet enough")
    GPIO.output(out_sensor, GPIO.LOW)
    time.sleep(wait*60)