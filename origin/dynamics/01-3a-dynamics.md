# 3A Dynamic Domain — reference dynamics

## 1. Space flow and bottleneck

A spatial node `V_k` has incoming and outgoing flow determined by the event's explicit `flow_role`/direction.

`F_in(V_k) = Σ magnitude(I_m)` for events classified as accumulating/loading into the node.

`F_out(V_k) = Σ magnitude(I_m)` for events classified as leaving/releasing from the node.

`B(V_k) = F_in(V_k) - F_out(V_k)`.

The result belongs to the spatial node. It must not be copied onto an entity merely because the entity is observed at that node.

## 2. Event count, topology cycle and repetition

`event_count` measures how many events involve an entity in the observation window.

`cycle_count` is a graph/topology property: directed closed paths returning to the starting node.

`K_rep` is temporal repetition of the same interaction motif, normally keyed by source, target and relation. The three measures answer different questions and cannot substitute for one another.

## 3. Rhythm

For a repeated relation sequence with timestamps `t1 ... tK`:

`Δt_i = t_{i+1} - t_i`.

The rhythm dispersion is computed from the interval sequence, not from a flat list of all timestamps associated with an entity. A low dispersion means the observed motif repeats at a regular cadence; a high dispersion means the sequence is less regular. The quality statement must remain descriptive and evidence-linked.

## 4. Time normalization

ISO 8601 timestamps are parsed with a standards-compliant datetime implementation and converted to an absolute time representation before interval calculations. The implementation must correctly handle offsets, UTC and day boundaries.

## 5. Dynamics without invented state

Historical BEC/state formulas belong to the research lineage unless explicitly validated and promoted. The strict reference rule is:

`known input + defined operator → computed quantity`.

`missing calibration/ground truth → unknown/uncomputed`, not guessed.

## 6. State transition

A state is an observation at a time, and a transition is a relation between successive observations:

`State(t) → State(t + Δt)`.

The transition does not imply an enduring essence of the entity. New evidence belongs to the appropriate future tick under forward-only policy.

## 7. Ground Truth / L4

Ground Truth closes the loop only through calibration. It does not rewrite a past canonical output. It supplies evidence for future parameter/profile decisions according to the calibration policy.
