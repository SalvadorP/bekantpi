# bekantpi
Project to add a raspberry pi zero to a Bekant desk.

## Files
### lights.py
Script to control the two lights the desk has, sends commands through MQTT to the Mosquitto broker and the Tasmotas power toggle the lights.
### bmp280.py
Adafruit script to control the bmp280 sensor for temp and pressure.
### si7021.py
Script to control the si7021 sensor, for temp and humidity
### adafruit_si7021.py
Adafruit script to control the temp and humidity, not working properly, investigate.
### vl53l0x.py
Script to control the vl53l0x ToF sensor, for distance.
