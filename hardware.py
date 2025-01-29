
import st7789 #type:ignore
import tft_config #type:ignore
import vga1_bold_16x32 as font #type:ignore

from machine import Pin
import time


BACKGROUND_COLOR = st7789.WHITE
SOLENOID_PIN = 4

COLORS ={
    "rood": st7789.RED,
    "geel": st7789.YELLOW,
    "groen": st7789.GREEN

}

class Solenoid:
    def __init__(self,pin_adress) -> None:
        self.pin = Pin(pin_adress, mode=Pin.OUT)
    def open(self,time_open = 0.5):
        self.pin.on()
        time.sleep(time_open)
        self.pin.off()

class Display:
    def __init__(self) -> None:
        self.tft = tft_config.config(0)
        self.tft.init()
        self.tft.rotation(1)
        self.tft.fill(BACKGROUND_COLOR)

    def write(self,text):
        self.tft.fill(BACKGROUND_COLOR)
        length = len(text)
        self.tft.text(
            font,
            text,
            self.tft.width() // 2 - length // 2 * font.WIDTH,
            self.tft.height() // 2 - font.HEIGHT,
            BACKGROUND_COLOR,
            st7789.WHITE)
    def clear_display(self):
        self.tft.fill(BACKGROUND_COLOR)
    
    def paint_dot(self,postition,size,color):
        # self.tft.fill(BACKGROUND_COLOR)
        [x,y] = postition
        self.tft.fill_circle(x,y,size,COLORS[color])
        
        

solenoid = Solenoid(SOLENOID_PIN)
display = Display()
if __name__ == "__main__":
    # 
    for i in range(1,5):
        display.paint_dot([i * 64, 240//2], 20, "groen")

# sol = Pin(4, mode=Pin.OUT)

# sol.on()
# time.sleep(0.5)
# sol.off()