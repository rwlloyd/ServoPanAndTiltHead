# Import libraries
from gpiozero import AngularServo
from gpiozero import Button
from picamera import PiCamera
import os
import time
from time import sleep

# Pan and tilt Servo Pins are 23 and 24 respectively
panServo = AngularServo(13, initial_angle=0, min_angle=-90, max_angle=90)
tiltServo = AngularServo(12, initial_angle=0, min_angle=-60, max_angle=60)

button = Button(25)

# Setup the camera
camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
#camera.shutter_speed = camera.exposure_speed
#camera.exposure_mode = 'off'
#g = camera.awb_gains
#camera.awb_mode = 'off'
#camera.awb_gains = g

#get current working directory
path = os.getcwd()
# make the folder name
folder_name = 'captureSession_' + time.strftime("%Y_%m_%d_%H_%M_%S")
# make the folder
os.mkdir(folder_name)
# construct the output folder path
output_folder = os.path.join(path, folder_name)

def runSequence():
    print("Capturing")
    panServo.angle = 90
    captureNext()
    panServo.angle = 90+45
    captureNext()
    panServo.angle = 90
    captureNext()
    panServo.angle = 90
    tiltServo.angle = 90
    scanNum =+ 1

def captureNext():
    # Dwell time for the camera to settle
    dwell = 0.5
    sleep(dwell)
    file_name = os.path.join(output_folder, 'image_' + time.strftime("%H_%M_%S") + '.jpg')
    camera.capture(file_name)
    print("captured image: " + 'image_' + time.strftime("%H_%M_%S") + '.jpg')
    sleep(dwell)

while True:
    button.when_pressed = runSequence

