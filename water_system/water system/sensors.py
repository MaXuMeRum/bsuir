from .domain import Measurement, Sensor
from datetime import datetime
import random

class SensorSimulator:
    """Generates realistic-enough samples for different sensor types."""
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    def sample(self) -> Measurement:
        base = self.sensor.last_value if self.sensor.last_value is not None else self._default_for_type()
        noise = self._noise()
        value = base + noise
        value = self._clamp(value)
        self.sensor.last_value = value
        return Measurement(sensor_id=self.sensor.id, timestamp=datetime.now(), value=round(value, 3))

    def _default_for_type(self):
        t = self.sensor.type
        return {'level': 250.0, 'flow': 100.0, 'ph': 7.0, 'turbidity': 1.0, 'chem': 0.1}.get(t, 0.0)

    def _noise(self):
        t = self.sensor.type
        if t == 'ph':
            return random.uniform(-0.2, 0.2)
        if t == 'level':
            return random.uniform(-1.0, 1.0)
        if t == 'flow':
            return random.uniform(-5.0, 5.0)
        if t == 'turbidity':
            return random.uniform(-0.3, 0.3)
        return random.uniform(-0.5, 0.5)

    def _clamp(self, v):
        if self.sensor.type == 'ph':
            return max(0.0, min(14.0, v))
        if self.sensor.type == 'turbidity':
            return max(0.0, v)
        return v
