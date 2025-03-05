ON_PICO = True

from interface.col_sense import *
from machine import Pin


class DigitalInput:
    def __init__(self, pin_id):
        self.pin_id = pin_id
        self.pin = Pin(pin_id, Pin.IN, Pin.PULL_DOWN)
    def value(self):
        global sim_input_pins
        global INPUT_MODE
        if INPUT_MODE == 0:
            return self.pin.value()
        elif INPUT_MODE == 1:
            return sim_input_pins[self.pin_id]
        elif INPUT_MODE == 2:
            next_val = self.pin.value()
            if next_val == sim_input_pins[self.pin_id][1]:
                return latest_pin_value(self.pin_id)
            else:
                sim_input_pins[self.pin_id][1] = next_val
                sim_input_pins[self.pin_id][2] = True
                return next_val
        else:
            raise RuntimeError
    def bind_interupt(self, callback, edge_id):
        global INPUT_MODE
        if INPUT_MODE == 0 or INPUT_MODE == 2:
            edge = [Pin.IRQ_FALLING, Pin.IRQ_RISING][edge_id]
            self.pin.irq(callback, edge)
        if INPUT_MODE == 1 or INPUT_MODE == 2:
            global sim_pin_interupt_callbacks
            sim_pin_interupt_callbacks[self.pin_id] = (callback, edge_id)
    def bind_interupt_falling(self, callback):
        self.bind_interupt(callback, 0)
    def bind_interupt_rising(self, callback):
        self.bind_interupt(callback, 1)


def null_callback(p):
    pass

def start_input_sim_monitor():
    def inner():
        global sim_input_pins, sim_pin_interupt_callbacks, sim_command_inputs
        sim_input_pins = [[0, 0, 1] for _ in range(28)]
        sim_pin_interupt_callbacks = [(null_callback, 0) for _ in range(28)]
        sim_command_inputs = dict()

        while True:
            command = input().strip()
            if command[:9] == "Control::":
                if command[9:16] == "set_pin":
                    p, v = [int(s) for s in command[1:-1].split(",")]
                    old_v = sim_input_pins[p]
                    sim_input_pins[p] = v
                    sim_input_pins[p][1] = False
                    if old_v != v and sim_pin_interupt_callbacks[p][1] == v:
                        sim_pin_interupt_callbacks[p][0](p)
                elif "#" in command[9:]:
                    identifier = command[9:].split("#")
                else:
                    identifier = command[9:].split("(")[0]
                    sim_command_inputs[identifier] = [command[9:], 1]

    if ON_PICO:
        import _thread
        _thread.start_new_thread(inner, ())

def latest_pin_value(pin_id):
    global sim_input_pins
    return sim_input_pins[pin_id][sim_input_pins[pin_id][2]]
