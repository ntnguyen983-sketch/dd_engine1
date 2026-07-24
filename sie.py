"""
engine/sie.py
Giai Đoạn 2: Bộ Trích Xuất Mạng Lưới Tương Tác (SIE) & Tầng Khí (S06) - Section 2.3, 3.2.

FIREWALL (nguyên lý bất can thiệp): module này TUYỆT ĐỐI không được gán nhãn
Cát/Hung hay bất kỳ nghĩa định tính nào (Tụ/Hợp/Tán/Ly/Hiện/Ẩn). Nó chỉ sinh ra
đồ thị tương tác cấu trúc (Interaction Network) và Vectơ Khí phi ngữ nghĩa
(A3: Tính Phi ngữ nghĩa của Khí). Diễn dịch ngữ nghĩa thuộc về engine/semantic.py (S07).
"""

from __future__ import annotations

from dataclasses import dataclass

from .hexagram import HEXAGRAMS, TRIGRAMS, HexagramData
from .pgl import Edge, Node, PrimitiveGraph, clamp


@dataclass
class KhiVector:
    """Vectơ Khí Mở Rộng 5 Chiều [S, D, I, F, T] - Section 3.2."""

    S: float  # Spatial Index - vị trí không gian, trong {0.0, 0.5, 1.0}
    D: float  # Directional Derivative - hướng biến đổi, trong [-1.0, 1.0]
    I: float  # Interaction Density - mật độ tương tác, trong [0.0, 1.0]
    F: float  # Force / Momentum Scalar - xung lực
    T: float  # Temporal Phase - nhịp thời gian / pha cấu trúc

    def as_list(self) -> list[float]:
        return [self.S, self.D, self.I, self.F, self.T]

    def to_dict(self) -> dict:
        return {"S": round(self.S, 4), "D": round(self.D, 4), "I": round(self.I, 4),
                "F": round(self.F, 4), "T": round(self.T, 4)}


def spatial_index(active_line: int) -> float:
    """S theo vị trí hào động z (Section 3.2):
    z in {1,2} -> 0.0 (Hạ/Nội bộ); z in {3,4} -> 0.5 (Trung/Biên); z in {5,6} -> 1.0 (Thượng/Ngoại cảnh)."""
    if active_line in (1, 2):
        return 0.0
    if active_line in (3, 4):
        return 0.5
    if active_line in (5, 6):
        return 1.0
    raise ValueError(f"active_line không hợp lệ: {active_line}")


def directional_derivative(que: HexagramData, psi: float = 1.0) -> float:
    """D = delta_H * psi (Section 3.2).
    delta_H = +1 nếu hào động Âm->Dương (Tiến Dương hóa), -1 nếu Dương->Âm (Thoái Âm hóa).
    psi là hyperparameter trọng số (A5), mặc định 1.0, đọc từ data/config.json ở tầng pipeline."""
    bits = que.full_bits()
    idx = que.active_line - 1
    original_bit = bits[idx]
    delta_h = 1.0 if original_bit == 0 else -1.0  # 0(Âm)->1 nghĩa là Tiến Dương hóa
    d = delta_h * psi
    return clamp(d, -1.0, 1.0)


def _quan_he_ngu_hanh(a: str, b: str) -> tuple[str, float]:
    """Xác định quan hệ Ngũ Hành thuần cấu trúc giữa hai thuộc tính Khí (không gán Cát/Hung).
    Trả về (loại_quan_hệ, trọng_số_thô [-1,1])."""
    if a == b:
        return "ty_hoa", 0.5  # tương đồng / hòa
    sinh = TRIGRAMS["ngu_hanh_sinh"]
    khac = TRIGRAMS["ngu_hanh_khac"]
    if sinh.get(a) == b or sinh.get(b) == a:
        return "tuong_sinh", 0.8
    if khac.get(a) == b or khac.get(b) == a:
        return "tuong_khac", -0.8
    return "trung_tinh", 0.0


