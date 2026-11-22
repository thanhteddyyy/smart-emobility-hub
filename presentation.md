# Khung nội dung & Bố cục Slide Thuyết trình (15 phút)

> **Cấu trúc tổng thể:** **11 Slide chính** + **3 Slide Phụ lục (Backup)** đặt sau Slide Cảm ơn (không chiếu khi trình bày, chỉ mở khi giảng viên hỏi sâu về thiết kế/kiểm thử cũ).
> **Nguyên tắc trình bày:** Mỗi slide tối đa 3–5 ý ngắn gọn, ưu tiên số liệu, từ khóa và ảnh chạy thật (`demo_UC1-17/`) thay cho đoạn văn dài.

---

## Tổng quan thời lượng & Luồng trình bày

| Slide | Tiêu đề | Mục tiêu | Thời lượng |
|---|---|---|---|
| **1** | Trang bìa | Giới thiệu môn học, đề tài, nhóm | `0:30` |
| **2** | Bối cảnh & Quy mô thí điểm | Giải trình con số 5 Hub · 700 xe · 830 chỗ · 220 cổng | `1:00` |
| **3** | Tổng quan 2 tác nhân & 17 Use Case | Chốt nhanh phạm vi toàn hệ thống | `0:45` |
| **4** | Kiến trúc Flask & Cách hiện thực | Vì sao chọn Flask + kiến trúc 3 tầng | `1:30` |
| **5** | Live Demo 1 — Phân hệ Sinh viên | Chạy thực tế `UC1–UC7, UC15, UC17` | `2:15` |
| **6** | Live Demo 2 — Phân hệ Operator | Chạy thực tế `UC8–UC14, UC15, UC17` | `2:45` |
| **7** | Kỹ thuật lõi #1 — Chống Race Condition | `DATA_LOCK (RLock)` + chạy `race_demo.py` | `1:15` |
| **8** | Kỹ thuật lõi #2 & #3 — Lọc gói trễ & Cô lập What-if | `packet_demo.py` + `PACKET_LOG` + `db.snapshot()` | `1:45` |
| **9** | Điểm đáng chú ý khi phát triển thực tế | 4 bài toán thật nhóm đã tự giải quyết (+ `87/87 pytest`) | `1:15` |
| **10** | Khai báo AI, Bài học & Hướng phát triển | Minh bạch AI 5 thành viên + tổng kết | `1:00` |
| **11** | Cảm ơn & Q&A | Mở phiên hỏi đáp | `0:15` |
| | *(Đệm chuyển cảnh & thao tác)* | *`Alt+Tab`, chuyển mic, gõ lệnh* | `0:45` |
| | **Tổng cộng** | | **15:00** |

---

## Chi tiết từng Slide (`Slide 1` – `Slide 11`)

### Slide 1 — Trang bìa (`0:30`)
- **Bố trí:** Căn giữa trang trọng, logo góc trên.
- **Nội dung chính:**
  - Trường ĐH Bách khoa – ĐHQG TP.HCM | Khoa Khoa học & Kỹ thuật Máy tính.
  - **Môn học:** Công nghệ Phần mềm (CO3001) — Lớp L03 · Nhóm 09 · HK261.
  - **Đề tài:** **Smart E-Mobility Hub (E-Hub)** — Hệ thống Điều phối Phương tiện Điện Thông minh.
  - **GVHD:** Nguyễn Minh Tâm.
  - **Thành viên:** Nguyễn Khang Kỳ, Châu Mạnh Phát, Hoàng Phạm Tiến Thành, Võ Tấn Phát, Đào Huy Phong.
- **Ảnh chèn:** Logo Bách khoa `Bao_Cao_Final/Bao_Cao_Final/Images/hcmut.png`.

---

### Slide 2 — Bối cảnh thực tế & Lý giải quy mô Pilot (`1:00`)
- **Bố trí:** Trên là 1 thanh thực trạng ngắn; dưới là **4 thẻ KPI ngang** giải thích từng con số.
- **Nội dung chính:**
  - **Thực trạng:** Khu ĐHQG-HCM và lân cận có **~8 trường đại học**, **> 32.000 SV nội trú** (KTX A & B) + lưu lượng từ **Ga Metro ĐHQG** → giờ cao điểm sáng xe buýt nội khu quá tải ở các chặng ngắn 1–3 km.
  - **5 Hub** *(Metro ĐHQG, KTX A, KTX B, BK CS2, NVH SV)*: 5 nút gom lưu lượng lõi cho cụm ~8 trường; thiết kế mở rộng động theo dữ liệu cho giai đoạn 2.
  - **700 xe điện:** Chặng ngắn quay vòng 4–5 lượt/sáng → phục vụ **~2.800–3.500 lượt**, san tải tương đương **~50–60 chuyến xe buýt đầy tải**.
  - **830 chỗ đỗ** *(dư +130 chỗ, ~1,19× số xe)*: Hệ số đệm chống đầy trạm (`HUB_FULL`) do luồng sáng lệch một chiều từ KTX về trường/Metro.
  - **220 cổng sạc** *(~31% đội xe, ~1 cổng / 3,2 xe)*: Sạc luân phiên tối ưu lưới điện, tạo bài toán thật cho *Lập lịch sạc (`UC13`)* và *Sạc khẩn (`UC7`)*.
