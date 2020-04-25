#/usr/bin/env python
# -*- coding: utf-8 -*-
from dronekit import connect,VehicleMode,LocationGlobalRelative
from pymavlink import mavutil
import time
# Receiving from command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--connect',help="PORT_NO")
args = parser.parse_args()

# Connecting to the vehicle
connection_string = args.connect
print("Connecting to...% s" % connection_string)
vehicle = connect('com7', wait_ready= False,baud=57600)

#Function to arm and takeoff to a specified altitude
def arm_and_takeoff(aTargetAlt):
	print("Basic Prearm checks..dont touch!!")
	print("Waiting for vehicle to initialize")
	time.sleep(1)
	print("Arming Motors..")
	# Copter should arm in Guided-mode
	vehicle.mode = VehicleMode("GUIDED")
	
	
	vehicle.armed = True
	vehicle.flush()
        print("Is Armed:% s"% vehicle.armed)
	
	while not vehicle.armed:
		print("Waiting for arming...Mode:% s"% vehicle.mode)
		print("Is Armed:% s"% vehicle.armed)
		vehicle.armed = True
		time.sleep(2)
		
	print("Taking Off..")
	vehicle.simple_takeOff(aTargetAlt)

	while True:
		print("Altitude: ",vehicle.location.global_relative_frame.alt)
		#Break and return from function just below target altitude.
		if vehicle.location.global_relative_frame.alt>=aTargetAlt: 
			print("Reached Target Altitude..")
			break
		time.sleep(2)
	
vehicle.close()
arm_and_takeoff(2)