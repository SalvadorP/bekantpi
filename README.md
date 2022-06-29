# bekantpi
Project to add a raspberry pi zero to a Bekant desk.

## Configuration to run script on each reboot
sudo crontab -e
Add the line.
@reboot sudo python3 /route/to/script

Save and reboot to test if it's working.


## Change i2c core to run at 1Mhz or 1000Khz.
### Do it editing the config.txt
sudo nano /boot/config.txt
dtparam=i2c_baudrate=1000000

### Or via dietpi-config if running on a dietpi distro.
In case of a dietpi put 1000Khz on i2c settings.

## Python libraries to install via pip
pip3 install adafruit-circuitpython-ssd1306
pip3 install adafruit-circuitpython-si7021
 - pip3 install adafruit-circuitpython-bme280
 - pip3 install adafruit-circuitpython-bmp280
 - pip3 install adafruit-circuitpython-ahtx0
pip3 install pyowm

## Libraries to install via apt 
sudo apt install i2c-tools python3-pil python3-numpy python3-gpiozero mosquitto-clients

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
### ssd1306.py
Adafruit script to control the monochromatic OLED of 128x64 lines.

