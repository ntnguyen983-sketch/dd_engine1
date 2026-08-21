# Đạo – Duyên – Dịch: lineage

## 1. Nền tảng

Duyên Dịch bắt đầu từ cách nhìn rằng hiện tượng không tồn tại như các vật thể độc lập, bất biến. Cái được quan sát là một lát cắt của một dòng điều kiện đang vận động.

- **Đạo**: quy luật vận hành của tương quan/duyên sinh và vận động/vô thường.
- **Duyên**: mẫu hình xuất hiện từ cấu trúc điều kiện tương quan; không tồn tại biệt lập.
- **Dịch**: sự vận động, biến đổi, tiến hóa hoặc tiêu biến của các mẫu hình khi tập điều kiện nền thay đổi.

Các tài liệu v2.3.6/v2.3.7 đã lượng hóa hướng này và đặt nguyên tắc rằng quẻ không quyết định sự việc; quẻ là một snapshot của trạng thái tại sát-na quan sát. fileciteturn30file0L11-L25 fileciteturn30file1L51-L70

## 2. Vô thường và vô ngã trong kiến trúc

Mô hình không nên gán bản chất cố định cho node. Trạng thái chỉ có nghĩa trong điều kiện, vị trí và thời điểm cụ thể. Tài liệu v2.8.7+ Rev.A ghi rõ quẻ là snapshot tại t0 và không gán bản chất cố định cho node; runtime phải giữ deterministic/forward-only và không dùng quan sát mới để sửa ngược trạng thái đã khóa. fileciteturn30file2L82-L109

Đây là lý do kiến trúc hiện tại chuyển từ các nhãn bản thể mạnh sang ba phương thức biểu đạt:

1. **Định danh (ID)** — ký hiệu quy chiếu để theo dõi một luồng quan sát.
2. **Định lượng (Quantity)** — số đo của quan sát, quan hệ, lực, thời gian, không gian, nhịp…
3. **Định tính (Quality)** — mẫu hình được mô tả từ các đại lượng và bằng chứng; không mặc định là phán xét tốt/xấu.

Ba lớp này không phải ba bản thể. Chúng là ba cách nói về dữ liệu và biến đổi của cùng một hệ mở.

## 3. Quẻ và hệ quy chiếu

Trong lineage cũ, quẻ là bộ mã hóa snapshot/trạng thái chứ không phải tác nhân nhân quả tuyệt đối. v2.3.6 nêu rõ quẻ chỉ là snapshot của Dòng và dự báo nhằm đánh giá xu hướng chuyển hóa, không xác định kết quả tất định. fileciteturn29file14L563-L584

## 4. Truy vết và điều kiện

Một kết luận phải truy vết được về dữ liệu và các toán tử đã dùng. Các nguyên tắc UK1–UK8 của v2.3.6 nhấn mạnh semantic independence, primitive completeness, observer equivalence, information preservation, bidirectional traceability, fusion neutrality, decoder isolation và extensibility. fileciteturn29file9L394-L409

## 5. Kết quả kiến trúc hiện tại

Không còn xem `Entity`, `Actor`, `Object`, `Duyên` hay bất kỳ nhãn nào là bản chất cố định. Chúng chỉ là định danh/khung quy chiếu phục vụ quan sát.

Chuỗi tổng quát:

`Quan sát → Định danh → Định lượng → Quan hệ/biến đổi → Mẫu hình định tính → kiểm chứng bằng bằng chứng/ground truth → cập nhật cho trạng thái tiếp theo.`

Không có bước nào được phép biến một mô tả tạm thời thành bản thể vĩnh viễn.
