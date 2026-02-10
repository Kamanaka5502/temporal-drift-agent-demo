import json
import time
from datetime import datetime

STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "memory": [],
            "last_event_time": None
        }


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def agent_decision(input_text):
    state = load_state()
    now = time.time()

    # memory accumulates forever
    state["memory"].append({
        "input": input_text,
        "timestamp": now
    })

    # decision logic depends on "recentness"
    recent_events = [
        m for m in state["memory"]
        if now - m["timestamp"] < 10
    ]

    decision = "ALLOW" if len(recent_events) < 3 else "DENY"

    print(f"\nTime: {datetime.fromtimestamp(now)}")
    print(f"Recent events: {len(recent_events)}")
    print(f"Decision: {decision}")

    save_state(state)


def rapid_fire():
    print("\n--- RAPID FIRE TEST ---")
    for _ in range(6):
        agent_decision("hello")
        time.sleep(1)


if __name__ == "__main__":
    rapid_fire()
