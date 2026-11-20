# Danh sách lỗi UI / Logic & Phân công khắc phục

- **Ngày ghi nhận**: 20/11/2026
- **Nguồn**: Rà soát kiểm thử thực tế giao diện Student & Operator

---

## 1. Danh sách vấn đề & phân công chi tiết (#0 – #20)

| STT | Phân hệ | Mô tả vấn đề & yêu cầu sửa | Phụ trách chính | Phối hợp | File liên quan | Trạng thái |
|---|---|---|---|---|---|---|
| **#0** | Dữ liệu & Toàn hệ thống | Cần số liệu rõ ràng cho từng xe, cổng sạc, chỗ đỗ trong từng Hub; mỗi Hub có quy mô khác nhau (vd: 50 xe / 30 cổng sạc / 100 chỗ đỗ); số liệu trống/tổng thay đổi đồng bộ khi người dùng thao tác. | **TV4** | TV1, TV2, TV3 | `data/seed.json`, `data/mock_data.py`, `services/` | Chưa làm |
| **#1** | Student (Tìm kiếm) | Thêm/đảm bảo lựa chọn **Ký túc xá khu B** khi chọn địa điểm đặt/bắt đầu. *(Lưu ý: `H3 – KTX Khu B` đã có sẵn `ACTIVE` trong `data/seed.json` cách `DEFAULT_LOCATION` ~2.28 km nhưng bị lọc mất do `config.py` đặt `DEFAULT_RADIUS_KM = 2.0`; cần nâng `DEFAULT_RADIUS_KM` hoặc bỏ lọc bán kính để hiện đủ 5 Hub).* | **TV4** | **TV1** | `data/seed.json`, `config.py`, `templates/student/hinh1_MapScreen.html`, `static/tv1/search.js` | Chưa làm |
| **#2** | Student (Bản đồ H1) | Thanh "Trạm gần nhất" không kéo lên/xuống được → sửa thành chỉ hiện khi tìm/chọn địa điểm giống Google Maps, mặc định chỉ hiển thị bản đồ. | **TV1** | — | `templates/student/hinh1_MapScreen.html`, `static/tv1/student.css`, `static/tv1/search.js` | Chưa làm |
| **#3** | Student (Đặt chỗ H2–H5) | Bấm *Confirm reservation* bị từ chối và 2 nút đều hiện *Back to map*; xử lý rõ 2 luồng tính toán đúng: còn xe/chỗ thì cho đặt thành công, hết xe/chỗ thì từ chối rõ ràng. | **TV1**, **TV4** | — | `static/tv1/search.js`, `templates/student/_booking_modal.html`, `services/booking_service.py`, `blueprints/api/routes.py` | Chưa làm |
| **#4** | Student (Tìm kiếm H1) | Bộ lọc không có tác dụng → bỏ khỏi giao diện. | **TV1** | — | `templates/student/hinh1_MapScreen.html`, `static/tv1/search.js` | Chưa làm |
| **#5** | Student (Tìm kiếm H1) | Sửa thành thanh tìm kiếm gợi ý đúng 5 nơi đặt trạm của hệ thống. | **TV1** | TV4 | `templates/student/hinh1_MapScreen.html`, `static/tv1/search.js` | Chưa làm |
| **#6** | Student (Bản đồ H1) | Xác định vị trí user ban đầu (chấm cố định tại **ĐH Bách khoa CS2**). | **TV1** | TV4 | `static/tv1/search.js`, `config.py` | Chưa làm |
| **#7** | Student (Bản đồ H1) | Khi chọn địa điểm thì gợi ý/vẽ tuyến đường từ vị trí mặc định (BK CS2) đến trạm muốn đến *(optional)*. | **TV1** | — | `static/tv1/search.js` | Chưa làm |
| **#8** | Student (Chuyến đi & Sạc) | Khi chưa đặt xe/sạc thì tab **Chuyến đi** & **Sạc** không được tự hiện dữ liệu giả. | **TV4** | **TV2** | `blueprints/student/routes.py`, `templates/student/pickup.html`, `templates/student/ride.html`, `templates/student/charging_slot.html` | Chưa làm |
| **#9** | Operator (Tổng quan & Cảnh báo) | Tại một Hub, mức sử dụng cao hơn nhưng mức độ nghiêm trọng lại thấp hơn → sửa lại logic tính & phân mức cảnh báo. | **TV4** | **TV3** | `services/alert_service.py`, `data/seed.json`, `templates/operator/overview.html`, `templates/operator/alerts.html` | Chưa làm |
| **#10** | Student (Chi tiết Hub UC2) | Bấm xem chi tiết Hub làm khung bị kéo dài ra → cố định chiều cao frame dù dữ liệu nhiều cỡ nào (cuộn bên trong). | **TV1**, **TV2** | — | `templates/base_mobile.html`, `static/tv1/student.css`, `static/css/student_web.css`, `templates/student/resource.html` | Chưa làm |
| **#11** | Student (Đặt xe/chỗ) | Thời gian đặt xe/chỗ còn cho phép chọn trong quá khứ → chặn cả UI và Backend. | **TV1**, **TV4** | — | `templates/student/hinh2_ReservationConfirm.html`, `static/tv1/search.js`, `services/booking_service.py`, `services/charging_service.py` | Chưa làm |
| **#12** | Operator (Mô phỏng What-if) | Dữ liệu What-if chạy cả 5 trường hợp đều cho ra giống nhau (cố định 12 giờ cao điểm) → sửa tính toán biến thiên theo kịch bản & khung giờ. | **TV4** | **TV3** | `services/simulation_service.py`, `templates/operator/simulation.html` | Chưa làm |
| **#13** | Dữ liệu & Toàn hệ thống | Tăng số lượng tài nguyên hiện có của mỗi Hub lên ~100–200 xe / cổng sạc / chỗ đỗ *(gộp xử lý chung với #0)*. | **TV4** | TV3 | `data/seed.json`, `data/mock_data.py`, `templates/operator/resources.html`, `templates/operator/dispatch.html` | Chưa làm |
| **#14** | Operator (Sự cố & Cảnh báo) | Bổ sung các lý do sự cố đa dạng trên UI (hiện tại chủ yếu chỉ có quá tải: thêm hỏng xe, lỗi pin, hỏng cổng sạc, mất kết nối IoT...). | **TV4**, **TV3** | — | `data/seed.json`, `services/incident_service.py`, `templates/operator/incidents.html`, `templates/operator/incident_detail.html`, `templates/operator/alerts.html`, `templates/operator/overview.html` | Chưa làm |
| **#15** | Operator (Demo bắt buộc UC16) | Hiển thị khung/bảng nhỏ Nhật ký gói dữ liệu trễ (`PACKET_LOG`) trên Dashboard Operator + thêm script demo gửi gói trễ vào `/api/telemetry`. | **TV4**, **TV3** | — | `services/realtime_service.py`, `blueprints/api/routes.py`, `blueprints/operator/routes.py`, `templates/operator/overview.html`, `scripts/` | Chưa làm |
| **#16** | Student (Chuyến đi H7) | Cập nhật `%` pin & thanh pin realtime mỗi 5 giây tại `ride.html` (trả thêm `vehicles` trong `/api/state` và bắt sự kiện `ehub:state`). | **TV4**, **TV2** | — | `blueprints/api/routes.py`, `templates/student/ride.html` | Chưa làm |
| **#17** | Toàn hệ thống (NFR05) | Hiện thông báo nhỏ cảnh báo mất kết nối realtime khi `/api/state` lỗi thay vì chỉ `console.warn`. | **TV4** | TV1, TV3 | `static/js/realtime.js` | Chưa làm |
| **#18** | Operator (Tổng quan UC8) | Tự động cập nhật lại class màu (`text-danger` / `text-warning`) của cột `Cảnh báo an toàn` (`safetyWarning`) khi `ehub:state` đổi trạng thái. | **TV3** | — | `templates/operator/overview.html` | Chưa làm |
| **#19** | Operator (Hiệu năng danh sách lớn) | Bọc khung cuộn cố định chiều cao hoặc lọc theo Hub mặc định ở `resources.html` và `dispatch.html` để không bị dài trang/lag khi tăng lên 100–200 xe/Hub (500–1000 xe toàn mạng). | **TV3** | — | `templates/operator/resources.html`, `templates/operator/dispatch.html`, `static/css/dashboard.css` | Chưa làm |
| **#20** | Tài liệu & Script (TV4) | Điền nốt các dòng `_TODO_` tên lớp Control trong `docs/ARCHITECTURE.md` (UC7, UC9–UC16), xóa dòng `_TODO_` còn sót trong `README.md`, và *(tùy chọn)* thêm kịch bản mẫu `--scenario hub_full` trong `scripts/reset_data.py`. | **TV4** | — | `docs/ARCHITECTURE.md`, `README.md`, `scripts/reset_data.py` | Chưa làm |

