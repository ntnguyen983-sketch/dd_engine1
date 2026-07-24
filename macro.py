"""
engine/macro.py
Giai Đoạn 3 (tiếp): Tầng Tượng S08 (Đại Quái & Đại Tượng) - Section 2.4, 3.7.

Trật tự động lực phân tầng:
Đạo -> Đại quái (Macro Field) -> Quẻ (Micro Structure) -> Hào động (Gradient Source)
    -> Quẻ biến (Target State)
"""

from __future__ import annotations

from dataclasses import dataclass

from .hexagram import HexagramData


@dataclass
class MacroProjection:
    """Kết quả Toán Tử Chiếu Vĩ Mô P: {0,1}^6 -> {-1,+1}^3 (Section 3.7)."""

    dia: int  # Địa = (h1, h2)
    nhan: int  # Nhân = (h3, h4)
    thien: int  # Thiên = (h5, h6)

    def as_list(self) -> list[int]:
        return [self.dia, self.nhan, self.thien]


def _pair_projection(h_a: int, h_b: int) -> int:
    """(+1,+1) hoặc (-1,-1) -> +1 (Đồng điệu/Tăng cường);
    (+1,-1) hoặc (-1,+1) -> -1 (Nghịch pha/Tiêu giảm). Bits gốc 0/1 quy đổi sang -1/+1 trước."""
    sign_a = 1 if h_a == 1 else -1
    sign_b = 1 if h_b == 1 else -1
    return 1 if sign_a == sign_b else -1


def macro_projection(que: HexagramData) -> MacroProjection:
    """P: {0,1}^6 -> {-1,+1}^3 với Địa=(h1,h2), Nhân=(h3,h4), Thiên=(h5,h6) - Section 3.7."""
    h1, h2, h3, h4, h5, h6 = que.full_bits()
    return MacroProjection(
        dia=_pair_projection(h1, h2),
        nhan=_pair_projection(h3, h4),
        thien=_pair_projection(h5, h6),
    )


def delta_field(que_goc: HexagramData, que_target: HexagramData, weights: dict) -> dict:
    """Delta_Field = w_TND ⊙ (P(G_Target) - P(G_Base)) - Section 3.7."""
    p_base = macro_projection(que_goc)
    p_target = macro_projection(que_target)
    w = [weights.get("dia", 1.0), weights.get("nhan", 1.0), weights.get("thien", 1.0)]
    raw = [p_target.as_list()[i] - p_base.as_list()[i] for i in range(3)]
    weighted = [w[i] * raw[i] for i in range(3)]
    return {
        "p_base": p_base.as_list(),
        "p_target": p_target.as_list(),
        "delta_field_raw": raw,
        "delta_field_weighted": weighted,
        "tang": ["Địa", "Nhân", "Thiên"],
    }


def dai_tuong(que: HexagramData) -> dict:
    """Đại Tượng: phép toán logic vị trí giữa Thượng quái và Hạ quái
    (Đại tượng gốc -> Đại tượng biến) - Section 2.4."""
    from .hexagram import TRIGRAMS

    upper = TRIGRAMS[str(que.upper)]
    lower = TRIGRAMS[str(que.lower)]
    bien = que.quẻ_bien()
    upper_b = TRIGRAMS[str(bien.upper)]
    lower_b = TRIGRAMS[str(bien.lower)]
    return {
        "goc": f"{upper['thuoc_tinh']} (trên) + {lower['thuoc_tinh']} (dưới)",
        "bien": f"{upper_b['thuoc_tinh']} (trên) + {lower_b['thuoc_tinh']} (dưới)",
    }


def force_function(field_delta: dict) -> float:
    """Hàm Lực Tổng Thể F = f(Field, Gradient, DeltaField) (Section 3.7) - xấp xỉ
    bằng tổng trị tuyệt đối của Delta_Field có trọng số; F tăng => kỳ vọng thời gian
    chuyển pha (E[Delta t_Phase]) giảm."""
    weighted = field_delta["delta_field_weighted"]
    return sum(abs(v) for v in weighted) / max(1, len(weighted))
