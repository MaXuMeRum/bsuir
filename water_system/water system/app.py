from .domain import Reservoir, Sensor, Actuator
from .controllers import DeviceController
from .views import BaseApp

def build_demo():
    r1 = Reservoir(id='R1', name='Reservoir A', capacity=1_000_000.0, level=250.0)
    r1.add_sensor(Sensor(id='S1', type='level', location='inlet', last_value=250.0))
    r1.add_sensor(Sensor(id='S2', type='flow', location='outlet', last_value=120.0))
    r1.add_sensor(Sensor(id='S3', type='ph', location='mid', last_value=7.2))
    r1.add_actuator(Actuator(id='A1', type='gate', state={'open': False}))

    r2 = Reservoir(id='R2', name='Reservoir B', capacity=500_000.0, level=120.0)
    r2.add_sensor(Sensor(id='S4', type='level', location='inlet', last_value=119.5))
    r2.add_sensor(Sensor(id='S5', type='turbidity', location='mid', last_value=1.2))
    r2.add_actuator(Actuator(id='A2', type='pump', state={'on': False}))

    controllers = [
        DeviceController(r1.sensors, r1.actuators),
        DeviceController(r2.sensors, r2.actuators)
    ]
    reservoirs = [r1, r2]
    return reservoirs, controllers

def run_gui():
    reservoirs, controllers = build_demo()
    app = BaseApp(reservoirs, controllers)
    app.mainloop()

if __name__ == '__main__':
    run_gui()
