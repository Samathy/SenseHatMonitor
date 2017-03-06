""" SenseHatMonitor - Monitors all the enviromental sensors on the Rapsberry Pi and stores them as a CSV File """
""" samathy.barratt@rolls-royce.com """
from sense_hat import SenseHat
import time
import datetime
from os import path


sense = SenseHat()

#Set the IMU config (turn on Gyro, Accelerometer and Magetometer)
#                  Compass, Gyro, Accel
sense.set_imu_config(True, True, True)

#Wait this many seconds before taking another reading of the temp, humidity and pressure
timeIntervalEnviroment = 4
#Wait this many seconds before taking another reading of the gyro, accel and compass
timeIntervialPositions = 1

outputFilePath = "/mnt/FAT/"    #The location to put the datafiles

#Get the date and time - useful for uniquly naming files.
dateTime = str(datetime.datetime.now())

try:
    enviromentFile = open(outputFilePath+"enviroment_"+dateTime.replace(" ", "_").replace(":","_")+".csv", "w+")
    positionalFile = open(outputFilePath+"positional_"+dateTime.replace(" ", "_").replace(":","_")+".csv", "w+")
except:
    print ("Could not open output files")
    sense.show_message("Could not open output files", text_colour=[100.0,0])
    exit()




while(1):
    humidity = sense.get_humidity()
    temp  = sense.get_temperature()
    pressure = sense.get_pressure()

    time.sleep(timeIntervalEnviroment/2)

    orientation = sense.get_orientation_degrees()    #Returns {pitch:n, roll:n, yaw:n}
    gyro = sense.get_gyroscope_raw() #Returns {x:n, y:n, z:n}
    accel = sense.get_accelerometer_raw()    #Returns {x:n, y:n, z:n}





    time.sleep(timeIntervalEnviroment/2)


    #compass = get_compass()
    




    time.sleep(4)

