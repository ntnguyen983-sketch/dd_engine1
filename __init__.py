"""
Gói engine của DUYÊN DỊCH (DCGF - Dynamic Condition & Graph Framework).

Kiến trúc phân tầng (Section 1.6):
    Layer 1 Ontology    -> (mô tả trong tài liệu gốc, không phải code)
    Layer 2 Mathematical -> pgl.py, hexagram.py, sie.py, macro.py
    Layer 3 Inference    -> semantic.py, verification.py
    Layer 4 Learning     -> (mở rộng tương lai: GNN/VAE/Bayesian, xem Phụ lục 5.5 M8-M11)

pipeline.py hợp nhất toàn bộ các tầng thành một luồng chạy end-to-end.
kernel.py cung cấp mô hình Snapshot-Kernel-Runtime độc lập cho Tick Engine.
report.py định dạng Output Chuẩn Hóa S12 (7 thành phần).
"""

from .pipeline import cast_and_run, run_pipeline  # noqa: F401

__version__ = "1.0.0"
__architecture_freeze__ = "Core: Ontology/Axioms/PGL/Pipeline frozen per Section 0.2"
