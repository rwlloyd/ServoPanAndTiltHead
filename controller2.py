# Import libraries
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
import time
from time import sleep
Scanning = False ##for testing
panServoPin = 13
tiltServoPin = 12
buttonPin = 25

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(panServoPin, GPIO.OUT)
GPIO.setup(tiltServoPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

panServo = GPIO.PWM(panServoPin,50) # Note panServoPin is pin, 50 = 50Hz pulse
tiltServo = GPIO.PWM(tiltServoPin,50)
#start PWM running, but with value of 0 (pulse off)
panServo.start(0)
tiltServo.start(0)
print ("Servos Init")
sleep(0.5)

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
print("Camera Init")
sleep(0.5)
print("Ready")

scanning = False

def captureNext():
    # Dwell time for the camera to settle
    dwell = 0.5
    sleep(dwell)
    file_name = os.path.join(output_folder, 'image_' + time.strftime("%H_%M_%S") + '.jpg')
    camera.capture(file_name)
    print("captured image: " + 'image_' + time.strftime("%H_%M_%S") + '.jpg')
    sleep(dwell)

def button_callback(self):
    scanning = True
    update(panServo, 90)
    update(tiltServo, 90)
    sleep(2)
    update(panServo, 90+45)
    sleep(2)
    update(panServo, 90)
    sleep(2)
#    update(panServo, -45)
#    captureNext()
#    update(panServo, 0)
#    captureNext()
#    update(panServo, 45)
#    captureNext()
#    update(panServo, 0)
    print("Scan Complete!")
    scanning = False

# Handling the files
#get current working directory
path = os.getcwd()
# make the folder name
folder_name = 'captureSession_' + time.strftime("%Y_%m_%d_%H_%M_%S")
# make the folder
os.mkdir(folder_name)
# construct the output folder path
output_folder = os.path.join(path, folder_name)

GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback)

try:
    while True:
        # Erm... theres not much to do here. I'll have a nap
        if not scanning:
            update(panServo, 0)
            update(tiltServo, 0)
#Clean things up at the end
except KeyboardInterrupt:
   panServo.stop()
   tiltServo.stop()
   GPIO.cleanup()
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
