### UNTESTED ON HARDWARE ###

# Import libraries
from gpiozero import AngularServo
from gpiozero import Button
from picamera import PiCamera
import os
import time
from time import sleep

# Pan and tilt Servo Pins are 23 and 24 respectively
panServo = AngularServo(12, initial_angle=0, min_angle=-90, max_angle=90)
tiltServo = AngularServo(13, initial_angle=0, min_angle=-60, max_angle=60)

button = Button(25)

# Setup the camera
camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

# Dwell time for camera shake to settle
dwell = 1
# Variable to keep track of the image and scan numbers
imageNum = 0
scanNum = 0

#scanning = False

def runSequence():
    #scanning = True
    print("Capturing")
    panServo.angle = -45
    sleep(dwell)
    captureNext()
    sleep(dwell)
    panServo.angle = 0
    sleep(dwell)
    captureNext()
    sleep(dwell)
    panServo.angle = 45
    sleep(dwell)
    captureNext()
    sleep(dwell)
    #scanning = False
    # Reset the Image number
    imageNum = 0
    # increment the scan number
    scanNum += 1

def captureNext():
    file_name = os.path.join(output_folder, 'scan{0:02d}_image{1:02d}.jpg'.format(scanNum, imageNum))
    camera.capture(file_name)
    print("captured image: " + 'scan{0:02d}_image{1:02d}.jpg'.format(scanNum, imageNum))
    imageNum += 1

if __name__ == "__main__":
    path = os.getcwd()
    folder_name = 'captureSession_' + time.strftime("%Y_%m_%d_%H_%M_%S")
    os.mkdir(folder_name)
    output_folder = os.path.join(path, folder_name)
    while True:
        print("Waiting...")
        button.when_pressed = runSequence
    

