# Nhật ký sửa lỗi tích hợp sau khi merge các nhánh (TV1)

- **Người thực hiện**: Thành viên 1 (TV1)
- **Ngày**: 20/11/2026
- **Ngữ cảnh**: Chạy kiểm thử toàn bộ dự án (`pytest -v`) trên nhánh `main` sau khi gộp code của các nhánh `feat/operator`, `tv1_Student_Search&Reservation`, `tv2-student-ride` và `TV4`.
- **Kết quả trước khi sửa**: `29 passed, 9 xfailed, 15 failed, 5 errors` (server không khởi động được).
- **Kết quả sau khi sửa**: `50 passed, 8 xfailed, 0 failed, 0 errors` (mọi màn hình Student & Operator đều chạy ổn định).

---

## Chi tiết các lỗi đã phát hiện và khắc phục

### 1. Lỗi trùng route làm crash server khi khởi động (5 `ERROR` ở `test_uc01_search`, `test_uc17_auth`)
- **File**: `blueprints/student/routes.py`
- **Nguyên nhân**: Tồn tại 2 hàm trùng tên `def returnPage()` liên tiếp cho route `/student/return`, khiến Flask báo lỗi `AssertionError: View function mapping is overwriting an existing endpoint function: student.returnPage`.
- **Cách sửa**: Xóa hàm `returnPage()` tĩnh bị thừa, giữ lại hàm `returnPage()` hỗ trợ `GET`/`POST` gọi `trip_service.returnVehicle`.

### 2. Lỗi `BuildError` do mất endpoint `student.page` (1 `FAILED` ở `test_uc01_search`)
- **File**: `blueprints/student/routes.py`
- **Nguyên nhân**: Khi tách các route tĩnh (`/resource`, `/pickup`, `/ride`, `/return`, `/charging`...), nhánh `TV4` đã xóa mất hàm `def page(page):`, trong khi `templates/base_mobile.html` và `templates/student/hinh1_MapScreen.html` vẫn dùng `url_for('student.page', page=...)`.
- **Cách sửa**: Bổ sung lại route fallback `@bp.route("/<page>") def page(page):` ở cuối `blueprints/student/routes.py` để giữ tương thích hoàn toàn với toàn bộ template của TV1 và TV2.

### 3. Thiếu hiện thực dịch vụ đăng ký sạc UC7 (4 `FAILED` ở `test_uc07_*`)
- **File**: `services/charging_service.py`
- **Nguyên nhân**: Test của UC7 đã được viết trong `tests/test_uc02_16_services.py`, nhưng 2 hàm `registerCharging` và `suggestNearestHubWithPort` vẫn để `raise NotImplementedError`.
- **Cách sửa**:
  - Hiện thực `registerCharging(userId, hubId, portId, timeSlot, batteryLevel)`: kiểm tra pin hợp lệ (`0..100`), kiểm tra cổng `AVAILABLE` và chống trùng `(portId, timeSlot)` dưới `DATA_LOCK`, ném đúng `INVALID_PARAMETERS` / `NO_PORT_AVAILABLE`.
  - Hiện thực `suggestNearestHubWithPort(hubId)`: tính khoảng cách Haversine và trả về Hub hoạt động gần nhất còn cổng sạc `AVAILABLE`.

### 4. Lệch cấu trúc dữ liệu trả về & tên action `AUDIT_LOGS` giữa Operator Services và Unit Tests (10 `FAILED` ở UC9–UC12)
- **Files**: `services/alert_service.py`, `services/dispatch_service.py`, `services/incident_service.py`, `blueprints/operator/routes.py`, `tests/test_uc02_16_services.py`
- **Nguyên nhân**: Do nhánh Operator và nhánh TV4 phát triển song song nên lệch một số tên key/action:
  - **UC9 (`alert_service.getHubResources`)**: Bổ sung thêm `hub["id"]`, `vehicles`, `chargingPorts` vào kết quả trả về (giữ nguyên `resources`, `allHubs` cho UI); đồng bộ mã lỗi test theo `DATA_CONTRACT.md` (`RESOURCE_NOT_FOUND` thay vì `"HUB_NOT_FOUND"`).
  - **UC10 (`alert_service.evaluateHubLoad`)**: Tách rõ mặc định `evaluateHubLoad(includeSeeded=False)` tính động theo tải thực tế của `db.HUBS` (trả `[]` khi không có Hub quá tải, có `severity: "CRITICAL" | "WARNING"`), còn giao diện Operator (`overview`, `alerts`) gọi `evaluateHubLoad(includeSeeded=True)` để hiển thị đầy đủ cảnh báo mẫu theo Figma. Bỏ `@pytest.mark.xfail` cũ ở test UC10.
  - **UC11 (`dispatch_service`)**: Bổ sung key `"Available vehicles"` và `"Available parking spots"` trong `getDispatchHubData`; đồng bộ tên audit action thành `"CREATE_DISPATCH_ORDER"` và `"CANCEL_DISPATCH_ORDER"`.
  - **UC12 (`incident_service`)**: Đồng bộ tên audit action thành `"HANDLE_INCIDENT"` và `"RESOLVE_INCIDENT"`; bổ sung logic hủy các booking `HOLDING` thuộc Hub khi chạy `isolateDisconnectedHub(hubId)`.

