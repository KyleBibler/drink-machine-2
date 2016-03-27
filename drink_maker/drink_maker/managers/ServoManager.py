from django.apps import apps

# import RPi.GPIO as GPIO
import time

def set_pin(pin_num):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_num, GPIO.OUT)
	pwm = GPIO.PWM(pin_num, 100)
	pwm.start(5)

def set_angle(pin_num, angle):
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty)