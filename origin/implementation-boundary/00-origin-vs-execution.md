# Origin vs execution boundary

## Origin / architectural anchor

The origin preserves the conceptual lineage, ontology, constraints, mathematical definitions that have been explicitly accepted, historical decisions, and unresolved questions. It is the reference against which implementations are checked.

## Execution

Implementations may:

- use Python, Rust, C++, Go or another language;
- change internal data structures;
- optimize graph parsing and numerical solvers;
- expose REST/API/CLI/UI interfaces;
- use databases or caches;
- add observability and tests;
- add adapters for new domains;
- run in different deployment environments.

## Prohibited silent changes

An implementation must not:

- turn a historical hypothesis into a canonical law;
- invent a missing formula merely to fill an output field;
- attach a spatial bottleneck to an entity as an intrinsic property;
- collapse event_count, cycle_count and K_rep;
- use semantic interpretation as a hidden input to pre-decoder computation;
- use later evidence to rewrite a past canonical state;
- label an implementation `PRODUCTION_READY` while canonical edge cases remain unimplemented.

## Production path

`ORIGIN → canonical test vectors → reference implementation → validation suite → optimized implementation → production API/UI`.

The reference implementation is disposable; the origin is not. If an implementation is replaced, the origin and validation vectors remain.
