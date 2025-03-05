from .base_input import DigitalInput
from machine import Timer

class LineSensor:
    
    # define the sensors as pin inputs
    def __init__(self, sensor_1_pin, sensor_2_pin, sensor_3_pin, sensor_4_pin):
        self.sensor1 = DigitalInput(sensor_1_pin)
        self.sensor2 = DigitalInput(sensor_2_pin)
        self.sensor3 = DigitalInput(sensor_3_pin)
        self.sensor4 = DigitalInput(sensor_4_pin)
        self.integration = 0
    
    def line_follow(self, time_interval):
        def control_function(self):
            result = 0
            return result
        
        timer = Timer()
        timer.init(freq=(1/time_interval), mode=Timer.PERIODIC, callback=integrate)
        
        def integrate(self, time_interval, integral):
            integral += control_function(self) * time_interval