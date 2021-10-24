#importing required libraries for the camera and gpio pins
from picamera import PiCamera
from time import sleep
from gpiozero import Button, LED

#create variables for all interfaces (button, camera, LEDs)
button = Button(2)
camera = PiCamera()
red_led = LED(21)
yellow_led = LED(20)
green_led = LED(16)

#start camera preview to take picture
camera.start_preview()

#reset camera settings
camera.brightness = 60
camera.contrast = 75

#wait for button press
button.wait_for_press()

#start sequence of flashing LEDs (red, yellow, green)
red_led.on()
sleep(1)
red_led.off()
yellow_led.on()
sleep(1)
yellow_led.off()
green_led.on()
sleep(1)
green_led.off()

#take and save picture
camera.capture("/home/pi/projects/SE101/images/image1.jpg")

#stop camera preview
camera.stop_preview()
