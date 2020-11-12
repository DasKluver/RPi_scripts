# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 13:45:17 2020

@author: Jonas
"""

from datetime import datetime as dt
from sense_hat import SenseHat
from time import time

sh = SenseHat()

sampleTime = 1 #Hvor lenge det skal gå mellom hver måling
indexCount = 0 

filename = str(dt.now()).split(".")[0].replace(":", ".").replace(" ", "_")

#path = "/home/pi/Documents/"+filename+".csv"
path = filename

def write_to_log(data): 
	with open(path, "a") as f: 
		f.write(str(data) + "\n")
        
def get_sensor_data(timeToSample=0, humidity=True, tempHumidity=True, tempPressure=True, pressure=True, 
                    magnetometer=True, gyroskop=True, akselerometer=True):
    
    header = ""
    data = ""
    
    if timeToSample > 0:
        humidityList, tempHumidityList, tempPressureList, pressureList = [], [], [], []
        magnetometerList, gyroskopList, akselerometerList = [[], [], []], [[], [], []], [[], [], []]
                    
        timeToSample = time() + timeToSample
        while timeToSample > time():
            if humidity:
                humidityList.append(sh.get_humidity())
            if tempHumidity:
                tempHumidityList.append(sh.get_temperature_from_humidity())
            if tempPressure:
                tempPressureList.append(sh.get_temperature_from_pressure())
            if pressure:
                pressureList.append(sh.get_pressure())
            if magnetometer:
                mag = sh.get_compass_raw()
                magnetometerList[0].append(mag["x"])
                magnetometerList[1].append(mag["y"])
                magnetometerList[2].append(mag["z"])
            if gyroskop:
                gyro = sh.get_gyroscope_raw()
                gyroskopList[0].append(gyro["x"])
                gyroskopList[1].append(gyro["y"])
                gyroskopList[2].append(gyro["z"])
            if akselerometer:
                aks = sh.get_accelerometer_raw()
                akselerometerList[0].append(aks["x"])
                akselerometerList[1].append(aks["y"])
                akselerometerList[2].append(aks["z"])
        if humidity:
            header += "," + "Humidity"
            data += "," + str(round(sum(humidityList)/len(humidityList), 2))
        if tempHumidity:
            header += "," + "TempFromHumidity"
            data += "," + str(round(sum(tempHumidityList)/len(tempHumidityList), 2))
        if tempPressure:
            header += "," + "TempFromPressure"
            data += "," + str(round(sum(tempPressureList)/len(tempPressureList), 2))
        if pressure:
            header += "," + "Pressure"
            data += "," + str(round(sum(pressureList)/len(pressureList), 2))
        if magnetometer:
            header += "," + "MagnetometerX" + "," + "MagnetometerY" + "," + "MagnetometerZ"
            data += ","  + str(round(sum(magnetometerList[0])/len(magnetometerList[0]), 4))
            data += ","  + str(round(sum(magnetometerList[1])/len(magnetometerList[1]), 4))
            data += ","  + str(round(sum(magnetometerList[2])/len(magnetometerList[2]), 4))
        if gyroskop:
            header += "," + "GyroskopX" + "," + "GyroskopY" + "," + "GyroskopZ"
            data += ","  + str(round(sum(gyroskopList[0])/len(gyroskopList[0]), 4))
            data += ","  + str(round(sum(gyroskopList[1])/len(gyroskopList[1]), 4))
            data += ","  + str(round(sum(gyroskopList[2])/len(gyroskopList[2]), 4))
        if akselerometer:
            header += "," + "AkselerometerX" +"," + "AkselerometerY" + "," + "AkselerometerZ"
            data += ","  + str(round(sum(akselerometerList[0])/len(akselerometerList[0]), 4))
            data += ","  + str(round(sum(akselerometerList[1])/len(akselerometerList[1]), 4))
            data += ","  + str(round(sum(akselerometerList[2])/len(akselerometerList[2]), 4))
            
        return header[1:], data[1:]
    
    else:
        if humidity:
            header += "," + "Humidity"
            data += ","  + str(round(sh.get_humidity(), 2))
        if tempHumidity:
            header += "," + "TempFromHumidity"
            data += ","  + str(round(sh.get_temperature_from_humidity(), 2))
        if tempPressure:
            header += "," + "TempFromPressure"
            data += ","  + str(round(sh.get_temperature_from_pressure(), 2))
        if pressure:
            header += "," + "Pressure"
            data += ","  + str(round(sh.get_pressure(), 2))
        if magnetometer:
            header += "," + "MagnetometerX" + "," + "MagnetometerY" + "," + "MagnetometerZ"
            mag = sh.get_compass_raw()
            data += ","  + str(round(mag["x"], 4)) + ","  + str(round(mag["y"], 4)) + ","  + str(round(mag["z"], 4))
        if gyroskop:
            header += "," + "GyroskopX" + "," + "GyroskopY" + "," + "GyroskopZ"
            gyro = sh.get_gyroscope_raw()
            data += ","  + str(round(gyro["x"], 4)) + ","  + str(round(gyro["y"], 4)) + ","  + str(round(gyro["z"], 4))
        if akselerometer:
            header += "," + "AkselerometerX" +"," + "AkselerometerY" + "," + "AkselerometerZ"
            aks = sh.get_accelerometer_raw()
            data += ","  + str(round(aks["x"], 4)) + ","  + str(round(aks["y"], 4)) + ","  + str(round(aks["z"], 4))
            
        return header[1:], data[1:]


header = "Index," + "Tid," + get_sensor_data()[0]
write_to_log(header) #Skriver header basert på hvilke målinger vi har valgt å logge
startTime = time()
nextSample = startTime + sampleTime
while(True):
    
    timeNow = time()
    if nextSample <= timeNow:
        data = str(indexCount) + "," + str(round(timeNow - startTime))
        data += "," + get_sensor_data()[1]
        write_to_log(data)
        indexCount += 1
        nextSample = nextSample + sampleTime
        