- **Ảnh chèn:** Không bắt buộc (hoặc 1 icon/sơ đồ mini 5 điểm quanh ĐHQG).

---

### Slide 3 — Tổng quan phạm vi 2 tác nhân & 17 Use Case (`0:45`)
- **Bố trí:** Chia 2 cột tỷ lệ **70% trái / 30% phải**.
- **Nội dung chính:**
  - **Bên trái (70%):** Ảnh sơ đồ Use Case tổng quát (khoanh mờ 2 khung màu tách biệt cụm Sinh viên và cụm Vận hành).
  - **Bên phải (30%):** 3 gạch đầu dòng to rõ:
    - **Sinh viên (`UC1–UC7`):** Tìm trạm, đặt xe/chỗ đỗ (giữ 15 phút), nhận–chạy–trả xe, đăng ký sạc.
    - **Đơn vị vận hành (`UC8–UC14`):** Giám sát mạng lưới, cảnh báo 3 mức, điều phối xe, xử lý sự cố, lập lịch sạc, mô phỏng What-if.
    - **Dùng chung (`UC15–UC17`):** Sáng/Tối & VN/EN, realtime lọc gói trễ, Dual-Portal SSO & RBAC.
- **Ảnh chèn:** `Bao_Cao_Final/Bao_Cao_Final/s1/UC-DIAGRAM.drawio.png`.

---

### Slide 4 — Kiến trúc & Cách hiện thực hệ thống (`1:30`)
- **Bố trí:** Chia **2 cột 50/50** (Trái: *Vì sao chọn Flask?* | Phải: *Kiến trúc & Tổ chức kỹ thuật*).
- **Nội dung chính:**
  - **Cột trái — Tại sao chọn Python Flask cho bản Demonstration:**
    - *So với Django:* Gọn nhẹ, không cần migration/ORM nặng nề, chạy ngay trên máy sạch với **2 lệnh** (`pip install -r requirements.txt` → `python app.py`).
    - *So với FastAPI:* Tích hợp sẵn **Jinja2 UI + Session + REST API** trong 1 dự án duy nhất, không cần dựng thêm frontend tách rời.
    - *Blueprints:* Tách tự nhiên thành 4 module (`auth`, `student`, `operator`, `api`).
  - **Cột phải — Tổ chức 3 tầng & Chuẩn hóa làm việc nhóm:**
    - **3 tầng độc lập:** `blueprints/` (route mỏng + RBAC) → `services/` (logic 17 UC, test độc lập) → `data/mock_data.py` (`seed.json` + `DATA_LOCK`, dễ thay bằng PostgreSQL).
    - **Khóa chuẩn giao tiếp:** `docs/DATA_CONTRACT.md` (đồng bộ tên trường FE/BE) + hệ biến `tokens.css` & `323` khóa song ngữ (`vi.json`/`en.json`).
    - **An toàn phân quyền:** Dual-Portal (`/login` vs `/operator/login`), chặn chéo role về `/denied`.
- **Ảnh chèn:** Không bắt buộc (dùng sơ đồ khối 3 tầng chữ nhật gọn vẽ trực tiếp trên PowerPoint).

---

### Slide 5 — Live Demo 1: Phân hệ Sinh viên (`UC1–UC7`, `UC15`, `UC17`) (`2:15`)
- **Bố trí:** Trên là **thanh lộ trình 5 bước**; giữa là **2 ảnh preview** xếp cạnh nhau; dưới là **1 dòng điểm nhấn**. *(Chiếu 5 giây rồi `Alt+Tab` qua trình duyệt chạy live `127.0.0.1:5000/student/search`.)*
- **Nội dung chính:**
  - **Lộ trình bấm:** `1. Bản đồ tìm trạm (UC1–2)` → `2. Đăng nhập /login (UC17)` → `3. Đặt xe & Nhận xe (UC3, UC5)` → `4. Đang đi & Trả xe (UC6)` → `5. Đặt chỗ đỗ & Đăng ký sạc (UC4, UC7)`.
  - **Điểm nhấn:** Xem bản đồ tự do trước khi đăng nhập · Hỗ trợ **Web / Mobile** · Gạt **Sáng/Tối & VN/EN** tức thì không reload.
