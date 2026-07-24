"""
engine/verification.py
Giai Đoạn 5: Kiểm Chứng, Hiệu Chỉnh (S11) - Section 2.6.

Chỉ Số Tin Cậy (C) trong [0.0, 1.0] qua 5 cấp độ:
Level 0 (Bản thể) -> Level 1 (Đo lường) -> Level 2 (Động lực)
    -> Level 3 (Can thiệp) -> Level 4 (Tổng quát hóa)
"""

from __future__ import annotations

from dataclasses import dataclass

from .pgl import clamp
from .sie import KhiVector


@dataclass
class LevelScore:
    level: str
    score: float
    ghi_chu: str


def level0_ban_the(khi: KhiVector) -> LevelScore:
    """Bản thể: dữ liệu có tuân thủ ràng buộc bản thể học không (A1: E trong [0,1], v.v.)."""
    ok = 0.0 <= khi.S <= 1.0 and -1.0 <= khi.D <= 1.0 and 0.0 <= khi.I <= 1.0
    return LevelScore("Level 0 - Bản thể", 1.0 if ok else 0.3, "Kiểm tra ràng buộc miền giá trị PGL (A1).")


def level1_do_luong(khi: KhiVector, graph_edge_count: int) -> LevelScore:
    """Đo lường: có đủ dữ liệu thô (đồ thị SIE có liên kết) để đo lường Vectơ Khí không."""
    score = clamp(0.4 + 0.1 * min(6, graph_edge_count), 0.0, 1.0)
    return LevelScore("Level 1 - Đo lường", score, f"Số liên kết SIE quan sát được: {graph_edge_count}.")


def level2_dong_luc(khi: KhiVector) -> LevelScore:
    """Động lực: độ nhất quán nội tại giữa I (mật độ) và F (xung lực) - nếu I cao mà F rất thấp,
    độ tin cậy động lực học giảm (thiếu nhất quán giữa mật độ và xung lực quan sát)."""
    consistency = 1.0 - abs(khi.I - khi.F)
    return LevelScore("Level 2 - Động lực", clamp(consistency, 0.0, 1.0), "Đối chiếu nhất quán I và F.")


def level3_can_thiep(has_actionable_nodes: bool) -> LevelScore:
    """Can thiệp: liệu có tồn tại Actionable Node để áp dụng Do(v_i = x*) hay không (Section 3.6)."""
    return LevelScore("Level 3 - Can thiệp", 0.7 if has_actionable_nodes else 0.4,
                       "Actionable Nodes khả dụng cho phân tích can thiệp." if has_actionable_nodes
                       else "Chưa xác định Actionable Node.")


def level4_tong_quat_hoa(history_len: int) -> LevelScore:
    """Tổng quát hóa: độ tin cậy tăng theo số lượng chu kỳ lịch sử (S09 feedback) đã tích lũy."""
    score = clamp(0.3 + 0.05 * min(14, history_len), 0.0, 1.0)
    return LevelScore("Level 4 - Tổng quát hóa", score, f"Số chu kỳ lịch sử tích lũy: {history_len}.")


def confidence_score(levels: list[LevelScore], level_weights: dict) -> float:
    """C tổng hợp = tổng có trọng số của 5 cấp độ (trọng số là hyperparameter A5, đọc từ config.json)."""
    key_map = {
        "Level 0 - Bản thể": "level0_ban_the",
        "Level 1 - Đo lường": "level1_do_luong",
        "Level 2 - Động lực": "level2_dong_luc",
        "Level 3 - Can thiệp": "level3_can_thiep",
        "Level 4 - Tổng quát hóa": "level4_tong_quat_hoa",
    }
    total = 0.0
    for lv in levels:
        w = level_weights.get(key_map[lv.level], 0.2)
        total += w * lv.score
    return clamp(total, 0.0, 1.0)


def self_correction_notes(confidence: float) -> list[str]:
    """Cơ Chế Hiệu Chỉnh Khép Kín (S11): gợi ý hiệu chỉnh khi C thấp.
    Level 3 (Trọng số Ngưỡng), Level 2 (Bản đồ Ánh xạ S03), Level 2 (Ma trận Đại quái)."""
    notes = []
    if confidence < 0.5:
        notes.append("C < 0.5: đề xuất hiệu chỉnh Level 3 - rà soát lại Trọng số Ngưỡng (config.json).")
        notes.append("C < 0.5: đề xuất hiệu chỉnh Level 2 - kiểm tra Bản đồ Ánh xạ S03 (Structural Mapping).")
    if confidence < 0.3:
        notes.append("C < 0.3: đề xuất hiệu chỉnh Level 2 - rà soát Ma trận Trực quan Đại quái (S08).")
    return notes
