"""
tests/test_pipeline.py — kiểm thử cơ bản cho DCGF engine.
Chạy: python -m pytest tests/ -v   (hoặc: python -m unittest discover tests)
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.hexagram import (  # noqa: E402
    HEXAGRAMS,
    TRIGRAMS,
    hexagram_engine,
    khoi_que_tu_mot_tin_hieu,
    mai_hoa_normalize,
    xac_dinh_hao_dong,
)
from engine.pipeline import cast_and_run, run_pipeline  # noqa: E402
from engine.report import build_s12_report  # noqa: E402
from engine.kernel import Snapshot, TickEngine, default_kernel_operator  # noqa: E402


class TestHexagramData(unittest.TestCase):
    def test_64_quai_dung_so_luong(self):
        self.assertEqual(len(HEXAGRAMS) - 1, 64)  # trừ khóa _meta

    def test_8_quai_don(self):
        self.assertEqual(len(TRIGRAMS) - 3, 8)  # trừ _meta, ngu_hanh_sinh, ngu_hanh_khac

    def test_mai_hoa_normalize_du_0(self):
        # tổng chia hết cho 8 và 6 -> quy về 8 và 6
        quai, hao = mai_hoa_normalize(48)  # 48 % 8 = 0, 48 % 6 = 0
        self.assertEqual(quai, 8)
        self.assertEqual(hao, 6)

    def test_xac_dinh_hao_dong_cong_thuc(self):
        # z = ((x + y + gio - 1) mod 6) + 1
        z = xac_dinh_hao_dong(x=3, y=5, gio=2)
        self.assertEqual(z, ((3 + 5 + 2 - 1) % 6) + 1)

    def test_ga_gay_4_am_vi_du_section_4_4(self):
        """Section 4.4: Quái số Chấn (4) -> Quẻ Chấn vi Lôi (51)."""
        que = khoi_que_tu_mot_tin_hieu(4)
        self.assertEqual(que.upper, 4)
        self.assertEqual(que.lower, 4)
        self.assertEqual(que.info["number"], 51)
        self.assertEqual(que.info["name"], "Chấn vi Lôi")


class TestPipeline(unittest.TestCase):
    def test_run_pipeline_tra_ve_du_cac_truong(self):
        que = hexagram_engine(upper=4, lower=2, active_line=4)
        result = run_pipeline(que, gio_dia_chi=3)
        for key in ("hexagram_report", "khi_vector", "sie_graph_summary", "semantic",
                    "macro", "confidence", "confidence_levels", "self_correction_notes"):
            self.assertIn(key, result)
        self.assertTrue(0.0 <= result["confidence"] <= 1.0)

    def test_khi_vector_trong_mien_gia_tri(self):
        que = hexagram_engine(upper=1, lower=8, active_line=6)
        result = run_pipeline(que)
        khi = result["khi_vector"]
        self.assertIn(khi["S"], (0.0, 0.5, 1.0))
        self.assertTrue(-1.0 <= khi["D"] <= 1.0)
        self.assertTrue(0.0 <= khi["I"] <= 1.0)

    def test_cast_and_run_thu_cong(self):
        result = cast_and_run("thu_cong", upper=1, lower=1, active_line=1)
        report = build_s12_report(result)
        self.assertIn("1_phan_tich_ky_thuat", report)
        self.assertEqual(report["1_phan_tich_ky_thuat"]["ma_que"]["que_chu"]["so_hieu"], 1)

    def test_cast_and_run_mot_tin_hieu(self):
        result = cast_and_run("mot_tin_hieu", total=4)
        report = build_s12_report(result)
        self.assertEqual(report["1_phan_tich_ky_thuat"]["ma_que"]["que_chu"]["ten_que"], "Chấn vi Lôi")


class TestKernelDeterminism(unittest.TestCase):
    def test_snapshot_kernel_runtime_determinism(self):
        """A: cùng (S_t, I_t) phải cho cùng S_{t+1} (Section 3.3.5)."""
        s0 = Snapshot(tick=0, payload={"a": 1})
        engine1 = TickEngine(s0, default_kernel_operator)
        engine2 = TickEngine(s0, default_kernel_operator)
        r1 = engine1.tick({"b": 2})
        r2 = engine2.tick({"b": 2})
        self.assertEqual(r1.payload, r2.payload)

    def test_rollback_replay(self):
        s0 = Snapshot(tick=0, payload={})
        engine = TickEngine(s0, default_kernel_operator)
        engine.tick({"x": 1})
        engine.tick({"x": 2})
        restored = engine.rollback(1)
        self.assertEqual(restored.tick, 1)
        self.assertEqual(restored.payload, {"x": 1})


if __name__ == "__main__":
    unittest.main()
