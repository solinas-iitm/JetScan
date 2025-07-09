from smbus2 import SMBus
import time
import math

bus = SMBus(1)

ICM_ADDR = 0x68  # or 0x69 depending on AP_AD0

WHO_AM_I     = 0x75
PWR_MGMT0    = 0x4E
GYRO_CONFIG0 = 0x4F
ACCEL_CONFIG0 = 0x50

ACCEL_XOUT_H = 0x1F
GYRO_XOUT_H  = 0x25

def read_word(bus, addr, reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    val = (high << 8) | low
    return val - 65536 if val > 32767 else val
def init_imu():

    device_id = bus.read_byte_data(ICM_ADDR, WHO_AM_I)
    #print("WHO_AM_I: 0x{:02X}".format(device_id))
    if device_id != 0x4E:
        raise Exception("IMU not found or incorrect WHO_AM_I")

    # Initialize IMU
    bus.write_byte_data(ICM_ADDR, PWR_MGMT0, 0x0F)      # Enable accel + gyro (low-noise mode)
    bus.write_byte_data(ICM_ADDR, GYRO_CONFIG0, 0x26)   # ±1000 dps, ODR 1 kHz
    bus.write_byte_data(ICM_ADDR, ACCEL_CONFIG0, 0x26)  # ±8g, ODR 1 kHz

    time.sleep(0.1)

init_imu()

def imu_monitor():
    try:
       while True:
          ax = read_word(bus, ICM_ADDR, ACCEL_XOUT_H)
          ay = read_word(bus, ICM_ADDR, ACCEL_XOUT_H + 2)
          az = read_word(bus, ICM_ADDR, ACCEL_XOUT_H + 4)

          gx = read_word(bus, ICM_ADDR, GYRO_XOUT_H)
          gy = read_word(bus, ICM_ADDR, GYRO_XOUT_H + 2)
          gz = read_word(bus, ICM_ADDR, GYRO_XOUT_H + 4)

          # Convert to g and dps
          ax_g = ax / 4096.0  # For ±8g (4096 LSB/g)
          ay_g = ay / 4096.0
          az_g = az / 4096.0

          gx_dps = gx / 32.8  # For ±1000 dps (32.8 LSB/dps)
          gy_dps = gy / 32.8
          gz_dps = gz / 32.8

          pitch = 180 * math.atan2(ax_g, math.sqrt(ay_g * ay_g + az_g * az_g)) / math.pi
          roll = 180 * math.atan2(ay_g, math.sqrt(ax_g * ax_g + az_g * az_g)) / math.pi
          #print(f"pitch: {pitch:.2f} roll: {roll:.2f}")
          #print(f"Accel (g): X={ax_g:.2f}, Y={ay_g:.2f}, Z={az_g:.2f} | Gyro (dps): X={gx_dps:.2f}, Y={gy_dps:.2f}, Z={gz_dps:.2f}")
          time.sleep(0.2)
          return {
              "pitch": round(pitch, 2),
              "roll": round(roll, 2),
              "accel": [round(ax_g, 2), round(ay_g, 2), round(az_g, 2)],
              "gyro": [round(gx_dps, 2), round(gy_dps, 2), round(gz_dps, 2)]}

    except Exception as e:
        print(f"[IMU] Error: {e}")
#if __name__ == "__main__":
 #   imu_monitor()
