import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish

from gpiozero import Button
from signal import pause

#mqttBroker = "192.168.2.123"

#client = mqtt.Client("house/desk/right-light")
#client.username_pw_set("mosquitto", "password")
#client.connect(mqttBroker)

def toggle_right_light():
    #client.publish("cmnd/Power", "toggle")
    publish.single("house/desk/right-light/cmnd/Power", "toggle", hostname="192.168.2.123",port=1883,auth={'username':"mosquitto", 'password':"password"})
    print("RIGHT LIGHT TOGGLED")

def toggle_left_light():
    publish.single("house/desk/left-light/cmnd/Power", "toggle", hostname="192.168.2.123",port=1883,auth={'username':"mosquitto", 'password':"password"})
    print("LEFT LIGHT TOGGLED")

def stop():
    print("STOPPED")

leftLightBtn = Button(23)
rightLightBtn = Button(24)

leftLightBtn.when_pressed = toggle_left_light
rightLightBtn.when_pressed = toggle_right_light


pause()
