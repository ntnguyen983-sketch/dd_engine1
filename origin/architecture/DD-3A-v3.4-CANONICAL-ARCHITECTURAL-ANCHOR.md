# DD-3A v3.4 — CANONICAL ARCHITECTURAL ANCHOR

## Trục biểu đạt

**Định danh | Định lượng | Định tính**

Duyên Dịch không mô hình hóa vật thể hay chân lý cố định. Nó mô hình hóa sự biến đổi được quan sát trong một hệ mở: cái gì được quy chiếu, dữ liệu nào được đo, và mẫu hình nào xuất hiện từ dữ liệu đó.

## N(n)

Mọi hiện tượng được quy chiếu qua các dòng quan sát N_i, Observation O_{i,k}, Interaction Event I_m, Space V_k và Time t_k. Ký hiệu chỉ là quy chiếu; không đồng nghĩa với một bản ngã hay bản chất bất biến.

## v3.0 ↔ 3A

- v3.0 / Structural Domain: cấu trúc, quẻ, hào vị, quan hệ cấu trúc, các ánh xạ định lượng/định tính đã được xác lập.
- 3A / Dynamic Domain: chuỗi sự kiện, dòng lực, topology, nhịp, lặp lại và chuyển dịch.
- Hai tầng cùng vận hành trên ontology N(n), không phải hai ontology cạnh tranh.

## Space ≠ Entity

Điểm nghẽn không gian B(V_k) là thuộc tính của nút không gian:

`B(V_k) = F_in(V_k) - F_out(V_k)`

Không được gán B(V_k) trực tiếp thành thuộc tính bản thể của N_i chỉ vì N_i đang ở V_k.

## Ba đại lượng phải tách

- `event_count`: số sự kiện mà thực thể tham gia.
- `cycle_count`: số chu trình có hướng khép kín trong topology.
- `K_rep`: số lần một motif/quan hệ cụ thể lặp lại theo chuỗi thời gian.

`K_rep` không được dùng thay cho `cycle_count`.

## Nhịp

`σ_rhythm` được tính từ các khoảng thời gian của cùng một quan hệ/motif sự kiện. Timestamp phải được xử lý bằng ISO 8601 và quy đổi theo thời gian tuyệt đối, không tách chuỗi thủ công.

## Canonical boundary

Khung kiến trúc giữ ontology và nguyên tắc phân biệt các đại lượng. Implementation có thể dùng Python, Rust, C++, Go hoặc công nghệ khác. L4 Calibration và Ground Truth là vòng phản hồi mở; không được tự chế công thức để lấp giá trị còn thiếu.

## Tinh thần bất nhị / vô ngã / vô thường

Không gắn nhãn giá trị như một bản chất cố định cho đối tượng. Định tính chỉ là mô tả mẫu hình được quy chiếu về định lượng và bằng chứng tại một cửa sổ quan sát; khi điều kiện đổi, mô tả có thể đổi.
