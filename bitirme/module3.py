#!/usr/bin/env python

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
from Queue import Queue
from flask import Flask, render_template, jsonify, Response, request
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



vehicle = None

# Allow us to reuse sockets after the are bound.
# http://stackoverflow.com/questions/25535975/release-python-flask-port-when-script-is-terminated
socket.socket._bind = socket.socket.bind
def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)
socket.socket.bind = my_socket_bind

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

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', branding=False)

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

# @app.route("/api/location", methods=['GET', 'POST', 'PUT'])
# def api_location():
#     if request.method == 'POST' or request.method == 'PUT':
#         try:
#             data = request.get_json()
#             (lat, lon) = (float(data['lat']), float(data['lon']))
#             goto(lat, lon)
#             return jsonify(ok=True)
#         except Exception as e:
#             print(e)
#             return jsonify(ok=False)
#     else:
#         return jsonify(**location_msg())

@app.route("/api/arm", methods=['POST', 'PUT'])
def api_location():
    if request.method == 'POST' or request.method == 'PUT':
        try:
            vehicle.armed = True
            vehicle.flush()
            return jsonify(ok=True)
        except Exception as e:
            print(e)
            return jsonify(ok=False)


@app.route("/api/mode", methods=['POST', 'PUT'])
def api_mode():
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
    point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
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

def connect_to_drone():
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    global vehicle
    connection_string = sitl.connection_string()
    vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
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


# Never cache
@app.after_request
def never_cache(response):
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


t2 = Thread(target=connect_to_drone)
t2.daemon = True
t2.start()

def main():
    app.run(threaded=True, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()
