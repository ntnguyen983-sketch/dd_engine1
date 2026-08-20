"""Duyên Dịch hexagram engine."""
from __future__ import annotations
import json, os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
def _load_json(filename: str) -> dict:
    with open(os.path.join(_DATA_DIR, filename), encoding="utf-8") as f: return json.load(f)
TRIGRAMS = _load_json("trigrams.json")
HEXAGRAMS = _load_json("hexagrams.json")
DIA_CHI_GIO = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

def gio_dia_chi_tu_datetime(dt: datetime) -> int:
    return (((dt.hour + 1) // 2) % 12) + 1

def mai_hoa_normalize(total: int) -> tuple[int, int]:
    quai = total % 8 or 8
    hao = total % 6 or 6
    return quai, hao

def xac_dinh_hao_dong(x: int, y: int, gio: int) -> int:
    return ((x + y + gio - 1) % 6) + 1

def bo_khuyet_mai_hoa_tu_tin_hieu(*so_lieu: int) -> tuple[int, int]:
    return mai_hoa_normalize(sum(so_lieu))

@dataclass
class HexagramData:
    upper: int
    lower: int
    active_line: int
    upper_bien: Optional[int] = None
    lower_bien: Optional[int] = None
    def __post_init__(self) -> None:
        for name, v in (("upper", self.upper), ("lower", self.lower)):
            if not 1 <= v <= 8: raise ValueError(f"{name} phải trong khoảng 1..8 (nhận {v})")
        if not 1 <= self.active_line <= 6: raise ValueError(f"active_line phải trong khoảng 1..6 (nhận {self.active_line})")
    @property
    def key(self) -> str: return f"{self.upper}-{self.lower}"
    @property
    def info(self) -> dict: return HEXAGRAMS.get(self.key, {"number": None, "name": "Không xác định"})
    def full_bits(self) -> list[int]:
        return list(TRIGRAMS[str(self.lower)]["bits"]) + list(TRIGRAMS[str(self.upper)]["bits"])
    def quẻ_bien(self) -> "HexagramData":
        bits = self.full_bits(); bits[self.active_line - 1] = 1 - bits[self.active_line - 1]
        return HexagramData(upper=_bits_to_trigram_num(bits[3:6]), lower=_bits_to_trigram_num(bits[0:3]), active_line=self.active_line)
    def to_report_dict(self) -> dict:
        bien = self.quẻ_bien()
        return {"que_chu": {"upper": self.upper, "lower": self.lower, "active_line": self.active_line, "upper_ten": TRIGRAMS[str(self.upper)]["ten"], "lower_ten": TRIGRAMS[str(self.lower)]["ten"], "so_hieu": self.info.get("number"), "ten_que": self.info.get("name")}, "que_bien": {"upper": bien.upper, "lower": bien.lower, "upper_ten": TRIGRAMS[str(bien.upper)]["ten"], "lower_ten": TRIGRAMS[str(bien.lower)]["ten"], "so_hieu": bien.info.get("number"), "ten_que": bien.info.get("name")}}

def _bits_to_trigram_num(bits: list[int]) -> int:
    for num, data in TRIGRAMS.items():
        if num in ("_meta", "ngu_hanh_sinh", "ngu_hanh_khac"): continue
        if data["bits"] == bits: return int(num)
    raise ValueError(f"Không tìm thấy quái cho bits {bits}")

def hexagram_engine(upper: int, lower: int, active_line: int) -> HexagramData: return HexagramData(upper=upper, lower=lower, active_line=active_line)
def khoi_que_tu_hai_so(x: int, y: int, dt: Optional[datetime] = None) -> HexagramData:
    dt = dt or datetime.now(); gio = gio_dia_chi_tu_datetime(dt); upper, _ = mai_hoa_normalize(x); lower, _ = mai_hoa_normalize(y); return hexagram_engine(upper, lower, xac_dinh_hao_dong(x, y, gio))
def khoi_que_tu_mot_tin_hieu(total: int) -> HexagramData:
    quai, hao = mai_hoa_normalize(total); return hexagram_engine(quai, quai, hao)
def khoi_que_tu_thoi_gian(dt: Optional[datetime] = None) -> HexagramData:
    dt = dt or datetime.now(); nam, thang, ngay = dt.year, dt.month, dt.day; gio = gio_dia_chi_tu_datetime(dt); upper, _ = mai_hoa_normalize(nam + thang + ngay); lower, _ = mai_hoa_normalize(nam + thang + ngay + gio); return hexagram_engine(upper, lower, xac_dinh_hao_dong(nam + thang + ngay, gio, gio))
