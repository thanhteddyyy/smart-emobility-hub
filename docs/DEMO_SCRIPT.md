# Kịch bản demo _(TV5 hoàn thiện; video 8–10 phút)_

## Chuẩn bị trước khi quay
1. Chạy lại server để dữ liệu về trạng thái gốc:
   ```bash
   python scripts/reset_data.py
   python app.py
   ```
2. Mở trình duyệt ở `http://127.0.0.1:5000` (cửa sổ 1: giao diện mobile/sinh viên; cửa sổ 2 hoặc ẩn danh: giao diện Operator).
3. Mở sẵn 1 terminal phụ để chạy `python scripts/race_demo.py` và gửi gói tin mẫu vào `/api/telemetry` ở Phần 8.

---

## Bảng phân bổ thời lượng

| # | Nội dung | Tài khoản | Use case | Thời lượng |
|---|---|---|---|---|
| 1 | Tìm Hub trên bản đồ, xem chi tiết | Chưa đăng nhập | UC1, UC2 | 1:00 |
| 2 | Đăng nhập, đặt xe, nhận xe, trả xe | Sinh viên | UC17, UC3, UC5, UC6 | 1:45 |
| 3 | Đặt chỗ đỗ, đăng ký sạc | Sinh viên | UC4, UC7 | 1:00 |
| 4 | Dashboard, tài nguyên, cảnh báo quá tải | Vận hành | UC8, UC9, UC10 | 1:30 |
| 5 | Điều phối xe, xử lý sự cố | Vận hành | UC11, UC12 | 1:30 |
| 6 | Lịch sạc, What-if → áp dụng sang điều phối | Vận hành | UC13, UC14 | 1:15 |
| 7 | Đổi Sáng/Tối, VN/EN khi đang nhập form | Bất kỳ | UC15 | 0:30 |
| 8 | 3 demo bắt buộc: đặt trùng xe, gói trễ, cô lập mô phỏng | Terminal + Web | UC3, UC16, UC14 | 1:30 |
| | **Tổng thời lượng dự kiến** | | | **~10:00** |

---

## Chi tiết từng phần (Bước bấm & Lời thoại)

### Phần 1: Tìm Hub trên bản đồ & xem chi tiết (UC1, UC2 — 1:00)
- **Bước bấm:**
  1. Truy cập `http://127.0.0.1:5000/student/search` (chưa đăng nhập).
  2. Quan sát bản đồ Leaflet khu ĐHQG-HCM với 5 marker Hub và thẻ **Trạm gần nhất** trượt từ dưới lên.
  3. Nhập bán kính `2` km, pin tối thiểu `30%`, bấm **Tìm**.
  4. Thử nhập bán kính `0.1` km hoặc pin `99%` để minh họa trạng thái rỗng (`search.empty`).
  5. Bấm **Xem chi tiết** trên một Hub (hoặc `/student/resource`) để xem trạng thái xe, chỗ đỗ và cảnh báo dữ liệu cũ nếu có.
- **Lời thoại:** *"Chào thầy/cô, đây là hệ thống E-Hub điều phối xe điện tại ĐHQG-HCM. Ở vai trò Sinh viên, không cần đăng nhập vẫn có thể tìm Hub gần nhất trên bản đồ Leaflet, lọc theo bán kính và mức pin tối thiểu, cũng như xem chi tiết tình trạng từng xe và chỗ đỗ."*

### Phần 2: Đăng nhập SSO, đặt xe, nhận xe, trả xe (UC17, UC3, UC5, UC6 — 1:45)
- **Bước bấm:**
  1. Bấm **Đăng nhập** → chọn tài khoản demo `student@hcmut.edu.vn` / `123456` → bấm **Đăng nhập**. (Nhắc nhanh trường hợp nhập sai mật khẩu báo lỗi `INVALID_CREDENTIALS`).
  2. Tại `/student/search`, chọn Hub → mở modal đặt xe (tab **E-bike**) → xác nhận đặt xe (giữ chỗ 15 phút).
  3. Chuyển sang `/student/pickup`: kiểm tra mã đặt xe, thông tin xe, thanh pin → bấm **Xác nhận nhận xe**.
  4. Màn hình chuyển sang `/student/ride` (bản đồ tuyến đi, pin cập nhật realtime) → bấm **Trả xe**.
  5. Tại `/student/return`: chọn Hub trả còn chỗ trống → xác nhận → hiện màn hình hoàn tất `/student/returned`.
- **Lời thoại:** *"Tiếp theo, sinh viên đăng nhập qua trang SSO giả lập, đặt trước một xe điện với thời gian giữ 15 phút, xác nhận nhận xe tại Hub, theo dõi chuyến đi trên bản đồ và thực hiện trả xe tại Hub đích."*

### Phần 3: Đặt chỗ đỗ & đăng ký sạc (UC4, UC7 — 1:00)
- **Bước bấm:**
  1. Mở lại modal đặt chỗ tại `/student/search`, chuyển sang tab **Parking** → chọn Hub và xác nhận đặt chỗ đỗ.
  2. Chuyển sang tab **Sạc** (`/student/charging`) → chọn khung giờ/cổng sạc còn trống → rà soát xác nhận.
  3. Minh họa trường hợp Hub hết cổng sạc → hệ thống gợi ý Hub sạc gần nhất còn cổng trống.
- **Lời thoại:** *"Ngoài thuê xe, sinh viên có thể đặt trước chỗ đỗ xe tại Hub và đăng ký khung giờ sạc pin. Nếu Hub hiện tại hết cổng sạc, hệ thống sẽ tự động gợi ý Hub gần nhất còn cổng khả dụng."*

