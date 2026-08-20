from __future__ import annotations

import unittest

import hexagram as hx
from v31_runtime import run_v31


class TestV31RuntimeBoundary(unittest.TestCase):
    def test_existing_sie_becomes_raw_l3_and_mapping_is_gated(self):
        que = hx.hexagram_engine(1, 1, 1)
        result = run_v31(que, gio_dia_chi=1, force_weight_table={"1": 0.15})

        self.assertEqual(result["contract_version"], "3.1.0")
        self.assertEqual(result["execution"]["runtime_status"], "PASSED")
        self.assertEqual(set(result["raw_measurements"]["khi_vector"]), {"S", "D", "I", "F", "T"})
        self.assertEqual(result["semantic_state"]["primary_label"], "MAPPING_UNRESOLVED")
        self.assertFalse(any("semantic_label" in e and e["semantic_label"] for e in result["raw_measurements"]["runtime_trace"]))
        self.assertTrue(result["uncertainty"]["confidence"]["f_net_out_excluded"])
        self.assertEqual(result["gate_results"]["GATE-3-INTERPRETATION"], "MAPPING_UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
