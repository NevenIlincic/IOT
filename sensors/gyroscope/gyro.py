#!/usr/bin/env python3
import MPU6050 
import time
import os
import math

def run_gyro_loop(mqtt_client, gyro_settings, data_lock, batch, callback, stop_event):
    mpu = MPU6050.MPU6050()     #instantiate a MPU6050 class object
    accel = [0]*3               #store accelerometer data
    gyro = [0]*3   
    mpu.dmp_initialize()  
    while(True):
        accel = mpu.get_acceleration()      #get accelerometer data
        gyro = mpu.get_rotation()           #get gyroscope data
        
        accel_value = math.sqrt(math.pow(accel[0], 2) +  math.pow(accel[1], 2) + math.pow(accel[2], 2))
        rotation_value = math.sqrt(math.pow(gyro[0], 2) +  math.pow(gyro[1], 2) + math.pow(gyro[2], 2))
        
        callback(mqtt_client, gyro_settings, data_lock, batch, rotation_value, accel_value, stop_event)
        time.sleep(gyro_settings["delay"])

