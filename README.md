# Duyên Dịch — DCGF (Dynamic Condition & Graph Framework)

Triển khai tham chiếu (reference implementation) bằng Python cho kiến trúc
**Duyên Dịch (DCGF)** mô tả trong tài liệu *"Đặc Tả Bản Thể Học Và Kiến Trúc
Hệ Thống Duyên Dịch"*: từ Ontology (Duyên – Khí – Lực/Hướng/Thế – Dòng), qua
Hexagram Engine (S03/S04), Tầng Khí phi ngữ nghĩa (SIE/S06), Diễn dịch ngữ
nghĩa (S07), Tầng Tượng (S08 Đại Quái), Snapshot–Kernel–Runtime, đến Output
Chuẩn Hóa 7 thành phần (S12).

> ⚠️ Đây là bản triển khai kỹ thuật của phần **Toán tử / Kiến trúc** (Chương
> 3 của tài liệu gốc). Một số thành phần được đánh dấu "Giả thuyết hợp lý"
> hoặc "Cần bổ sung thuật toán" trong Phụ lục 5.5 (Maturity Matrix) — ví dụ
> Interaction Engine đầy đủ (M11), khôi phục Best-Fit π⁻¹ (M8) — được cài đặt
> ở đây dưới dạng **xấp xỉ tối giản, có thể mở rộng**, không phải bản đầy đủ
> cuối cùng. Xem ghi chú "Giới hạn hiện tại" bên dưới.

## Cấu trúc dự án

```
duyen_dich/
├── app.py                     # Web API (Flask)
├── main.py                    # CLI
├── requirements.txt
├── README.md
├── engine/
│   ├── __init__.py
│   ├── pgl.py                 # PGL (10 tham số nguyên thủy) + Schema Duyên (S02)
│   ├── hexagram.py            # S03/S04: Ánh xạ cấu trúc, Hexagram Engine, Bồ khuyết Mai Hoa
│   ├── sie.py                 # S06: SIE + Vectơ Khí 5 chiều (Firewall phi ngữ nghĩa)
│   ├── semantic.py            # S07: Diễn dịch ngữ nghĩa (Tụ/Hợp/Tán/Ly/Hiện/Ẩn) + S10
│   ├── macro.py                # S08: Đại Quái Động Lực, toán tử chiếu vĩ mô P, Đại Tượng
│   ├── kernel.py               # Mô hình Snapshot–Kernel–Runtime, Tick Engine, Rollback/Replay
│   ├── verification.py         # S11: Chỉ số tin cậy C (5 cấp độ) + Self-Correction Loop
│   ├── pipeline.py             # Orchestrator: hợp nhất toàn bộ pipeline S00→S12
│   └── report.py               # S12: Output Chuẩn Hóa 7 Thành Phần
├── data/
│   ├── trigrams.json           # 8 Quái (Mai Hoa order), Ngũ Hành, quan hệ Sinh/Khắc
│   ├── hexagrams.json          # 64 Quẻ (không gian trạng thái tối thiểu — Phụ lục 5.1)
│   ├── semantic_thresholds.json# Bảng tra ngưỡng ngữ nghĩa S07 (Phụ lục 5.2)
│   └── config.json             # Hyperparameter khởi tạo (Tiên đề A5)
└── tests/
    └── test_pipeline.py        # Kiểm thử unit (unittest, không phụ thuộc ngoài)
```

## Cài đặt

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Lõi `engine/` chỉ dùng thư viện chuẩn Python ≥3.10 (dataclasses, json...).
`flask` chỉ cần nếu bạn muốn chạy `app.py`.

## Chạy thử — CLI

```bash
# Khởi quẻ theo thời điểm hiện tại
python main.py thoi-gian

# Khởi quẻ Mai Hoa từ hai số (vd giờ + số bất kỳ)
python main.py hai-so --x 7 --y 3

# Bồ khuyết Mai Hoa từ một tín hiệu mơ hồ (Section 4.4: "Gà gáy 4 âm")
python main.py mot-tin-hieu --total 4
# -> Quẻ chủ: Chấn vi Lôi (51), Hào 4 động -> Quẻ biến: Địa Lôi Phục (24)

# Nhập trực tiếp Thượng/Hạ quái + Hào động
python main.py thu-cong --upper 4 --lower 2 --active-line 4

# Xuất JSON đầy đủ (Output S12) thay vì bản tóm tắt văn bản
python main.py thu-cong --upper 4 --lower 2 --active-line 4 --json
```

## Chạy thử — Web API

```bash
python app.py
# http://127.0.0.1:5000
```

```bash
curl http://127.0.0.1:5000/health

curl -X POST http://127.0.0.1:5000/api/khoi-que \
  -H "Content-Type: application/json" \
  -d '{"mode": "mot_tin_hieu", "total": 4}'
```

## Chạy test

```bash
python -m unittest discover tests -v
# hoặc, nếu đã cài pytest:
python -m pytest tests/ -v
```

