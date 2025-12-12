import json
from pathlib import Path
from typing import Any
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

class Storage:
    def __init__(self, path: str = 'data/state.json'):
        self.path = Path(path)
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, obj: Any):
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(obj, f, default=str, ensure_ascii=False, indent=2)

    def load(self):
        if not self.path.exists():
            return None
        with self.path.open('r', encoding='utf-8') as f:
            return json.load(f)

class HistoryStorage(Storage):
    def append_measurements(self, measurements):
        data = self.load() or {'history': []}
        for m in measurements:
            d = {'sensor_id': m.sensor_id, 'timestamp': str(m.timestamp), 'value': m.value}
            data.setdefault('history', []).append(d)
        self.save(data)
