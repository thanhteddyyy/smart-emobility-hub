# Danh sách lỗi UI / Logic & Phân công khắc phục

- **Ngày ghi nhận**: 20/11/2026
- **Cập nhật trạng thái**: 21/11/2026 (Đã hoàn thành sau merge TV1 + TV2 + TV4 + sửa TV3/TV4)

---

## 1. Danh sách vấn đề & phân công chi tiết (#0 – #20)

| STT | Phân hệ | Mô tả vấn đề & yêu cầu sửa | Phụ trách chính | Phối hợp | File liên quan | Trạng thái |
|---|---|---|---|---|---|---|
| **#0** | Dữ liệu & Toàn hệ thống | Cần số liệu rõ ràng cho từng xe, cổng sạc, chỗ đỗ trong từng Hub; mỗi Hub có quy mô khác nhau; số liệu trống/tổng thay đổi đồng bộ khi người dùng thao tác. | **TV4** | TV1, TV2, TV3 | `data/seed.json`, `scripts/generate_seed.py`, `services/` | Đã xong |
| **#1** | Student (Tìm kiếm) | Thêm/đảm bảo lựa chọn **Ký túc xá khu B** khi chọn địa điểm đặt/bắt đầu (`DEFAULT_RADIUS_KM = 10.0`). | **TV4** | **TV1** | `data/seed.json`, `config.py`, `templates/student/hinh1_MapScreen.html`, `static/tv1/search.js` | Đã xong |
| **#2** | Student (Bản đồ H1) | Thanh thông tin trạm mặc định ẩn, chỉ hiện khi tìm/chọn địa điểm giống Google Maps. | **TV1** | — | `templates/student/hinh1_MapScreen.html`, `static/tv1/student.css`, `static/tv1/search.js` | Đã xong |
| **#3** | Student (Đặt chỗ H2–H5) | Sửa nút *Confirm reservation* & modal lỗi/thành công cho cả 2 luồng còn chỗ và hết xe/chỗ. | **TV1**, **TV4** | — | `static/tv1/search.js`, `templates/student/_booking_modal.html`, `services/booking_service.py`, `blueprints/api/routes.py` | Đã xong |
| **#4** | Student (Tìm kiếm H1) | Bỏ bộ lọc không có tác dụng khỏi giao diện bản đồ. | **TV1** | — | `templates/student/hinh1_MapScreen.html`, `static/tv1/search.js` | Đã xong |
| **#5** | Student (Tìm kiếm H1) | Thanh tìm kiếm gợi ý đúng 5 nơi đặt trạm của hệ thống (hỗ trợ không dấu). | **TV1** | TV4 | `templates/student/hinh1_MapScreen.html`, `static/tv1/search.js` | Đã xong |
| **#6** | Student (Bản đồ H1) | Xác định vị trí user ban đầu (chấm cố định tại **ĐH Bách khoa CS2**). | **TV1** | TV4 | `static/tv1/search.js`, `config.py` | Đã xong |
| **#7** | Student (Bản đồ H1) | Vẽ tuyến đường gợi ý từ BK CS2 đến trạm chọn + link chỉ đường đi bộ. | **TV1** | — | `static/tv1/search.js`, `templates/student/hinh1_MapScreen.html` | Đã xong |
| **#8** | Student (Chuyến đi & Sạc) | Chưa đặt xe/sạc thì tab **Chuyến đi** & **Sạc** không hiện dữ liệu giả. | **TV4** | **TV2** | `blueprints/student/routes.py`, `templates/student/pickup.html`, `templates/student/ride.html`, `templates/student/charging_slot.html` | Đã xong |
| **#9** | Operator (Tổng quan & Cảnh báo) | Đồng bộ mức sử dụng vs mức độ nghiêm trọng cảnh báo (`HIGH`/`MEDIUM`/`LOW`) trên cả seed, `alert_service.py`, `alerts.html` và `overview.html`. | **TV4** | **TV3** | `services/alert_service.py`, `scripts/generate_seed.py`, `templates/operator/overview.html`, `templates/operator/alerts.html` | Đã xong |
| **#10** | Student (Chi tiết Hub UC2) | Cố định chiều cao khung `.phone` và giới hạn cuộn danh sách xe trong `resource.html`. | **TV1**, **TV2** | — | `templates/base_mobile.html`, `static/tv1/student.css`, `static/css/student_web.css`, `templates/student/resource.html` | Đã xong |
| **#11** | Student (Đặt xe/chỗ) | Chặn chọn thời gian đặt xe/chỗ/sạc trong quá khứ cả ở UI và Backend. | **TV1**, **TV4** | — | `templates/student/hinh2_ReservationConfirm.html`, `static/tv1/search.js`, `services/booking_service.py`, `services/charging_service.py` | Đã xong |
| **#12** | Operator (Mô phỏng What-if) | Tính toán What-if theo quy mô 700 xe, biến thiên theo thời tiết, `timeFrame` & `scenario`, có đầy đủ dropdown trên UI. | **TV4** | **TV3** | `services/simulation_service.py`, `blueprints/operator/routes.py`, `templates/operator/simulation.html` | Đã xong |
| **#13** | Dữ liệu & Toàn hệ thống | Tăng quy mô tài nguyên lên 110–200 xe/chỗ/cổng mỗi Hub (700 xe, 830 chỗ đỗ, 220 cổng sạc), hiển thị rõ `trống / tổng`. | **TV4** | TV3 | `scripts/generate_seed.py`, `data/seed.json`, `templates/operator/resources.html`, `templates/operator/overview.html` | Đã xong |
| **#14** | Operator (Sự cố & Cảnh báo) | Bổ sung lý do sự cố đa dạng trên seed & hiển thị cột phân loại/lý do + gợi ý lý do nhanh + sự cố cần xử lý trên Dashboard. | **TV4**, **TV3** | — | `scripts/generate_seed.py`, `templates/operator/incidents.html`, `templates/operator/incident_detail.html`, `templates/operator/overview.html` | Đã xong |
| **#15** | Operator (Demo bắt buộc UC16) | Hiển thị khung **Nhật ký gói dữ liệu trễ (`PACKET_LOG`)** đẹp gọn dưới bảng Hub (đủ song ngữ VN/EN) + `scripts/packet_demo.py`. | **TV4**, **TV3** | — | `services/realtime_service.py`, `blueprints/api/routes.py`, `blueprints/operator/routes.py`, `templates/operator/overview.html`, `scripts/packet_demo.py` | Đã xong |
| **#16** | Student (Chuyến đi H7) | Cập nhật `%` pin & 5 vạch pin realtime mỗi 5 giây tại `ride.html`. | **TV4**, **TV2** | — | `blueprints/api/routes.py`, `templates/student/ride.html` | Đã xong |
| **#17** | Toàn hệ thống (NFR05) | Hiện thông báo cảnh báo mất kết nối realtime ở cả khung Student và Dashboard Operator. | **TV4** | TV1, TV3 | `static/js/realtime.js`, `templates/base_mobile.html` | Đã xong |
| **#18** | Operator (Tổng quan UC8) | Tự động đổi class màu cột `Cảnh báo an toàn` (`safetyWarning`) khi `ehub:state` đổi trạng thái. | **TV3**, **TV4** | — | `templates/operator/overview.html` | Đã xong |
| **#19** | Operator (Hiệu năng danh sách lớn) | Bọc khung cuộn cố định chiều cao (sticky header) + tìm kiếm nhanh & đếm số dòng cho `resources.html`, `dispatch.html`, `incidents.html`. | **TV3** | — | `templates/operator/resources.html`, `templates/operator/dispatch.html`, `templates/operator/incidents.html`, `static/css/dashboard.css` | Đã xong |
| **#20** | Tài liệu & Script (TV4) | Điền đầy đủ tên lớp Control trong `docs/ARCHITECTURE.md`, bỏ `_TODO_` trong `README.md`, cập nhật `scripts/reset_data.py`. | **TV4** | — | `docs/ARCHITECTURE.md`, `README.md`, `scripts/reset_data.py` | Đã xong |

---

## 2. Tóm tắt khối lượng đã hoàn thành theo từng thành viên (TV1 – TV4)

| Thành viên | Các mục đã xử lý | Ghi chú kiểm tra tiếp theo |
|---|---|---|
| **TV1** | **#1–#7, #10, #11, #17** | Chạy kiểm tra lại luồng tìm 5 trạm, chấm BK CS2, đặt xe & đặt chỗ đỗ trên trình duyệt. |
| **TV2** | **#10, #16** | Chạy kiểm tra cuộn danh sách xe ở `resource.html` và `%` pin nhảy realtime ở `ride.html`. |
| **TV3** | **#9 (UI), #12 (UI), #13 (UI), #14 (UI), #15 (UI), #18, #19** | Kiểm tra Dashboard Operator (`overview`, `resources`, `alerts`, `incidents`, `dispatch`, `simulation`, `schedule`) ở cả Sáng/Tối & VN/EN. |
| **TV4** | **#0, #1, #3, #8, #9, #11–#17, #20** | Còn bước cuối cùng: cùng nhóm gộp nhánh `origin/phong-tv5` (TV5) và rà soát checklist trước khi đóng gói `.zip`. |
