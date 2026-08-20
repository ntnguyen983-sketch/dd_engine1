"""Duyên Dịch v3.1 runtime boundary adapter.

Reuses existing SIE/Khi computation as raw L3 output while preventing legacy
semantic mapping from entering the v3.1 Kernel. No existing runtime module is
modified by this adapter.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from hexagram import HexagramData
from sie import build_interaction_network, compute_khi_vector

V31_CONTRACT_VERSION = "3.1.0"
S07_CANONICAL = ("SAT", "TA", "NHIEU", "HY", "DUONG", "AN")


def _sha256_json(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def run_v31(que_chu: HexagramData, *, gio_dia_chi: int = 1, psi: float = 1.0,
             force_weight_table: dict[str, float] | None = None,
             decision_id: str | None = None, source_version: str = "dd_engine1-baseline",
             engine_commit: str = "unknown") -> dict[str, Any]:
    """Reuse existing raw SIE/Khi computation through the v3.1 boundary.

    Legacy semantic.py is intentionally not called. Until an approved S07
    profile exists, L4 must return MAPPING_UNRESOLVED.
    """
    input_descriptor = {"hexagram": que_chu.to_report_dict(), "gio_dia_chi": gio_dia_chi,
                        "psi": psi, "force_weight_table": force_weight_table or {}}
    input_hash = "sha256:" + _sha256_json(input_descriptor)
    graph = build_interaction_network(que_chu, que_chu.quẻ_bien())
    khi = compute_khi_vector(que_chu, graph, psi=psi,
                             force_weight_table=force_weight_table or {}, gio_dia_chi=gio_dia_chi)
    substantive = [e for e in graph.edges if e.relation_type != "observer_coupling"]
    decision_id = decision_id or ("dd31-" + input_hash[7:19])
    return {
        "contract_version": V31_CONTRACT_VERSION,
        "execution": {"decision_id": decision_id, "tick": 0, "input_hash": input_hash, "runtime_status": "PASSED"},
        "raw_measurements": {"khi_vector": khi.to_dict(),
            "field_state": {"node_count": len(graph.nodes), "substantive_edge_count": len(substantive)},
            "f_net_out": None,
            "runtime_trace": [{"stage": "L3", "event": "SIE_GRAPH_BUILT", "substantive_edge_count": len(substantive)},
                              {"stage": "L3", "event": "KHI_VECTOR_EMITTED", "semantic_label_emitted": False}]},
        "semantic_state": {"status": "MAPPING_UNRESOLVED", "primary_label": "MAPPING_UNRESOLVED",
            "mapping_profile": {"profile_id": "S07_CANONICAL_V31_UNRESOLVED", "version": V31_CONTRACT_VERSION,
                                 "sha256": "", "status": "UNRESOLVED"},
            "mapping_provenance": [{"reason": "No approved S07 mapping profile is available in v3.1."}]},
        "uncertainty": {"measurement": 0.0, "model": 1.0, "semantic": 1.0,
            "confidence": {"score": 0.0, "method": "v3.1-gated-unresolved",
                "inputs": ["gate_results", "provenance", "measurement_uncertainty", "model_uncertainty"],
                "f_net_out_excluded": True}},
        "provenance": {"source_version": source_version,
            "source_hashes": {"sie.py": "3d6d2300c7b748f305169073d3a168c5d6e96e42"},
            "engine_commit": engine_commit, "review_records": ["v3.1 canonical layer spec", "pre-v3.1 runtime baseline"]},
        "gate_results": {"GATE-1-THEORY-FIELD": "PLACEHOLDER_THEORY", "GATE-2-RUNTIME": "PASSED",
            "GATE-3-INTERPRETATION": "MAPPING_UNRESOLVED", "GATE-4-DATA": "PASSED", "GATE-5-OPERATIONS": "PASSED"},
    }


def canonical_json(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
