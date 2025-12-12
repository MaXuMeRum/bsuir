from typing import List

class Analyzer:
    @staticmethod
    def moving_average(values: List[float], window: int = 3) -> List[float]:
        if not values:
            return []
        res = []
        for i in range(len(values)):
            start = max(0, i-window+1)
            w = values[start:i+1]
            res.append(sum(w)/len(w))
        return res

    @staticmethod
    def linear_forecast(values: List[float], steps: int = 3) -> List[float]:
        if not values:
            return [0.0]*steps
        if len(values) == 1:
            return [values[0]]*steps
        diffs = [values[i+1]-values[i] for i in range(len(values)-1)]
        avg = sum(diffs)/len(diffs)
        last = values[-1]
        res = []
        for _ in range(steps):
            last += avg
            res.append(last)
        return res
