

from bottle import route, run, template, request, redirect,TEMPLATE_PATH
from battery_monitor_charging import read_cell_voltages, get_charger_status, battery_charge
from gpio import pwm, current_brightness, set_led_brightness
from imu_icm40627 import imu_monitor
from system_status import get_uptime, get_free_storage, get_temperature, get_current_time
import RPi.GPIO as GPIO
#from camera_module import start_recording, stop_recording

TEMPLATE_PATH.insert(0, '/home/raspberry/Jetscan/temp')  # or 'temp'

@route('/')
def index():
    cells = read_cell_voltages()
    total_mv = sum(cells)
    percent = battery_charge() #min(max(int((total_mv - 1000) / (12600 - 1000) * 100), 0), 100)
    imu_data = {
        "pitch": None, "roll": None,
        "accel": [None, None, None],
        "gyro": [None, None, None]
    }

    try:
        imu_data = imu_monitor()
    except Exception as e:
        print("IMU error:", e)
    return template('dashboard',
                    total_voltage=total_mv / 1000,
                    charge_percent=percent,
                    charger_status=get_charger_status(),
                    cell_voltages=cells,
                    brightness=current_brightness,
                    pitch = imu_data["pitch"],
		    roll=imu_data["roll"],
                    accel=imu_data["accel"],
                    gyro=imu_data["gyro"])

@route('/api/status')
def api_status():
    cells = read_cell_voltages()
    total_mv = sum(cells)
    percent = min(max(int((total_mv - 1000) / (12600 - 1000) * 100), 0), 100)

    try:
        imu_data = imu_monitor()
    except Exception as e:
        print("IMU error:", e)
        imu_data = {
            "pitch": None,
            "roll": None,
            "accel": [None, None, None],
            "gyro": [None, None, None]
        }

#    camera_status = get_camera_status()

    return {
        "total_voltage": round(total_mv/1000 , 2),
        "charge_percent": percent,
        "charger_status": get_charger_status(),
        "brightness": current_brightness,
        "pitch": round(imu_data["pitch"], 1) if imu_data["pitch"] else 0,
        "roll": round(imu_data["roll"], 1) if imu_data["roll"] else 0,
        "accel": [round(x, 2) if x else 0 for x in imu_data["accel"]],
        "gyro": [round(x, 1) if x else 0 for x in imu_data["gyro"]],
        "video_quality": "1080p",
        "uptime": get_uptime(),
        "temperature": f"{get_temperature()}°C",
        "current_time": get_current_time()
        
    }

@route('/set_pwm', method='POST')
def set_pwm():
    try:
#    from gpio import set_led_brightness
    	brightness = int(request.forms.get('brightness'))
    	set_led_brightness(brightness)
    except:
       pass
    return redirect('/')

@route('/cleanup')
def cleanup():
    pwm.stop()
    GPIO.cleanup()
    return "GPIO cleaned up."

def start_web_server():
    run(host='0.0.0.0', port=8081, debug=True, reloader=True)
