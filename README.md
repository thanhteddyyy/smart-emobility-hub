# Smart E-Mobility Hub

Bài tập lớn môn **Công nghệ Phần mềm (CO3001)** – Nhóm 9, lớp L03, HK261.
Hệ thống điều phối phương tiện điện trong Khu đô thị ĐHQG-HCM: sinh viên tìm Hub, đặt xe, nhận/trả xe, đăng ký sạc; đơn vị vận hành giám sát mạng lưới, điều phối, xử lý sự cố và mô phỏng What-if.

Đây là bản **MVP để demo**: giao diện làm theo mockup Submission 2, logic làm theo Class diagram và Method description Submission 3, **dữ liệu giả lập, không dùng database**.

> **Trạng thái hiện tại: hoàn thiện đầy đủ MVP trên `main` (62/62 test passed).** Đã hoàn chỉnh cả 2 cổng tách biệt (Sinh viên Responsive Web + Mobile App và Đơn vị vận hành chỉ Web Desktop), toàn bộ luồng Sinh viên **UC1–UC7** (tìm Hub, xem chi tiết xe/Hub, đặt xe/chỗ chống race condition, nhận xe, bản đồ chuyến đi Leaflet polyline, trả xe, đăng ký sạc & gợi ý trạm sạc khẩn), toàn bộ Dashboard Vận hành **UC8–UC14** (kể cả Lịch sạc thông minh và Mô phỏng What-if cô lập), đổi Sáng/Tối & VN/EN (**UC15**), cập nhật realtime & lọc gói trễ (**UC16**), phân quyền & AuditLog (**UC17**).

---

## 1. Chạy thử

```
pip install -r requirements.txt
python app.py
```

Hoặc bấm đúp `run.bat` trên Windows, `./run.sh` trên macOS/Linux.

### Hai cổng truy cập tách biệt (Dual-Portal Login)

| Cổng | Đường dẫn | Trải nghiệm & Luồng đăng nhập |
|---|---|---|
| **Cổng Sinh viên (Responsive Web + Mobile App)** | http://127.0.0.1:5000 (hoặc `/student/search`) | **Không bắt đăng nhập ngay**: tự động hiển thị giao diện **Web Desktop** (Top Navbar + bản đồ 2 cột rộng + danh sách Hub) trên máy tính và **App Mobile** chuẩn Figma (`414px`) trên màn hình nhỏ, có thêm nút gạt nhanh `Web / Mobile` trên thanh đầu trang để demo. Khi xác nhận **Đặt xe / Đặt chỗ** hoặc vào màn hình chuyến đi/sạc (`UC3–UC7`), mới chuyển sang `/login`. Đăng xuất quay về `/student/search`. |
| **Cổng Đơn vị vận hành (Chỉ Web Desktop)** | http://127.0.0.1:5000/operator/login (hoặc `/operator/`) | **Bắt buộc đăng nhập ngay** với giao diện Desktop quản trị riêng (chỉ chấp nhận tài khoản vai trò `OPERATOR`). Đăng nhập xong vào thẳng `/operator/overview`; đăng xuất sẽ quay về `/operator/login`. |

> Ở chân mỗi trang đăng nhập đều có liên kết chuyển nhanh giữa **Cổng Sinh viên** và **Cổng Đơn vị vận hành** để tiện trình bày khi demo.

### Tài khoản demo

| Vai trò | Email | Mật khẩu | Cổng đăng nhập |
|---|---|---|---|
| Sinh viên | `student@hcmut.edu.vn` | `123456` | `/login` |
| Đơn vị vận hành | `operator@ehub.vn` | `123456` | `/operator/login` |
| Không đủ quyền (để demo lỗi) | `guest@gmail.com` | `123456` | Cả 2 cổng đều báo `ACCESS_DENIED` |

_TODO: bổ sung phiên bản Python khuyến nghị và kịch bản demo chi tiết trước khi nộp._

---

## 2. Hiểu dự án trong 1 phút

Mỗi lần người dùng mở một trang, yêu cầu đi qua 4 chặng:

```
Trình duyệt mở /student/search
        │
        ▼
blueprints/student/routes.py     ← nhận yêu cầu, gọi service        (tầng Presentation)
        │
        ▼
services/search_service.py       ← xử lý: lọc Hub, tính khoảng cách  (tầng Business)
        │
        ▼
data/mock_data.py                ← dữ liệu giả, đọc từ seed.json     (tầng Data Access)
        │
        ▼
templates/student/search.html    ← đổ dữ liệu vào HTML rồi trả về trình duyệt
```

