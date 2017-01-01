# Allow flashing of the RPi LED
# Provided the following have been run as root on the command line:
#    echo none > /sys/class/leds/led0/trigger
#    chmod a+w /sys/class/leds/led0/brightness

import os.path
import time

def has_led_control():
    return os.path.isfile('/sys/class/leds/led0/brightness')

def led_on():
    if has_led_control():
        with open('/sys/class/leds/led0/brightness', 'w') as f:
            print('1', file=f)

def led_off():
    if has_led_control():
        with open('/sys/class/leds/led0/brightness', 'w') as f:
            print('0', file=f)

def set_led(b):
    if b:
        led_on()
    else:
        led_off()

def blink_led(sec: int, frequency: float, onTime: float, numBlinks: int):
    offTime = frequency - onTime * (2 * numBlinks - 1)
    iterations = int(float(sec) / float(frequency))
    for i in range(iterations):
        led_off()
        time.sleep(offTime)
        for j in range(numBlinks):
            led_on()
            time.sleep(onTime)
            if j < numBlinks - 1:
                led_off()
                time.sleep(onTime)
    led_off()

# while we're updating status: give a few quick blinks
def blink_led_updating(sec: int):
    blink_led(sec, frequency=0.2, onTime=0.1, numBlinks=1)

# this is called when the internet is down: slow flash
def blink_led_internet_down(sec: int):
    blink_led(sec, frequency=1, onTime=1, numBlinks=1)

# this is called when the router is down: two quick blinks
def blink_led_router_down(sec: int):
    blink_led(sec, frequency=0.5, onTime=0.1, numBlinks=2)

# this is called when the modem is unreachable: three quick blinks
def blink_led_modem_down(sec: int):
    blink_led(sec, frequency=0.5, onTime=0.1, numBlinks=3)

# keep LED on for this long, then turn it back off
def show_led(sec: int):
    time.sleep(0.05)
    led_on()
    time.sleep(sec)
    led_off()
