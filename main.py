
from threading import Thread
import time
from camera_module import camera_thread
from web_ui import start_web_server
from utils import setup_countdown
from imu_icm40627 import imu_monitor
from display import display_thread
if __name__ == "__main__":
#    setup_countdown(20)

    # Start camera thread
#    cam_thread = Thread(target=camera_thread)
 #   cam_thread.start()
      # start imu thrread
    #imu_thread = Thread(target=imu_monitor)
    #imu_thread.start()
    #display thread
    display_th = Thread(target=display_thread)
    display_th.start()
    # Start web server
    web_thread = Thread(target=start_web_server)
    web_thread.start()
    camera_thread()

