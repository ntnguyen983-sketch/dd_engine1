"""engine/macro.py
Giai Đoạn 3 (tiếp): Tầng Tượng S08 (Đại Quái & Đại Tượng) - Section 2.4, 3.7.
"""
from __future__ import annotations
from dataclasses import dataclass
from hexagram import HexagramData, TRIGRAMS

@dataclass
class MacroProjection:
    dia: int
    nhan: int
    thien: int
    def as_list(self) -> list[int]: return [self.dia, self.nhan, self.thien]

def _pair_projection(h_a: int, h_b: int) -> int:
    sign_a = 1 if h_a == 1 else -1
    sign_b = 1 if h_b == 1 else -1
    return 1 if sign_a == sign_b else -1

def macro_projection(que: HexagramData) -> MacroProjection:
    h1,h2,h3,h4,h5,h6 = que.full_bits()
    return MacroProjection(_pair_projection(h1,h2),_pair_projection(h3,h4),_pair_projection(h5,h6))

def delta_field(que_goc: HexagramData, que_target: HexagramData, weights: dict) -> dict:
    p_base=macro_projection(que_goc); p_target=macro_projection(que_target)
    w=[weights.get("dia",1.0),weights.get("nhan",1.0),weights.get("thien",1.0)]
    raw=[p_target.as_list()[i]-p_base.as_list()[i] for i in range(3)]
    return {"p_base":p_base.as_list(),"p_target":p_target.as_list(),"delta_field_raw":raw,"delta_field_weighted":[w[i]*raw[i] for i in range(3)],"tang":["Địa","Nhân","Thiên"]}

def dai_tuong(que: HexagramData) -> dict:
    upper=TRIGRAMS[str(que.upper)]; lower=TRIGRAMS[str(que.lower)]; bien=que.quẻ_bien()
    return {"goc":f"{upper['thuoc_tinh']} (trên) + {lower['thuoc_tinh']} (dưới)","bien":f"{TRIGRAMS[str(bien.upper)]['thuoc_tinh']} (trên) + {TRIGRAMS[str(bien.lower)]['thuoc_tinh']} (dưới)"}

def force_function(field_delta: dict) -> float:
    weighted=field_delta["delta_field_weighted"]
    return sum(abs(v) for v in weighted)/max(1,len(weighted))
