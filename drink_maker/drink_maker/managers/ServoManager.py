from django.apps import apps

import RPi.GPIO as GPIO 
import time

 

def set_pin(pin_num):
	#pwn = None #JR
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_num, GPIO.OUT)
	
	#pwm.start(5)	
	pwm = GPIO.PWM(pin_num, 100)
	return pwm

def start(pwm):	
	pwm.start(5)
	

def set_angle(pwm, duty):
	#duty = float(angle) / 18.0 + 2
	print duty
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)

def tear_down(pwm):
	#GPIO.setup(pin_num, GPIO.IN)
	#GPIO.output(pin_num, 0)
	pwm.stop()
	#GPIO.cleanup()
