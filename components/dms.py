import time
import threading
from simulators.dms import run_dms_simulator
from enum import Enum
from classes.security_sistem import SecuritySystem
from classes.alarm import Alarm
import json
from enums import State, Attempt, AlarmState


def dms_callback(mqtt_client, settings, value, alarm: Alarm, security_system: SecuritySystem):
    success = Attempt.SUCCESS
    if settings["password"] == value:
        print(security_system.value == State.OFF)
        if security_system.value == State.OFF:
            if alarm.value == AlarmState.ACTIVE:
                alarm.value = AlarmState.NOT_ACTIVE
            else:
                time.sleep(10)
                security_system.value = State.ON
        else:
            if alarm.value == AlarmState.ACTIVE:
                alarm.turn_off()
            security_system.value = State.OFF
    else:
        success = Attempt.FAIL
        
    value = "SYSTEM ACTIVATED" if security_system.value == State.ON else "SYSTEM DEACTIVATED"
    
    data_to_send = {
                    "name": settings["name"],
                    "value": value,
                    "attempt": success.name,
                    "simulated": True,
                    "timestamp": time.time()
                } 

    mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
    
def run_dms(mqtt_client, alarm, security_system, settings, batch, data_lock, threads, stop_event):
        if settings['simulated']:
            print("Starting DMS simulator")
            # dms_thread = threading.Thread(target = run_dms_simulator, args=(settings, dms_callback, stop_event), daemon=True)
            # dms_thread.start()
            # threads.append(dms_thread)
            # print("DMS simulator started")
        else:
            from sensors.dms import run_dms_loop, DMS
            print("Starting DMS loop")
            dms = DMS(settings, batch, data_lock, alarm, security_system, mqtt_client)
            dms_thread = threading.Thread(target=run_dms_loop, args=(dms, stop_event, dms_callback), daemon=True)
            dms_thread.start()
            threads.append(dms_thread)
            print("DMS loop started")