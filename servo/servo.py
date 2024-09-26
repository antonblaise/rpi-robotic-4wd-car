import threading
from flask import Flask, render_template, request
from adafruit_servokit import ServoKit

app = Flask(__name__)

kit = ServoKit(channels=16)
speed = 10
servo_lock = threading.Lock()  # Lock for synchronizing servo commands


def right():
    with servo_lock:
        kit.servo[0].angle = 95 - speed + 2

def down():
    with servo_lock:
        kit.servo[1].angle = 95 + speed

def left():
    with servo_lock:
        kit.servo[0].angle = 95 + speed

def up():
    with servo_lock:
        kit.servo[1].angle = 95 - speed - 5

def stop():
    with servo_lock:
        kit.servo[0].angle = 95
        kit.servo[1].angle = 95


def control_servos(direction):

    if direction in ["left", "right", "up", "down"]:

        if direction == "right":
            right()

        if direction == "up":
            up()

        if direction == "left":
            left()

        if direction == "down":
            down()

    else:
        
        stop()


@app.route('/')
def index():
    return render_template('servo.html')  # Reference to your HTML template

@app.route('/control', methods=['POST'])
def control():

    direction = request.form['direction']
    control_servos(direction)

    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
