
#!/usr/bin/env python3
"""
Smart Camera Recording Controller for Raspberry Pi
Controls recording based on BMS charging state, battery voltage, and storage space
"""

import os
import time
import subprocess
import logging
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from battery_monitor_charging import  read_cell_voltages, get_charger_status
import threading
import signal
import sys

# Configuration
BATTERY_MIN_VOLTAGE = 9.5  # Minimum battery voltage
MIN_STORAGE_GB = 1.0  # Minimum storage space in GB
VIDEO_DIR = "/home/raspberry/Jetscan/videos"
LOG_FILE = "/home/raspberry/Jetscan/camera_log.txt"
CHECK_INTERVAL = 10  # Check conditions every 10 seconds

class CameraController:
    def __init__(self):
        self.camera = None
        self.encoder = None
        self.output = None
        self.recording = False
        self.running = True
        self.current_file = None

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Create video directory
        os.makedirs(VIDEO_DIR, exist_ok=True)

        # Initialize camera
        self.init_camera()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def init_camera(self):
        """Initialize the camera"""
        try:
            self.camera = Picamera2()
            # Configure camera for video recording
            video_config = self.camera.create_video_configuration(
                main={"size": (1920, 1080)},
                lores={"size": (640, 480)},
                display="lores"
            )
            self.camera.configure(video_config)
            self.camera.start()
            self.logger.info("Camera initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize camera: {e}")
            raise

    def get_battery_voltage(self):
        """
        Get battery voltage from BMS
        
        """
        try:
            cells = read_cell_voltages()
            voltage = sum(cells) / 1000
            return voltage

        except Exception as e:
            self.logger.error(f"Error reading battery voltage: {e}")
            return 12.0  # Default safe value


    def is_charging(self):
        """
        Check if BMS is in charging state
        
        """
        try:
            charge_state = get_charger_status()
            if charge_state in["Pre-Charge", "Fast-Charge", "Taper-Charge"] :
                return True
            return None

        except Exception as e:
            self.logger.error(f"Error checking charging state: {e}")
            return False

    def get_storage_space_gb(self):
        """Get available storage space in GB"""
        try:
            statvfs = os.statvfs(VIDEO_DIR)
            # Available space in bytes
            available_bytes = statvfs.f_bavail * statvfs.f_frsize
            # Convert to GB
            available_gb = available_bytes / (1024 ** 3)
            return available_gb
        except Exception as e:
            self.logger.error(f"Error checking storage space: {e}")
            return 0.0

    def start_recording(self):
        """Start video recording"""
        if self.recording:
            return

        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_file = os.path.join(VIDEO_DIR, f"recording_{timestamp}.h264")

            # Setup encoder and output
            self.encoder = H264Encoder(bitrate=10000000)
            self.output = FileOutput(self.current_file)

            # Start recording
            self.camera.start_recording(self.encoder, self.output)
            self.recording = True
            self.logger.info(f"Started recording: {self.current_file}")

        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            self.recording = False

    def stop_recording(self):
        """Stop video recording"""
        if not self.recording:
            return

        try:
            self.camera.stop_recording()
            self.recording = False
            self.logger.info(f"Stopped recording: {self.current_file}")
            self.current_file = None

        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")

    def check_conditions(self):
        """Check all conditions and control recording"""
        try:
            # Get current status
            voltage = self.get_battery_voltage()
            charging = self.is_charging()
            storage_gb = self.get_storage_space_gb()

            self.logger.info(f"Status - Voltage: {voltage:.2f}V, Charging: {charging}, Storage: {storage_gb:.2f}GB")

            # Check stop conditions
            should_stop = (
                    voltage < BATTERY_MIN_VOLTAGE or
                    storage_gb < MIN_STORAGE_GB or
                    charging
            )

            if should_stop and self.recording:
                reason = []
                if voltage < BATTERY_MIN_VOLTAGE:
                    reason.append(f"Low battery ({voltage:.2f}V)")
                if storage_gb < MIN_STORAGE_GB:
                    reason.append(f"Low storage ({storage_gb:.2f}GB)")
                if charging:
                    reason.append("Charging detected")

                self.logger.info(f"Stopping recording: {', '.join(reason)}")
                self.stop_recording()

            elif not should_stop and not self.recording:
                self.logger.info("Starting recording: All conditions met")
                self.start_recording()

        except Exception as e:
            self.logger.error(f"Error in check_conditions: {e}")

    def run(self):
        """Main control loop"""
        self.logger.info("Camera controller started")

        # Initial check
        self.check_conditions()

        try:
            while self.running:
                time.sleep(CHECK_INTERVAL)
                self.check_conditions()

        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.logger.info("Cleaning up...")

        if self.recording:
            self.stop_recording()

        if self.camera:
            self.camera.stop()
            self.camera.close()

        self.logger.info("Camera controller stopped")

    def signal_handler(self, signum, frame):
        #Handle system signals
        self.logger.info(f"Received signal {signum}")
        self.running = False

def is_recording():
    controller = CameraController()
    return controller.is_charging()

def camera_thread():
    controller = CameraController()
    controller.run()
    

"""if __name__ == "__main__":
   # camera_thread()
    try:
        controller = CameraController()
        controller.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)"""




