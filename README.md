## Temporal Drift in Long-Running Agent Systems

A minimal reproduction of a production failure mode in long-running AI/agent systems.

This demo shows how decision logic that depends on recency can silently fail over time when state is allowed to accumulate without lifecycle management.

The logic remains correct.
The timestamps remain correct.
The system still fails.

This is not a bug in logic.
It is a bug in time handling.

## The Core Failure Pattern

Many AI systems rely on recency-based rules:

“Reject repeated requests within N seconds.”

“Ignore duplicate events within a sliding window.”

“Suppress retry spam.”

“Avoid reprocessing recent inputs.”

These rules are valid.

The failure emerges when:

Memory grows on every interaction.

Decisions depend on time-window filtering.

Old state is never pruned.

The filter’s operating domain expands over time.

Eventually, the system denies valid inputs — permanently.

The drift is gradual.
It passes tests.
It fails in production.

## Concrete Example

Imagine an agent that denies repeated requests within 10 seconds.

Each request timestamp is appended to an internal list.

Filtering checks:

“Does any timestamp exist within the last 10 seconds?”

If yes → deny.

If old timestamps are never pruned, the list grows indefinitely.

Under sustained traffic, the density of timestamps increases.
Eventually, nearly every new request falls within 10 seconds of some prior request.

The system transitions from selective denial to permanent denial.

No logic changed.
The system simply accumulated time without governing it.

## Minimal Reproduction

This script recreates the failure in under 30 lines.

The agent:

Stores timestamps for each request.

Denies requests if a recent one exists within a defined window.

Never removes old timestamps.

State evolution:

t1
t1, t2
t1, t2, t3
...
t1, t2, ... tN


Without pruning, the decision boundary expands as historical state accumulates.

At first, the system behaves correctly.

As interactions accumulate, the state list grows.
Filtering becomes biased by historical density.
The agent begins rejecting valid requests.

Nothing is broken syntactically.
The model is not hallucinating.
The logic is correct.

The system drifts because time was treated as an attribute — not as a lifecycle dimension.

## Why Tests Don’t Catch It

Unit tests typically:

Run for short durations.

Reset state between test cases.

Validate correctness under low iteration counts.

Temporal drift only emerges under sustained execution.

Systems that appear stable in CI pipelines can fail after hours or days of runtime.

This class of failure is invisible to prompt tuning and model swapping.

It is architectural.

## Production Implications

This pattern appears in:

LLM context accumulation

Retry loops with timestamp tracking

Fraud detection throttling systems

Rate limiters without pruning

Agents that store interaction logs indefinitely

AI systems are stateful over time.

If state grows but is never governed, entropy accumulates.

Over time, the system begins optimizing against stale context or dense historical residue.

That is drift.

## General Principle

Any system that makes decisions based on time-bounded conditions must also manage the lifecycle of time-bounded state.

If you enforce a sliding window in logic, you must enforce a sliding window in memory.

Without symmetry between decision rules and state pruning, drift is inevitable.

## The Takeaway

Most AI production failures are not caused by bad prompts or bad models.

They are caused by:

Timestamp reliance without pruning

Retry loops that stack state

Context windows that grow silently

Systems that pass tests but fail under duration

Durability requires explicit lifecycle management of state.

Time must be treated as a first-class architectural constraint.
