from config import *

SIM_OUT = True
SIM_IN = False

if SIM_OUT:
    from interface.base_output_sim import *
else:
    from interface.base_output import *
if SIM_IN:
    from interface.base_input_sim import *
    start_input_sim_monitor()
else:
    from interface.base_input import *
from math import cos, sin, pi


class Tank:
    def __init__(self, m0, m1, axel_length):
        self.m0 = m0
        self.m1 = m1
        self.axel_rad = axel_length * 0.5
    def default(axel_length, vel_scale=1.0):
        return Tank(Motor(0, vel_scale), Motor(1, vel_scale), axel_length)
    def drive(self, v_f, v_r=0.0):
        self.run_raw(*self.get_motor_speeds(v_f, v_r))
    def stop(self):
        self.m0.off()
        self.m1.off()
    def get_motor_speeds(self, v_f, v_r=0.0):
        diff_vel = v_r * self.axel_rad
        v0, v1 = v_f + diff_vel, v_f - diff_vel
        limit = max(abs(v0), abs(v1))
        if limit > 1.0:
            v0 /= limit
            v1 /= limit
        return (v0, v1)
    def run_raw(self, v0, v1):
        self.m0.run(v0)
        self.m1.run(v1)
    

class TrackedTank:
    def __init__(self, m0, m1, axel_length, wheel_diam):
        self.inner = Tank(m0, m1, axel_length)
        self.pos = [0,0,0,0]
        self.motion = [0, 0]
        self.wheel_circ = wheel_diam * pi
    def default(axel_length, wheel_diam, vel_scale=1.0):
        return TrackedTank(Motor(0, vel_scale), Motor(1, vel_scale), axel_length, wheel_diam)
    def drive(self, v_f, *args):
        if len(args) == 0:
            v_r, t = 0, 0
        elif len(args) == 1:
            v_r, t = 0, args[0]
        else:
            v_r, t = args[0], args[1]
        self.tick(t)
        v0, v1 = self.inner.get_motor_speeds(v_f, v_r)
        cal_v0 = 0.0 if v0 < MOTOR_CAL_T else MOTOR_CAL_M * v0 + MOTOR_CAL_C
        cal_v1 = 0.0 if v1 < MOTOR_CAL_T else MOTOR_CAL_M * v1 + MOTOR_CAL_C
        cal_v_f, cal_v_r = 0.5 * (cal_v0 + cal_v1), 0.5 * (cal_v0 - cal_v1) / self.inner.axel_rad
        self.motion = [cal_v_f, cal_v_r]
        self.inner.drive(v_f, v_r)
    def stop(self):
        self.inner.stop()
    def tick(self, time):
        radial = (self.motion[1] * time * self.wheel_circ) % pi
        if abs(self.motion[1]) < 1e-3:
            dist = self.motion[0] * self.wheel_circ * time
            theta = self.pos[2] + (0.5 * radial)
            dx, dy = dist * cos(theta), dist * sin(theta)
        else:
            motion_rad = self.motion[0] / self.motion[1]
            theta = self.pos[2] + radial
            dx, dy = motion_rad * (sin(theta) - sin(self.pos[2])), motion_rad * (cos(self.pos[2]) - cos(theta))
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += radial
        self.pos[3] += time
        return self.pos
    def last_pos(self):
        return self.pos
