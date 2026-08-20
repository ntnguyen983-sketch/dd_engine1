"""Dien dich ngu nghia S07."""
from __future__ import annotations
from dataclasses import dataclass
from pgl import PrimitiveGraph
from sie import KhiVector

@dataclass
class SemanticLabel:
    label: str
    dien_giai: str
    truy_vet: dict

def _eval_condition(condition: str, khi: KhiVector) -> bool:
    allowed_names={"S":khi.S,"D":khi.D,"I":khi.I,"F":khi.F,"T":khi.T}
    return bool(eval(condition,{"__builtins__":{}},allowed_names))

def density_direction_label(khi, rules):
    for rule in sorted(rules,key=lambda r:r["order"]):
        if _eval_condition(rule["condition"],khi): return SemanticLabel(rule["label"],rule["dien_giai"],{"I":khi.I,"D":khi.D,"condition":rule["condition"]})
    return None

def spatial_force_label(khi, rules):
    for rule in sorted(rules,key=lambda r:r["order"]):
        if _eval_condition(rule["condition"],khi): return SemanticLabel(rule["label"],rule["dien_giai"],{"S":khi.S,"F":khi.F,"condition":rule["condition"]})
    return None

def resolve_conflict(sie_graph: PrimitiveGraph, s07_labels: list[SemanticLabel]) -> dict:
    substantive=[e for e in sie_graph.edges if e.relation_type!="observer_coupling"]
    overrules=[]
    for lb in s07_labels:
        if lb.label in ("TỤ","HỢP") and len(substantive)==0:
            overrules.append({"label_bi_ghi_de":lb.label,"ly_do":"Đồ thị SIE không ghi nhận liên kết thực chất nào; SIE áp đảo và hạ nhãn xuống TÁN/LY chờ tái đánh giá."})
    return {"priority_axis":"S00=S01 > S06(SIE) > S07 > ...","overrules":overrules}

def dien_dich_ngu_nghia(khi, sie_graph, thresholds):
    dd_label=density_direction_label(khi,thresholds["density_direction_rules"])
    sf_label=spatial_force_label(khi,thresholds["spatial_force_rules"])
    labels=[lb for lb in (dd_label,sf_label) if lb is not None]
    return {"tu_hop_tan_ly":dd_label.__dict__ if dd_label else None,"hien_an":sf_label.__dict__ if sf_label else None,"s10_conflict_resolution":resolve_conflict(sie_graph,labels)}
