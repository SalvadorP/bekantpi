import math
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA
import busio
import adafruit_ssd1306
import smbus
import adafruit_vl53l0x
import board
import digitalio

# Define OLED Sizes.
WIDTH = 128
HEIGHT = 64  # Change to 32 if needed

i2c = busio.I2C(SCL, SDA)
i2cvl = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2cvl)
disp = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
disp.fill(0)
disp.show()
i2c = busio.I2C(SCL, SDA)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()

# Instantiate the bus for the sh7021
bus = smbus.SMBus(1)

# Display image. Clear screen.
disp.image(image)
disp.show()

# Load default font.
font = ImageFont.load_default()

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 5

while True:
    # Measure temp and humidity
    # SI7021 address, 0x40(64)
    # Read data, 2 bytes, Humidity MSB first
    rh = bus.read_i2c_block_data(0x40, 0xE5, 2)
    #what really happens here is that master sends a 0xE5 command (measure RH, hold master mode) and read 2 bytes back
    #if you read 3 bytes the last one is the CRC!
#    time.sleep(0.1)
    # Convert the data
    humidity = ((rh[0] * 256 + rh[1]) * 125 / 65536.0) - 6


    # SI7021 address, 0x40(64)
    # Read data , 2 bytes, Temperature MSB first
    temp = bus.read_i2c_block_data(0x40, 0xE3,2)
    #what really happens here is that master sends a 0xE3 command (measure temperature, hold master mode) and read 2 bytes back
    #if you read 3 bytes the last one is the CRC!

    # Convert the data
    temperature = ((temp[0] * 256 + temp[1]) * 175.72 / 65536.0) - 46.85

    # Convert to str the float.
    temperature = "Temp: " + format(temperature, '.2f') + " C"
    humidity = "Humd: " + format(humidity, '.2f') + " %"

    # Measure distance
    # vl53.measurement_timing_budget = 200000
    distance = "Dist: " + format(vl53.range, '.2f') + " mm"

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Retrieve the system data, like hostname, ip, cpu load and mem.
    cmd_hostname = "hostname"
    cmd_ip = "hostname -I | cut -d' ' -f1"
    cmd_cpu_temp = "cat /sys/class/thermal/thermal_zone0/temp"
    cpu_temp = subprocess.check_output(cmd_cpu_temp, shell=True).decode("utf-8")
    cpu_temp = "T:" + cpu_temp[0:2]
    hostname = subprocess.check_output(cmd_hostname, shell=True).decode("utf-8")
    ip = subprocess.check_output(cmd_ip, shell=True).decode("utf-8")
    cmd_load = "top -bn1 | grep load | awk '{printf \"L:%.2f\", $(NF-2)}'"
    cpu_load = subprocess.check_output(cmd_load, shell=True).decode("utf-8")
    cmd_mem = "free -m | awk 'NR==2{printf \"M:%.0f%%\", $3*100/$2}'"
    sys_mem = subprocess.check_output(cmd_mem, shell=True).decode("utf-8")


    # Write four lines of text.
    draw.text((x, top + 5),  hostname, font=font, fill=255)
    draw.text((x + 52, top + 5),  ip, font=font, fill=255)
    draw.text((x, top + 15), cpu_load, font=font, fill=255)
    draw.text((x + 50, top + 15), cpu_temp, font=font, fill=255)
    draw.text((x + 85, top + 15), sys_mem, font=font, fill=255)
    draw.text((x, top + 30),  temperature, font=font, fill=255)
    draw.text((x, top + 42), humidity, font=font, fill=255)
    draw.text((x, top + 53), distance, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)
