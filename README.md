# Temporal Drift Agent Demo

A 30-line reproduction of a real failure mode in long-running AI/agent systems.
This is a minimal demonstration of a failure pattern seen in long-running AI/agent systems:

**decision logic that depends on “recency” without managing memory over time.**

The result is a system that works correctly at first, then begins denying valid inputs as internal state accumulates.

This demo shows how:

- Memory grows on every interaction
- Decisions depend on time-window filtering
- Old state is never cleared
- The system drifts into permanent denial

This is not a bug in logic.
It is a bug in **time handling**.

## What this demonstrates

Many agent failures in production are not caused by bad prompts or bad models, but by:

- Timestamp reliance without pruning
- Retry loops that stack state
- Context windows that grow silently
- Systems that pass tests but fail after running for a while

This script recreates that behavior in under 30 lines.

## Run

python agent.py

Then observe the rapid fire test.

The agent begins by allowing input.
Within seconds, it begins denying everything.

Nothing changed except **time** and **state accumulation**.

## Why this matters

This is a simplified illustration of temporal drift in AI systems and agents operating in live environments.

It shows how systems can pass validation, then fail in production purely due to unmanaged memory and time-dependent logic.

## Expected Output

The agent starts by allowing input:

Recent events: 1 → ALLOW

Then within seconds:

Recent events: 3 → DENY  
Recent events: 4 → DENY  
Recent events: 5 → DENY  

Nothing changed except time and accumulated state.

## How this maps to real systems

This same pattern appears in:

- Agents that rely on sliding time windows
- Retry loops that append state without pruning
- Evaluation pipelines that pass tests but fail after hours or days
- Systems where "recent context" is used without lifecycle management

This is not a model failure.

This is a control-plane and time-handling failure.
