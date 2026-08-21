# DD ORIGIN — Validation, Ground Truth & Calibration Lineage

## 1. Core validation principle

The project repeatedly converged on deterministic execution, traceability and explicit separation between calculation and interpretation. A canonical input plus a fixed execution profile should produce one reproducible result.

## 2. Regression requirements inherited from the runtime lineage

Historical regression checklists require preservation of the intended pipeline, explicit matrix dimensions/constants/versioning, deterministic canonical JSON and hash, evidence chains for warnings, forecast windows with uncertainty, recommendation-to-actor mapping and no feedback from observation/warning/recommendation into frozen core state.

## 3. Ground Truth

Ground Truth is an observation used to evaluate whether a previous model output corresponded to what subsequently occurred. It is not permission to rewrite the old output. The result becomes calibration evidence for later executions.

## 4. Calibration

Calibration may update parameters/profiles where the relevant implementation profile allows it. It must preserve provenance and distinguish:

- source data;
- derived quantities;
- model assumptions;
- calibrated parameters;
- observed outcomes.

## 5. Research status

A formula or label that has not been established by the active canonical contract must carry an explicit research/unvalidated status. In particular, an implementation must not invent values for states such as S07 merely because an output field exists.

## 6. Current 3A validation invariants

1. Entity and space are distinct references.
2. B(V_k) is computed at the spatial node from its IN and OUT flows.
3. event_count, cycle_count and K_rep remain independent.
4. Rhythm is calculated from event sequences, not from an unrelated flat timestamp list.
5. ISO 8601 timestamps are parsed with timezone-aware standard datetime handling.
6. Ranking uses the explicitly declared tie-break order of the active profile.
7. Undeclared dynamics remain absent/None rather than fabricated.
8. Every qualitative statement must be traceable to quantitative values and evidence.

## 7. Minimum test families

- empty/insufficient payload;
- single entity/no interactions;
- repeated same relation with regular intervals;
- repeated same relation with irregular intervals;
- cross-day and offset-aware timestamps;
- IN/OUT flow at one spatial node;
- same entity occupying a bottleneck node without owning the bottleneck;
- multiple candidates exercising every tie-break level;
- missing proxy/evidence;
- missing L4 state, ensuring unsupported qualitative outputs remain uncomputed;
- deterministic rerun and canonical hash comparison.

## 8. Acceptance rule

'Passed' means the implementation satisfied the declared contract for the supplied test case. It does not mean the model has become a universal truth. The architecture remains conditional, observable and revisable at the implementation/calibration layer.
