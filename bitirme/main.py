

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
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

vehicle = None
point1 = None
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
        "lon": vehicle.location.global_relative_frame.lon,
        "point1": point1
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
    aTargetAltitude = 20
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)


    print("Taking off!")
    vehicle.simple_takeoff(20)  # Take off to target altitude

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


    print("set default/target airspeed to 3")
    vehicle.airspeed = 3

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(39.9853521, 32.6448407, 20)
    vehicle.simple_goto(point1)

    return jsonify(ok=True)


    #while True:
    #    print(" Altitude: ", vehicle.location.global_relative_frame.alt)
    #    # Break and return from function just below target altitude.
    #    if vehicle.location.global_relative_frame.alt <=  0.5:
    #        print("Landed safely")
    #        break
    #    time.sleep(1)

    #print("Set default/target airspeed to 3")
    #vehicle.airspeed = 3

    #print("Going towards first point for 30 seconds ...")
    #point1 = LocationGlobalRelative(39.9853521, 32.6448407, 20)
    #vehicle.simple_goto(point1)

@app.route("/api/auto", methods = ['POST','PUT'])
def api_autoMode():
    parameters = request.json['dataX']
    targetAltitude = float(parameters["altitude"])
    
    print(targetAltitude)
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")

    # Check if the vehicle is already armed
    if not (vehicle.armed):
        vehicle.armed = True
        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(targetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= targetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    print("Going towards first point for 30 seconds ...")
    global point1
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


@app.route("/api/land", methods=['POST', 'PUT'])
def api_land():
    
    print("Now let's land")
    vehicle.mode = VehicleMode("LAND")

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt <=  0.5:
            print("Landed safely")
            break
        time.sleep(1)
    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()
    return jsonify(ok=True)

@app.route("/api/loiter", methods=['POST', 'PUT'])
def api_loiter():
    
    print("Loiter mode is on")
    vehicle.mode = VehicleMode("LOITER")

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.mode != VehicleMode("LOITER"):
            print("Loiter mode is ended")
            break
        time.sleep(1)
    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()
    return jsonify(ok=True)





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



### from dronekit-python examples

#    NO 1 
#   The function is useful when you want to move the vehicle around specifying locations relative to 
#    the current vehicle position.


def get_location_metres(original_location, dNorth, dEast):
  
    earth_radius = 6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation;

# NO 2

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)


## NO 3

def goto_position_target_global_int(aLocation):
    """
    Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified LocationGlobal.

    For more information see: https://pixhawk.ethz.ch/mavlink/#SET_POSITION_TARGET_GLOBAL_INT

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111111000, # type_mask (only speeds enabled)
        aLocation.lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
        aLocation.lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        aLocation.alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
        0, # X velocity in NED frame in m/s
        0, # Y velocity in NED frame in m/s
        0, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)

# NO 4

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    """

    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def goto_position_target_global_int(aLocation):
    """
    Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified LocationGlobal.

    For more information see: https://pixhawk.ethz.ch/mavlink/#SET_POSITION_TARGET_GLOBAL_INT

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111111000, # type_mask (only speeds enabled)
        aLocation.lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
        aLocation.lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        aLocation.alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
        0, # X velocity in NED frame in m/s
        0, # Y velocity in NED frame in m/s
        0, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)

t = Thread(target=tcount)
t.daemon = True
t.start()

def main():
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.config["CACHE_TYPE"] = "null"
    app.jinja_env.auto_reload = True
    app.run(threaded=True,host='127.0.0.1', port=5000)
    

if __name__=="__main__":
    main()