def build_interaction_network(que_chu: HexagramData, que_bien: HexagramData) -> PrimitiveGraph:
    """Bộ Trích Xuất Mạng Lưới Tương Tác (SIE) - Section 2.3.
    Đầu vào: Quẻ chủ, Quẻ biến, Hào động, Thượng Hạ quái, Ngũ hành...
    Đầu ra: Interaction Network (đồ thị PGL) xác định thành phần, loại quan hệ, nguồn gốc truy vết."""
    g = PrimitiveGraph()
    g.ensure_observer_node()

    nodes_spec = {
        "que_chu.thuong": que_chu.upper,
        "que_chu.ha": que_chu.lower,
        "que_bien.thuong": que_bien.upper,
        "que_bien.ha": que_bien.lower,
    }
    for node_id, trigram_num in nodes_spec.items():
        tdata = TRIGRAMS[str(trigram_num)]
        g.add_node(Node(node_id=node_id, existence=1.0, attributes={
            "quai_so": trigram_num,
            "ten": tdata["ten"],
            "ngu_hanh": tdata["ngu_hanh"],
            "source": "S03/S04 Structural Mapping",  # A4: truy vết về Quẻ Gốc
        }))

    # Tương tác Quái - Quái (hào ứng/tỷ/hình/xung/khắc/hợp thu gọn về quan hệ Ngũ Hành)
    pairs = [
        ("que_chu.thuong", "que_chu.ha"),
        ("que_bien.thuong", "que_bien.ha"),
        ("que_chu.thuong", "que_bien.thuong"),
        ("que_chu.ha", "que_bien.ha"),
        ("que_chu.thuong", "que_bien.ha"),
        ("que_chu.ha", "que_bien.thuong"),
    ]
    for a, b in pairs:
        ngu_hanh_a = g.nodes[a].attributes["ngu_hanh"]
        ngu_hanh_b = g.nodes[b].attributes["ngu_hanh"]
        rel, w = _quan_he_ngu_hanh(ngu_hanh_a, ngu_hanh_b)
        if w != 0.0:
            g.add_edge(Edge(source=a, target=b, weight=w, relation_type=rel))

    # Observer tương tác đệ quy với toàn mạng (A7)
    for node_id in nodes_spec:
        g.add_edge(Edge(source=g.observer_id, target=node_id, weight=0.1, relation_type="observer_coupling"))

    return g


def interaction_density(graph: PrimitiveGraph) -> float:
    """I = số liên kết thực tế / số liên kết tối đa trên SIE (Section 3.2), không tính cạnh observer."""
    substantive_edges = [e for e in graph.edges if e.relation_type != "observer_coupling"]
    non_observer_nodes = [n for n in graph.nodes if n != graph.observer_id]
    max_edges = max(1, len(non_observer_nodes) * (len(non_observer_nodes) - 1) // 2)
    return clamp(len(substantive_edges) / max_edges, 0.0, 1.0)


def force_scalar(active_line: int, graph: PrimitiveGraph, weight_table: dict) -> float:
    """F: trọng số động năng do hào động và xung kích thời không tạo ra (Section 3.2).
    Kết hợp trọng số vị trí hào động (config, A5) với cường độ tương khắc trên mạng lưới."""
    base = weight_table.get(str(active_line), 0.5)
    khac_edges = [e for e in graph.edges if e.relation_type == "tuong_khac"]
    khac_boost = min(0.3, 0.05 * len(khac_edges))
    return clamp(base + khac_boost, 0.0, 1.0)


def temporal_phase(active_line: int, gio_dia_chi: int) -> float:
    """T: nhịp thời gian / pha cấu trúc - vị trí tuần hoàn của hào động trong chu kỳ Địa Chi (Section 3.2)."""
    return clamp(((active_line + gio_dia_chi) % 12) / 12.0, 0.0, 1.0)


def compute_khi_vector(
    que_chu: HexagramData,
    graph: PrimitiveGraph,
    *,
    psi: float = 1.0,
    force_weight_table: dict | None = None,
    gio_dia_chi: int = 1,
) -> KhiVector:
    """Tổng hợp Vectơ Khí [S, D, I, F, T] từ Quẻ chủ và Interaction Network (Firewall S06).
    Hàm này KHÔNG trả về bất kỳ nhãn ngữ nghĩa nào."""
    force_weight_table = force_weight_table or {}
    que_bien = que_chu.quẻ_bien()
    S = spatial_index(que_chu.active_line)
    D = directional_derivative(que_chu, psi=psi)
    I = interaction_density(graph)
    F = force_scalar(que_chu.active_line, graph, force_weight_table)
    T = temporal_phase(que_chu.active_line, gio_dia_chi)
    return KhiVector(S=S, D=D, I=I, F=F, T=T)
