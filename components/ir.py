
import threading
import time
import json
from components.rgb import rgb_callback
from enums import RGBColor

def ir_callback(mqtt_client, ir_settings, rgb, rgb_settings, stop_event, value):
    payload = {
            "name": ir_settings["name"],
            "value": value,
            "simulated": ir_settings["simulated"],
            "timestamp": time.time()
    }
    mqtt_client.publish(ir_settings["topic"], json.dumps(payload))
    
    if rgb:
        rgb.change_color(value)
        rgb_callback(mqtt_client, rgb.settings, stop_event, rgb.value)
    else:
        rgb_value = RGBColor.OFF
        match value:
            case "0":
                rgb_value = RGBColor.OFF
            case "1":
                rgb_value = RGBColor.WHITE
            case "2":
                rgb_value = RGBColor.RED
            case "3":
                rgb_value = RGBColor.GREEN
            case "4":
                rgb_value = RGBColor.BLUE
            case "5":
                rgb_value = RGBColor.YELLOW
            case "6":
                rgb_value = RGBColor.PURPLE
            case "7":
                rgb_value = RGBColor.LIGHT_BLUE
        rgb_callback(mqtt_client, rgb_settings, stop_event, rgb_value)

def run_ir(mqtt_client, ir_settings, threads, stop_event):
        if ir_settings['simulated']:
            print("Starting dus simulator")
            # dus1_thread = threading.Thread(target = run_dus_simulator, args=(dus_settings, data_lock, batch, dus_callback, stop_event), daemon=True)
            # dus1_thread.start()
            # threads.append(dus1_thread)
            # print("Dus simulator started")
        else:
            from sensors.ir import run_ir_loop, IR 
            print("Starting IR loop")
            ir = IR(ir_settings)
            ir_thread = threading.Thread(target=run_ir_loop, args=(ir, mqtt_client, ir_callback, stop_event))
            ir_thread.start()
            threads.append(ir_thread)
            print("IR loop started")
