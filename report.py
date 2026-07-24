"""
engine/report.py
Output Chuẩn Hóa 7 Thành Phần (S12) - Section 2.6, Phụ lục 5.4.

1. Phân tích kỹ thuật (Mã quẻ, Vectơ Khí, Đồ thị SIE, Đại tượng, C)
2. Luận động lực học & tương quan lực lượng
3. Tiến trình vận hành (dự đoán xu hướng nhịp điệu thời gian theo Đại quái)
4. Các khả năng theo tương tác (Thuận vs Nghịch)
5. Lập luận giả định (mô phỏng kịch bản chuyển hóa)
6. Thực chứng (ghi nhận phản hồi thực tế - để trống, chờ input người dùng)
7. Hiệu chỉnh mô hình (tái hiệu chuẩn tham số)
"""

from __future__ import annotations

from typing import Any


def build_s12_report(pipeline_result: dict[str, Any]) -> dict[str, Any]:
    khi = pipeline_result["khi_vector"]
    que = pipeline_result["hexagram_report"]
    semantic = pipeline_result["semantic"]
    macro = pipeline_result["macro"]
    confidence = pipeline_result["confidence"]
    levels = pipeline_result["confidence_levels"]
    correction_notes = pipeline_result["self_correction_notes"]

    thanh_phan_1 = {
        "ma_que": que,
        "vecto_khi": khi,
        "do_thi_sie": pipeline_result["sie_graph_summary"],
        "dai_tuong": macro["dai_tuong"],
        "chi_so_tin_cay_C": round(confidence, 4),
        "chi_tiet_5_cap_do": [lv.__dict__ for lv in levels],
    }

    thanh_phan_2 = {
        "luc_tong_the_F": round(macro["force_function"], 4),
        "delta_field": macro["delta_field"],
        "ghi_chu": "F tăng => kỳ vọng thời gian chuyển pha (E[Delta t_Phase]) giảm (Section 3.7).",
    }

    thanh_phan_3 = {
        "nhip_thoi_gian_T": khi["T"],
        "xu_huong": semantic.get("tu_hop_tan_ly"),
        "bieu_hien": semantic.get("hien_an"),
    }

    thanh_phan_4 = {
        "thuan": "Duy trì Hướng (D) và Thế hiện tại nếu Lực F ổn định và không có tương khắc mới.",
        "nghich": "Xuất hiện tương khắc/nghịch pha trong SIE hoặc Delta_Field đổi dấu ở tầng Nhân/Thiên.",
    }

    thanh_phan_5 = {
        "kich_ban_gia_dinh": (
            "Nếu tập điều kiện nền dịch chuyển (Tính Phụ Thuộc Điều Kiện - Hiến Pháp DD), "
            "kết luận tại Thành phần 3 và 4 bắt buộc phải hiệu chỉnh tương ứng."
        ),
        "luu_y": "Đây là mô phỏng kịch bản (counterfactual), không phải tiên đoán tất định (Tiên đề 7).",
    }

    thanh_phan_6 = {
        "phan_hoi_thuc_te": None,
        "ghi_chu": "Chờ ghi nhận thực chứng từ người dùng để nạp vào S09 Feedback_Signal.",
    }

    thanh_phan_7 = {
        "de_xuat_hieu_chinh": correction_notes,
        "ghi_chu": "Tái hiệu chuẩn tham số hyperparameter (A5) qua vòng lặp Self-Correction (S11).",
    }

    return {
        "1_phan_tich_ky_thuat": thanh_phan_1,
        "2_dong_luc_hoc": thanh_phan_2,
        "3_tien_trinh_van_hanh": thanh_phan_3,
        "4_kha_nang_tuong_tac": thanh_phan_4,
        "5_lap_luan_gia_dinh": thanh_phan_5,
        "6_thuc_chung": thanh_phan_6,
        "7_hieu_chinh_mo_hinh": thanh_phan_7,
    }


def render_text(report: dict[str, Any]) -> str:
    """Định dạng S12 report thành văn bản dễ đọc cho CLI."""
    lines = []
    tp1 = report["1_phan_tich_ky_thuat"]
    que_chu = tp1["ma_que"]["que_chu"]
    que_bien = tp1["ma_que"]["que_bien"]

    lines.append("=" * 60)
    lines.append("DUYÊN DỊCH (DCGF) — OUTPUT CHUẨN HÓA S12")
    lines.append("=" * 60)
    lines.append(f"Quẻ chủ : {que_chu['ten_que']} (số {que_chu['so_hieu']}) "
                  f"[{que_chu['upper_ten']}/{que_chu['lower_ten']}] — Hào {que_chu['active_line']} động")
    lines.append(f"Quẻ biến: {que_bien['ten_que']} (số {que_bien['so_hieu']}) "
                  f"[{que_bien['upper_ten']}/{que_bien['lower_ten']}]")
    lines.append("")
    lines.append(f"Vectơ Khí [S,D,I,F,T] = {tp1['vecto_khi']}")
    lines.append(f"Chỉ số tin cậy C = {tp1['chi_so_tin_cay_C']}")
    lines.append("")

    tp3 = report["3_tien_trinh_van_hanh"]
    xu_huong = tp3.get("xu_huong")
    bieu_hien = tp3.get("bieu_hien")
    if xu_huong:
        lines.append(f"[S07] Xu hướng: {xu_huong['label']} — {xu_huong['dien_giai']}")
    if bieu_hien:
        lines.append(f"[S07] Biểu hiện: {bieu_hien['label']} — {bieu_hien['dien_giai']}")
    lines.append("")

    tp2 = report["2_dong_luc_hoc"]
    lines.append(f"Lực tổng thể F = {tp2['luc_tong_the_F']}")
    lines.append("")

    tp4 = report["4_kha_nang_tuong_tac"]
    lines.append(f"Thuận: {tp4['thuan']}")
    lines.append(f"Nghịch: {tp4['nghich']}")
    lines.append("")

    tp7 = report["7_hieu_chinh_mo_hinh"]
    if tp7["de_xuat_hieu_chinh"]:
        lines.append("Đề xuất hiệu chỉnh (S11):")
        for note in tp7["de_xuat_hieu_chinh"]:
            lines.append(f"  - {note}")
    lines.append("=" * 60)
    return "\n".join(lines)
