# DD ORIGIN — Data, Schema & Input Lineage

## 1. Why this exists

Duyên Dịch repeatedly evolved its input representation: symbolic hexagram snapshots, AppSheet/REST/IoT ingestion, six-line state, then general Entity/Observation/Interaction/Space/Time payloads. This file records the transition without forcing one historical schema to impersonate the present schema.

## 2. Historical S00/S01 contract

The v2.8.x family defined a Raw Input Snapshot (S00) containing snapshot id, ISO timestamp, input channel, context scope and hexagram data. S01 normalized the input, extracted the original hexagram, moving lines and timestamp, and produced a six-bit state representation. Multiple channels were allowed: AppSheet, Mai Hoa signal, REST API and IoT/server clock.

## 3. Six-line computational lineage

The earlier runtime treated six line positions as state locations and then derived structural relationships, Qi vectors, force and later dynamics. This remains important as a historical adapter path: a hexagram input is not itself the final world model; it is a source signal that can be mapped into the general ontology.

## 4. General N(n) payload

The current architectural direction uses:

- Entity: a reference identity for an observed stream/phenomenon.
- Observation: what was observed, where and when, with evidence.
- Interaction Event: a directed event between references, with relation, magnitude, time and optional spatial node.
- Space node: a reference location/topology node.
- Quantities: measurable values such as flow, force, interval and bottleneck.
- Qualities: patterns derived from those quantities and evidence.

## 5. Space/entity separation

A spatial bottleneck B(V_k) belongs to the spatial node. It must not be copied onto an entity merely because the entity occupies or traverses that node. This distinction is a required invariant of the current 3A lineage.

## 6. Three independent counters

`event_count` counts events involving an entity.

`cycle_count` counts directed closed graph cycles involving the entity.

`K_rep` counts repetitions of a particular interaction motif through time.

They must never be silently substituted for one another.

## 7. Evidence and provenance

Historical schemas consistently move toward traceability: raw input → normalized state → graph/relations → calculations → output → evidence. Canonical output should retain source version and input provenance. Calibration changes future profiles; it must not retroactively rewrite a previously issued state.

## 8. Current canonical direction

The current representational contract is intentionally simpler: **Định danh | Định lượng | Định tính**. Entity names/types, symbolic labels and historical hexagram terminology are references or adapters, not immutable essence.
