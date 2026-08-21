# DD ORIGIN — UI, Input Form & Integration Lineage

## 1. Field-level input lineage

The project evolved toward a practical capture form carrying:

- question/context text;
- numeric signal;
- optional image from upload/camera;
- observation time/date-time;
- GPS latitude/longitude;
- human-readable address.

These are input channels, not competing theories. The runtime should preserve the raw values and provenance before normalization.

## 2. Input gateway

Historical runtime documents establish a multi-channel gateway: AppSheet/structured form, Mai Hoa signal, REST/Webhook JSON and server/IoT time. All channels converge into S00 Raw Input before S01 normalization.

## 3. UI boundary

The UI displays runtime output. It must not add calculation rules that are absent from the active contract. Historical v2.8.7 BEC guidance explicitly says the UI should not become a new specification.

## 4. Output evolution

The project has experimented with compact mobile-first reports, root/BEC comparison, operation detail, phase windows, interaction diagrams, warning/recommendation blocks and evidence. These are presentation strategies. The current architecture requires that the underlying output remain traceable to identifiers, quantities, qualities and evidence.

## 5. AI/GEM integration

The historical GEM strategy was intentionally lightweight: provide the implementation guide/knowledge layer and instruct the runtime to calculate first and interpret second. External Chu Dịch/Lục Hào knowledge is an adapter/decoder layer and cannot silently mutate the computational core.

## 6. API integration lessons

An API payload must match the actual endpoint contract. A wrapper that expects a flat `question` field must not be sent a nested or differently named payload merely because an earlier internal representation used those names. Adapters exist precisely to translate between UI/input schemas and the canonical internal schema.

## 7. Production boundary

The UI/API branch may evolve independently from Origin. Any production implementation should record its contract/profile and expose failures as explicit validation errors rather than silently filling missing data with fabricated values.
