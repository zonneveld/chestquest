# Import necessary modules
import network
import socket

import time

from machine import Pin, Timer

import st7789 #type:ignore
import tft_config #type:ignore
import vga1_bold_16x32 as font #type:ignore

tft = tft_config.config(0)
sol = Pin(4, mode=Pin.OUT)

HINT_SPEED = 1

# display functions:
def center(text):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT,
        st7789.BLACK,
        st7789.WHITE)

def show_frame(text,color):
    tft.fill(st7789.WHITE)
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT,
        color,
        st7789.WHITE)
    
def show_frame2(text,color,background):
    tft.fill(background)
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT,
        color,
        background)

class FrameData:
    def __init__(self,text,color) -> None:
        self.text = text
        self.color = color

hint_animation = {
    FrameData("blauw",   st7789.RED),
    FrameData("groen",  st7789.YELLOW),
    FrameData("rood",  st7789.BLUE),
    FrameData("blauw",  st7789.GREEN),

    FrameData("geel",  st7789.BLUE),
    FrameData("groen",  st7789.RED),
    FrameData("blauw",  st7789.GREEN),
    FrameData("rood",  st7789.YELLOW)
}



def hint():
    for frame in hint_animation:
        show_frame(frame.text,frame.color)
        time.sleep(HINT_SPEED)
    # pass
  
def wrong():
    for flashcount in range(2):
        show_frame2("FOUT", st7789.RED,st7789.BLACK)
        time.sleep(0.5)
        show_frame2("FOUT", st7789.BLACK,st7789.RED)
        time.sleep(0.5)

# solenoid functions:
def set():
    sol.on()
    print("on")

def release():
    sol.off()
    print("off")

def unlock():
    set()
    time.sleep(0.1)
    release()
    for flashcount in range(2):
        show_frame2("GOED!", st7789.GREEN,st7789.WHITE)
        time.sleep(0.5)
        show_frame2("GOED!", st7789.WHITE,st7789.GREEN)
        time.sleep(0.5)

    # t = Timer(mode=Timer.ONE_SHOT, period=100, callback=release)
    # t.init()
# Wi-Fi credentials
release()
ssid = 'Workshop'
password = 'NovaCollegeWorkshop'

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
# wlan.ifconfig(('192.168.2.110', '255.255.254.0', '10.0.0.2', '8.8.8.8'))
wlan.connect(ssid, password)

# Wait for Wi-Fi connection
connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

# Set up socket and start listening
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

print('Listening on', addr)

tft.init()
tft.rotation(1)
tft.fill(st7789.BLACK)
center(""+str(network_info[0]))




while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print('Request content = %s' % request)

        try:

            action = request.split()[1]
            
            if action == "/unlock":
                unlock()

            if action == "/hint":
                hint()

            if action == "/wrong":
                wrong()

        except IndexError:
            pass
        
        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        file = open("index.html", "r")
        
        content = file.readlines()
        file.close()

        for line in content:
            conn.send(line)
        
        # print(len(content))
        
        # conn.send(content)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')

