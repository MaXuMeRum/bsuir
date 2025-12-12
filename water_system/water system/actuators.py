from .domain import Actuator

class ActuatorController:
    def __init__(self, actuator: Actuator):
        self.actuator = actuator

    def set(self, **kwargs):
        # for demo, enforce known keys
        allowed = {'open','flow_rate','mode','on'}
        for k in kwargs:
            if k not in allowed:
                raise ValueError(f'Invalid actuator parameter: {k}')
        return self.actuator.set_state(**kwargs)
