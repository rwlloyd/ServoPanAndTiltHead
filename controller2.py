# Import libraries
import RPi.GPIO as GPIO
import time

panServoPin = 23
tiltServoPin = 24
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
print ("Servos Initiated")
time.sleep(1)

# Define variable duty
"""

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

def update(thisServo, angle):
        duty = float(angle) / 10.0 + 2.5
        thisServo.ChangeDutyCycle(duty)

def button_callback():
    update(panServo, 0)
    update(tiltServo, 0)

# Wait a couple of seconds
time.sleep(2)

GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback)

    #Clean things up at the end
#except KeyboardInterrupt:
#    panServo.stop()
#    tiltServo.stop()
#    GPIO.cleanup()
#    print ("Goodbye")
