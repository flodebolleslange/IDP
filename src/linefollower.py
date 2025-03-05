from interface.interface import *
from interface.linesensors import *

def linefollower(Tank):
    
    # black = 0, white = 1

    while True:
        sll = sensor.ll #leftmost sensor
        sl = sensor.l #centreleft sensor
        sr = sensor.r #centreright sensor
        srr = sensor.rr #rightmost sensor

        while True:
            if srr == 0 and sll == 0:
                if sl == 0 and sr == 0:
                    motor.r = 1 #right motor
                    motor.l = 1 #left motor
                    break
            if sr == 1:
                motor.r = 0.5 #half-power/half-speed
                motor.l = 1
                break
            if sl == 1:
                motor.l = 0.5
                motor.r = 1

            if sll == 1 or srr == 1:
                
                while True:
                    sll = sensor.ll
                    sl = sensor.l
                    sr = sensor.r
                    srr = sensor.rr

                    if sll == 0 and srr == 0:
                        break

                    while True:
                        if sll == 1 and sl == 1:
                            #90 degree left turn
                            while srr != 0 and sll != 0:
                                motor.l = -1 #rotate backwards
                                motor.r = 1
                            break

                        if srr == 1 and sr == 1:
                            #90 degree right turn
                            while srr != 0 and sll != 0:
                                motor.r = -1
                                motor.l = 1
                            break

    
