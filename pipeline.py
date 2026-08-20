"""Duyên Dịch pipeline entry point.

Repository implementation modules live at the repository root. Absolute
imports keep the engine loadable by Vercel's Python runtime.
"""
from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Any, Optional
import hexagram as hx
import macro as mc
import semantic as sm
import verification as vf
from hexagram import HexagramData
from kernel import Snapshot, TickEngine
from sie import build_interaction_network, compute_khi_vector

_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_json(filename: str) -> dict:
    with open(os.path.join(_DATA_DIR, filename), encoding="utf-8") as f:
        return json.load(f)

CONFIG = _load_json("config.json")
THRESHOLDS = _load_json("semantic_thresholds.json")

def _sie_kernel_operator(snapshot: Snapshot, inputs: dict[str, Any]) -> Snapshot:
    new_payload = dict(snapshot.payload)
    history = list(new_payload.get("history", []))
    history.append(inputs)
    new_payload["history"] = history
    new_payload["last_input"] = inputs
    return Snapshot(tick=snapshot.tick, payload=new_payload)

def run_pipeline(que_chu: HexagramData, *, gio_dia_chi: int = 1, history_len: int = 0, has_actionable_nodes: bool = True, config: Optional[dict] = None, thresholds: Optional[dict] = None) -> dict[str, Any]:
    cfg = config or CONFIG
    thr = thresholds or THRESHOLDS
    que_bien = que_chu.quẻ_bien()
    graph = build_interaction_network(que_chu, que_bien)
    khi = compute_khi_vector(que_chu, graph, psi=cfg["psi_directional_weight"], force_weight_table=cfg["force_active_line_weight"], gio_dia_chi=gio_dia_chi)
    semantic_result = sm.dien_dich_ngu_nghia(khi, graph, thr)
    p_base = mc.macro_projection(que_chu)
    p_target = mc.macro_projection(que_bien)
    field_delta = mc.delta_field(que_chu, que_bien, cfg["macro_field_weights"])
    macro_result = {"macro_projection_goc": p_base.as_list(), "macro_projection_bien": p_target.as_list(), "delta_field": field_delta, "force_function": mc.force_function(field_delta), "dai_tuong": mc.dai_tuong(que_chu)}
    substantive_edges = [e for e in graph.edges if e.relation_type != "observer_coupling"]
    levels = [vf.level0_ban_the(khi), vf.level1_do_luong(khi, len(substantive_edges)), vf.level2_dong_luc(khi), vf.level3_can_thiep(has_actionable_nodes), vf.level4_tong_quat_hoa(history_len)]
    confidence = vf.confidence_score(levels, cfg["confidence_level_weights"])
    return {"hexagram_report": que_chu.to_report_dict(), "khi_vector": khi.to_dict(), "sie_graph_summary": {"so_node": len(graph.nodes), "so_edge_thuc_chat": len(substantive_edges), "quan_he": [{"nguon": e.source, "dich": e.target, "loai": e.relation_type, "trong_so": e.weight} for e in substantive_edges]}, "semantic": semantic_result, "macro": macro_result, "confidence": confidence, "confidence_levels": levels, "self_correction_notes": vf.self_correction_notes(confidence)}

def new_tick_engine(initial_payload: Optional[dict[str, Any]] = None) -> TickEngine:
    return TickEngine(initial_snapshot=Snapshot(tick=0, payload=initial_payload or {}), kernel_operator=_sie_kernel_operator)

def cast_and_run(mode: str, **kwargs) -> dict[str, Any]:
    dt = kwargs.get("dt") or datetime.now()
    gio = hx.gio_dia_chi_tu_datetime(dt)
    if mode == "hai_so": que = hx.khoi_que_tu_hai_so(kwargs["x"], kwargs["y"], dt)
    elif mode == "mot_tin_hieu": que = hx.khoi_que_tu_mot_tin_hieu(kwargs["total"])
    elif mode == "thoi_gian": que = hx.khoi_que_tu_thoi_gian(dt)
    elif mode == "thu_cong": que = hx.hexagram_engine(kwargs["upper"], kwargs["lower"], kwargs["active_line"])
    else: raise ValueError(f"mode không hợp lệ: {mode}")
    return run_pipeline(que, gio_dia_chi=gio, history_len=kwargs.get("history_len", 0), has_actionable_nodes=kwargs.get("has_actionable_nodes", True))
