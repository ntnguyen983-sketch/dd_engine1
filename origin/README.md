# DUYÊN DỊCH — ORIGIN

Đây là nhánh chỉnh lý nguồn gốc. Mục tiêu là giữ lại tiến trình tư tưởng, ontology, kiến trúc và các đặc tả đã hình thành qua các giai đoạn; không dùng thư mục Origin làm nơi chứa code production.

## Trục hiện tại

**Định danh | Định lượng | Định tính**

- Định danh: ký hiệu quy chiếu cho luồng quan sát, không gán bản ngã hay bản chất cố định.
- Định lượng: dữ liệu đo được trong không-thời gian và các đại lượng của tương tác.
- Định tính: mẫu hình vận động được rút ra từ dữ liệu định lượng và bằng chứng, không mặc định là phán xét tốt/xấu.

## Kiến trúc tham chiếu

N(n) là ontology chung. v3.0 là Structural Domain; 3A là Dynamic Execution Layer. Space và Entity phải được phân biệt. B(V_k) thuộc nút không gian; event_count, cycle_count và K_rep là ba đại lượng khác nhau.

## Nguyên tắc

Mọi implementation chỉ là một cách thực thi khung tham chiếu. Các module có thể thay đổi; dữ liệu, calibration và ground truth có thể làm thay đổi trạng thái quan sát. Không coi một snapshot hay một nhãn là bản thể cố định.
