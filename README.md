# ServoPanAndTiltHead
Servo driven pan and tilt head based around a Raspberry Pi and hobby servos.


Instructions

flash sd - ctrl+Shift+X to setup properly

sudo apt update
sudo apt upgrade
sudo raspi-config 
------------------------------
	3 Interface options
		- Turn on camera
		- Enable Remote GPIO

------------------------------------

sudo apt install git
git clone https://github.com/rwlloyd/ServoPanAndTiltHead.git

install python libraries
sudo apt install python3-pip

sudo apt install pigpio python-pigpio python3-pigpio
pip3 install evdev
pip3 install gpiozero
pip3 install picamera

https://gpiozero.readthedocs.io/en/stable/api_pins.html#changing-pin-factory

# Start the pigpio daemon. Add this to bashrc along with the pin factory setting.
sudo pigpiod 
export GPIOZERO_PIN_FACTORY=pigpio - (uses pigpio daemon for the rest of the session)
