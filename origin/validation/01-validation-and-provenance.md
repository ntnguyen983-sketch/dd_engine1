# Validation, provenance and evidence boundary

## 1. Validation philosophy

The engine validates structure and computation rather than forcing an answer. A failed gate is a computational state, not a reason to guess.

## 2. Historical v2.8.6 gate lineage

The v2.8.6/fixxx family introduced explicit execution gates including temporal checks, structural checks, matrix-dimension checks, solver-variable checks and firewall direction checks. Failed gates halt the pipeline rather than permitting downstream contamination.

## 3. Canonical trace

The preferred trace is:

`raw input → canonical state → graph → weights → field → kinematics → emergence → output → evidence/calibration`.

Every derived quantity should be reproducible from its declared inputs and operators.

## 4. Determinism

For a fixed canonical input, fixed research/calibration profile and fixed runtime policy, a deterministic engine should produce the same output. Determinism does not mean the world is static; it means the same computation applied to the same declared state produces the same computation result.

## 5. Forward-only evidence

Evidence collected after a snapshot must not silently mutate the historical snapshot. It may contribute to a later tick/state transition.

## 6. Unknowns

If a formula is not defined by the canonical reference or requires a missing calibration state, output `None`, `UNKNOWN`, or an explicit uncomputed marker according to the API contract. Never replace a missing formula with an invented approximation and call it canonical.

## 7. Quality statements

A qualitative statement must be traceable to quantitative observations and evidence. The system should describe patterns such as convergence, divergence, regular repetition or irregularity rather than smuggling in moral/value judgments.

## 8. Ground Truth

Ground Truth is an external observation against which a prior prediction/output can be evaluated. Its role is calibration for subsequent computation; it is not retrospective permission to rewrite the issued historical output.
