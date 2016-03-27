from django.apps import apps

import usb.core
import usb.util

VENDOR_ID = 0x0922
PRODUCT_ID = 0x8003

# find the USB device
device = usb.core.find(idVendor=VENDOR_ID,
                       idProduct=PRODUCT_ID)

def device_ready():
	return device is None

def get_scale_data():	
	# use the first/default configuration
	if not device_ready():
		return False
		
	reattach = False
	if device.is_kernel_driver_active(0):
	    reattach = True
	    device.detach_kernel_driver(0)

	device.set_configuration()
	# first endpoint
	endpoint = device[0][(0,0)][0]

	# read a data packet
	attempts = 10
	data = None
	while data is None and attempts > 0:
	    try:
	        data = device.read(endpoint.bEndpointAddress,
	                           endpoint.wMaxPacketSize)
	    except usb.core.USBError as e:
	        data = None
	        if e.args == ('Operation timed out',):
	            attempts -= 1
	            continue

	print data
	return data