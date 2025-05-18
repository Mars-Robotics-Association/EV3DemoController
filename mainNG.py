#!/usr/bin/env python3


import evdev
import ev3dev2.auto as ev3
import ev3dev2.motor
import ev3dev2
from sys import stderr
#import os.system

    # Type: 1
    #   Codes:
    #       311 right bumper
    #       313 right trigger
    #       310 left bumper
    #       312 left trigger
    #   https://antonsmindstorms.com/2019/04/24/how-to-connec-a-ps3-sixaxis-gamepad-to-an-ev3-brick/

    #   Logitech F710 codes:
    #       311 right bumper
    #       Stick: 5 right trigger
    #       310 left bumper
    #       Stick: 2 left trigger
    #       3 right stick x
    #       4 right stick y
    #       0 left stick x
    #       1 left stick y

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'Logitech Gamepad F710':
        gamepad = evdev.InputDevice(device.fn)


for event in gamepad.read_loop():
    if event.type == 1:
        if event.code == 311:
            if event.value == 1:
                ev3.LargeMotor(ev3.OUTPUT_B).on(100)
            else:
                ev3.LargeMotor(ev3.OUTPUT_B).on(0)


