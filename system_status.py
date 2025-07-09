import os
import time
import shutil
import psutil
from datetime import datetime

def get_uptime():
    return round(time.time() - psutil.boot_time()) // 3600  # in hours

def get_free_storage():
    total, used, free = shutil.disk_usage('/')
    return round(free / (1024 ** 3), 2)  # GB

def get_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000
        return f"{temp:.1f}°C"
    except:
        return "N/A"

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def shutdown_system():
    return os.system("sudo shutdown now")