Ba tầng này chính là Implementation view trong Submission 3.

**Muốn xem một ví dụ làm trọn vẹn?** Đọc lần lượt 4 file ở sơ đồ trên (UC1). Mọi màn hình khác làm theo đúng kiểu đó.

---

## 3. Thư mục nào để làm gì

```
smart-emobility-hub/
├── app.py                 Khởi động web, đăng ký các blueprint
├── config.py              Hằng số dùng chung (cổng, ngưỡng dữ liệu cũ, thời gian giữ xe…)
├── requirements.txt       Thư viện cần cài
├── run.bat / run.sh       Chạy nhanh
│
├── data/
│   ├── seed.json          Dữ liệu gốc: 5 Hub, 40 xe, 76 chỗ đỗ, 20 cổng sạc, 6 sự cố, 3 tài khoản
│   └── mock_data.py       Nạp seed.json vào bộ nhớ + vài hàm tra cứu
│
├── services/              LOGIC NGHIỆP VỤ – tên hàm giống Method description Submission 3
├── blueprints/            ROUTE – nối đường dẫn web với service và template
│   ├── auth/              /login (Sinh viên), /operator/login (Vận hành), /logout, /denied
│   ├── student/           /student/...   (màn hình mobile)
│   ├── operator/          /operator/...  (web dashboard)
│   └── api/               /api/...       (trả JSON cho realtime và nút bấm)
│
├── templates/             GIAO DIỆN (HTML)
│   ├── base_mobile.html       Khung chung cho màn hình Sinh viên
│   ├── base_dashboard.html    Khung chung cho dashboard Vận hành
│   ├── auth/                  login.html (Mobile SSO), operator_login.html (Desktop), denied.html
│   ├── student/               Màn hình mobile Sinh viên (UC1–UC7)
│   └── operator/              Màn hình dashboard Vận hành (UC8–UC14)
│
├── static/
│   ├── css/tokens.css     Bảng màu sáng/tối – mọi màu lấy từ đây
│   ├── css/mobile.css, dashboard.css
│   ├── js/theme.js        Đổi Sáng/Tối (UC15)
│   ├── js/i18n.js         Đổi VN/EN (UC15)
│   ├── js/realtime.js     Tự cập nhật số liệu mỗi 5 giây (UC16)
│   └── i18n/vi.json, en.json   Từ điển song ngữ
│
├── tests/                 Test tự động (pytest) – ứng với test case Submission 3
├── scripts/               race_demo.py (demo đặt trùng xe), reset_data.py
└── docs/                  Tài liệu nội bộ của nhóm (xem mục 7)
```

---

## 4. Ai làm ở đâu

| Thành viên | Vai trò | Làm việc chủ yếu trong |
|---|---|---|
| **TV1** | UI Sinh viên: tìm kiếm, đặt chỗ, đăng nhập (Hình 1–5, 13–14) + layout mobile | `templates/base_mobile.html`, `templates/student/search.html`, `_booking_modal.html`, `templates/auth/`, `static/` |
| **TV2** | UI Sinh viên: nhận/trả xe, sạc (Hình 6–12) + chi tiết xe/Hub | `templates/student/` (các file còn lại) |
| **TV3** | UI Dashboard vận hành (Hình 15–20) | `templates/base_dashboard.html`, `templates/operator/`, `static/css/dashboard.css` |
| **TV4** | Logic, dữ liệu, API, tích hợp, 3 demo bắt buộc, What-if (Hình 21), lịch sạc | `services/`, `blueprints/`, `data/`, `tests/`, `scripts/` |
| **TV5** | Tài liệu, kiểm thử, video, slide, quy ước giao diện | `docs/`, `static/i18n/`, `static/css/tokens.css`, `tests/` |

Tìm việc của mình: tìm chữ **`TODO(`** trong toàn bộ dự án (VS Code: `Ctrl+Shift+F`). Mỗi TODO ghi rõ use case và việc cần làm.

---

## 5. Cách thêm một màn hình (làm theo UC1)

Ví dụ làm màn hình **Trả xe (UC6 – Hình 8)**:

