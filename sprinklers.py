## Simple sprinkler program
## Brandon Mutari 5/1/2017

import RPi.GPIO as GPIO
import time
from datetime import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO pins for zones
Z1 = 4
Z2 = 17
Z3 = 18
Z4 = 22
Z5 = 23
Z6 = 24

# Time to run each zone in minutes (WARNING: the number of zones must equal the number of times)
# **** EDIT HERE TO ADJUST WATERING TIME PER ZONE ****
timeZ1 = 1
timeZ2 = 1
timeZ3 = 1
timeZ4 = 1
timeZ5 = 1
timeZ6 = 1

# Build zone and time arrays
zone = [Z1, Z2, Z3, Z4, Z5, Z6]
timeZ = [timeZ1, timeZ2, timeZ3, timeZ4, timeZ5, timeZ6]

# loop through pins, set mode and state to 'off' (relay is on when input is sunk to GND)
for x in range(len(zone)):
    GPIO.setup(zone[x], GPIO.OUT)
    GPIO.output(zone[x], GPIO.HIGH)

try:
    print datetime.now().strftime('%a %m/%d/%Y')
    # INSERT RAIN TEST HERE
    for x in range(len(zone)):
        print "Zone"+ str(x+1) +":\nstarted  " + datetime.now().strftime('%H:%M:%S')
        GPIO.output(zone[x],GPIO.LOW)
        time.sleep(timeZ[x]*60)
        GPIO.output(zone[x],GPIO.HIGH)
        print "finished " + datetime.now().strftime('%H:%M:%S')
        time.sleep(1)

    GPIO.cleanup()
    print "Watering has finished.\n \n"

# End program cleanly with keyboard
except KeyboardInterrupt:
    print "  Quit"
    # Reset GPIO settings
    GPIO.cleanup()
