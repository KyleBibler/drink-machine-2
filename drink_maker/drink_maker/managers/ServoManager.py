from django.apps import apps

import RPi.GPIO as GPIO
import time

def set_pin(pin_num, old_pwm=None):
	if old_pwm is None:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin_num, GPIO.OUT)
		pwm = GPIO.PWM(pin_num, 100)
		#pwm.start(5)
	else:
		pwm = old_pwm
	pwm.start(5)
	return pwm

def set_angle(pwm, angle):
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)

def tear_down(pwm, pin_num):
	#GPIO.setup(pin_num, GPIO.IN)
	#GPIO.output(pin_num, 0)
	pwm.stop()
	#GPIO.cleanup()
