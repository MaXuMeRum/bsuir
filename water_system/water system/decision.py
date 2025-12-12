from typing import Dict

class DecisionEngine:
    def __init__(self, low_thresh: float = 0.25, high_thresh: float = 0.85):
        self.low = low_thresh
        self.high = high_thresh

    def evaluate_level(self, level: float, capacity: float) -> Dict:
        ratio = level / capacity if capacity else 0.0
        if ratio < self.low:
            return {'action':'increase_inflow', 'reason':'low_level', 'ratio': ratio}
        if ratio > self.high:
            return {'action':'open_spillway', 'reason':'high_level', 'ratio': ratio}
        return {'action':'hold', 'reason':'normal', 'ratio': ratio}

    def evaluate_quality(self, ph: float = None, turbidity: float = None) -> Dict:
        issues = []
        if ph is not None and not (6.5 <= ph <= 8.5):
            issues.append('ph_out_of_range')
        if turbidity is not None and turbidity > 5.0:
            issues.append('high_turbidity')
        return {'action':'alert' if issues else 'ok', 'issues': issues}
