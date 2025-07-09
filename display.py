
from smbus2 import SMBus
import time
import os
from datetime import datetime
from battery_monitor_charging import get_charger_status, battery_charge
from gpio import get_brightness 
#from camera_module import is_recording
from threading import Thread

I2C_ADDR = 0x3D
CMD = 0X00
DAT = 0X40


bus = SMBus(1)
def check_i2c_device(address):
    try:
        bus.write_quick(address)
        return True
    except:
        return False

def write_cmd(cmd):
    bus.write_byte_data(I2C_ADDR, CMD, cmd)

def write_data(cmd):
    bus.write_byte_data(I2C_ADDR, DAT, cmd)

def oled_init():
    for cmd in [
        0xAE,             # Display OFF
        0x20, 0x00,       # Set Memory Addressing Mode: Horizontal
        0xB0,             # Page Start Address
        0xC8,             # COM Output Scan Direction: remapped mode
        0x00,             # Low column address
        0x10,             # High column address
        0x40,             # Start line address
        0x81, 0x7F,       # Contrast
        0xA1,             # Segment remap
        0xA6,             # Normal display (not inverted)
        0xA8, 0x3F,       # Multiplex: 0x3F for 128x64
        0xA4,             # Display RAM content
        0xD3, 0x00,       # Display offset
        0xD5, 0x80,       # Oscillator frequency
        0xD9, 0xF1,       # Pre-charge period
        0xDA, 0x12,       # COM pins hardware config
        0xDB, 0x40,       # VCOMH deselect level
        0x8D, 0x14,       # Enable charge pump
        0xAF              # Display ON
    ]:
        write_cmd(cmd)
    time.sleep(0.1)

def clear_display():
    for page in range(8):  # 8 pages
        write_cmd(0xB0 + page)  # Set page start
        write_cmd(0x00)         # Set lower column
        write_cmd(0x10)         # Set higher column
        for col in range(128):
            write_data(0x00)

def set_cursor(page, column):
    write_cmd(0xB0 + page)
    write_cmd(0x00 + (column & 0x0F))
    write_cmd(0x10 + ((column >> 4) & 0x0F))

# Extended font set for numbers and symbols
font = {
    'J': [0x41, 0x41, 0x3F, 0x01, 0x01],
    'e': [0x38, 0x54, 0x54, 0x54, 0x18],
    't': [0x04, 0x04, 0x3F, 0x44, 0x44],
    's': [0x48, 0x54, 0x54, 0x54, 0x24],
    'c': [0x38, 0x44, 0x44, 0x44, 0x28],
    'a': [0x20, 0x54, 0x54, 0x54, 0x78],
    'n': [0x7C, 0x08, 0x04, 0x04, 0x78],
    'A': [0x7C, 0x12, 0x11, 0x12, 0x7C],
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7F, 0x41, 0x41, 0x41, 0x3E],
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7F, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3E, 0x41, 0x49, 0x49, 0x7A],
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F],
    'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
    'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
    'W': [0x3F, 0x40, 0x30, 0x40, 0x3F],
    'h': [0x7F, 0x08, 0x04, 0x04, 0x78],
    'i': [0x00, 0x44, 0x7D, 0x40, 0x00],
    'g': [0x98, 0xA4, 0xA4, 0xA4, 0x7C],
    'r': [0x7C, 0x08, 0x04, 0x04, 0x08],
    'd': [0x38, 0x44, 0x44, 0x44, 0x7F],
    'o': [0x38, 0x44, 0x44, 0x44, 0x38],
    'l': [0x00, 0x41, 0x7F, 0x40, 0x00],
    'u': [0x3C, 0x40, 0x40, 0x40, 0x3C],
    'm': [0x7C, 0x04, 0x18, 0x04, 0x78],
    'p': [0xFC, 0x24, 0x24, 0x24, 0x18],
    'y': [0x9C, 0xA0, 0xA0, 0xA0, 0x7C],
    'f': [0x08, 0x7F, 0x09, 0x01, 0x02],
    'b': [0x7F, 0x48, 0x44, 0x44, 0x38],
    'k': [0x7F, 0x10, 0x28, 0x44, 0x00],
    'v': [0x1C, 0x20, 0x40, 0x20, 0x1C],
    'w': [0x3C, 0x40, 0x30, 0x40, 0x3C],
    'x': [0x44, 0x28, 0x10, 0x28, 0x44],
    'z': [0x44, 0x64, 0x54, 0x4C, 0x44],
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
    '2': [0x42, 0x61, 0x51, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '%': [0x46, 0x26, 0x10, 0x08, 0x64],
    '°': [0x02, 0x05, 0x02, 0x00, 0x00],
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '/': [0x20, 0x10, 0x08, 0x04, 0x02],
    '(': [0x00, 0x1C, 0x22, 0x41, 0x00],
    ')': [0x00, 0x41, 0x22, 0x1C, 0x00],
    '!': [0x00, 0x00, 0x5F, 0x00, 0x00],
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
}

