# DD ORIGIN — Adapters, AI & Implementation Lineage

## 1. Separation of concerns

The origin archive is the source-of-truth for lineage and architectural intent. Executable branches are implementations. They may be written in different languages and may expose different APIs/UI, provided they declare which contract/profile they implement.

## 2. Hexagram / v3.0 adapter

A v3.0 adapter maps a question/snapshot, number signal, timestamp, moving lines, gua/structural data and related evidence into the general N(n) representation. The adapter must preserve provenance and must not invent missing observations.

## 3. Knowledge/GEM/AI layer

Historical runtime documents establish a strong boundary: external knowledge such as Chu Dịch/Lục Hào explanations may be a Knowledge Layer or decoder. It must not silently modify core state or core formulas. AI-generated interpretation therefore belongs after the computational contract unless an explicit implementation profile says otherwise.

## 4. API/input lineage

The project has used AppSheet, REST-style input, server/IoT timestamps and later web UI/API services. The common rule is: normalize raw input first, preserve the original timestamp/provenance, then execute the declared computational profile.

## 5. UI lineage

UI is not the ontology. A UI may show question, number, image, current time, GPS, address, quẻ/hào, calculated quantities, qualitative patterns, evidence and recommendations. It must not manufacture hidden state merely to make a screen look complete.

## 6. Production branches

Production implementations should be derived from this Origin archive through an explicit Canonical Contract. The production branch may optimize algorithms, change language or storage, and expose APIs/UX, but it must not silently change the meaning of the Origin anchor.

## 7. Required implementation metadata

Every executable branch should declare:

- origin/contract reference;
- implementation version;
- runtime profile;
- calibration profile if any;
- input schema version;
- output schema version;
- deterministic/hash policy;
- known unsupported fields.

## 8. Copilot/Manus/other agents

AI agents may be used as workers for documentation, code generation, testing, auditing or migration. Their output is evidence/work product, not authority. Human-approved canonical contracts and repository review remain the boundary.
