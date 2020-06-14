

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
import glob
import serial.tools.list_ports
import threading
from threading import Thread, Event
from subprocess import Popen
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from array import *
import dronekit_sitl
from dronekit_sitl import SITL
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('autoModeModal.html', branding = False)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///theUactDB.db'

db = SQLAlchemy(app)

class GuidedFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    targetLat = db.Column(db.Float, nullable=False)
    targetLon = db.Column(db.Float, nullable=False)
    run_velocity = db.Column(db.Float, nullable=False)
    run_altitude = db.Column(db.Float, nullable=False)
    afterReach = db.Column(db.Text, nullable=False)
    run_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def as_dict(self):
        #return '[id:'+ self.id +',targetLat:'+self.targetLat+',targetLon:'+self.targetLon+',run_velocity:'+self.run_velocity+',run_altitude:'+self.run_altitude+',run_date:',self.run_date+']'
        return {c.name: unicode(getattr(self, c.name)) for c in self.__table__.columns}

sitl = None
vehicleState = None
vehicle = None
point1 = None
spinner = None
battery = None
def sse_encode(obj, id=None):
    return "data: %s\n\n" % json.dumps(obj)

def state_msg():
    if vehicle.location.global_relative_frame.lat == None:
        raise Exception('no position info')
    if vehicle.armed == None:
        raise Exception('no armed info')
    return {
        "vehicleState": vehicleState,
        "armed": vehicle.armed,
        "alt": vehicle.location.global_relative_frame.alt,
        "vel": vehicle.airspeed,
        "mode": vehicle.mode.name,
        "heading": vehicle.heading or 0,
        "lat": vehicle.location.global_relative_frame.lat,
        "lon": vehicle.location.global_relative_frame.lon,
        "spinner" : spinner,
        "batteryLevel" : vehicle.battery.level,
        "current" : vehicle.battery.current,
        "voltage" : vehicle.battery.voltage

    }

listeners_location = []
listeners_location

import time
def tcount():
    while True:
        time.sleep(0.10)
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

cancelFlight = False

@app.route("/api/guided", methods = ['POST','PUT'])
def api_guided():
    

    """
    Arms vehicle and fly to aTargetAltitude.
    """
    parameter = request.json['dataY']        
    targetAltitude = float(parameter["altitude"])
    velocity = float(parameter["velocity"])
    point1Lat = float(parameter["point1Lat"])
    point1Lon = float(parameter["point1Lon"])
    afterArrival = parameter["afterArrival"]
    print velocity
    print targetAltitude
    
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready


    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
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


    print("set default/target airspeed to velocity")
    vehicle.airspeed = velocity

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(point1Lat, point1Lon, targetAltitude)
    vehicle.simple_goto(point1)
    global cancelFlight
    while targetReached(point1,vehicle.location.global_relative_frame) != True and cancelFlight != True:
        print 'goiiinnnn'

    print 'ARRIVED'
    if afterArrival == "RTL":
        api_rtl()
    if afterArrival == "LAND":
        api_land()
    if afterArrival == "LOITER":
        api_loiter()

    flight = GuidedFlight(targetLat=point1Lat,targetLon=point1Lon,run_velocity=velocity,run_altitude=targetAltitude,afterReach=afterArrival)

    db.session.add(flight)
    db.session.commit()

            

    return jsonify(ok=True)

