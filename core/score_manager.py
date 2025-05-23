import json
import os
from datetime import datetime

SCORE_FILE = os.path.join("assets", "scores.json")

def save_score(score, total, mode):
    data = load_scores()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "total": total,
        "mode": mode
    }
    data.append(entry)
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
