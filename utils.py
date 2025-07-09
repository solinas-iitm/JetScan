import time

def setup_countdown(seconds=20):
    print("Setup phase starting...")
    for i in range(seconds, 0, -1):
        print(f"Starting in {i}s", end='\r')
        time.sleep(1)
    print("Setup complete.\n")