@app.route("/api/auto", methods = ['POST','PUT'])
def api_autoMode():
    parameter = request.json['dataX']
    targetAltitude = float(parameter["altitude"])
    velocity = float(parameter["velocity"])
    point1Lat = float(parameter["point1Lat"])
    point1Lon = float(parameter["point1Lon"])
    land1 = str(parameter["land1"])
    land2 = str(parameter["land2"])
    land3 = str(parameter["land3"])
    land4 = str(parameter["land4"])
    rtl1 = str(parameter["rtl1"])
    rtl2 = str(parameter["rtl2"])
    rtl3 = str(parameter["rtl3"])
    rtl4 = str(parameter["rtl4"])

    landOptions = [land1, land2, land3, land4] 
    rtlOptions = [rtl1, rtl2, rtl3, rtl4] 

    points = [[point1Lat, point1Lon]]

    numberOfPoints = 1
    if((parameter["point2Lat"]) != ""):
        numberOfPoints=2
        point2Lat = float(parameter["point2Lat"])
        point2Lon = float(parameter["point2Lon"])    
        points = [[point1Lat, point1Lon], [point2Lat, point2Lon]] 
        if((parameter["point3Lat"]) != ""):
            point3Lat = float(parameter["point3Lat"])
            point3Lon = float(parameter["point3Lon"])
            points = [[point1Lat, point1Lon], [point2Lat, point2Lon], [point3Lat, point3Lon]]    
            numberOfPoints=3
            if((parameter["point4Lat"]) != ""):
                point4Lat = float(parameter["point4Lat"])
                point4Lon = float(parameter["point4Lon"])
                points = [[point1Lat, point1Lon], [point2Lat, point2Lon], [point3Lat, point3Lon], [point4Lat, point4Lon]]
                numberOfPoints=4

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
         ##print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= targetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    print("Set default/target airspeed")         
    vehicle.airspeed = velocity
    
    count = 0

    for x in range(0,numberOfPoints):
        if (vehicle.mode == VehicleMode("LAND")):
            vehicle.mode = VehicleMode("GUIDED")
            while not vehicle.is_armable:
                print(" Waiting for vehicle to initialise...")
                time.sleep(1)
            vehicle.armed = True
            while not vehicle.armed:
                print(" Waiting for arming...")
                time.sleep(1)
            print("Taking off!")
            vehicle.simple_takeoff(targetAltitude)
            while True:
               if vehicle.location.global_relative_frame.alt >= targetAltitude * 0.95:
                   print("Reached target altitude")
                   break
               time.sleep(1)
        

        print("Going towards first point for 30 seconds ...")
        point1 = LocationGlobalRelative(points[x][0], points[x][1], targetAltitude)
        vehicle.simple_goto(point1)
        while not targetReached(point1,vehicle.location.global_relative_frame):
            print 'goind'
            pass
        print 'ARRIVED'
        if(landOptions[count] == 'Next Step: LAND'):
            api_land()
        time.sleep(5)    

        count=count+1



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
    global cancelFlight
    cancelFlight = True
   

    return jsonify(ok=True)

@app.route("/api/test", methods=['POST', 'PUT'])
def api_test():
    print 'rebooting'
    global vehicle
    global guided_on
    cancelFlight = True
    vehicle.armed = False
    reboot_msg = vehicle.message_factory.command_long_encode(
            0, 0,  # target_system, target_component
            mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,  # command
            0,  # confirmation
            1,  # param 1, autopilot (reboot)
            0,  # param 2, onboard computer (do nothing)
            0,  # param 3, camera (do nothing)
            0,  # param 4, mount (do nothing)
            0, 0, 0)  # param 5 ~ 7 not used

    vehicle.send_mavlink(reboot_msg)
    vehicle.close()
    vehicle = None
    if sitl:
        sitl.stop()
    
    
    #vehicle = None

    return jsonify(ok=True)

@app.route("/api/loiter", methods=['POST', 'PUT'])
def api_loiter():
    pointLoiterAlt = vehicle.location.global_relative_frame.alt
    pointLoiterLon = vehicle.location.global_relative_frame.lon
    pointLoiterLat = vehicle.location.global_relative_frame.lat
    loiterPoint = LocationGlobalRelative(pointLoiterLat, pointLoiterLon, pointLoiterAlt)
    vehicle.simple_goto(loiterPoint)
    time.sleep(1)
    print("Loiter mode is on")
    #vehicle.mode = VehicleMode("STABILIZE")
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        ##if vehicle.mode != VehicleMode("LOITER"):
          ##  print("Loiter mode is ended")
            ##break
        time.sleep(1)
    
    return jsonify(ok=True)

