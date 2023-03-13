# boot.py -- run on boot-up

from network import WLAN
import pycom
import time
import config


pycom.rgbled(0x7f7f00) #Sets the sensor LED led to Yellow -- *For configuring*

print("Hello There!")
print("Connecting to WiFi...")

# Connect to wifi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(config.WIFI_SSID, auth=(WLAN.WPA2, config.WIFI_PASS), timeout=1260000)
time.sleep(30.0)

while not wlan.isconnected():	
	print("WiFi not connected, trying again!")	
	wlan.connect(config.WIFI_SSID, auth=(WLAN.WPA2, config.WIFI_PASS), timeout=1260000)
	time.sleep(30.0)

print("WiFi connected succesfully!")
print(wlan.ifconfig())