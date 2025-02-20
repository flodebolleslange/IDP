from machine import Pin, PWM
from math import cos, sin, pi


class Motor:
	def __init__(self, m_id, vel_scale=1.0):
		self.dir_pin = Pin(7 + 2*m_id, Pin.OUT)
		self.pwm_pin = PWM(Pin(6 + 2*m_id))
		self.pwm_pin.freq(1000)
		self.pwm_pin.duty_u16(0)
		self.vel_scale = vel_scale
	def off(self):
		self.pwm_pin.duty_u16(0)
	def run(self, velocity):
		if velocity > 0:
			self.dir_pin.value(0)
		else:
			self.dir_pin.value(1)
			velocity += 1
		self.pwm_pin.duty_u16(int(65535*velocity*self.vel_scale))

class Tank:
	def __init__(self, m1, m2, axel_length):
		self.m1 = m1
		self.m2 = m2
		self.axel_rad = axel_length
	def default(axel_length, vel_scale=1.0):
		return Tank(Motor(0, vel_scale), Motor(1, vel_scale), axel_length)
	def drive(self, v_f, v_r=0.0):
		self.run_raw(*self.get_motor_speeds(v_f, v_r))
	def get_motor_speeds(self, v_f, v_r=0.0):
		diff_vel = v_r * axel_length
		v1, v2 = v_f + diff_vel, v_f - diff_vel
		limit = max(abs(v1), abs(v2))
		if limit > 1.0:
			v1 /= limit
			v2 /= limit
		return (v1, v2)
	def run_raw(self, v1, v2):
		self.m1.run(v1)
		self.m2.run(v2)

class TrackedTank:
	def __init__(self, m1, m2, axel_length, wheel_diam):
		self.inner = Tank(m1, m2, axel_length)
		self.pos = [0,0,0,0]
		self.motion = [0, 0]
		self.wheel_circ = wheel_diam * 2 * pi
	def default(axel_length, wheel_diam, vel_scale=1.0):
		self.inner = Tank::default(axel_length, vel_scale)
		self.pos = [0,0,0,0]
		self.motion = [0, 0]
		self.wheel_diam = wheel_diam
	def drive(self, v_f, *args):
		if len(args) == 1:
			v_r, t = 0, args[0]
		else:
			v_r, t = args[0], args[1]
		self.tick(time)
		self.motion = [v_f, v_r]
		self.inner.drive(v_f, v_r)
	def tick(self, time):
		motion_rad = self.motion[0] / self.motion[1]
		radial = (self.motion[1] * time  * self.wheel_circ) % pi
		dx, dy = motion_rad * cos(self.pos[2] + radial), motion_rad * sin(self.pos[2] + radial)
		self.pos[0] += dx
		self.pos[1] += dy
		self.pos[2] += radial
		self.pos[3] += time
		return self.pos
	def last_pos(self):
		return self.pos
