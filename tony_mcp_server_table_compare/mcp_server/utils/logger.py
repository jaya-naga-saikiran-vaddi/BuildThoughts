import json
from datetime import datetime


def log_trace(goal, result):
    log = {
        "timestamp": datetime.now().isoformat(),
        "goal": goal,
        "result": result
    }
    with open("trace_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")
