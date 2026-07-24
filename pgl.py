"""
engine/pgl.py
Ngôn ngữ Đồ thị Nguyên thủy (Primitive Graph Language - PGL) và Schema Duyên (S02).

Tham chiếu: Section 3.1 (A. Schema Dữ Liệu Duyên, B. PGL).
Lõi Kernel chỉ thao tác trên 10 tham số nguyên thủy:
Node(V), Edge(E), Weight(W in [-1,1]), Momentum(M), Existence(E in [0,1]),
Topology(T), Time(T), Observer(O), Evidence(Ev), Uncertainty(sigma).

Tuân thủ A3 (Tính Phi ngữ nghĩa của Khí): các cấu trúc ở tầng này thuần túy
hình học/toán học, KHÔNG được gán nghĩa định tính (Cát/Hung, Tụ/Tán, ...).
Nghĩa định tính chỉ được sinh ra ở tầng S07 trở đi.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def clamp(value: float, lo: float, hi: float) -> float:
    """Kẹp giá trị vào khoảng đóng [lo, hi] - dùng để bảo đảm A1 (Giới hạn Hiện hữu) v.v."""
    return max(lo, min(hi, value))


@dataclass
class StateVector:
    """Tứ Kiện [H, L, K, T] của một Duyên - Section 3.1.A.

    H (Hướng / Direction), L (Lực / Force), K (Khí / State), T (Thế / Context).
    """

    huong: float = 0.0
    luc: float = 0.0
    khi: float = 0.0
    the: float = 0.0

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.huong, self.luc, self.khi, self.the)


@dataclass
class Duyen:
    """Schema Dữ liệu Duyên (S02) - Section 3.1.A.

    Identity_ID không đại diện cho một thực thể độc lập (Tiên đề 2 / Tính Vô Ngã) -
    nó chỉ là điểm quy chiếu kỹ thuật phục vụ truy vết (A4).
    """

    identity_id: str
    tu_kien: StateVector = field(default_factory=StateVector)
    relation_edges: dict[str, float] = field(default_factory=dict)  # target_id -> weight
    momentum_value: float = 0.0
    history_log: list[dict[str, Any]] = field(default_factory=list)
    existence: float = 1.0  # E in [0, 1] - A1

    def __post_init__(self) -> None:
        self.existence = clamp(self.existence, 0.0, 1.0)

    def push_history(self, snapshot_tick: int, note: str) -> None:
        self.history_log.append({"tick": snapshot_tick, "note": note, "tu_kien": self.tu_kien.as_tuple()})

    def decay_momentum(self, rate: float, has_new_input: bool, m_imax: float = 1.0) -> None:
        """A2 (Nội suy hao Động năng): nếu không có input mới, M suy hao đơn điệu.
        Nếu có input mới, M có thể tăng nhưng bị chặn trên bởi m_imax."""
        if not has_new_input:
            self.momentum_value = max(0.0, self.momentum_value * (1.0 - rate))
        else:
            self.momentum_value = clamp(self.momentum_value, 0.0, m_imax)


@dataclass
class Node:
    """PGL Node (V)."""

    node_id: str
    existence: float = 1.0  # E in [0, 1] - A1
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.existence = clamp(self.existence, 0.0, 1.0)


@dataclass
class Edge:
    """PGL Edge (E) mang Weight (W in [-1, 1])."""

    source: str
    target: str
    weight: float = 0.0
    relation_type: str = "generic"  # vd: ung, ty, hinh, xung, khac, hop (thuần cấu trúc, không gán Cát/Hung)

    def __post_init__(self) -> None:
        self.weight = clamp(self.weight, -1.0, 1.0)


@dataclass
class Evidence:
    """PGL Evidence (Ev) đi kèm Uncertainty (sigma) - UK4, A8."""

    source_observer: str
    value: Any
    sigma: float = 0.0  # độ bất định, bắt buộc công khai theo A8/UK4

    def __post_init__(self) -> None:
        self.sigma = clamp(self.sigma, 0.0, 1.0)


@dataclass
class PrimitiveGraph:
    """Đồ thị Điều kiện (OCG) tối giản dựng trên tập 10 tham số PGL.

    topology và time_tick tương ứng Topology(T) và Time(T) trong PGL;
    observer_id tương ứng Observer(O) - A7 (Node_Obs đặc biệt, tương tác đệ quy).
    """

    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    time_tick: int = 0
    observer_id: str = "Node_Obs"
    evidences: list[Evidence] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def ensure_observer_node(self) -> None:
        """A7: Observer được mô hình hóa trực tiếp như một Node đặc biệt."""
        if self.observer_id not in self.nodes:
            self.add_node(Node(node_id=self.observer_id, existence=1.0, attributes={"role": "observer"}))

    def max_possible_edges(self) -> int:
        """Số liên kết tối đa lý thuyết trên đồ thị hiện tại (đồ thị đơn vô hướng)."""
        n = len(self.nodes)
        return max(1, n * (n - 1) // 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: {"existence": n.existence, "attributes": n.attributes} for nid, n in self.nodes.items()},
            "edges": [
                {"source": e.source, "target": e.target, "weight": e.weight, "relation_type": e.relation_type}
                for e in self.edges
            ],
            "time_tick": self.time_tick,
            "observer_id": self.observer_id,
        }
