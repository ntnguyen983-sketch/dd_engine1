"""SIE interaction network and Khi vector."""
from __future__ import annotations
from dataclasses import dataclass
from hexagram import HEXAGRAMS, TRIGRAMS, HexagramData
from pgl import Edge, Node, PrimitiveGraph, clamp

@dataclass
class KhiVector:
    S: float; D: float; I: float; F: float; T: float
    def as_list(self): return [self.S,self.D,self.I,self.F,self.T]
    def to_dict(self): return {"S":round(self.S,4),"D":round(self.D,4),"I":round(self.I,4),"F":round(self.F,4),"T":round(self.T,4)}

def spatial_index(active_line):
    if active_line in (1,2): return 0.0
    if active_line in (3,4): return 0.5
    if active_line in (5,6): return 1.0
    raise ValueError(f"active_line không hợp lệ: {active_line}")

def directional_derivative(que,psi=1.0):
    bits=que.full_bits(); original_bit=bits[que.active_line-1]; return clamp((1.0 if original_bit==0 else -1.0)*psi,-1.0,1.0)

def _quan_he_ngu_hanh(a,b):
    if a==b:return "ty_hoa",0.5
    sinh=TRIGRAMS["ngu_hanh_sinh"]; khac=TRIGRAMS["ngu_hanh_khac"]
    if sinh.get(a)==b or sinh.get(b)==a:return "tuong_sinh",0.8
    if khac.get(a)==b or khac.get(b)==a:return "tuong_khac",-0.8
    return "trung_tinh",0.0

def build_interaction_network(que_chu,que_bien):
    g=PrimitiveGraph(); g.ensure_observer_node()
    nodes_spec={"que_chu.thuong":que_chu.upper,"que_chu.ha":que_chu.lower,"que_bien.thuong":que_bien.upper,"que_bien.ha":que_bien.lower}
    for node_id,trigram_num in nodes_spec.items():
        tdata=TRIGRAMS[str(trigram_num)]
        g.add_node(Node(node_id=node_id,existence=1.0,attributes={"quai_so":trigram_num,"ten":tdata["ten"],"ngu_hanh":tdata["ngu_hanh"],"source":"S03/S04 Structural Mapping"}))
    pairs=[("que_chu.thuong","que_chu.ha"),("que_bien.thuong","que_bien.ha"),("que_chu.thuong","que_bien.thuong"),("que_chu.ha","que_bien.ha"),("que_chu.thuong","que_bien.ha"),("que_chu.ha","que_bien.thuong")]
    for a,b in pairs:
        rel,w=_quan_he_ngu_hanh(g.nodes[a].attributes["ngu_hanh"],g.nodes[b].attributes["ngu_hanh"])
        if w!=0:g.add_edge(Edge(source=a,target=b,weight=w,relation_type=rel))
    for node_id in nodes_spec:g.add_edge(Edge(source=g.observer_id,target=node_id,weight=0.1,relation_type="observer_coupling"))
    return g

def interaction_density(graph):
    substantive=[e for e in graph.edges if e.relation_type!="observer_coupling"]
    n=len([n for n in graph.nodes if n!=graph.observer_id]); return clamp(len(substantive)/max(1,n*(n-1)//2),0.0,1.0)

def force_scalar(active_line,graph,weight_table):
    base=weight_table.get(str(active_line),0.5); khac_edges=[e for e in graph.edges if e.relation_type=="tuong_khac"]
    return clamp(base+min(0.3,0.05*len(khac_edges)),0.0,1.0)

def temporal_phase(active_line,gio_dia_chi): return clamp(((active_line+gio_dia_chi)%12)/12.0,0.0,1.0)

def compute_khi_vector(que_chu,graph,*,psi=1.0,force_weight_table=None,gio_dia_chi=1):
    force_weight_table=force_weight_table or {}
    return KhiVector(spatial_index(que_chu.active_line),directional_derivative(que_chu,psi),interaction_density(graph),force_scalar(que_chu.active_line,graph,force_weight_table),temporal_phase(que_chu.active_line,gio_dia_chi))
