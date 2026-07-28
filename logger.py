import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("run.jsonl")


def log_event(event):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            **event
        }) + "\n")