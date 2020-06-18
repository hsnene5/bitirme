# The UACT - Unmanned Autonomous Cargo Transporter

The UACT is a web application that allows you to instantly control your Ardupilot installed drone and create some tasks. It is fast and easy to use with its Flask server, SQLAlchemy support and Bootstrap design.


# Flight Modes

There are multiple flight modes that you can perform with the Uact. These flight modes are **MAVLink** messages created with **DroneKit** support.

## Guided

Guided mode allows you to send your drone to the point you set at the desired height and speed.

## Auto

Auto mode allows you to select a maximum of 4 points and different flight modes. With this mode, you can complete a fully autonomous flight.
## RTL

RTL mode allows you to take the drone back to the starting point of the flight. You can use this mode during the flight or after the flight is completed.
## Land

The Land mode allows you to land the drone at the spot you desire. You can use land mode during flight.

## Loiter

The Loiter mode allows you to keep the drone steady in its current position and height. After switching to loiter mode, you can continue the flight from where you left off or change your destination.
## Cancel

The cancel mode allows you to cancel the flight. While the drone is in the air, you need to choose RTL (Return to Launch), Loiter or Land options.


# Connection Modes

## Connect

With Connet mode, you can see the telemetries currently connected to your computer and connect to the drone of your choice through the telemetry you choose.

## Simulation

Simulasyon modunu eğer bağlı bir dronunuz yoksa kullanabilirsiniz. Oldukça gerçekçi olan simulasyon moduyla uçuş denemeleri ve uçuş provaları yapabilirsiniz. Dronun başlangıç noktasına kadar seçebilirsiniz. Simulasyon modu DroneKit-SITL desteğiyle çalışmaktadır.

# Other Options

## Arm

Arm moduyla dronunuzu çalıştırabilirsiniz. Dronunuz pil tasarrufu sağlamak için sadece 10 saniye Armed durumunda kalabilir.

## Reboot

Reboot mode allows you to restart the drone when there is any problem. It is not safe to use this mode during flight.

## Prev Fligths

From this option, you can see the flight information you made previously and repeat these flights. Flight records will be added here after the flight is completed, not instant.
# Dashboard

## Run Mode

Indicates that you are in simulation or connect mode.

## Vehicle

Shows the vehicle's current ArduPilot mode.


## Armed

Shows vehicle armed or not.

## Altitude

Shows vehicle's current altitude in meters.

## Heading

Shows the vehicle's heading angle in degrees. 360 total.


## Velocity

Shows vehicle's current airspeed. (meters per second)
## Battery

Shows vehicle's current battery level in percentage. If battery level is less than **25%** this part will turn to red.

## Heading

Shows the vehicle's current voltage in volts.


## Velocity

Shows vehicle's current current in amperes.
## Main Map

On this Google Maps map you can see the locations of drones, simulation start, users and destinations.



# Resources

You can see used resources below.


## DroneKit

All vehicle operations are done with **DroneKit Python API.** [Dronekit](http://dronekit.io/).

## SQLAlchemy


All database operations are done with **SQLAlchemy.** [SQLAlchemy](https://www.sqlalchemy.org/)

## Flask

Server is deployed with Flask. **Flask.**[Flask](https://flask.palletsprojects.com/en/1.1.x/)
## Bootstrap


Interface is designed with **Bootstrap 4.** [Bootstrap 4](https://getbootstrap.com/)
## GoogleMaps JavaScript API V3


Map operations are handled with **GoogleMaps.** [GoogleMaps](https://developers.google.com/maps/documentation/javascript/reference)
## ngrok


**ngrok** is used to make localhost server https public [ngrok](https://ngrok.com/)

# Installation
After downloading or clone the project, install a virtual environment and load the libraries in the **requirements.txt** file
After making the necessary downloads:
You can set where the server is installed in the **main.py** file. Just change the     
*app.run(threaded=True,host='127.0.0.1', port=5000)* line to make this change.



**For detailed information and contact** 
[The UACT Website.](https://theuact.xyz/)

18.06.2020 Hasan Enes DOGAN