## Ánh xạ Kiến trúc ↔ Mã nguồn

| Thành phần tài liệu | Mục | File |
|---|---|---|
| Tiên đề bản thể học, Hiến pháp DD | 1.2–1.3 | *(triết lý nền — thể hiện qua docstring toàn bộ engine/)* |
| PGL (10 tham số), Schema Duyên S02 | 3.1 | `engine/pgl.py` |
| Structural Mapping, Hexagram Engine, Bồ khuyết Mai Hoa | 2.2, 3.9 | `engine/hexagram.py` |
| SIE, Vectơ Khí `[S,D,I,F,T]`, Firewall | 2.3, 3.2 | `engine/sie.py` |
| S07 Diễn dịch ngữ nghĩa, S10 SIE áp đảo | 2.4, 2.5, Phụ lục 5.2 | `engine/semantic.py` |
| S08 Đại Quái, toán tử P, Đại Tượng, ΔField | 2.4, 3.7 | `engine/macro.py` |
| Snapshot–Kernel–Runtime, Tick Engine | 3.3 | `engine/kernel.py` |
| S11 Chỉ số tin cậy C (5 cấp độ), Self-Correction | 2.6 | `engine/verification.py` |
| Pipeline tổng quát S00→S12 | 2.1 | `engine/pipeline.py` |
| Output Chuẩn Hóa 7 Thành Phần (S12) | 2.6, Phụ lục 5.4 | `engine/report.py` |
| 64 Quẻ (State Space Ontology) | Phụ lục 5.1 | `data/hexagrams.json` |

## Nguyên tắc thiết kế đã tuân thủ

- **A3 (Phi ngữ nghĩa của Khí)**: `engine/sie.py` không sinh bất kỳ nhãn định
  tính nào (Cát/Hung/Tụ/Tán...) — chỉ trả về đồ thị cấu trúc và Vectơ Khí số.
- **A4 (Truy vết toàn vẹn)**: mọi nhãn ở `engine/semantic.py` mang theo
  `truy_vet` trỏ ngược về giá trị Vectơ Khí đã sinh ra nó.
- **A5 (Hyperparameter)**: các trọng số không suy ra trực tiếp từ toán học
  (psi, trọng số Lực theo hào, trọng số MDL...) đều nằm trong
  `data/config.json`, không hard-code trong logic.
- **A9 (Model Separation)**: không có "nhảy tầng" — `pipeline.py` gọi tuần tự
  `hexagram → sie → semantic/macro → verification → report`, không module nào
  gọi tắt qua module khác.
- **Section 3.3 (Stateless Kernel)**: `TickEngine` không giữ trạng thái
  nghiệp vụ ngoài chuỗi `Snapshot`; `rollback()`/`replay()` chỉ thao tác trên
  lịch sử Snapshot đã lưu.
- **Section 0.2 (Architecture Freeze)**: `data/config.json` và
  `data/semantic_thresholds.json` tách riêng khỏi mã nguồn để các thành phần
  "được phép mở rộng" (Cost Function, Adapters...) có thể hiệu chỉnh mà không
  đụng vào lõi Ontology/Pipeline.

## Giới hạn hiện tại (theo Phụ lục 5.5 — Maturity Matrix)

- `khoi_que_tu_thoi_gian()` dùng **lịch Dương** làm xấp xỉ; hệ Mai Hoa
  Dịch Số thời gian truyền thống dùng Âm lịch + Can Chi năm/tháng/ngày. Cần
  một Adapter Âm lịch riêng (tuân UK8 - Extensibility) để chính xác tuyệt đối.
- `engine/macro.py` và `engine/verification.py` cài đặt các công thức F,
  Delta_Field, chỉ số tin cậy C ở dạng **xấp xỉ tường minh** (explicit,
  không phải mô hình học máy) — đúng tinh thần M8–M11 trong Phụ lục 5.5
  ("Đề xuất Mô hình" / "Cần bổ sung thuật toán"), sẵn sàng để thay thế bằng
  GNN/VAE/Bayesian ở Layer 4 (Learning Layer) mà không phá vỡ interface hiện có.
- Khôi phục Best-Fit `π⁻¹` (Section 3.5) chưa được cài đặt như một bộ giải
  tối ưu MDL đầy đủ; công thức `Cost(Ĝ)` được để lại dưới dạng tài liệu tham
  chiếu trong docstring, chưa có solver.
- Adapter Kabbalah (Section 4.3) và các Adapter môn học khác chưa có trong
  mã nguồn — kiến trúc `UK8 (Extensibility)` cho phép bổ sung dưới dạng
  module mới trong `engine/adapters/` (thư mục chưa tạo) mà không cần sửa Lõi.

## Giấy phép / Ghi chú

Mã nguồn này là bản triển khai tham chiếu dựa trên tài liệu đặc tả do người
dùng cung cấp. Vui lòng tự quyết định giấy phép phân phối phù hợp với dự án
của bạn.
