"""
engine/pipeline.py
Tổng Quan Pipeline Duyên Dịch (Section 2.1):

Quan sát -> Nhận diện Duyên -> Hình thành mạng lưới Duyên -> Tính Khí
    -> Suy diễn tương tác -> Hình thành Lực/Hướng/Thế -> Xác định Dòng
    -> Snapshot (Quẻ) -> Đánh giá xu hướng chuyển hóa -> Dự báo

Đây là điểm vào (entry point) hợp nhất toàn bộ engine/*.py, tuân thủ A4
(Tính Truy Vết Toàn Vẹn): Quẻ Gốc -> Vectơ Khí -> Toán tử Hệ thống -> Đồ thị Điều kiện.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Optional

from . import hexagram as hx
from . import macro as mc
from . import semantic as sm
from . import verification as vf
from .hexagram import HexagramData
from .kernel import Snapshot, TickEngine
from .sie import build_interaction_network, compute_khi_vector

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load_json(filename: str) -> dict:
    with open(os.path.join(_DATA_DIR, filename), encoding="utf-8") as f:
        return json.load(f)


CONFIG = _load_json("config.json")
THRESHOLDS = _load_json("semantic_thresholds.json")


def _sie_kernel_operator(snapshot: Snapshot, inputs: dict[str, Any]) -> Snapshot:
    """Toán tử Kernel dùng cho TickEngine trong ngữ cảnh Duyên Dịch: mỗi tick nạp
    một Feedback_Signal (S09) làm Duyên mới, hợp nhất vào payload Snapshot."""
    new_payload = dict(snapshot.payload)
    history = list(new_payload.get("history", []))
    history.append(inputs)
    new_payload["history"] = history
    new_payload["last_input"] = inputs
    return Snapshot(tick=snapshot.tick, payload=new_payload)


def run_pipeline(
    que_chu: HexagramData,
    *,
    gio_dia_chi: int = 1,
    history_len: int = 0,
    has_actionable_nodes: bool = True,
    config: Optional[dict] = None,
    thresholds: Optional[dict] = None,
) -> dict[str, Any]:
    """Chạy toàn bộ pipeline từ một Quẻ Gốc (Hexagram) đến Output S12.

    Tham số:
        que_chu: Quẻ gốc {upper, lower, active_line} (đầu ra của S04 Hexagram Engine).
        gio_dia_chi: số Địa Chi giờ hiện tại (1..12), phục vụ tính T (Temporal Phase).
        history_len: số chu kỳ lịch sử đã tích lũy (phục vụ Level 4 - Tổng quát hóa).
        has_actionable_nodes: có Actionable Node cho phân tích can thiệp Do(v_i=x*) không.
        config, thresholds: cho phép override tham số/ngưỡng (mặc định đọc từ data/*.json).
    """
    cfg = config or CONFIG
    thr = thresholds or THRESHOLDS

    # --- Giai đoạn 2: SIE & Tầng Khí (S06) - Firewall phi ngữ nghĩa ---
    que_bien = que_chu.quẻ_bien()
    graph = build_interaction_network(que_chu, que_bien)
    khi = compute_khi_vector(
        que_chu,
        graph,
        psi=cfg["psi_directional_weight"],
        force_weight_table=cfg["force_active_line_weight"],
        gio_dia_chi=gio_dia_chi,
    )

    # --- Giai đoạn 3: S07 Diễn Dịch Ngữ Nghĩa & S08 Tầng Tượng ---
    semantic_result = sm.dien_dich_ngu_nghia(khi, graph, thr)
    p_base = mc.macro_projection(que_chu)
    p_target = mc.macro_projection(que_bien)
    field_delta = mc.delta_field(que_chu, que_bien, cfg["macro_field_weights"])
    macro_result = {
        "macro_projection_goc": p_base.as_list(),
        "macro_projection_bien": p_target.as_list(),
        "delta_field": field_delta,
        "force_function": mc.force_function(field_delta),
        "dai_tuong": mc.dai_tuong(que_chu),
    }

    # --- Giai đoạn 5: S11 Kiểm chứng 5 cấp độ & Chỉ số tin cậy C ---
    substantive_edges = [e for e in graph.edges if e.relation_type != "observer_coupling"]
    levels = [
        vf.level0_ban_the(khi),
        vf.level1_do_luong(khi, len(substantive_edges)),
        vf.level2_dong_luc(khi),
        vf.level3_can_thiep(has_actionable_nodes),
        vf.level4_tong_quat_hoa(history_len),
    ]
    confidence = vf.confidence_score(levels, cfg["confidence_level_weights"])
    correction_notes = vf.self_correction_notes(confidence)

    return {
        "hexagram_report": que_chu.to_report_dict(),
        "khi_vector": khi.to_dict(),
        "sie_graph_summary": {
            "so_node": len(graph.nodes),
            "so_edge_thuc_chat": len(substantive_edges),
            "quan_he": [{"nguon": e.source, "dich": e.target, "loai": e.relation_type, "trong_so": e.weight}
                        for e in substantive_edges],
        },
        "semantic": semantic_result,
        "macro": macro_result,
        "confidence": confidence,
        "confidence_levels": levels,
        "self_correction_notes": correction_notes,
    }


def new_tick_engine(initial_payload: Optional[dict[str, Any]] = None) -> TickEngine:
    """Khởi tạo TickEngine (Runtime) cho các phiên mô phỏng nhiều Tick liên tiếp (S09 feedback loop)."""
    snap0 = Snapshot(tick=0, payload=initial_payload or {})
    return TickEngine(initial_snapshot=snap0, kernel_operator=_sie_kernel_operator)


def cast_and_run(mode: str, **kwargs) -> dict[str, Any]:
    """Điểm vào tiện lợi: khởi quẻ theo `mode` rồi chạy pipeline đầy đủ.

    mode="hai_so": cần x, y (int), tùy chọn dt (datetime)
    mode="mot_tin_hieu": cần total (int) - Bồ khuyết Mai Hoa cho tín hiệu đơn (vd Section 4.4)
    mode="thoi_gian": tùy chọn dt (datetime), mặc định thời điểm hiện tại
    mode="thu_cong": cần upper, lower, active_line (int)
    """
    dt = kwargs.get("dt") or datetime.now()
    gio = hx.gio_dia_chi_tu_datetime(dt)

    if mode == "hai_so":
        que = hx.khoi_que_tu_hai_so(kwargs["x"], kwargs["y"], dt)
    elif mode == "mot_tin_hieu":
        que = hx.khoi_que_tu_mot_tin_hieu(kwargs["total"])
    elif mode == "thoi_gian":
        que = hx.khoi_que_tu_thoi_gian(dt)
    elif mode == "thu_cong":
        que = hx.hexagram_engine(kwargs["upper"], kwargs["lower"], kwargs["active_line"])
    else:
        raise ValueError(f"mode không hợp lệ: {mode}")

    result = run_pipeline(
        que,
        gio_dia_chi=gio,
        history_len=kwargs.get("history_len", 0),
        has_actionable_nodes=kwargs.get("has_actionable_nodes", True),
    )
    return result
