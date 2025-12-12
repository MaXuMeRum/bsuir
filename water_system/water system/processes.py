from .analysis import Analyzer
from .decision import DecisionEngine
from .domain import Reservoir
from typing import List

class MonitoringProcess:
    def __init__(self, engine: DecisionEngine):
        self.engine = engine

    def run(self, reservoir: Reservoir, history: List[float] = None):
        reservoir.update_level_from_sensors()
        hist = history or [reservoir.level]
        forecast = Analyzer.linear_forecast(hist, steps=3)
        decision = self.engine.evaluate_level(reservoir.level, reservoir.capacity)
        return {'reservoir': reservoir.name, 'level': reservoir.level, 'forecast': forecast, 'decision': decision}

class PlanningProcess:
    def __init__(self, engine: DecisionEngine):
        self.engine = engine

    def simulate_rainfall(self, reservoir: Reservoir, rainfall_mm: float):
        # Simple mapping: mm -> volume fraction for demo
        delta = (rainfall_mm * 1000.0) / reservoir.capacity
        simulated = reservoir.level + delta
        forecast = Analyzer.linear_forecast([reservoir.level, simulated], steps=5)
        decision = self.engine.evaluate_level(simulated, reservoir.capacity)
        return {'simulated_level': simulated, 'forecast': forecast, 'decision': decision}

class ReportingProcess:
    def __init__(self):
        pass

    def generate_report(self, history: List[float]):
        mv = Analyzer.moving_average(history, window=3)
        long_forecast = Analyzer.linear_forecast(history, steps=12)
        return {'moving_average': mv, 'long_forecast': long_forecast}
