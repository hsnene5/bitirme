

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
from Queue import Queue
from flask import Flask, render_template, jsonify, Response, request,url_for
import time
import json
import urllib
import atexit
import os
import sys
import socket
from threading import Thread
from subprocess import Popen
from flask import render_template
from flask import Flask, Response
from datetime import datetime

def sse_encode(obj, id=None):
    return "data: %s\n\n" % json.dumps(obj)

def state_msg():
    if vehicle.location.global_relative_frame.lat == None:
        raise Exception('no position info')
    if vehicle.armed == None:
        raise Exception('no armed info')
    return {
        "armed": vehicle.armed,
        "alt": vehicle.location.global_relative_frame.alt,
        "mode": vehicle.mode.name,
        "heading": vehicle.heading or 0,
        "lat": vehicle.location.global_relative_frame.lat,
        "lon": vehicle.location.global_relative_frame.lon
    }

listeners_location = []
listeners_location

from threading import Thread
import time
def tcount():
    while True:
        time.sleep(0.25)
        try:
            msg = state_msg()
            for x in listeners_location:
                x.put(msg)
        except Exception as e:
            pass
t = Thread(target=tcount)
t.daemon = True
t.start()

vehicle = None
app = Flask(__name__)

@app.route("/api/sse/state")
def api_sse_location():
    def gen():
        q = Queue()
        listeners_location.append(q)
        try:
            while True:
                result = q.get()
                ev = sse_encode(result)
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            listeners_location.remove(q)

    return Response(gen(), mimetype="text/event-stream")




@app.route("/")
def home():
    return render_template('autoModeModal.html', branding = False)

@app.route("/api/guided", methods = ['POST','PUT'])
def api_guided():
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    aTargetAltitude = 10
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
    return jsonify(ok=True)

@app.route("/api/auto", methods = ['POST','PUT'])
def api_autoMode():
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(10)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= 10 * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(39.9853521, 32.6448407, 20)
    vehicle.simple_goto(point1)

    # sleep so we can see the change in map
    time.sleep(30)
    
    print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
    point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
    vehicle.simple_goto(point2, groundspeed=10)
    
    # sleep so we can see the change in map
    time.sleep(30)
    
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")
    
    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()
    return jsonify(ok=True)

@app.route("/api/arm", methods=['POST', 'PUT'])
def api_arm():
    if request.method == 'POST' or request.method == 'PUT':
        try:
            vehicle.armed = True
            vehicle.flush()
            return jsonify(ok=True)
        except Exception as e:
            print(e)
            return jsonify(ok=False)

@app.route("/api/connect", methods=['POST','PUT'])
def connect_to_drone():
    if request.method == 'POST' or request.method == 'PUT':

        global vehicle

        print 'connecting to drone...'
        while not vehicle:
            try:
                vehicle = connect('com7', wait_ready=False,baud=57600)
            except Exception as e:
                print 'waiting for connection... (%s)' % str(e)
                time.sleep(2)

    # if --sim is enabled...

    print 'connected!'

@app.route("/api/simulation", methods=['POST','PUT'])
def enableSimulation():
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    global vehicle
    connection_string = sitl.connection_string()
    vehicle = connect(connection_string, wait_ready=True)
    print 'simulation mode enabled'
    return jsonify(ok=True)

#t2 = Thread(target=connect_to_drone)
#t2.daemon = True
#t2.start()

def main():
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(threaded=True,host='127.0.0.1', port=5000)
    

if __name__=="__main__":
    main()
