# Import necessary modules
import network
import socket
import time
import random
from machine import Pin

import st7789
import tft_config
import vga1_16x16 as font

tft = tft_config.config(0)

def center(text):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        st7789.RED)

# Create an LED object on pin 'LED'
led = Pin('LED', Pin.OUT)

# Wi-Fi credentials
ssid = 'ICT21x'
password = 'RaspBerryPi'
tft.init()
tft.rotation(1)
tft.fill(st7789.RED)
center("hallo kaas!")
# HTML template for the webpage


# Connect to WLAN
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
# wlan.config(hostname="chestquest")  
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

# Initialize variables
state = "OFF"
random_value = 0
file = open("index.html", "r")
content = file.read()
file.close()
# Main loop to listen for connections
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print('Request content = %s' % request)

        try:
            request = request.split()[1]
            request = request.split('?')[1]
            request = request.split('=')[1]
            tft.fill(st7789.RED)
            center(request)
            
            print('Request:', request)
        except IndexError:
            pass
        
        # Process the request and update variables
        # Generate HTML response
        #response = webpage(random_value, state)  

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(content)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')

