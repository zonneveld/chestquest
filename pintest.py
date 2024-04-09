
from machine import Pin, Timer

import time
sol = Pin(4, mode=Pin.OUT) # 3.3V on output -> the led will be on



def set():
    # sol.on()
    print("on")

def release(timer):
    # sol.off()
    print("off")

def unlock():
    set()
    t = Timer(mode=Timer.ONE_SHOT, period=1000, callback=release)
    t.init()
    

unlock()
# time.sleep(5)