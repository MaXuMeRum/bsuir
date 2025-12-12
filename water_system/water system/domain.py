from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict

@dataclass
class Measurement:
    sensor_id: str
    timestamp: datetime
    value: float
    def to_dict(self):
        return {'sensor_id': self.sensor_id, 'timestamp': self.timestamp.isoformat(), 'value': self.value}

@dataclass
class Sensor:
    id: str
    type: str  # 'level','flow','ph','turbidity','chem'
    location: str
    last_value: Optional[float] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return {'id': self.id, 'type': self.type, 'location': self.location, 'last_value': self.last_value, 'metadata': self.metadata}

@dataclass
class Actuator:
    id: str
    type: str  # 'gate','pump','valve'
    state: Dict = field(default_factory=dict)
    def to_dict(self):
        return {'id': self.id, 'type': self.type, 'state': self.state}

    def set_state(self, **kwargs):
        self.state.update(kwargs)
        return self.state

@dataclass
class Reservoir:
    id: str
    name: str
    capacity: float
    level: float
    sensors: List[Sensor] = field(default_factory=list)
    actuators: List[Actuator] = field(default_factory=list)

    def add_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)

    def add_actuator(self, actuator: Actuator):
        self.actuators.append(actuator)

    def update_level_from_sensors(self):
        vals = [s.last_value for s in self.sensors if s.type == 'level' and s.last_value is not None]
        if vals:
            self.level = sum(vals)/len(vals)
        return self.level

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'capacity': self.capacity, 'level': self.level,
            'sensors':[s.to_dict() for s in self.sensors], 'actuators':[a.to_dict() for a in self.actuators]
        }
