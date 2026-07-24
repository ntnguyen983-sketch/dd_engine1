"""
engine/semantic.py
Giai Đoạn 3: Diễn Dịch Ngữ Nghĩa (S07) - Section 2.4, Phụ lục 5.2.

Đây là ranh giới đầu tiên nơi nghĩa định tính được phép xuất hiện (sau Firewall S06).
Mọi nhãn ở đây PHẢI truy vết được ngược về Vectơ Khí (A4: Tính Truy vết Toàn vẹn).

Quy Tắc SIE Áp Đảo S07 (Section 2.5): nếu nhãn ngữ nghĩa xung đột với đồ thị SIE
gốc, đồ thị SIE giữ quyền quyết định cao nhất - hàm resolve_conflict() thể hiện điều này.
"""

from __future__ import annotations

from dataclasses import dataclass

from .pgl import PrimitiveGraph
from .sie import KhiVector


@dataclass
class SemanticLabel:
    label: str
    dien_giai: str
    truy_vet: dict  # A4: nguồn gốc từ Vectơ Khí


def _eval_condition(condition: str, khi: KhiVector) -> bool:
    """Đánh giá biểu thức điều kiện từ bảng tra (Phụ lục 5.2) trên các biến S,D,I,F,T.
    Chỉ cho phép namespace an toàn, không eval mã tùy ý từ bên ngoài hệ thống."""
    allowed_names = {"S": khi.S, "D": khi.D, "I": khi.I, "F": khi.F, "T": khi.T}
    return bool(eval(condition, {"__builtins__": {}}, allowed_names))  # noqa: S307 - biểu thức nội bộ, tin cậy


def density_direction_label(khi: KhiVector, rules: list[dict]) -> SemanticLabel | None:
    """Ánh xạ TỤ / HỢP / TÁN / LY theo (I, D) - Phụ lục 5.2."""
    for rule in sorted(rules, key=lambda r: r["order"]):
        if _eval_condition(rule["condition"], khi):
            return SemanticLabel(
                label=rule["label"],
                dien_giai=rule["dien_giai"],
                truy_vet={"I": khi.I, "D": khi.D, "condition": rule["condition"]},
            )
    return None


def spatial_force_label(khi: KhiVector, rules: list[dict]) -> SemanticLabel | None:
    """Ánh xạ HIỆN / ẨN theo (S, F) - Phụ lục 5.2."""
    for rule in sorted(rules, key=lambda r: r["order"]):
        if _eval_condition(rule["condition"], khi):
            return SemanticLabel(
                label=rule["label"],
                dien_giai=rule["dien_giai"],
                truy_vet={"S": khi.S, "F": khi.F, "condition": rule["condition"]},
            )
    return None


def resolve_conflict(sie_graph: PrimitiveGraph, s07_labels: list[SemanticLabel]) -> dict:
    """Section 2.5 - Quy Tắc SIE Áp Đảo S07: khi nhãn S07 mâu thuẫn nội tại
    (ví dụ mật độ tương tác thực tế trên đồ thị SIE quá thấp để biện minh cho TỤ/HỢP),
    đồ thị SIE (I thực đo trên graph) giữ quyền quyết định cao nhất.
    Trả về ghi chú overrule nếu có, phục vụ truy vết S10."""
    substantive = [e for e in sie_graph.edges if e.relation_type != "observer_coupling"]
    overrules = []
    for lb in s07_labels:
        if lb.label in ("TỤ", "HỢP") and len(substantive) == 0:
            overrules.append({
                "label_bi_ghi_de": lb.label,
                "ly_do": "Đồ thị SIE không ghi nhận liên kết thực chất nào (substantive edges = 0), "
                         "SIE áp đảo và hạ nhãn xuống TÁN/LY chờ tái đánh giá.",
            })
    return {"priority_axis": "S00=S01 > S06(SIE) > S07 > ...", "overrules": overrules}


def dien_dich_ngu_nghia(khi: KhiVector, sie_graph: PrimitiveGraph, thresholds: dict) -> dict:
    """Toàn bộ S07: sinh nhãn TỤ/HỢP/TÁN/LY và HIỆN/ẨN, đồng thời áp Quy Tắc SIE Áp Đảo (S10)."""
    dd_label = density_direction_label(khi, thresholds["density_direction_rules"])
    sf_label = spatial_force_label(khi, thresholds["spatial_force_rules"])
    labels = [lb for lb in (dd_label, sf_label) if lb is not None]
    conflict_report = resolve_conflict(sie_graph, labels)
    return {
        "tu_hop_tan_ly": dd_label.__dict__ if dd_label else None,
        "hien_an": sf_label.__dict__ if sf_label else None,
        "s10_conflict_resolution": conflict_report,
    }
