#!/usr/bin/env python3

## A simple script to monitor MQTT topics and trigger sprinklers
## Brandon Mutari
## 6/7/2020

import gpiozero
import paho.mqtt.client as mqtt

# setup the pins for each zone
z1 = gpiozero.DigitalOutputDevice(4,active_high=False,initial_value=False)
z2 = gpiozero.DigitalOutputDevice(17,active_high=False,initial_value=False)
z3 = gpiozero.DigitalOutputDevice(18,active_high=False,initial_value=False)
z4 = gpiozero.DigitalOutputDevice(22,active_high=False,initial_value=False)
z5 = gpiozero.DigitalOutputDevice(23,active_high=False,initial_value=False)
z6 = gpiozero.DigitalOutputDevice(24,active_high=False,initial_value=False)
z7 = gpiozero.DigitalOutputDevice(25,active_high=False,initial_value=False)
z8 = gpiozero.DigitalOutputDevice(27,active_high=False,initial_value=False)

zones = [0, z1, z2, z3, z4, z5, z6, z7, z8]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sprinklers/control")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    zone,ctrl = msg.payload.decode().split(',')
    if (ctrl == "on"):
        print("turning on zone " + zone)
        zones[int(zone)].on()
    if (ctrl == "off"):
        print("turning off zone " + zone)
        zones[int(zone)].off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.25.83.11", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