def display_text(text, page=0, column=0):
    set_cursor(page, column)
    for char in text:
        if char in font:
            for byte in font[char]:
                write_data(byte)
            write_data(0x00)  # spacing
        else:
            for _ in range(6):
                write_data(0x00)  # unknown char = blank

def display_small_text(text, page=0, column=0):
    """Display text with smaller font (4 pixels wide)"""
    set_cursor(page, column)
    for char in text:
        if char in font:
            # Use only first 4 bytes of each character for compact display
            for i in range(4):
                write_data(font[char][i] if i < len(font[char]) else 0x00)
            write_data(0x00)  # spacing
        else:
            for _ in range(5):
                write_data(0x00)

def draw_line(page, start_col, end_col, pattern=0xFF):
    """Draw horizontal line"""
    set_cursor(page, start_col)
    for col in range(start_col, end_col + 1):
        write_data(pattern)

def draw_battery_icon(page, column, percentage):
    """Draw battery icon with fill level"""
    set_cursor(page, column)
    # Battery outline
    write_data(0x7E)  # left side
    write_data(0x42)  # empty
    write_data(0x42)  # empty
    write_data(0x42)  # empty
    write_data(0x42)  # empty
    write_data(0x7E)  # right side
    write_data(0x3C)  # battery tip

    # Fill battery based on percentage
    fill_level = int((percentage / 100) * 4)
    set_cursor(page, column + 1)
    for i in range(4):
        if i < fill_level:
            write_data(0x7E)  # filled
        else:
            write_data(0x42)  # empty

def draw_page_dots(current_page, total_pages):
    """Draw page indicator dots at bottom"""
    start_col = 60 - (total_pages * 4)
    set_cursor(7, start_col)
    for i in range(total_pages):
        if i == current_page:
            write_data(0x18)  # filled dot
            write_data(0x18)
        else:
            write_data(0x10)  # empty dot
            write_data(0x10)
        write_data(0x00)  # spacing

def get_free_space_mb(path="/"):
    """Get free space in MB"""
    try:
        stat = os.statvfs(path)
        return (stat.f_bavail * stat.f_frsize) / 1024 / 1024
    except:
        return 0


