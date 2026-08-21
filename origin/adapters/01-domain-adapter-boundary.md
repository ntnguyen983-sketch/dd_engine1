# Domain adapters — boundary and purpose

## Purpose

Adapters convert a domain-specific observation format into the general Duyên Dịch ontology. A quẻ/hào adapter is one example; other domains may represent people, vehicles, orders, money flows, locations, objects or events.

## Adapter contract

An adapter may populate:

- identifiers/references;
- observations and timestamps;
- spatial references;
- interaction events and relations;
- structural references supplied by the domain;
- evidence/provenance.

It must not silently invent dynamic quantities that belong to the engine or calibration layer.

## Quẻ/hào adapter

The quẻ/hào layer is a knowledge/structural input adapter. Historical versions mapped quẻ, hào động, ngũ hành and related structural information into computational primitives. The current architectural boundary treats that mapping as an adapter over N(n), not as a separate ontology.

## Separation of concerns

`Domain data → Adapter → N(n) canonical payload → Structural/Dynamic computation → Quality description → Evidence/Calibration`.

A downstream implementation may replace the adapter or add a new one without changing the origin architecture.
