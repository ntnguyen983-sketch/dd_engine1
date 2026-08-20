"""Macro projection layer."""
from __future__ import annotations
from dataclasses import dataclass
from .hexagram import HexagramData, TRIGRAMS

@dataclass
class MacroProjection:
    dia: int
    nhan: int
    thien: int
    def as_list(self): return [self.dia, self.nhan, self.thien]

def _pair_projection(a,b): return 1 if a == b else -1

def macro_projection(que: HexagramData):
    h1,h2,h3,h4,h5,h6=que.full_bits()
    return MacroProjection(_pair_projection(h1,h2),_pair_projection(h3,h4),_pair_projection(h5,h6))

def delta_field(que_goc, que_target, weights):
    a=macro_projection(que_goc); b=macro_projection(que_target)
    w=[weights.get("dia",1.0),weights.get("nhan",1.0),weights.get("thien",1.0)]
    raw=[b.as_list()[i]-a.as_list()[i] for i in range(3)]
    return {"p_base":a.as_list(),"p_target":b.as_list(),"delta_field_raw":raw,"delta_field_weighted":[w[i]*raw[i] for i in range(3)],"tang":["Địa","Nhân","Thiên"]}

def dai_tuong(que):
    upper=TRIGRAMS[str(que.upper)]; lower=TRIGRAMS[str(que.lower)]; bien=que.quẻ_bien()
    return {"goc":f"{upper['thuoc_tinh']} (trên) + {lower['thuoc_tinh']} (dưới)","bien":f"{TRIGRAMS[str(bien.upper)]['thuoc_tinh']} (trên) + {TRIGRAMS[str(bien.lower)]['thuoc_tinh']} (dưới)"}

def force_function(field_delta):
    w=field_delta["delta_field_weighted"]; return sum(abs(v) for v in w)/max(1,len(w))
