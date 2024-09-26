from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import threading

app = Flask(__name__)

# GPIO pin setup
motor_pins = {
    'front_left': {'A': 23, 'B': 24},
    'front_right': {'A': 27, 'B': 22},
    'rear_left': {'A': 10, 'B': 9},
    'rear_right': {'A': 5, 'B': 6}
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for wheel in motor_pins.values():
    GPIO.setup(wheel['A'], GPIO.OUT) # Set all the pins as outputs.
    GPIO.setup(wheel['B'], GPIO.OUT)

# Setup PWM
## FL - front left
fl_pwm_a = GPIO.PWM(motor_pins['front_left']['A'], 100)
fl_pwm_a.start(0)
fl_pwm_b = GPIO.PWM(motor_pins['front_left']['B'], 100)
fl_pwm_b.start(0)

## FR - front right
fr_pwm_a = GPIO.PWM(motor_pins['front_right']['A'], 100)
fr_pwm_a.start(0)
fr_pwm_b = GPIO.PWM(motor_pins['front_right']['B'], 100)
fr_pwm_b.start(0)

## RL - rear left
rl_pwm_a = GPIO.PWM(motor_pins['rear_left']['A'], 100)
rl_pwm_a.start(0)
rl_pwm_b = GPIO.PWM(motor_pins['rear_left']['B'], 100)
rl_pwm_b.start(0)

## RR - rear right
rr_pwm_a = GPIO.PWM(motor_pins['rear_right']['A'], 100)
rr_pwm_a.start(0)
rr_pwm_b = GPIO.PWM(motor_pins['rear_right']['B'], 100)
rr_pwm_b.start(0)

# Input = PWM and speed data from webpage
# Output = Duty cycle (determines how fast the motor spins)
def set_motor_pwm(pwm, speed):
    duty_cycle = max(0.0, min(speed * 100, 100.0))  # Clamp duty cycle to [0.0, 100.0]
    pwm.ChangeDutyCycle(duty_cycle)

# Controls what each motor does when the
# joystick is dragged to a certain angle and 
# a certain distance from the center. 
# The further the distance, the greater the force.
def control_motors(angle, force):

    # Restrict angle to be between 0-360 degrees.
    if angle < 0:
        angle += 360
    if angle >= 360:
        angle -= 360

    # Zones between 340-0 and 180-200 are treated as 0 and 180 respectively.
    if angle >= 340:
        angle = 0
    elif angle > 180 and angle <= 200:
        angle = 180

    # Interpolated zones

    ## Forwards

    ### Rightward
    if angle >= 0 and angle < 90:
        fl_speed = 1
        # fr_speed = (2/90)*angle - 1 # skid
        fr_speed = (1/90)*angle # normal
        rl_speed = 1
        # rr_speed = (2/90)*angle - 1 # skid
        rr_speed = (1/90)*angle # normal

    ### Leftward
    elif angle >= 90 and angle <= 180:
        # fl_speed = (-2/90)*angle + 3 # skid
        fl_speed = (-1/90)*angle + 2 # normal
        fr_speed = 1
        # rl_speed = (-2/90)*angle + 3 # skid
        rl_speed = (-1/90)*angle + 2 # normal
        rr_speed = 1

    ## Reverses

    ### Leftward
    elif angle > 200 and angle <= 260:
        # fl_speed = (-2/60)*angle + (23/3) # skid
        fl_speed = (-1/60)*angle + (10/3) # normal
        fr_speed = -1
        # rl_speed = (-2/60)*angle + (23/3) # skid
        rl_speed = (-1/60)*angle + (10/3) # normal
        rr_speed = -1

    ### Straight
    elif angle > 260 and angle <= 280:
        fl_speed = -1
        fr_speed = -1
        rl_speed = -1
        rr_speed = -1
    
    ### Rightward
    elif angle > 280 and angle < 340:
        fl_speed = -1
        # fr_speed = (2/60)*angle - (31/3) # skid
        fr_speed = (1/60)*angle - (17/3) # normal
        rl_speed = -1
        # rr_speed = (2/60)*angle - (31/3) # skid
        rr_speed = (1/60)*angle - (17/3) # normal
    
    ## Stop
    else:
        # fl_speed = 0
        # fr_speed = 0
        # rl_speed = 0
        # rr_speed = 0

        fl_speed = 0
        fr_speed = 0
        rl_speed = 0
        rr_speed = 0

    # Wheels' speeds depend on how far away the joystick is dragged from its center.    
    fl_speed *= force
    fr_speed *= force
    rl_speed *= force
    rr_speed *= force


    # Logic of a motor:
    # 
    #     input a   |   input b     |   action
    # --------------------------------------------
    #       0       |       0       |   brake
    #       0       |       1       |   reverse
    #       1       |       0       |   forward
    #       1       |       1       |   coast  
    # 
    # Note: Forward and reverse are only RELATIVE to the motor itself. 
    #       The actual direction depends on how the motor is attached.     
    
    # FL wheel action
    if fl_speed > 0: # Forward
        set_motor_pwm(fl_pwm_a, 0)
        set_motor_pwm(fl_pwm_b, abs(fl_speed))
    elif fl_speed < 0: # Backward
        set_motor_pwm(fl_pwm_a, abs(fl_speed))
        set_motor_pwm(fl_pwm_b, 0)
    else: # Coast
        fl_pwm_a.ChangeDutyCycle(100)
        fl_pwm_b.ChangeDutyCycle(100)

    # FR wheel action
    if fr_speed > 0: # Forward
        set_motor_pwm(fr_pwm_a, abs(fr_speed))
        set_motor_pwm(fr_pwm_b, 0)
    elif fr_speed < 0: # Backward
        set_motor_pwm(fr_pwm_a, 0)
        set_motor_pwm(fr_pwm_b, abs(fr_speed))
    else: # Coast
        fr_pwm_a.ChangeDutyCycle(100)
        fr_pwm_b.ChangeDutyCycle(100)
    
    # RL wheel action
    if rl_speed > 0: # Forward
        set_motor_pwm(rl_pwm_a, 0)
        set_motor_pwm(rl_pwm_b, abs(rl_speed))
    elif rl_speed < 0: # Backward
        set_motor_pwm(rl_pwm_a, abs(rl_speed))
        set_motor_pwm(rl_pwm_b, 0)
    else:
        rl_pwm_a.ChangeDutyCycle(100)
        rl_pwm_b.ChangeDutyCycle(100)

    # RR wheel action
    if rr_speed > 0: # Forward
        set_motor_pwm(rr_pwm_a, abs(rr_speed))
        set_motor_pwm(rr_pwm_b, 0)
    elif rr_speed < 0: # Backward
        set_motor_pwm(rr_pwm_a, 0)
        set_motor_pwm(rr_pwm_b, abs(rr_speed))
    else:
        rr_pwm_a.ChangeDutyCycle(100)
        rr_pwm_b.ChangeDutyCycle(100)

# Multithreading function
def control_motors_thread(angle, force):
    threading.Thread(target=control_motors, args=(angle, force)).start()

@app.route('/')
def index():
    return render_template('wheels.html')

@app.route('/control', methods=['POST'])
def control():

    angle = request.form['angle']
    force = float(request.form['force'])
    if force < 0.15: force = 0

    if angle == 'stop':
        control_motors_thread(0, 0)
    else:
        angle = float(angle)
        control_motors_thread(angle, force)

    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
