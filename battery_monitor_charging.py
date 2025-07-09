from smbus import SMBus


BATTERY_MONITOR_ADDR = 0x08
BATTERY_CHARGER_ADDR = 0x6B
CHARGER_STATUS_REG = 0x1B
CELL_REGISTERS = [0x14, 0x16, 0x18, 0x1A, 0x1C]

bus = SMBus(1)

def read_word(addr, reg):
    try:
        data = bus.read_i2c_block_data(addr, reg, 2)
        return data[1] << 8 | data[0]
    except:
        return 0

def read_cell_voltages():
    return [read_word(BATTERY_MONITOR_ADDR, reg) for reg in CELL_REGISTERS]
    
def get_charger_status():
    try:
        chrg = (bus.read_byte_data(BATTERY_CHARGER_ADDR, CHARGER_STATUS_REG) >> 2) & 0x07
        return {
            0: "Not Charging",
            1: "Trickle-Charge",
            2: "Pre-Charge",
            3: "Fast-Charge",
            4: "Taper-Charge",
            5: "Reserved",
            6: "Top-off Timer Active",
            7: "Charge Terminated"
        }.get(chrg, "Unknown")
    except:
        return "Unavailable"

def battery_charge():
    cells = read_cell_voltages()
    total_mv = sum(cells)
    percent = min(max(int((total_mv - 1000) / (12600 - 1000) * 100), 0), 100)
    return percent