@app.route("/api/cancel", methods=['POST', 'PUT'])
def api_cancel():

    sel = request.json['dataSelected']
    print sel
    
    if(sel == "loiter"):
       api_loiter();
    elif(sel == "land"):
        api_land();
    elif(sel == "rtl"):
        api_rtl();
    return jsonify(ok=True)

@app.route("/api/rtl", methods=['POST', 'PUT'])
def api_rtl():
    vehicle.parameters['RTL_ALT'] = 0
    vehicle.mode = VehicleMode("RTL")
    print("Coming home!")

    return jsonify(ok=True)

@app.route("/api/availableDevices", methods=['POST','PUT'])
def availableDevices():

    ports = list( serial.tools.list_ports.comports() )

    resultPorts = []
    descriptions = []
    for port in ports:
        return jsonify(port.description)
    return jsonify(ok=False)

@app.route("/api/connect", methods=['POST','PUT'])
def connect_to_drone():
    if request.method == 'POST' or request.method == 'PUT':

        global vehicle
        global vehicleState
        print 'connecting to drone...'
        while not vehicle:
            try:
                vehicle = connect('com7', wait_ready=False,baud=57600)
            except Exception as e:
                print 'waiting for connection... (%s)' % str(e)
                time.sleep(2)

    # if --sim is enabled...
    #api_arm()
    vehicleState = 'Connected'
    print 'connected!'
    return jsonify(ok=True)


@app.route("/api/simulation", methods=['POST','PUT'])
def enableSimulation():
    parameter = request.json['homeLocation']
    homeLocationLat = float(parameter["lat"])
    homeLocationLng = float(parameter["lng"])
    global vehicle
    global sitl
    homeArg = '--home='+str(homeLocationLat)+','+str(homeLocationLng)+',0,180'
    sitl = dronekit_sitl.start_default(homeLocationLat,homeLocationLng)
    #sitl.download('copter','3.3', verbose=True)
    #sitl_args = ['-I0', '--model', 'quad', homeArg]
    #sitl.launch(sitl_args,await_ready=True, restart = True)
    #connection_string = 'tcp:127.0.0.1:5760'
    connection_string = sitl.connection_string()

    while not vehicle:
            try:
                vehicle = connect(connection_string, wait_ready=True, baud=57600)
            except Exception as e:
                print 'waiting for connection... (%s)' % str(e)
                time.sleep(2)

    global vehicleState
    vehicleState = 'Simulation'
    spinner = False
    print 'simulation mode enabled'
    
    
    return jsonify(ok=True)

@app.route("/api/getDB", methods=['POST','PUT'])
def getDB():
    users = GuidedFlight.query.all()
    for user in users:
        return jsonify([u.as_dict() for u in GuidedFlight.query.all()])

#t2 = Thread(target=connect_to_drone)
#t2.daemon = True
#t2.start()

###################################
## TARGET POINT REACHED FUNCTION ##
###################################
def targetReached(point1, point2):
    if "{:.5f}".format(point1.lat) == "{:.5f}".format(point2.lat):
        if "{:.5f}".format(point1.lon) == "{:.5f}".format(point2.lon):
            print 'going'
            return True
    else:
        return False

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('401.html'), 401

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('autoModeModal.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('about.html')

   
@app.route('/401', methods=['GET', 'POST'])
def error401():
    return render_template('401.html')

@app.route('/404', methods=['GET', 'POST'])
def error404():
    return render_template('404.html')

@app.route('/500', methods=['GET', 'POST'])
def error500():
    return render_template('500.html')

def main():
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.config["CACHE_TYPE"] = "null"
    app.jinja_env.auto_reload = True
    db.create_all()
    app.run(threaded=True,host='127.0.0.1', port=5000)
    

if __name__=="__main__":
    main()
