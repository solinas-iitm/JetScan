import RPi.GPIO as GPIO

LED_PIN = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 1000)
current_brightness = 0
pwm.start(current_brightness)

def get_brightness():
    global current_brightness
    return current_brightness

def set_led_brightness(brightness):
    global current_brightness

    brightness = max(0, min(brightness, 100))
    if brightness > 40:
        brightness = 40
        pwm.ChangeDutyCycle(brightness)
    if brightness == 0:
        pwm.ChangeDutyCycle(0)
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
        pwm.ChangeDutyCycle(brightness)
	
    current_brightness = brightness