### 5. Lệch kiểm tra tham số rỗng ở UC14 & xfail cũ ở UC8 (1 `FAILED` ở UC14 + 1 `XFAIL` cũ ở UC8)
- **Files**: `services/simulation_service.py`, `blueprints/operator/routes.py`, `tests/test_uc02_16_services.py`
- **Nguyên nhân**: `validateParameters({})` trước đó tự điền giá trị mặc định thay vì ném `ServiceError(INVALID_PARAMETERS)`, và các test UC8/UC14 vẫn giữ `@pytest.mark.xfail` cũ dù chức năng đã được hoàn thiện.
- **Cách sửa**: Cho `validateParameters({})` ném `INVALID_PARAMETERS` khi thiếu tham số; truyền bộ tham số mặc định tường minh tại `applyRecommendation()` và route `/operator/simulation`; gỡ `@pytest.mark.xfail` cũ ở test UC8 và UC14.

### 6. Sai đường dẫn API giữa giao diện Lịch sạc UC13 (`schedule.html`) và `blueprints/api/routes.py`
- **File**: `blueprints/api/routes.py`
- **Nguyên nhân**: `templates/operator/schedule.html` gọi `/api/hubs/<hubId>/charging-schedule/generate`, `/api/charging-schedule/edit`, `/api/charging-schedule/validate`, `/api/charging-schedule/approve` (số ít và cần trả trường `data`), trong khi `blueprints/api/routes.py` chỉ khai báo `/charging-schedules/...` (số nhiều), thiếu route `/validate` và không trả `data` khi sửa/duyệt. Ngoài ra sửa điều kiện kiểm tra thiếu dữ liệu (`hubId and timeSlot`, `batteryLevel is not None`, mã lỗi `NO_PORT_AVAILABLE`).
- **Cách sửa**: Bổ sung alias cho các route UC13, thêm endpoint `/validate`, trả đầy đủ `data` từ `editSchedule` / `approveSchedule`, và bảo vệ `request.get_json(silent=True) or {}`.

---

## Các phần còn `XFAIL` (chưa hiện thực, đang chờ TV1 & TV4 hoàn thiện tiếp)
Hiện còn **8 test đánh dấu `XFAIL`** tương ứng các hàm còn đang để `TODO`:
1. **UC2**: `status_service.buildVehicleStatus`, `status_service.getResourceStatus("VEHICLE", ...)`
2. **UC3, UC4**: `booking_service.bookVehicle` (kèm `DATA_LOCK` cho `scripts/race_demo.py`), `bookParking`, `cancelBooking`, `isBookingValid`
3. **UC5**: `trip_service.confirmPickup`

---

## Bổ sung: Tách riêng 2 luồng đăng nhập Sinh viên & Đơn vị vận hành (Dual-Portal Login)
- **Mục tiêu**:
  - **Sinh viên (Mobile UI)**: Mở `/` hoặc `/student/search` có thể xem bản đồ, tìm Hub/xe tự do không cần đăng nhập; khi xác nhận đặt xe hoặc truy cập màn hình chuyến đi/sạc (`UC3–UC7`) mới chuyển sang `/login` (giao diện Mobile SSO). Đăng xuất quay về `/student/search`.
  - **Đơn vị vận hành (Desktop UI)**: Truy cập `/operator/...` bị chuyển hướng ngay sang `/operator/login` với giao diện quản trị Desktop riêng (`templates/auth/operator_login.html`, đồng bộ `tokens.css` Sáng/Tối & VN/EN). Chỉ chấp nhận vai trò `OPERATOR` (tài khoản `STUDENT`/`GUEST` bị từ chối với `ACCESS_DENIED`). Đăng xuất từ Dashboard quay về `/operator/login`.
- **Các file đã cập nhật**:
  - `services/auth_service.py`: `loginRequired("OPERATOR")` chuyển hướng về `auth.operatorLogin` thay vì `auth.login`.
  - `blueprints/auth/routes.py`: thêm route `/operator/login` (chặn vai trò không phải `OPERATOR`), kiểm tra URL `next` an toàn, tách luồng chuyển hướng sau `/logout` theo vai trò/cổng.
  - `templates/auth/operator_login.html` & `static/css/dashboard.css`: giao diện đăng nhập Desktop riêng cho Operator (100% dùng biến CSS trong `tokens.css`).
  - `templates/auth/hinh13_SSOLogin.html`, `templates/auth/denied.html`, `templates/base_dashboard.html`, `static/tv1/student.css`: bổ sung liên kết chuyển nhanh giữa 2 cổng và nút quay về bản đồ.
  - `static/i18n/vi.json`, `static/i18n/en.json`: bổ sung khóa song ngữ cho cổng Operator Login và xóa khóa trùng `denied.body`.
  - `tests/test_uc17_auth.py`: bổ sung 4 testcase kiểm tra 2 luồng đăng nhập/đăng xuất riêng.
  - `README.md`, `docs/UI_GUIDE.md`, `docs/DEMO_SCRIPT.md`: cập nhật hướng dẫn 2 cổng đăng nhập và kịch bản demo.

