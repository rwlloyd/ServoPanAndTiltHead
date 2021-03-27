"""
controller.py

Python3 script to  control two servos and a raspberry pi camera in a pan and tilt mechanism.
The first servo pans the second servo and tilt mechanism which holds the raspberry pi camera.

dependencies:
pip3 install gpiozero
pip3 install picamera

Things also work much more smoothly if you use the pigpio pin factory
https://gpiozero.readthedocs.io/en/stable/api_pins.html#changing-pin-factory

Rob Lloyd
Lincoln, March 2021.
"""

# Import libraries
from gpiozero import AngularServo
from gpiozero import Button
from picamera import PiCamera
import os
import time
from time import sleep

panServoPin = 13
tiltServoPin = 12
buttonPin = 25
scanning = False

# These are angles from the centre point
panMin = -60
panMax = 60
tiltMin = -60
tiltMax = 60

# Scanning Parameters
scan_shape =  [5,5] # X x Y positions..
home = [0,0]  # Save the home position for later

# Pan and tilt Servo servos set up
panServo = AngularServo(panServoPin, initial_angle=panMin+panMax, min_angle=panMin, max_angle=panMax)
tiltServo = AngularServo(tiltServoPin, initial_angle=tiltMin+tiltMax, min_angle=tiltMin, max_angle=tiltMax)
# Button setup
button = Button(buttonPin, bounce_time = 0.1)

# Setup the camera
camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(1)
# Now fix the values
#camera.shutter_speed = camera.exposure_speed
#camera.exposure_mode = 'off'
#g = camera.awb_gains
#camera.awb_mode = 'off'
#camera.awb_gains = g

def set_position(newPos):
    print(f"Moving to: {newPos}")
    panServo.angle = newPos[0]
    tiltServo.angle = newPos[1]

def button_callback(self):
    # Calculate the positions of the array
    panStep = (panMax - panMin) / scan_shape[0]
    tiltStep = (tiltMax - tiltMin) / scan_shape[1]
    print(f"panStep = {panStep}, tiltStep = {tiltStep}")
    set_position([panMax, tiltMax])
    captureNext()
    for pStep in range(1, scan_shape[0] + 1):
        for tStep in range(1,scan_shape[1] + 1):
            set_position([None, tiltMax - (tStep*tiltStep)])
            captureNext()
        set_position([panMax-(pStep*panStep), None])
        captureNext()

    # Go back to the centre point
    set_position(home)
    print("Scan Done")
    sleep(0.25)
    print("ready")

def captureNext():
    # Dwell time for the camera to settle
    dwell = 0.5
    sleep(dwell)
    file_name = os.path.join(output_folder, 'image_' + time.strftime("%H_%M_%S") + '.jpg')
    print("*")
    #camera.capture(file_name)
    #print("captured image: " + 'image_' + time.strftime("%H_%M_%S") + '.jpg')
    sleep(dwell)

# Handling the files
#get current working directory
path = os.getcwd()
# make the folder name
folder_name = 'captureSession_' + time.strftime("%Y_%m_%d_%H_%M_%S")
# make the folder
os.mkdir(folder_name)
# construct the output folder path
output_folder = os.path.join(path, folder_name)

# Callback for dealing with button press'
button.when_released = button_callback
panServo.angle = 5
tiltServo.angle = 5
sleep(0.25)
panServo.angle = 0
tiltServo.angle = 0
print("ready")
try:
    while True:
        # Erm... theres not much to do here. I'll have a nap
        sleep(0.1)
        pass
#Clean things up at the end
except KeyboardInterrupt:
    print ("Goodbye")

"""
The short version of how servos are controlled

https://raspberrypi.stackexchange.com/questions/108111/what-is-the-relationship-between-angle-and-servo-motor-duty-cycle-how-do-i-impl
Servos are controlled by pulse width, the pulse width determines the horn angle.

A typical servo responds to pulse widths in the range 1000 to 2000 µs.

A pulse width of 1500 µs moves the servo to angle 0. 
Each 10 µs increase in pulse width typically moves the servo 1 degree more clockwise. 
Each 10 µs decrease in pulse width typically moves the servo 1 degree more anticlockwise.

Small 9g servos typically have an extended range and may respond to pulse widths in 
the range 500 to 2500 µs.

Why do people think servos are controlled by duty cycle? 
Because servos are typically given 50 pulses per second (50 Hz). 
So each pulse is potentially a maximum of 20000 µs (1 million divided by 50). 
A duty cycle is the percentage on time. 100% will be a 20000 µs pulse, way outside 
the range accepted by a servo.

Do some calculations at 50 Hz for sample pulse widths.

 500 / 20000 = 0.025 or  2.5 % dutycycle
1000 / 20000 = 0.05  or  5.0 % dutycycle
1500 / 20000 = 0.075 or  7.5 % dutycycle
2000 / 20000 = 0.1   or 10.0 % dutycycle
2500 / 20000 = 0.125 or 12.5 % dutycycle

Don't use dutycycles, if possible use pulse widths, and think in pulse widths. 
If you send pulses at 60 Hz by duty cycle the servo will go to the wrong position.

"""

