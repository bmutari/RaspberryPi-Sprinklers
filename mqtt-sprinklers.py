#!usr/bin/python3

## A simple script to monitor MQTT topics and trigger sprinklers
## Brandon Mutari
## 6/7/2020

import gpiozero
import paho.mqtt.client as mqtt
from datetime import datetime
import logging

logging.basicConfig(filename='sprinkles.log', level=logging.DEBUG)

# setup the pins for each zone
z1 = gpiozero.DigitalOutputDevice(4,active_high=False,initial_value=False)
z2 = gpiozero.DigitalOutputDevice(17,active_high=False,initial_value=False)
z3 = gpiozero.DigitalOutputDevice(18,active_high=False,initial_value=False)
z4 = gpiozero.DigitalOutputDevice(22,active_high=False,initial_value=False)
z5 = gpiozero.DigitalOutputDevice(23,active_high=False,initial_value=False)
z6 = gpiozero.DigitalOutputDevice(24,active_high=False,initial_value=False)
z7 = gpiozero.DigitalOutputDevice(25,active_high=False,initial_value=False)
z8 = gpiozero.DigitalOutputDevice(21,active_high=False,initial_value=False)

zones = {
    'sprinklers/z1':z1,
    'sprinklers/z2':z2,
    'sprinklers/z3':z3,
    'sprinklers/z4':z4,
    'sprinklers/z5':z5,
    'sprinklers/z6':z6,
    'sprinklers/z7':z7,
    'sprinklers/z8':z8,
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sprinklers/z1")
    client.subscribe("sprinklers/z2")
    client.subscribe("sprinklers/z3")
    client.subscribe("sprinklers/z4")
    client.subscribe("sprinklers/z5")
    client.subscribe("sprinklers/z6")
    client.subscribe("sprinklers/z7")
    client.subscribe("sprinklers/z8")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    z = zones[msg.topic]
    if (msg.payload.decode("utf-8") == 'on'):
        logging.info(datetime.now().strftime('%a %m/%d/%Y - %H:%M:%S') + ' turning on: ' + str(msg.topic))    
        z.on()
    if (msg.payload.decode("utf-8") == 'off'):
        logging.info(datetime.now().strftime('%a %m/%d/%Y - %H:%M:%S') + ' turning off: ' + str(msg.topic))
        z.off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.25.83.11", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