---

## Bổ sung 2: Giao diện Responsive Web + Mobile cho Cổng Sinh viên (Phương án 2)
- **Mục tiêu**: Giữ 1 bộ URL duy nhất cho Sinh viên (`/student/...`, `/login`), tự động hiển thị giao diện **Web Desktop** trên màn hình `≥ 900px` (Top Navbar, màn hình tìm/đặt xe 2 cột bản đồ + danh sách Hub, trang đăng nhập và các trang H6–H12/UC2 dạng Web Card căn giữa) và giữ nguyên 100% **App Mobile (`414px`)** chuẩn Figma khi thu nhỏ hoặc chọn nút gạt nhanh `Web / Mobile`. Không đụng vào bất kỳ file HTML nào của TV2, TV3 hay Backend TV4.
- **Các file đã thêm / cập nhật**:
  - `static/js/student_view.js` *(mới)*: lưu & chuyển đổi chế độ xem `Web / Mobile` (`localStorage["ehub-student-view"]`), phát sự kiện `ehub:viewchange`.
  - `static/css/student_web.css` *(mới)*: toàn bộ style Desktop Responsive (100% dùng biến `var(--...)`, 0 mã màu cứng).
  - `templates/base_mobile.html`: thêm thanh điều hướng ngang `.web-navbar` (chỉ hiện trên Desktop Web) và thanh nổi chuyển lại Web khi xem thử Mobile trên PC.
  - `static/tv1/search.js`: tự mở bản đồ Leaflet và hiển thị toàn bộ danh sách Hub khi ở chế độ Desktop Web, bấm vào thẻ Hub để chọn & pan bản đồ, đồng bộ `map.invalidateSize()` khi resize/chuyển chế độ.
  - `static/i18n/vi.json`, `static/i18n/en.json`, `README.md`: thêm khóa song ngữ `view.*` và cập nhật mô tả 2 cổng.

---

## Bổ sung 3: Hoàn thiện toàn bộ luồng UC2–UC7, 3 demo bắt buộc & chuẩn hóa UI/i18n (đạt 62/62 passed)
- **Backend Services & API (phần T6 20/11 — xóa sạch 8 `XFAIL`)**:
  - `services/status_service.py`: hiện thực `buildVehicleStatus` và `getResourceStatus("VEHICLE", ...)` (UC2).
  - `services/booking_service.py`: hiện thực `bookVehicle` (bọc `with db.DATA_LOCK:` đạt demo bắt buộc `scripts/race_demo.py`), `bookParking`, `cancelBooking`, `isBookingValid` (UC3, UC4).
  - `services/trip_service.py`: hiện thực `confirmPickup` (UC5).
  - `services/auth_service.py`: bổ sung ghi `AuditLog` khi đăng nhập thành công (UC17).
  - `blueprints/api/routes.py`: bổ sung alias `POST /api/bookings/parking` khớp `search.js` và bảo vệ `get_json(silent=True) or {}`.
  - `blueprints/student/routes.py`: nối dữ liệu thật cho toàn bộ 8 màn hình (`resource`, `pickup`, `ride`, `return`, `returned`, `charging`, `charging-review`, `charging-suggest`) và hỗ trợ đi thông toàn luồng đặt xe → nhận xe → đang đi → trả xe → sạc.
  - `tests/test_uc02_16_services.py`: gỡ toàn bộ 8 `@pytest.mark.xfail`.
- **Giao diện TV2 (8 trang Student) & TV3 (`schedule.html`) + Song ngữ**:
  - Cập nhật 8 file `templates/student/{resource,pickup,ride,return,returned,charging_slot,charging_review,charging_suggest}.html`: nối dữ liệu thật, gắn `<form>`/`href` đi đúng luồng `H6→H7→H8→H9` và `H10→H11→H12`, bổ sung bản đồ Leaflet polyline cho `ride.html`, bản đồ chọn Hub trả cho `return.html` và bản đồ gợi ý trạm sạc cho `charging_suggest.html`.
  - Chuẩn hóa `templates/operator/schedule.html` theo `dashboard.css` (`.panel-card`, `.table-x`, `.btn-primary-x`, `<select>` chọn Hub) và gắn đầy đủ `data-i18n`.
  - Bổ sung đầy đủ toàn bộ khóa song ngữ mới vào cả `static/i18n/vi.json` và `static/i18n/en.json` (0 khóa thiếu trên toàn bộ 28 file HTML).