---

## 2. Tóm tắt khối lượng theo từng thành viên (TV1 – TV4)

| Thành viên | Phụ trách chính / Cùng làm | Phối hợp | Tóm tắt đầu việc |
|---|---|---|---|
| **TV1** | **#2, #3, #4, #5, #6, #7, #10, #11** | **#0, #1, #17** | Ẩn thanh trạm mặc định trên bản đồ; bỏ bộ lọc; search bar gợi ý đúng 5 trạm (gồm KTX khu B khi nới/bỏ lọc bán kính); chấm vị trí BK CS2 & vẽ tuyến gợi ý; sửa 2 nút + luồng modal đặt chỗ; khóa chiều cao khung `.phone` cố định; chặn chọn thời gian quá khứ ở UI; phối hợp cảnh báo mất kết nối realtime trên khung Student. |
| **TV2** | **#10, #16** | **#0, #8** | Giới hạn chiều cao & bật thanh cuộn danh sách xe trong `resource.html`; bắt `ehub:state` để cập nhật `%` pin & thanh pin realtime mỗi 5 giây trên `ride.html`; phối hợp hiển thị đúng `trống/tổng` và rà soát trạng thái trống trên các trang Chuyến đi & Sạc (H6–H12). |
| **TV3** | **#14, #15, #18, #19** | **#0, #9, #12, #13, #17** | Hiển thị đa dạng loại & lý do sự cố trên Dashboard Operator (`overview`, `alerts`, `incidents`, `incident_detail`); thêm khung/bảng hiển thị `PACKET_LOG` (lọc gói trễ UC16); cập nhật màu cột `safetyWarning` theo `ehub:state`; bọc khung cuộn / lọc Hub mặc định ở `resources.html` & `dispatch.html` để chịu tải 500–1000 xe; kiểm tra badge mức nghiêm trọng, biểu đồ What-if & cảnh báo mất kết nối. |
| **TV4** | **#0, #1, #3, #8, #9, #11, #12, #13, #14, #15, #16, #17, #20** | **#5, #6** | Tăng quy mô `seed.json` lên 100–200 xe/cổng/chỗ khác nhau theo kích thước từng Hub và nới `DEFAULT_RADIUS_KM` để hiện đủ KTX khu B `ACTIVE`; đảm bảo tab Chuyến đi/Sạc không hiện dữ liệu giả khi chưa đặt; sửa logic đặt xe/chỗ 2 luồng và chặn thời gian quá khứ ở backend; sửa logic mức sử dụng vs độ nghiêm trọng cảnh báo; sửa tính toán What-if theo nhiều khung giờ; thêm đa dạng loại sự cố; hoàn thiện API/script demo gói trễ `PACKET_LOG`, trả `vehicles` trong `/api/state`, cảnh báo mất kết nối NFR05 trong `realtime.js` và điền nốt `_TODO_` trong `ARCHITECTURE.md` / `README.md` / `reset_data.py`. |

