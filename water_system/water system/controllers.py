from .sensors import SensorSimulator
from .actuators import ActuatorController
from .domain import Sensor, Actuator, Measurement
from typing import List

class DeviceController:
    def __init__(self, sensors: List[Sensor], actuators: List[Actuator]):
        self.sensors = sensors
        self.actuators = actuators

    def sample_all(self):
        measurements = []
        for s in self.sensors:
            sim = SensorSimulator(s)
            measurements.append(sim.sample())
        return measurements

    def command_actuator(self, actuator_id: str, **kwargs):
        for a in self.actuators:
            if a.id == actuator_id:
                ctrl = ActuatorController(a)
                return ctrl.set(**kwargs)
        raise KeyError('Actuator not found: ' + actuator_id)
