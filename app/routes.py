import json
from flask import Blueprint, render_template
from datetime import datetime

# Define a Blueprint
main = Blueprint("main", __name__)

# File to store trading logs
LOG_FILE = "trading_log.json"

def read_trading_log():
    """Read the trading log from a JSON file."""
    try:
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"total_value": 0, "start_time": str(datetime.now()), "logs": []}

@main.route("/")
def index():
    """Render the homepage with trading log data."""
    # Read the trading log
    data = read_trading_log()

    # Calculate trading duration
    start_time = datetime.fromisoformat(data["start_time"])
    duration = datetime.now() - start_time

    return render_template(
        "index.html",
        total_value=data["total_value"],
        duration=str(duration),
        logs=data["logs"]
    )
