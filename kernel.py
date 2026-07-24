"""
engine/kernel.py
Snapshot-Kernel-Runtime Model - Section 3.3.

Snapshot = Materialized Runtime State (Trạng thái)
Kernel   = Toán tử chuyển Snapshot(t) -> Snapshot(t+1) (Phép biến đổi)
Runtime  = {S0 -> S1 -> S2 -> ...} (Tiến trình, KHÔNG mang trạng thái riêng)

Hệ quả kiến trúc: Stateless Engine, Single Source of Truth, Implementation-Neutral
Time Travel (rollback/replay), Decoupled Tick Engine.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Snapshot:
    """Trạng thái hệ thống tại một Simulation Tick - vật chất hóa hoàn toàn (Section 3.3.2)."""

    tick: int
    payload: dict[str, Any] = field(default_factory=dict)

    def clone(self) -> "Snapshot":
        return Snapshot(tick=self.tick, payload=copy.deepcopy(self.payload))


TransitionOperator = Callable[[Snapshot, dict[str, Any]], Snapshot]


class TickEngine:
    """Runtime = chuỗi lặp toán tử Kernel K theo trục Simulation Ticks (Section 3.3.6).

    Stateless: bản thân engine không lưu trạng thái nghiệp vụ nào ngoài chuỗi Snapshot
    (history) - đúng nguyên lý 'Runtime không tồn tại như một thực thể độc lập' (3.3.8).
    """

    def __init__(self, initial_snapshot: Snapshot, kernel_operator: TransitionOperator) -> None:
        self._kernel_operator = kernel_operator
        self._history: list[Snapshot] = [initial_snapshot.clone()]

    @property
    def current(self) -> Snapshot:
        return self._history[-1]

    @property
    def history(self) -> list[Snapshot]:
        return self._history

    def tick(self, inputs: dict[str, Any] | None = None) -> Snapshot:
        """Áp dụng Kernel K: S_t -> S_{t+1}. Tính xác định (Determinism, Section 3.3.5):
        cùng (S_t, I_t) luôn cho ra cùng S_{t+1}."""
        inputs = inputs or {}
        next_snapshot = self._kernel_operator(self.current, inputs)
        next_snapshot.tick = self.current.tick + 1
        self._history.append(next_snapshot.clone())
        return next_snapshot

    def rollback(self, target_tick: int) -> Snapshot:
        """Implementation-Neutral Time Travel: tua lại dựa thuần túy vào chuỗi Snapshot đã lưu."""
        for snap in self._history:
            if snap.tick == target_tick:
                self._history = [s for s in self._history if s.tick <= target_tick]
                return snap.clone()
        raise ValueError(f"Không tìm thấy Snapshot tại tick={target_tick} trong lịch sử.")

    def replay(self, from_tick: int, inputs_sequence: list[dict[str, Any]]) -> list[Snapshot]:
        """Mô phỏng tới (Replay) từ một tick trong quá khứ, áp dụng lại chuỗi input."""
        self.rollback(from_tick)
        results = []
        for inputs in inputs_sequence:
            results.append(self.tick(inputs))
        return results


def default_kernel_operator(snapshot: Snapshot, inputs: dict[str, Any]) -> Snapshot:
    """Toán tử Kernel mặc định: gộp payload mới vào Snapshot hiện tại (S_{t+1} = K(S_t)).
    Trong pipeline chính (engine/pipeline.py), Kernel thực tế điều phối SIE/S07/S08 -
    hàm này chỉ là phép biến đổi hợp nhất trạng thái đơn giản cho mục đích minh họa
    Runtime/Tick Engine (thành phần được PHÉP mở rộng theo 0.2.4)."""
    new_payload = copy.deepcopy(snapshot.payload)
    new_payload.update(inputs)
    return Snapshot(tick=snapshot.tick, payload=new_payload)