1. **Giao diện (TV2)** – mở `templates/student/return.html`, thay ô TODO bằng HTML theo Figma. Giữ dòng `{% extends "base_mobile.html" %}` để có sẵn khung, nút theme, nút ngôn ngữ.
2. **Logic (TV4)** – mở `services/trip_service.py`, viết thân hàm `returnVehicle(...)`. Khi có lỗi nghiệp vụ thì `raise ServiceError(HUB_FULL, "...")`.
3. **Nối lại (TV4)** – trong `blueprints/student/routes.py`, tách `return` thành route riêng: gọi service, bắt `ServiceError`, truyền dữ liệu vào `render_template(...)`.
4. **Hiển thị dữ liệu (TV2)** – trong HTML dùng `{{ hub.name }}`, `{% for %}`, `{% if error %}` như ở `search.html`.
5. **Tự kiểm tra** – thử sáng/tối, VN/EN, trạng thái lỗi; đối chiếu test case UC6 trong Submission 3.
6. **Gửi Pull Request** vào `main`.

Trong lúc chờ TV4 viết logic, người làm UI cứ gõ dữ liệu mẫu trực tiếp trong HTML theo đúng tên trường ở `docs/DATA_CONTRACT.md`.

---

## 6. Ba thứ dùng chung, ai cũng cần biết

**Đổi ngôn ngữ** – gắn `data-i18n` vào mọi chữ hiển thị, rồi thêm key vào **cả** `vi.json` và `en.json`:
```html
<span data-i18n="action.book">Đặt xe</span>
```

**Số liệu tự cập nhật** – gắn `data-rt` là đường dẫn tới giá trị trong `/api/state`:
```html
<b data-rt="hubs.H1.availableVehicles">7</b>
```

**Màu sắc** – không viết mã màu trực tiếp, luôn dùng biến trong `tokens.css` để bản tối tự đúng:
```css
color: var(--color-primary);
```

---

## 7. Quy ước

- **Đặt tên** (theo biên bản họp nhóm): class `PascalCase`, hàm và biến `camelCase`, hằng số `ALL_CAPS`. Vì vậy hàm Python trong dự án viết `searchVehicleAndHub` thay vì kiểu `snake_case` thông thường, để khớp tên trong báo cáo.
- **Route không chứa logic.** Logic nằm trong `services/`.
- **Service không hiển thị lỗi.** Service ném `ServiceError(MÃ_LỖI)`; giao diện quyết định hiện thế nào. Danh sách mã lỗi: `services/errors.py`.
- **Sửa dữ liệu dùng chung** thì bọc trong `with db.DATA_LOCK:`.
- **Git:** mỗi người một nhánh (`tv1-...`, `tv2-...`), mở Pull Request vào `main`, chỉ TV4 merge. Không sửa `seed.json`, `base_*.html`, `tokens.css` của người khác mà không báo nhóm.

Tài liệu chi tiết trong `docs/`:

| File | Nội dung | Phụ trách |
|---|---|---|
| `DATA_CONTRACT.md` | Tên trường dữ liệu, mã trạng thái, mã lỗi – "hợp đồng" giữa UI và logic | TV4 |
| `ARCHITECTURE.md` | Thư mục ↔ Implementation view ↔ Class diagram | TV4 |
| `UI_GUIDE.md` | Tên thương hiệu, màu, font, key song ngữ | TV5 |
| `TEST_MATRIX.md` | Test case Submission 3 ↔ màn hình ↔ kết quả | TV5 |
| `DEMO_SCRIPT.md` | Kịch bản video demo | TV5 |
| `AI_USAGE.md` | Khai báo sử dụng Generative AI | TV5 (cả nhóm điền) |

---

## 8. Chạy test

```
pytest
python scripts/race_demo.py     # demo đặt trùng xe – đạt sau khi làm xong bookVehicle
```

---

## 9. Ba demo bắt buộc

| Demo | Ở đâu | Cách chứng minh |
|---|---|---|
| Race condition khi đặt xe (UC3) | `services/booking_service.py` | `scripts/race_demo.py`: 2 người đặt 1 xe, chỉ 1 thành công |
| Lọc gói dữ liệu trễ (UC16) | `services/realtime_service.py` | Gửi gói có thời gian cũ vào `/api/telemetry`, gói bị bỏ và ghi log |
| Cô lập dữ liệu mô phỏng (UC14) | `services/simulation_service.py` | Chạy What-if xong, số liệu dashboard không đổi |

---

## 10. Nhóm thực hiện

| MSSV | Họ và tên |
|---|---|
| 2412565 | Châu Mạnh Phát |
| 2412628 | Đào Huy Phong |
| 2413148 | Hoàng Phạm Tiến Thành |
| 2411819 | Nguyễn Khang Kỳ |
| 2412616 | Võ Tấn Phát |

GVHD: Nguyễn Minh Tâm
