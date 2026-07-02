# stats.py
import json
import os
from datetime import datetime

STATS_FILE = "bot_stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"wins": 0, "losses": 0, "total_signals": 0, "date": str(datetime.now().date())}
    with open(STATS_FILE, 'r') as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def update_stats(result):
    stats = load_stats()
    current_date = str(datetime.now().date())
    
    # Reset stats daily
    if stats.get("date") != current_date:
        stats = {"wins": 0, "losses": 0, "total_signals": 0, "date": current_date}
        
    stats["total_signals"] += 1
    if result.lower() == "win":
        stats["wins"] += 1
    elif result.lower() == "loss":
        stats["losses"] += 1
        
    save_stats(stats)

def get_win_rate():
    stats = load_stats()
    if stats["total_signals"] == 0:
        return 0.0
    return round((stats["wins"] / stats["total_signals"]) * 100, 2)
