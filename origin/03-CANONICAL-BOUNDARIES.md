# Duyên Dịch — Canonical Boundaries

## Immutable architectural anchor

The current anchor is the architecture, not any one implementation. Its invariant direction is the representation of change through **Định danh | Định lượng | Định tính**, without treating a temporary observation label as a fixed essence.

### Identity

An identifier is a reference handle for an observed stream: entity, space, event, relation or other node. It exists for traceability and computation, not as proof of an independent permanent substance. Earlier Identity_ID definitions already make this distinction explicit. fileciteturn56file9

### Quantity

Quantities must come from observable data or explicitly declared calibrated inputs: position, time, event magnitude, inflow/outflow, intervals, recurrence, uncertainty, and other defined measurements.

### Quality

Qualitative descriptions are derived patterns over quantities and evidence. They are not allowed to masquerade as primitive facts. Earlier Duyên Dịch rules require qualitative conclusions to be traceable to the underlying snapshot, interaction matrix and Qi vector. fileciteturn56file15

## Structural vs dynamic responsibility

The historical structural domain contains the snapshot, six-line representation, elemental/reference mappings, topology and other structural operators. The dynamic domain contains event sequences, force/flow, temporal rhythm and state transition. They share the same underlying observation/interaction world rather than representing two unrelated ontologies.

## Entity vs space

A spatial bottleneck is a property of a spatial node or region, not automatically a property of the entity occupying or traversing it. Therefore `B(V_k)` must remain separate from the identifier of any `N_i` located at `V_k`.

## event_count / cycle_count / K_rep

These quantities are independent:

- `event_count`: number of interaction events involving the referenced entity in the observation window.
- `cycle_count`: number of directed closed topology cycles involving the node.
- `K_rep`: repetition count of a specified interaction motif across its temporal sequence.

A repeated pair of events is not automatically a graph cycle, and a graph cycle is not automatically behavioral repetition.

## Rhythm

`σ_rhythm` belongs to an event/relation sequence. ISO-8601 timestamps must be converted with timezone-aware datetime semantics; interval statistics must be computed on the ordered sequence of the same interaction motif rather than on a flat collection of unrelated timestamps.

## Calibration boundary

A value that is not supplied by the canonical input and has no closed, source-backed formula must not be invented by a reference implementation. It remains `None`, unavailable, or explicitly marked as requiring calibration/ground truth. This follows the historical hyperparameter discipline and the Rev.B separation between Frozen Core and Research/BEC. fileciteturn54file2 fileciteturn54file8

## Implementation freedom

Python, Rust, C++, Go and other implementation languages are replaceable. Database schemas, APIs, UI and optimization internals are replaceable. The implementation must preserve the architectural boundaries above and maintain provenance.
