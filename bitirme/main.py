

from dronekit import connect, VehicleMode
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
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('landingPage.html', branding = False)

@app.route("/api/guided", methods = ['POST','PUT'])
def api_guided():
    while not vehicle.is_armable:
        print "Waiting for vehicle to become armable"
        time.sleep(1)

    #Switch vehicle to GUIDED mode and wait for change
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode!="GUIDED":
        print "Waiting for vehicle to enter GUIDED mode"
        time.sleep(1)

    #Arm vehicle once GUIDED mode is confirmed
    vehicle.armed=True

    while vehicle.armed==False:
        print "Waiting for vehicle to become armed."
        time.sleep(1)



    while True:
        print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt>=1*.95:
            break
        time.sleep(1)

    print("Target altitude reached")
    return None

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

def connect_to_drone():
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

t2 = Thread(target=connect_to_drone)
t2.daemon = True
t2.start()

def main():
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(threaded=True,host='127.0.0.1', port=5000)
    

if __name__=="__main__":
    main()
