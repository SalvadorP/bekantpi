
# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

import smbus
import adafruit_vl53l0x
import time
import board
import digitalio
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 3

# Load default font.
font = ImageFont.load_default()

bus = smbus.SMBus(1)
while True:

    # Use for I2C.
    i2c = board.I2C()
    i2cvl = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2cvl)
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,
        fill=0,
    )


    # SI7021 address, 0x40(64)
    # Read data, 2 bytes, Humidity MSB first
    rh = bus.read_i2c_block_data(0x40, 0xE5, 2)
    #what really happens here is that master sends a 0xE5 command (measure RH, hold master mode) and read 2 bytes back
    #if you read 3 bytes the last one is the CRC!
    time.sleep(0.1)
    # Convert the data
    humidity = ((rh[0] * 256 + rh[1]) * 125 / 65536.0) - 6


    # SI7021 address, 0x40(64)
    # Read data , 2 bytes, Temperature MSB first
    temp = bus.read_i2c_block_data(0x40, 0xE3,2)
    #what really happens here is that master sends a 0xE3 command (measure temperature, hold master mode) and read 2 bytes back
    #if you read 3 bytes the last one is the CRC!

    time.sleep(0.1)

    # Convert the data
    cTemp = ((temp[0] * 256 + temp[1]) * 175.72 / 65536.0) - 46.85

    # Convert to str the float.
    cTemp = format(cTemp, '.2f') + " C"
    humidity = format(humidity, '.2f') + " %"
    
    # Measure distance
    vl53.measurement_timing_budget = 200000
    distance = format(vl53.range, '.2f') + " mm"

    # Draw Some Text
    text = cTemp
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, 15),
        cTemp,
        font=font,
        fill=255,
    )
    draw.text(
        (oled.width // 2 - font_width // 2, 25),
        humidity,
        font=font,
        fill=255,
    )
    draw.text(
        (oled.width // 2 - font_width // 2, 35),
        distance,
        font=font,
        fill=255,
    )

    # Display image
    oled.image(image)
    oled.show()

    # print ("Humidity %%RH: %.2f%%" %humidity)
    print("Humidity: " + humidity)
    print("Temperature: " + cTemp)
    print("Distance: " + distance)
    # print ("Temperature: %.2f??C" %cTemp)

    time.sleep(1)
