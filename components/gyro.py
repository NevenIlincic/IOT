from simulators.gyro import run_gyro_simulator
import threading
import time

def gyro_callback(gyro_settings, data_lock, batch, rotation, activity, stop_event, alarm):
    payload = {
        "name": gyro_settings["name"],
        "rotation": rotation,
        "acceleration": activity,
        "simulated": gyro_settings["simulated"],
        "timestamp": time.time()
    }
    
    if abs(gyro_settings["last_acceleration_value"] - activity) > 50 or abs(gyro_settings["last_rotation_value"] - rotation) > 30:
        alarm.turn_on()
    
    gyro_settings["last_acceleration_value"] = activity
    gyro_settings["last_rotation_value"] = rotation
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return



def run_gyro(settings, threads, stop_event, data_lock, batch, alarm):
        if settings['simulated']:
            print("Starting GYRO sumilator")
            gyro_thread = threading.Thread(target = run_gyro_simulator, args=(settings, data_lock, batch, gyro_callback, stop_event, alarm))
            gyro_thread.start()
            threads.append(gyro_thread)
            print("GYRO sumilator started")
        else:
            from sensors.gyroscope.gyro import run_gyro_loop
            print("Starting GYRO loop")
            dht1_thread = threading.Thread(target=run_gyro_loop, args=(settings, data_lock, batch, gyro_callback, stop_event, alarm))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("GYRO loop started")