### Phần 4: Dashboard Vận hành, tài nguyên & cảnh báo quá tải (UC8, UC9, UC10 — 1:30)
- **Bước bấm:**
  1. Thử truy cập `/operator/` bằng tài khoản Sinh viên → hệ thống chặn và chuyển về `/denied` (RBAC NFR10).
  2. Đăng xuất và đăng nhập lại bằng tài khoản `operator@ehub.vn` / `123456`.
  3. Tại `/operator/overview`: chỉ 4 thẻ KPI tổng quan, bảng mức sử dụng Hub, thử ô tìm kiếm/bộ lọc.
  4. Bấm **Xem tài nguyên** của một Hub (`/operator/resources/H1`) để xem danh sách xe và cổng sạc.
  5. Vào `/operator/alerts`: chọn một cảnh báo quá tải ở bảng trái, xem chi tiết bên phải, bấm **Xử lý xong** (hoặc chuyển sang Điều phối).
- **Lời thoại:** *"Ở phân hệ Đơn vị vận hành, tài khoản sinh viên sẽ bị chặn theo phân quyền RBAC. Khi đăng nhập bằng tài khoản Operator, hệ thống hiển thị Dashboard tổng quan mạng lưới tự cập nhật mỗi 5 giây, chi tiết tài nguyên từng Hub và danh sách cảnh báo quá tải."*

### Phần 5: Điều phối xe & xử lý sự cố (UC11, UC12 — 1:30)
- **Bước bấm:**
  1. Vào `/operator/dispatch`: chọn Hub nguồn, tick chọn xe sẵn sàng, chọn Hub đích còn chỗ → bấm **Điều phối xe** → quan sát lệnh điều phối mới ở bảng bên dưới.
  2. Vào `/operator/incidents`: chọn một sự cố ưu tiên cao → bấm vào chi tiết (`/operator/incidents/<id>`).
  3. Bấm **Tạm ngưng vận hành tài nguyên** → trạng thái sự cố chuyển `IN_PROGRESS` và ghi AuditLog.
  4. Chọn trạng thái khôi phục `AVAILABLE`, nhập ghi chú → bấm **Cập nhật tiến độ** → sự cố chuyển `RESOLVED`.
- **Lời thoại:** *"Operator có thể điều phối xe từ Hub thừa sang Hub thiếu trực tiếp trên bản đồ mạng lưới, đồng thời tiếp nhận sự cố, tạm ngưng tài nguyên lỗi để đảm bảo an toàn và cập nhật tiến độ khôi phục."*

### Phần 6: Lịch sạc & What-if → áp dụng sang điều phối (UC13, UC14 — 1:15)
- **Bước bấm:**
  1. Vào `/operator/schedule`: xem danh sách đề xuất lịch sạc ưu tiên xe pin thấp và phê duyệt lịch.
  2. Vào `/operator/simulation`: điều chỉnh thanh trượt **Nhu cầu sinh viên** (`+40%`), **Xe điện sẵn sàng** (`-5`), chọn thời tiết **Mưa lớn** → bấm chạy mô phỏng.
  3. Quan sát biểu đồ Chart.js so sánh cung/cầu 9 giờ và khung giờ thiếu hụt cao nhất.
  4. Bấm **Áp dụng sang Điều phối** → chuyển sang `/operator/dispatch` với Hub nguồn/đích và số lượng xe đã được điền sẵn.
- **Lời thoại:** *"Hệ thống hỗ trợ lập lịch sạc thông minh và mô phỏng What-if với các biến số thời tiết, nhu cầu sinh viên để dự báo thiếu hụt theo giờ, sau đó chuyển thẳng đề xuất sang màn hình Điều phối."*

### Phần 7: Đổi Sáng/Tối & VN/EN khi đang nhập form (UC15 — 0:30)
- **Bước bấm:**
  1. Mở form bất kỳ (ví dụ ô tìm kiếm `/student/search` hoặc form mô phỏng `/operator/simulation`), gõ sẵn một giá trị vào ô nhập.
  2. Bấm nút gạt **Sáng / Tối** và **VN / EN** trên thanh trên cùng.
  3. Chỉ rõ giao diện đổi màu và ngôn ngữ ngay lập tức, **không tải lại trang** và dữ liệu đang nhập trong form vẫn giữ nguyên.
- **Lời thoại:** *"Người dùng có thể chuyển đổi chế độ Sáng/Tối và ngôn ngữ Việt/Anh bất cứ lúc nào. Toàn bộ giao diện cập nhật tức thì qua CSS variables và từ điển i18n mà không làm mất dữ liệu đang nhập."*

### Phần 8: Ba demo bắt buộc (UC3, UC16, UC14 — 1:30)
- **Bước bấm & Lời thoại:**
  1. **Race condition (UC3):** Chạy `python scripts/race_demo.py` trên terminal → 2 luồng đồng thời đặt cùng xe `EB-201`, chỉ 1 thành công, luồng còn lại nhận `VEHICLE_CONFLICT`.
  2. **Lọc gói dữ liệu trễ (UC16):** Gửi gói tin có `timestamp` cũ hơn hiện tại vào `POST /api/telemetry` → gói tin bị bỏ qua (`OUTDATED_PACKET`), không ghi đè dữ liệu mới hơn.
  3. **Cô lập dữ liệu mô phỏng (UC14):** Ghi nhớ tổng số xe sẵn sàng trên `/operator/overview`, chạy mô phỏng What-if với biến động cực đoan tại `/operator/simulation`, quay lại `/operator/overview` → số liệu thực tế hoàn toàn không thay đổi.