class JetscanDisplay:
    def __init__(self):
        self.current_page = 0
        self.total_pages = 3
        self.page_duration = 3  # seconds per page
        self.last_page_change = time.time()
        oled_init()

    def draw_header(self):
        #Draw Jetscan header
        display_text("JETSCAN", page=0, column=35)
        draw_line(page=1, start_col=0, end_col=127, pattern=0x02)

    def draw_page_1(self):
        #Power & Battery Page
        clear_display()
        self.draw_header()

        # Get battery info
        try:
            #cells = read_cell_voltages()
            #total_mv = sum(cells)
            percent = battery_charge() #min(max(int((total_mv - 10000) / (12600 - 10000) * 100), 0), 100)
            charger_status = get_charger_status()
            
            # Display battery percentage
            display_text(f"Battery", page=2, column=5)

            # Display battery percentage
            display_text(f"{percent}%", page=3, column=5)

            # LED brightness
            display_text(f"LED", page=2, column=67)
            display_text(f"{get_brightness()} %", page=3, column=67)

            draw_line(page=4, start_col=0, end_col=127, pattern=0x01)
            display_text(f"{charger_status}", page=5, column=10)
            draw_battery_icon(page=5, column= 100, percentage= percent)
            
            # Display charging status
            """if charger_status in ["Charging", "Fast-Charge", "Taper-Charge"]:
                display_text("Charging", page=5, column=10)
                draw_battery_icon(page=5, column= 100, percentage= percent)
            else:
                display_text("DEVICE ON", page=5, column=25)"""
        except Exception as e:
            display_text("Battery: Error", page=2, column=5)

        # Page indicators
        draw_page_dots(self.current_page, self.total_pages)

    def draw_page_2(self):
        #Environmental & System Page
        clear_display()
        self.draw_header()

        # Pressure
        #pressure = get_pressure()
        pressure = 1;
        display_text(f"Pressure", page=2, column=3)
        display_text(f"{pressure} bar", page=3, column=3)
        # Temperature
        #temp = get_temperature()
        temp = 23
        display_text(f"Temperature", page=2, column=56)
        display_text(f"{temp}°C", page=3, column=56)

        draw_line(page=4, start_col=0, end_col=127, pattern=0x01)

        #date
        current_date = datetime.now().strftime("%d:%m:%Y")
        display_text(f"{current_date}", page=5, column=25)

	# Time
        current_time = datetime.now().strftime("%H:%M:%S")
        display_text(f"{current_time}", page=6, column=30)

        # Page indicators
        draw_page_dots(self.current_page, self.total_pages)

    def draw_page_3(self):
        #Storage & System Info Page
        clear_display()
        self.draw_header()

        # SD Card space
        free_space = get_free_space_mb()
        display_text(f"SD", page=2, column=5)
        display_text(f"{free_space/1024:.1f}GB", page=3, column=5)
        draw_line(page=4, start_col=0, end_col=127, pattern=0x01)


        # Uptime
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.read().split()[0])
                uptime_hours = int(uptime_seconds / 3600)
            display_text(f"Up: {uptime_hours}h", page=5, column=5)
        except:
            display_text("Up: N/A", page=5, column=5)
        
        # Show recording status
        status = get_charger_status()
        if status in  ["Pre-Charge", "Fast-Charge", "Taper-Charge"]:
           display_text(f"REC OFF", page=6, column=25)
        else:
           display_text(f"REC ON", page=6, column=25)

        # Page indicators
        draw_page_dots(self.current_page, self.total_pages)

    def update_display(self):
        #Update the display with current page
        if self.current_page == 0:
            self.draw_page_1()
        elif self.current_page == 1:
            self.draw_page_2()
        elif self.current_page == 2:
            self.draw_page_3()

    def next_page(self):
        #Go to next page
        self.current_page = (self.current_page + 1) % self.total_pages
        self.last_page_change = time.time()

    def run(self):

        clear_display()
        display_text("Checking devices", page=2, column=10)
        time.sleep(1)

        battery_ok = check_i2c_device(0x08)
        charger_ok = check_i2c_device(0x6B)
        imu_ok = check_i2c_device(0x68)

        if battery_ok and charger_ok and imu_ok:
            display_text("All devices OK", page=3, column=10)
        else:
            display_text("Device check FAIL", page=3, column=10)
            if not battery_ok:
                display_text("Battery Missing", page=4, column=10)
            if not charger_ok:
                display_text("Charger Missing", page=5, column=10)
            if not imu_ok:
                display_text("IMU Missing", page=6, column=10)

            time.sleep(3)
            return
        time.sleep(2)
        clear_display()
        display_text("Device Ready", page=3, column=25)
        time.sleep(2)
        clear_display()

        #Main display loop
        print("Starting Jetscan Display System...")
        try:
            while True:
                self.update_display()

                # Check if it's time to change page
                if time.time() - self.last_page_change >= self.page_duration:
                    self.next_page()

                time.sleep(10)  # Update every 10s

                low_volt = battery_charge()
                if low_volt <= 75 :  #limit to 9.5V to shutdown
                   clear_display()
                   display_text("Low Battery....",page = 2, column=15)
                   time.sleep(3)
                   display_text("Shutting Down....", page=3, column=15)
                   os.system("sudo shutdown now")

        except KeyboardInterrupt:
            print("\nStopping display...")
            clear_display()
            display_text("Shutting Down...", page=3, column=15)
            time.sleep(2)
            clear_display()

def display_thread():
    #Function to run display in separate thread
    display = JetscanDisplay()
    display.run()
"""
if __name__ == "__main__":
    # Run display system
    display = JetscanDisplay()
    display.run()
"""

