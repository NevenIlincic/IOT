
from simulators.dpir1 import run_dpir_simulator
from components.dl import dl_callback
import threading
import time
from enums import DoorLightState
from enums import MotionDetected
import json

last_state_1 = MotionDetected.NOT_DETECTED
last_state_2 = MotionDetected.NOT_DETECTED

def dpir_callback(mqtt_client, dpir_settings, dl, dl_settings, data_lock, batch, stop_event, value, dus_settings, dpir_dus_shared_dict, all_settings):
    global last_state_1
    global last_state_2
    payload = {
            "name": dpir_settings["name"],
            "value": value.name,
            "simulated": dpir_settings["simulated"],
            "timestamp": time.time()
    }
    
    if dpir_settings["name"] == "dpir_1":
        if value == MotionDetected.DETECTED:
            if last_state_1 == MotionDetected.NOT_DETECTED:
                dus_settings["start_distance"] = dpir_dus_shared_dict["dus_1"][2]
                last_state_1 = MotionDetected.DETECTED

            if dl:
                dl.toggle_light(data_lock, stop_event, dl_callback)
            
            else:       
                dl_thread = threading.Thread(target = run_simulated_dl_thread, args=(dl_settings, data_lock, batch, stop_event), daemon=True)
                dl_thread.start()
        else:
            if last_state_1 == MotionDetected.DETECTED:
                dus_settings["end_distance"] = dpir_dus_shared_dict["dus_1"][2]
                last_state_1 = MotionDetected.NOT_DETECTED
                
                start_distance = dus_settings["start_distance"]
                end_distance = dus_settings["end_distance"]
                
                
                if start_distance >= end_distance:
                    mqtt_client.publish("commands/add_people", json.dumps({"add": 1}))
                else:
                    mqtt_client.publish("commands/subtract_people", json.dumps({"subtract": 1}))
                  
    if dpir_settings["name"] == "dpir_2":
        if value == MotionDetected.DETECTED:
            if last_state_2 == MotionDetected.NOT_DETECTED:
                dus_settings["start_distance"] = dpir_dus_shared_dict["dus_2"][2]
                last_state_2 = MotionDetected.DETECTED
        else:
            if last_state_2 == MotionDetected.DETECTED:
                dus_settings["end_distance"] = dpir_dus_shared_dict["dus_2"][2]
                last_state_2 = MotionDetected.NOT_DETECTED
                
                start_distance = dus_settings["start_distance"]
                end_distance = dus_settings["end_distance"]
                
                if start_distance >= end_distance:
                    mqtt_client.publish("commands/add_people", json.dumps({"add": 1}))
                else:
                    mqtt_client.publish("commands/subtract_people", json.dumps({"subtract": 1}))
                        
    if dpir_settings["name"] == "dpir_3":
        if value == MotionDetected.DETECTED and all_settings["people"] == 0:
            mqtt_client.publish("commands/alarm", json.dumps({"action": "ON"}))
            # alarm.turn_on()
            
    with data_lock:
        batch.append(payload)
            
    if stop_event.is_set():
        return


def run_dpir(mqtt_client, settings, threads, stop_event, batch, data_lock, dl, dl_settings, dus_settings, dpir_dus_shared_dict, all_settings):
    if settings['simulated']:
        print("Starting DPIR simulator")
        dpir_thread = threading.Thread(target = run_dpir_simulator, args=(mqtt_client, settings, data_lock, batch, dpir_callback, stop_event, dl, dl_settings, dus_settings, dpir_dus_shared_dict, all_settings), daemon=True)
        dpir_thread.start()
        threads.append(dpir_thread)
        print("DPIR simulator started")
    else:
        from sensors.dpir import run_dpir_loop, DPIR
        print("Starting DPIR loop")
        dpir = DPIR(settings)
        dpir_thread = threading.Thread(target=run_dpir_loop, args=(mqtt_client, dpir, settings, data_lock, batch, stop_event, dpir_callback, dl, dl_settings, dus_settings, dpir_dus_shared_dict, all_settings), daemon=True)
        dpir_thread.start()
        threads.append(dpir_thread)
        print("DPIR loop started")

def run_simulated_dl_thread(dl_settings, data_lock, batch, stop_event):
    dl_callback(dl_settings, data_lock, batch, stop_event, DoorLightState.ON.name)
    time.sleep(10)
    dl_callback(dl_settings, data_lock, batch, stop_event, DoorLightState.OFF.name)