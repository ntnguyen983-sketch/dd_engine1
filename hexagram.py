"""
engine/hexagram.py
Giai Đoạn 1: Tiếp Nhận & Ánh Xạ Đầu Vào (S03 & S04) - Section 2.2, 3.9.

Pipeline con:
[Observation] -> [Cognitive Filter] -> [Structural Mapping] -> [Hexagram Engine]

Tuân thủ Quy tắc Ưu tiên Ánh xạ Dữ liệu Mơ hồ (Section 3.9):
  1. First Observable Priority (Thượng quái -> Hạ quái -> Hào động)
  2. Minimal Representation Priority (Lượng -> Hình -> Ý nghĩa đơn)
  3. Semantic Cluster Priority (giữ nguyên cụm ý, không tách nhỏ)
  4. Mai Hoa Normalization (mod 8 / mod 6, dư 0 quy về 8/6)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load_json(filename: str) -> dict:
    with open(os.path.join(_DATA_DIR, filename), encoding="utf-8") as f:
        return json.load(f)


TRIGRAMS = _load_json("trigrams.json")
HEXAGRAMS = _load_json("hexagrams.json")

# 12 Địa Chi theo giờ, quy ước Tý=1 ... Hợi=12 (Section 2.2)
DIA_CHI_GIO = [
    "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ",
    "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi",
]


def gio_dia_chi_tu_datetime(dt: datetime) -> int:
    """Quy đổi giờ dương lịch (0-23h) sang số thứ tự Địa Chi (1-12).
    Mỗi Địa Chi chiếm 2 giờ, bắt đầu từ Tý (23h-1h) = 1.
    """
    hour = dt.hour
    # Tý: 23h-0h59, Sửu: 1h-2h59, ...
    index = (((hour + 1) // 2) % 12)
    return index + 1  # 1..12


def mai_hoa_normalize(total: int) -> tuple[int, int]:
    """Quy tắc 4 - Chuẩn hóa Mai Hoa (Section 3.9).
    Quái số = tổng mod 8 (dư 0 -> 8); Hào động = tổng mod 6 (dư 0 -> 6)."""
    quai = total % 8
    if quai == 0:
        quai = 8
    hao = total % 6
    if hao == 0:
        hao = 6
    return quai, hao


def xac_dinh_hao_dong(x: int, y: int, gio: int) -> int:
    """Thuật toán xác định Hào động (z) - Section 2.2.
    z = ((x + y + Giờ - 1) mod 6) + 1
    """
    return ((x + y + gio - 1) % 6) + 1


def bo_khuyet_mai_hoa_tu_tin_hieu(*so_lieu: int) -> tuple[int, int]:
    """Bồ khuyết Mai Hoa cho tín hiệu mơ hồ: tổng thời gian/âm thanh/kích thước
    chia 8 dư làm Quái, chia 6 dư làm Hào động (Section 2.2)."""
    total = sum(so_lieu)
    return mai_hoa_normalize(total)


@dataclass
class HexagramData:
    """Cấu trúc dữ liệu quẻ gốc: Hexagram { upper, lower, active_line } - Section 2.2 Bước 4."""

    upper: int
    lower: int
    active_line: int
    upper_bien: Optional[int] = None
    lower_bien: Optional[int] = None

    def __post_init__(self) -> None:
        for name, v in (("upper", self.upper), ("lower", self.lower)):
            if not 1 <= v <= 8:
                raise ValueError(f"{name} phải trong khoảng 1..8 (nhận {v})")
        if not 1 <= self.active_line <= 6:
            raise ValueError(f"active_line phải trong khoảng 1..6 (nhận {self.active_line})")

    @property
    def key(self) -> str:
        return f"{self.upper}-{self.lower}"

    @property
    def info(self) -> dict:
        return HEXAGRAMS.get(self.key, {"number": None, "name": "Không xác định"})

    def full_bits(self) -> list[int]:
        """6 hào từ h1 (đáy, hạ quái) đến h6 (đỉnh, thượng quái)."""
        lower_bits = TRIGRAMS[str(self.lower)]["bits"]
        upper_bits = TRIGRAMS[str(self.upper)]["bits"]
        return list(lower_bits) + list(upper_bits)

    def quẻ_bien(self) -> "HexagramData":
        """Tạo Quẻ biến bằng cách lật (flip) đúng hào động (Chu Dịch cổ điển).
        Đây là hệ quả trực tiếp của Delta Layer (S03: ChangedBits = BaseBits XOR TargetBits)."""
        bits = self.full_bits()
        idx = self.active_line - 1
        bits[idx] = 1 - bits[idx]
        new_lower_bits = bits[0:3]
        new_upper_bits = bits[3:6]
        new_lower = _bits_to_trigram_num(new_lower_bits)
        new_upper = _bits_to_trigram_num(new_upper_bits)
        return HexagramData(upper=new_upper, lower=new_lower, active_line=self.active_line)

    def to_report_dict(self) -> dict:
        bien = self.quẻ_bien()
        return {
            "que_chu": {
                "upper": self.upper,
                "lower": self.lower,
                "active_line": self.active_line,
                "upper_ten": TRIGRAMS[str(self.upper)]["ten"],
                "lower_ten": TRIGRAMS[str(self.lower)]["ten"],
                "so_hieu": self.info.get("number"),
                "ten_que": self.info.get("name"),
            },
            "que_bien": {
                "upper": bien.upper,
                "lower": bien.lower,
                "upper_ten": TRIGRAMS[str(bien.upper)]["ten"],
                "lower_ten": TRIGRAMS[str(bien.lower)]["ten"],
                "so_hieu": bien.info.get("number"),
                "ten_que": bien.info.get("name"),
            },
        }


def _bits_to_trigram_num(bits: list[int]) -> int:
    for num, data in TRIGRAMS.items():
        if num == "_meta" or num in ("ngu_hanh_sinh", "ngu_hanh_khac"):
            continue
        if data["bits"] == bits:
            return int(num)
    raise ValueError(f"Không tìm thấy quái cho bits {bits}")


def hexagram_engine(upper: int, lower: int, active_line: int) -> HexagramData:
    """Bước 4 (Section 2.2): Hexagram Engine - xuất cấu trúc dữ liệu quẻ gốc."""
    return HexagramData(upper=upper, lower=lower, active_line=active_line)


def khoi_que_tu_hai_so(x: int, y: int, dt: Optional[datetime] = None) -> HexagramData:
    """Khởi quẻ mặc định Mai Hoa từ hai số x, y (thời gian/âm thanh/kích thước ...).
    upper = x mod 8, lower = y mod 8, active_line theo công thức z (Section 2.2)."""
    dt = dt or datetime.now()
    gio = gio_dia_chi_tu_datetime(dt)
    upper, _ = mai_hoa_normalize(x)
    lower, _ = mai_hoa_normalize(y)
    z = xac_dinh_hao_dong(x, y, gio)
    return hexagram_engine(upper=upper, lower=lower, active_line=z)


def khoi_que_tu_mot_tin_hieu(total: int) -> HexagramData:
    """Bồ khuyết Mai Hoa khi chỉ có một tín hiệu mơ hồ (vd: 'gà gáy 4 âm' -> Chấn(4)).
    Thượng = Hạ = Quái số (quẻ thuần); Hào động = tổng mod 6."""
    quai, hao = mai_hoa_normalize(total)
    return hexagram_engine(upper=quai, lower=quai, active_line=hao)


def khoi_que_tu_thoi_gian(dt: Optional[datetime] = None) -> HexagramData:
    """Khởi quẻ theo thời gian hiện tại (Năm+Tháng+Ngày -> Thượng; +Giờ -> Hạ),
    quy ước phổ biến của Mai Hoa Dịch Số thời gian khởi quẻ.
    LƯU Ý: đây là xấp xỉ trên lịch Dương; hệ Mai Hoa truyền thống dùng Âm lịch
    và Can Chi năm/tháng/ngày - có thể thay bằng adapter Âm lịch chuẩn xác hơn."""
    dt = dt or datetime.now()
    nam, thang, ngay = dt.year, dt.month, dt.day
    gio = gio_dia_chi_tu_datetime(dt)
    upper, _ = mai_hoa_normalize(nam + thang + ngay)
    lower, _ = mai_hoa_normalize(nam + thang + ngay + gio)
    z = xac_dinh_hao_dong(nam + thang + ngay, gio, gio)
    return hexagram_engine(upper=upper, lower=lower, active_line=z)
