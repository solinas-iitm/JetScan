from datetime import datetime
from battery_monitor_charging import read_cell_voltages
import os

log_folder = "/home/raspberry/Jetscan/logs"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "data_log.csv")

def log_data():
    voltages = read_cell_voltages()
    total = sum(voltages) / 1000
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{now},{total:.2f}V,{','.join(str(v) for v in voltages)}\n")