- **Ảnh chèn:**
  - `Bao_Cao_Final/Bao_Cao_Final/demo_UC1-17/UC01_tim_phuong_tien_va_hub.jpg`
  - `Bao_Cao_Final/Bao_Cao_Final/demo_UC1-17/UC05_nhan_phuong_tien_2_chuyen_di.jpg`

---

### Slide 6 — Live Demo 2: Phân hệ Operator Dashboard (`UC8–UC14`, `UC15`, `UC17`) (`2:45`)
- **Bố trí:** Giống Slide 5 (thanh lộ trình 5 bước + 2 ảnh preview + 1 dòng điểm nhấn). *(`Alt+Tab` sang cửa sổ trình duyệt ẩn danh `127.0.0.1:5000/operator/login`.)*
- **Nội dung chính:**
  - **Lộ trình bấm:** `1. Cổng /operator/login & RBAC (UC17)` → `2. Overview & 700 xe (UC8–9)` → `3. Cảnh báo 3 mức (UC10)` → `4. Điều phối bản đồ & Sự cố (UC11–12)` → `5. Lịch sạc & What-if (UC13–14)`.
  - **Điểm nhấn:** Cập nhật **realtime mỗi 5 giây** từ thao tác Sinh viên · Đổi Sáng/Tối & VN/EN **khi đang nhập form không mất dữ liệu**.
- **Ảnh chèn:**
  - `Bao_Cao_Final/Bao_Cao_Final/demo_UC1-17/UC08_giam_sat_mang_luoi_hub.jpg`
  - `Bao_Cao_Final/Bao_Cao_Final/demo_UC1-17/UC14_mo_phong_what_if.jpg`

---

### Slide 7 — Kỹ thuật lõi #1: Chống Race Condition khi đặt xe (`UC3`) (`1:15`)
- **Bố trí:** Chia **2 cột** (Trái: *Bài toán & 4 dòng code khóa* | Phải: *Demo kiểm chứng*).
- **Nội dung chính:**
  - **Vấn đề:** 2 sinh viên đặt cùng 1 xe tại 1 thời điểm → dễ đặt đúp nếu không đồng bộ.
  - **Cơ chế (`services/booking_service.py`):**
    ```python
    with db.DATA_LOCK:                    # threading.RLock(): xếp hàng từng luồng
        if vehicle["status"] != "AVAILABLE":
            raise ServiceError(VEHICLE_CONFLICT)
        vehicle["status"] = "RESERVED"    # Đổi trạng thái & lưu booking nguyên tử
    ```
  - **Kiểm chứng trực tiếp:**
    - Chạy `python scripts/race_demo.py` (`threading.Barrier(2)` thả 2 luồng cùng lúc) → đúng **1 người thành công**, 1 người nhận **`VEHICLE_CONFLICT`** (`=> ĐẠT: chỉ 1 người đặt được.`).
    - *(Chuyển sang CSDL thật tương đương Transaction + `SELECT ... FOR UPDATE`.)*
- **Ảnh chèn:** Tùy chọn 1 ảnh terminal kết quả `race_demo.py` làm dự phòng.

---

### Slide 8 — Kỹ thuật lõi #2 & #3: Lọc gói trễ (`UC16`) & Cô lập What-if (`UC14`) (`1:45`)
- **Bố trí:** Chia đôi **Trái (`UC16`) / Phải (`UC14`)**.
- **Nội dung chính:**
  - **Nửa trái — Lọc gói dữ liệu trễ (`UC16` / NFR08):**
    - Kiểm tra định dạng (`validatePacket`) và đối chiếu mốc thời gian: `packetTimestamp <= currentTimestamp` (`services/realtime_service.py`).
    - Chạy `python scripts/packet_demo.py` gửi gói cũ năm `2020` → API trả `ok: true, updated: false, reason: "OUTDATED_PACKET"` → ghi log lên bảng **`PACKET_LOG`**, không ghi đè dữ liệu mới của `EB-201`.
  - **Nửa phải — Cô lập mô phỏng What-if (`UC14` / NFR07):**
    - `initVirtualEnvironment()` gọi `db.snapshot()` (`copy.deepcopy` toàn bộ mạng lưới).
    - Chạy kịch bản cực đoan tại `/operator/simulation`, quay lại `/operator/overview` → số liệu vận hành thật **không đổi 1 xe**.
- **Ảnh chèn:** `Bao_Cao_Final/Bao_Cao_Final/demo_UC1-17/UC16_cap_nhat_trang_thai_2_packet_log.jpg` *(góc dưới nửa trái)*.

---

### Slide 9 — Điểm đáng chú ý trong quá trình phát triển (`1:15`)
- **Bố trí:** **Lưới 2×2 gồm 4 thẻ vấn đề thực tế** (không chia cột riêng cho `pytest`), góc trên phải gắn 1 huy hiệu nhỏ: **`87/87 pytest passed (100%)`**.
- **Nội dung chính (4 thẻ):**
  1. **Bản đồ 3 lớp chống lỗi tải tile (`map_tiles.js`):** OSM chập chờn & CARTO bất ngờ đòi API key → xây Dual-CDN Leaflet + tự failover Esri/OSM + lớp nền vector nội bộ ĐHQG-HCM, không bao giờ xám trắng.
  2. **Bắt & sửa lỗi lệch múi giờ UTC+7 (`UC4`):** Test tay phát hiện trình duyệt gửi giờ UTC (`Z`) còn backend cắt múi giờ nhầm → chuẩn hóa `.astimezone()`.
  3. **Mở rộng quy mô 700 xe & tinh chỉnh UX:** Thêm bảng cuộn + tìm kiếm nhanh, phân tầng tải 5 Hub (Overload/Danger/Safe), tách Dual-Portal Login, cố định nút `Web | Mobile` và bỏ nút thừa.
  4. **Quản trị Git 5 nhánh & Hợp đồng dữ liệu:** Khóa sớm `DATA_CONTRACT.md` giúp FE/BE làm song song, kiểm soát merge conflict sạch qua 5 nhánh.
- **Ảnh chèn:** Không cần (lưới 4 thẻ chữ to rõ đã rất thoáng).

---

### Slide 10 — Khai báo Generative AI, Bài học & Hướng phát triển (`1:00`)
- **Bố trí:** Khối ngang phía trên tóm tắt AI Usage; bên dưới chia **2 cột nhỏ (Bài học kinh nghiệm | Hướng phát triển)**.
- **Nội dung chính:**
  - **Minh bạch Generative AI (5/5 thành viên):**
    - *Công cụ:* ChatGPT, Claude & agent lập trình.
    - *Phạm vi:* Gợi ý phân công, khung Flask MVP, gợi ý test case/tài liệu & rà soát lỗi.
    - *Tự kiểm chứng:* 100% mã nguồn, giao diện, số liệu đều do nhóm tự đối chiếu mockup Figma, chạy `pytest` (`87/87`) và chỉnh sửa bằng tay.
  - **Bài học kinh nghiệm:** Thành thạo GitHub nhánh nhóm; chuẩn hóa `DATA_CONTRACT` khi phối hợp nhiều người; ứng dụng AI có kiểm soát và kiểm chứng thực tế.
  - **Hướng phát triển:** Thay `seed.json` bằng **PostgreSQL / Redis**; nâng polling 5 giây sang **WebSocket**; tích hợp **SSO ĐHQG-HCM** & GPS/IoT thật.

---

### Slide 11 — Cảm ơn & Q&A (`0:15`)
- **Bố trí:** Tối giản, căn giữa.
- **Nội dung chính:** *"Cảm ơn Thầy đã lắng nghe — Mời Thầy đặt câu hỏi (Q&A)"* · `Smart E-Mobility Hub (E-Hub)` · `Nhóm 09 – Lớp L03`.

---

## Các Slide Phụ lục dự phòng (Backup Slides — Đặt sau Slide 11)
> Chỉ mở khi giảng viên đặt câu hỏi chuyên sâu trong phần Q&A:
- **Backup 1 — Kiến trúc triển khai & thành phần:** Chèn `Bao_Cao_Final/Bao_Cao_Final/s3/deployment_view.drawio.png` và `Bao_Cao_Final/Bao_Cao_Final/s3/implementation_view.drawio.png`.
- **Backup 2 — Sơ đồ lớp chi tiết:** Chèn `Bao_Cao_Final/Bao_Cao_Final/s3/class_diagram_submission3.drawio.png`.
- **Backup 3 — Bảng khai báo chi tiết AI Usage (TV1–TV5):** Chụp/trích nguyên bảng từ `docs/AI_USAGE.md`.

