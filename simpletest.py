# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
from adxl345 import ADXL345
from _ast import Or
adxl345 = ADXL345()
import Adafruit_PCA9685

def check_position():
    axes = adxl345.getAxes(True)
    #print "ADXL345 on address 0x%x:" % (adxl345.address)
    print "   x = %.3fG" % ( axes['x'] )
    print "   y = %.3fG" % ( axes['y'] )
    print "   z = %.3fG" % ( axes['z'] )
    position = [axes['x'],axes['y'],axes['z']]
    return position


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo = 100  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
old_servo = 100

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    servo = check_position()
    servo = int(abs(servo[0])*400)
    print(servo)
    #print("############################")
    #print("                            ")
    if old_servo+50 < servo or old_servo-50 > servo :
        #pwm.set_pwm(0, 0, servo)
        print(old_servo)
        #print("Set servo")
        old_servo = servo
    time.sleep(0.3)
    #pwm.set_pwm(0, 0, servo_max)
    #time.sleep(0.5)