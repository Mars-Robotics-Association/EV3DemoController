#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct

from sys import stderr
from sys import stdout

# Declare motors 
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize variables. 
# Assuming sticks are in the middle when starting.
stick_scale_low = 32768
stick_scale_high = -32768
#stick_scale = 255
left_stick_y = (stick_scale_high+stick_scale_low)/2
right_stick_x = (stick_scale_high+stick_scale_low)/2






# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]






# Find the PS3 Gamepad:
# /dev/input/event3 is the usual file handler for the gamepad.
# look at contents of /proc/bus/input/devices if it doesn't work.
# ***** Logitech F710 is event2 *****
infile_path = "/dev/input/event2"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHi'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)







while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    #print("type: "+str(ev_type)+"  code: "+str(code)+"  value: "+str(value))
    if ev_type == 3 and code == 1:
        left_stick_y = value
        #print("Left Stick: "+ str(value))
    if ev_type == 3 and code == 3:
        right_stick_x = value
    
    # Scale stick positions to -100,100
    forward = scale(left_stick_y, (stick_scale_low, stick_scale_high), (100,-100))
    left = scale(right_stick_x, (stick_scale_low, stick_scale_high), (100,-100))
    #left = 0
    #print("FWD: " + str(forward) + "   LEFT: " + str(left), stdout)
    # Set motor voltages. If we're steering left, the left motor
    # must run backwards so it has a -left component
    # It has a forward component for going forward too. 
    left_motor.dc(forward - left)
    right_motor.dc(forward + left)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()