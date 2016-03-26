from django.apps import apps

# import RPi.GPIO as GPIO
import time

def set_pin(pin_num):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
	pwm = GPIO.PWM(18, 100)
	pwm.start(5)

def set_angle(pin_num, angle):
	set_pin(pin_num)
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty)