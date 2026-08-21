# DUYÊN DỊCH — ORIGIN

Đây là nhánh chỉnh lý nguồn gốc. Mục tiêu là giữ lại tiến trình tư tưởng, ontology, kiến trúc, toán học, runtime, nghiên cứu, mâu thuẫn và đặc tả đã hình thành qua các giai đoạn; **không dùng thư mục Origin làm nơi chứa code production**.

## Trục hiện tại

**Định danh | Định lượng | Định tính**

- Định danh: ký hiệu quy chiếu cho luồng quan sát, không gán bản ngã hay bản chất cố định.
- Định lượng: dữ liệu đo được trong không-thời gian và các đại lượng của tương tác.
- Định tính: mẫu hình vận động được rút ra từ dữ liệu định lượng và bằng chứng, không mặc định là phán xét tốt/xấu.

## Kiến trúc tham chiếu

N(n) là ontology chung. v3.0 là Structural Domain; 3A là Dynamic Execution Layer. Space và Entity phải được phân biệt. B(V_k) thuộc nút không gian; event_count, cycle_count và K_rep là ba đại lượng khác nhau.

## Tổ chức Origin

- `00-ORIGIN-CONTENTS.md` — mục lục đã có từ các vòng chỉnh lý trước.
- `00-SOURCE-REGISTER.md` — đăng ký nguồn.
- `00-ORIGIN-MAP.md` — bản đồ đầy đủ các nhóm nguồn cần hợp nhất.
- `01-FOUNDATIONAL-LINEAGE.md` — lineage nền tảng đã được rót trước.
- `01-PHILOSOPHY-AND-ONTOLOGY-LINEAGE.md` — chỉnh lý triết lý/ontology.
- `02-ARCHITECTURE-LINEAGE-v2.3-v2.9.md` — lịch sử kiến trúc.
- `03-CANONICAL-BOUNDARIES.md` — ranh giới canonical.
- `04-RUNTIME-LINEAGE-AND-MODULES.md` — lineage runtime/module.
- `05-HISTORICAL-RESEARCH-AND-CONFLICTS.md` — nghiên cứu cũ và các điểm mâu thuẫn cần quarantine.
- `09-3A-v3.4-CURRENT-ANCHOR.md` — architectural anchor hiện tại.

Các số mục còn trống **không có nghĩa là thiếu nội dung**; chúng là các ngăn dành cho những nhóm tài liệu chưa được rót xong. Tiếp tục tìm nguồn trước khi đóng Origin.

## Nguyên tắc biên soạn

1. Nguồn cũ không bị xóa chỉ vì nguồn mới thay thế nó.
2. Quy tắc đã supersede phải ghi rõ lịch sử và lý do.
3. Công thức nghiên cứu chưa được xác nhận không được nâng thành canonical bằng cách viết lại.
4. Khi hai nguồn mâu thuẫn, giữ cả hai, ghi quyết định hợp nhất hoặc đánh dấu unresolved.
5. Mọi implementation chỉ là một cách thực thi khung tham chiếu.
6. Dữ liệu, calibration và ground truth có thể làm thay đổi trạng thái quan sát; không coi một snapshot hay một nhãn là bản thể cố định.

## Đích cuối

`ORIGIN đầy đủ → Canonical Contract → Adapter → Implementation branches → Validation Suite → Production Engine`.
