#!/usr/bin/python3

""" SenseHatMonitor - Monitors all the enviromental sensors on the Rapsberry Pi and stores them as a CSV File """
""" samathy.barratt@rolls-royce.com """
from sense_hat import SenseHat
import time
import datetime
import asyncio
import websockets
import json
from time import sleep
import multiprocessing

from os import path
from os import fsync



def set_all_pixels(color, sense):

    pixels = [color]*64

    sense.set_pixels(pixels)

def selectInterval(sense):
    """Allow user to select a shorter, or longer intival. Returns string "long" or "short" """

    while (True):
        sense.show_message("Short", text_colour=[0,100,0])
        event = sense.stick.wait_for_event(emptybuffer = True)
        if (str(event.direction) == "middle"):
            return "short"
        else:
            print(event)
            event = []
            sense.show_message("Long",text_colour=[0,100,0])
        event = sense.stick.wait_for_event(emptybuffer = True)
        if (str(event.direction) == "middle"):
            print(event)
            return "long"
        event = []

@asyncio.coroutine
def monitor(socket, path):
    """Serves the accel, temp and pressure values 
    to a websocket"""
    while True:
        orientation = sense.get_orientation_degrees()    #Returns {pitch:n, roll:n, yaw:n} gyro = sense.get_gyroscope_raw() #Returns {x:n, y:n, z:n}
        accel = sense.get_accelerometer_raw()    #Returns {x:n, y:n, z:n}
        humidity = sense.get_humidity()
        temp  = sense.get_temperature()
        pressure = sense.get_pressure()

        d = {'accel': accel, 'ori':orientation, 'humidity':humidity, 'temp':temp, 'pressure':pressure}

        yield from socket.send(json.dumps(d))

        sleep(0.3)
    

def webserver():
    print("Running webserver")
    #Run the web server and continue
    server_socket = websockets.serve(monitor, '127.0.0.1', 5678)
    print (server_socket)
    asyncio.get_event_loop().run_until_complete(server_socket)
    asyncio.get_event_loop().run_forever()
    print ("webserver ended")
    
	




sense = SenseHat()

server = multiprocessing.Process(target=webserver)
server.start()

nowrite = False #If we can't open the output files, don't try to write them.

#Set the IMU config (turn on Gyro, Accelerometer and Magetometer)
#                  Compass, Gyro, Accel
sense.set_imu_config(True, True, True)

#Wait this many seconds before taking another reading of the temp, humidity and pressure
timeIntervalEnviroment = 4
#Wait this many seconds before taking another reading of the gyro, accel and compass
timeIntervialPositions = 1

outputFilePath = "/media/usb0/"    #The location to put the datafiles. We have usbmount so this should be the default first memorystick

#Get the date and time - useful for uniquly naming files.
dateTime = str(datetime.datetime.now())

from subprocess import call
call(["mkdir", outputFilePath+"SenseHatMonitor/"]) #Try to make a directory to store the files. if already exists, isnt a problem
outputFilePath = outputFilePath+"SenseHatMonitor/"


try:
    enviromentFile = open(outputFilePath+"enviroment_"+dateTime.replace(" ", "_").replace(":","_")+".csv", "w+")
    orientationFile = open(outputFilePath+"orientation_"+dateTime.replace(" ", "_").replace(":","_")+".csv", "w+")
    gyroscopeFile = open(outputFilePath+"gyroscope_"+dateTime.replace(" ", "_").replace(":","_")+".csv", "w+")
    accelerometerFile = open(outputFilePath+"accelerometer_"+dateTime.replace(" ", "_").replace(":","_")+".csv", "w+")
except:
    print ("Could not open output files")
    sense.show_message("Could not open output files", text_colour=[100.0,0])
    nowrite = True
    exit()



sense.show_message("Select Interval", text_colour=[100,0,0])
interval = selectInterval(sense)

if interval == "short":
    timeIntervalEnviroment = 1
    timeIntervalPositions = 1
else:
    timeIntervalEnviroment = 4
    timeIntervalPositions = 1


print ("initialised files")

#Let the user know everything is okay!

set_all_pixels([0,150,0], sense)

if not nowrite:
    enviromentFile.write("humidity, temperature, pressure\n")
    orientationFile.write("pitch, rolls, yaw\n")
    gyroscopeFile.write("x, y, z\n")
    accelerometerFile.write("x, y, z\n")

print ("Wrote initial column headers")

set_all_pixels([0,0,0], sense)    #Flash the pixels so the user knows everything is okay.

iterator = 0
exit = 0

sense.stick.wait_for_event()



while(exit == 0):

    print ("Looping")
    set_all_pixels([0,0,0], sense)    #Flash the pixels so the user knows everything is okay.

    events = sense.stick.get_events()
    print (events)

    for event in events:
        if str(event.direction) == "middle":
            print ("Break")
            exit = 1
    if exit:
        break

    if iterator == 2:
        set_all_pixels([0,50,0], sense)    #Flash the pixels so the user knows everything is okay.
        iterator = 0

    humidity = sense.get_humidity()
    temp  = sense.get_temperature()
    pressure = sense.get_pressure()

    time.sleep(timeIntervalEnviroment/2)

    orientation = sense.get_orientation_degrees()    #Returns {pitch:n, roll:n, yaw:n}
    gyro = sense.get_gyroscope_raw() #Returns {x:n, y:n, z:n}
    accel = sense.get_accelerometer_raw()    #Returns {x:n, y:n, z:n}

    if not nowrite:
        enviromentFile.write(str(humidity)+", "+str(temp)+", "+str(pressure)+"\n")
        orientationFile.write(str(orientation['pitch'])+", "+ str(orientation['roll'])+", "+str(orientation['yaw'])+"\n")
        gyroscopeFile.write(str(gyro['x'])+", "+str(gyro['y'])+", "+str(gyro['z'])+"\n")
        accelerometerFile.write(str(accel['x'])+", "+str(accel['y'])+", "+str(accel['z'])+"\n")

        #The Pi might be turned off at any time. So make sure to flush the data to disk
        enviromentFile.flush()
        orientationFile.flush()
        gyroscopeFile.flush()
        accelerometerFile.flush()

        fsync(enviromentFile)
        fsync(orientationFile)
        fsync(gyroscopeFile)
        fsync(accelerometerFile)
            

    time.sleep(timeIntervalEnviroment/2)

    #compass = get_compass()
    
    iterator+=1

print ("Quitting")

set_all_pixels([0,0,0], sense)    #Flash the pixels so the user knows everything is okay.

if not nowrite:
    enviromentFile.flush()
    orientationFile.flush()
    gyroscopeFile.flush()
    accelerometerFile.flush()

    fsync(enviromentFile)
    fsync(orientationFile)
    fsync(gyroscopeFile)

    enviromentFile.close()
    orientationFile.close()
    gyroscopeFile.close()
    accelerometerFile.close()
            
sense.show_message("Click again to Shutdown", text_colour=[100,0,0])
events = sense.stick.wait_for_event()

for event in events:
    if str(event.action) == "pressed" or str(event.action) == "released" or str(event.action) == "held":
        subprocess.call(["shutdown","-h", "now", "&"])

set_all_pixels([100,0,0], sense)    #Flash the pixels so the user knows everything is okay.
