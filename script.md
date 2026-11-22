# Kịch bản thuyết trình 15 phút (Chia người nói & Thao tác)

> **Người mở đầu:** **Hoàng Phạm Tiến Thành (TV3)** dẫn nhập mạch câu chuyện tổng quan, bối cảnh, kiến trúc; sau đó lần lượt chuyển mic qua phần Demo Sinh viên (**TV1, TV2**), quay lại phần Operator (**TV3**), phần 3 kỹ thuật lõi (**TV4**) và tổng kết (**TV5**).

---

## 1. Bảng phân công người nói & Thời lượng

| Thứ tự | Người nói | Slide đảm nhận | Nội dung chính | Thời lượng |
|---|---|---|---|---|
| **1** | **Hoàng Phạm Tiến Thành (TV3)** | Slide 1, 2, 3, 4 | Chào mở đầu, bối cảnh 5 Hub/700 xe, tổng quan 17 UC, kiến trúc Flask | `3:45` |
| **2** | **Nguyễn Khang Kỳ (TV1)** | Slide 5 *(nửa đầu)* | Live Demo Sinh viên: tìm trạm bản đồ, đăng nhập `/login`, đặt xe/chỗ đỗ (`UC1, UC3, UC4, UC17`) | `1:10` |
| **3** | **Châu Mạnh Phát (TV2)** | Slide 5 *(nửa sau)* | Live Demo Sinh viên: xem chi tiết xe, nhận–chạy–trả xe, sạc & đổi giao diện (`UC2, UC5, UC6, UC7, UC15`) | `1:05` |
| **4** | **Hoàng Phạm Tiến Thành (TV3)** | Slide 6 | Live Demo Operator: `/operator/login`, Overview nhảy số realtime, cảnh báo, điều phối, sự cố, lịch sạc, What-if (`UC8–UC15, UC17`) | `2:45` |
| **5** | **Võ Tấn Phát (TV4)** | Slide 7, 8 | Trình bày & chạy 3 kỹ thuật lõi: `DATA_LOCK` (`race_demo.py`), Lọc gói trễ (`packet_demo.py`), Cô lập What-if | `3:00` |
| **6** | **Đào Huy Phong (TV5)** | Slide 9, 10, 11 | 4 vấn đề phát triển thực tế (+ `87/87 pytest`), AI Usage, Bài học, Hướng phát triển & Kết thúc | `2:30` |
| | *(Đệm chuyển cảnh & thao tác)* | | Chuyển `Alt+Tab`, đổi người cầm mic | `0:45` |
| | **Tổng cộng** | **11 Slide** | | **15:00** |

---

## 2. Checklist chuẩn bị 2 phút trước khi thuyết trình

1. Mở Terminal 1 tại thư mục dự án, reset dữ liệu sạch và bật server:
   ```powershell
   python scripts/reset_data.py
   python app.py
   ```
2. Mở sẵn **2 cửa sổ trình duyệt** (không chung session):
   - **Cửa sổ 1 (thường):** `http://127.0.0.1:5000/student/search` *(chưa đăng nhập sẵn để demo luôn bước `/login`)*.
   - **Cửa sổ 2 (Ẩn danh):** `http://127.0.0.1:5000/operator/overview` *(hoặc mở sẵn `/operator/login` rồi đăng nhập trực tiếp `operator@ehub.vn` / `123456`)*.
3. Mở sẵn **Terminal 2** gõ chờ sẵn `python scripts/race_demo.py` (không bấm Enter trước, lên tới Slide 7 mới bấm).

---

## 3. Lời thoại & Thao tác chi tiết từng Slide

### Slide 1 — Trang bìa (`0:30` — **Tiến Thành**)
- *"Xin chào thầy và các bạn. Em là **Tiến Thành**, đại diện **Nhóm 09 – Lớp L03**. Hôm nay nhóm em xin trình bày kết quả cuối kỳ môn Công nghệ Phần mềm với đề tài **Smart E-Mobility Hub (E-Hub)** — Hệ thống điều phối phương tiện điện thông minh trong khuôn viên ĐHQG-HCM."*

---

### Slide 2 — Bối cảnh & Quy mô hệ thống (`1:00` — **Tiến Thành**)
- *"Xuất phát từ bài toán thực tế tại khu đô thị ĐHQG-HCM với khoảng **8 trường đại học**, hơn **32.000 sinh viên nội trú** cùng luồng di chuyển từ **Ga Metro ĐHQG**, giờ cao điểm sáng xe buýt nội khu thường xuyên bị dồn ép ở các chặng ngắn 1–3 km.*
- *Nhóm định hướng giai đoạn thí điểm gồm **5 Hub trung chuyển lõi** tại Metro ĐHQG, KTX Khu A, KTX Khu B, Bách khoa CS2 và Nhà văn hóa Sinh viên — thiết kế mở rộng động để giai đoạn 2 có thể thêm Hub cho các trường còn lại mà không cần sửa code.*
- *Bộ số liệu **700 xe – 830 chỗ đỗ – 220 cổng sạc** cũng được tính theo tỷ lệ vận hành thực tế: 700 xe quay vòng 4–5 lượt buổi sáng đáp ứng ~3.000 lượt, san tải tương đương 50–60 chuyến buýt; dư +130 chỗ đỗ làm khoảng đệm chống đầy trạm khi luồng sáng lệch một chiều; và 220 cổng sạc giới hạn chính là lý do hệ thống cần lập lịch sạc thông minh."*

---

### Slide 3 — Tổng quan 2 tác nhân & 17 Use Case (`0:45` — **Tiến Thành**)
- *"Đây là sơ đồ Use Case tổng quát của hệ thống — em xin không đi sâu lại chi tiết phân rã từ Submission 1, mà chỉ chốt nhanh phạm vi nhóm đã hiện thực trọn vẹn **17/17 chức năng** cho 2 tác nhân:*
  - ***Sinh viên (`UC1–UC7`):** Tìm trạm trên bản đồ, đặt xe/chỗ đỗ, nhận–chạy–trả xe và đăng ký sạc.*
  - ***Đơn vị vận hành (`UC8–UC14`):** Giám sát 5 Hub, cảnh báo quá tải, điều phối xe, xử lý sự cố, lập lịch sạc và mô phỏng What-if.*
  - *Cùng **3 tính năng nền tảng dùng chung (`UC15–UC17`)**: đổi Sáng/Tối & VN/EN, cập nhật realtime lọc gói trễ và xác thực SSO."*

---

### Slide 4 — Kiến trúc Flask & Cách hiện thực (`1:30` — **Tiến Thành**)
- *"Về mặt kỹ thuật, nhóm chọn **Python Flask** làm nền tảng cho bản demo. So với Django khá nặng về cấu hình ORM/CSDL, hay FastAPI đòi hỏi tách thêm một frontend riêng, Flask cực kỳ gọn nhẹ — chạy ngay trên máy sạch bằng đúng 2 lệnh — đồng thời tích hợp sẵn Jinja2 để dựng giao diện lẫn REST API trong cùng một dự án.*
- *Nhóm chia code theo **kiến trúc 3 tầng** kết hợp Flask Blueprints:*
  - *Tầng `blueprints/` chỉ điều hướng và kiểm tra phân quyền **Dual-Portal RBAC** (tách riêng cổng `/login` và `/operator/login`).*
  - *Toàn bộ logic 17 Use Case nằm độc lập trong `services/` để kiểm thử tự động bằng `pytest`.*
  - *Tầng `data/` dùng `seed.json` kèm khóa `DATA_LOCK`, nhờ vậy sau này thay bằng PostgreSQL cũng không làm vỡ tầng trên.*
- *Nhờ khóa sớm `DATA_CONTRACT.md` và dùng chung hệ biến `tokens.css` cùng 323 khóa song ngữ, cả 5 thành viên có thể làm song song và tích hợp sạch sẽ.*
- *Tiếp theo, mời bạn **Khang Kỳ** và **Mạnh Phát** demo trực tiếp luồng **Sinh viên** trên localhost."*

---

### Slide 5 — Live Demo 1: Phân hệ Sinh viên (`2:15` — **Khang Kỳ & Mạnh Phát**)
> **[Chuyển cảnh]** Chiếu Slide 5 trong 3 giây → `Alt+Tab` qua **Cửa sổ 1 (`/student/search`)**.

- **Phần 1 — Khang Kỳ (`1:10` — `UC1, UC17, UC3, UC4`):**
  - **[Thao tác]:** Chọn trạm `ĐH Bách khoa CS2` hoặc `Ga Metro ĐHQG` trên bản đồ (chỉ đường đi bộ từ `BK CS2`, gạt nhanh `Web | Mobile`). Bấm **Đặt xe** → chuyển sang `/login`, đăng nhập `student@hcmut.edu.vn` / `123456`. Đặt 1 xe (`UC3`), rồi mở lại modal sang tab **Chỗ đỗ xe** đặt thử 1 khung giờ tương lai (`UC4`).
  - **Lời thoại:** *"Chưa cần đăng nhập, sinh viên vẫn mở được `/student/search` để xem bản đồ 5 Hub, vị trí BK CS2, quãng đường đi bộ và chuyển chế độ Web hoặc Mobile. Khi bấm **Đặt xe**, hệ thống yêu cầu xác thực tại cổng `/login`. Ở tab **Thuê xe điện**, em chọn xe và đặt ngay — hệ thống giữ chỗ 15 phút và dẫn sang trang nhận xe. Còn ở tab **Chỗ đỗ xe**, sinh viên chọn giờ đến trong tương lai và hệ thống tự chặn nếu chọn giờ quá khứ."*
  - *(Chuyển chuột & mic cho Mạnh Phát.)*

- **Phần 2 — Mạnh Phát (`1:05` — `UC2, UC5, UC6, UC7, UC15`):**
  - **[Thao tác]:** Từ nút **Đến trang nhận xe →** bấm **Xác nhận nhận xe** (`/student/pickup` → `/student/ride`), chỉ thanh pin & bản đồ → bấm **Trả xe** (`/student/return`), chọn Hub còn chỗ trống → xác nhận (`/student/returned`). Vào nhanh tab **Sạc** (`/student/charging` → bấm gợi ý/đăng ký sạc). Gạt nhanh **VN/EN** và **Sáng/Tối** ở góc trên phải.
  - **Lời thoại:** *"Khi tới trạm, sinh viên vào `/student/pickup` xác nhận nhận xe để chuyển sang màn hình chuyến đi `/student/ride` có bản đồ tuyến đường và mức pin cập nhật realtime. Khi đến đích, chọn Hub trả còn chỗ ở `/student/return` để hoàn tất chuyến đi. Ngoài ra mục **Sạc** cho phép đặt khung giờ sạc hoặc gợi ý trạm gần nhất còn cổng trống khi cần sạc khẩn cấp. Em xin bàn giao lại cho anh **Tiến Thành** trình bày phần **Dashboard Operator**."*

---

### Slide 6 — Live Demo 2: Phân hệ Operator (`2:45` — **Tiến Thành**)
> **[Chuyển cảnh]** Chiếu Slide 6 trong 3 giây → `Alt+Tab` qua **Cửa sổ 2 (Ẩn danh — `/operator/login`)**.

- **[Thao tác]:**
  1. Thử nhắc/mở nhanh tab Student gõ `/operator/overview` bị đẩy về `/denied` *(tùy chọn nếu kịp, hoặc nói thẳng khi đang ở `/operator/login`)*; đăng nhập `operator@ehub.vn` / `123456`.
  2. Vào **Overview** (`/operator/overview`): chỉ 4 KPI + bảng 5 Hub có màu phân tầng `Overload / Danger / Safe`.
  3. Lướt nhanh **Tài nguyên** (`/operator/resources` — gõ ô tìm kiếm lọc trong 700 xe) & **Cảnh báo** (`/operator/alerts` — phân 3 cấp `HIGH/MEDIUM/LOW`).
  4. Vào **Điều phối** (`/operator/dispatch`): bấm 1 marker trên bản đồ chọn Hub nguồn/đích, tick 1 xe bấm **Điều phối xe**.
  5. Vào **Sự cố** (`/operator/incidents`) & **Lịch sạc** (`/operator/schedule`) giới thiệu nhanh thao tác xử lý/phê duyệt.
  6. Vào **Mô phỏng What-if** (`/operator/simulation`): giữ nguyên hoặc gõ 1 giá trị, **gạt VN/EN & Sáng/Tối** ngay trên form → đổi kịch bản `Mưa lớn` / `Khung giờ` → bấm chạy ra biểu đồ Chart.js & khuyến nghị → bấm **Áp dụng sang Điều phối**.
- **Lời thoại:**
  - *"Ở phân hệ vận hành, tài khoản Sinh viên nếu cố truy cập sẽ bị RBAC chặn về `/denied`. Khi đăng nhập đúng cổng `/operator/login`, trang **Overview** hiển thị tức thời KPI và 5 Hub phân tầng tải rõ ràng — mọi thao tác đặt hay trả xe vừa rồi của sinh viên đều được đồng bộ realtime về đây mỗi 5 giây.*
  - *Mục **Tài nguyên** hỗ trợ tra cứu nhanh 700 xe, mục **Cảnh báo** phân loại 3 mức `HIGH/MEDIUM/LOW`. Trên màn hình **Điều phối**, Operator nhấp trực tiếp marker trên bản đồ để chọn nguồn–đích và chuyển xe giữa các Hub; kết hợp quản lý **Sự cố** và phê duyệt **Lịch sạc thông minh** ưu tiên xe pin yếu.*
  - *Cuối cùng ở **Mô phỏng What-if**, khi em thử gạt **Sáng/Tối** hoặc **VN/EN** ngay lúc đang nhập form, toàn bộ giao diện cập nhật tức thì mà không tải lại trang hay mất dữ liệu. Chạy thử kịch bản mưa lớn sẽ xuất biểu đồ dự báo thiếu hụt theo giờ và có nút chuyển thẳng sang Điều phối. Sau đây mời **Tấn Phát** đi sâu vào **3 cơ chế kỹ thuật lõi** phía sau."*

---

### Slide 7 — Kỹ thuật lõi #1: Chống Race Condition (`1:15` — **Tấn Phát**)
- **[Thao tác]:** Chiếu Slide 7 (30 giây) → chuyển qua **Terminal 2**, bấm Enter chạy:
  ```powershell
  python scripts/race_demo.py
  ```
- **Lời thoại:**
  - *"Cơ chế lõi đầu tiên giải quyết bài toán hai sinh viên cùng bấm đặt **1 chiếc xe duy nhất** ở đúng cùng một thời điểm. Trong `booking_service.py`, nhóm dùng khóa `DATA_LOCK = threading.RLock()` bọc toàn bộ đoạn kiểm tra trạng thái, đổi xe sang `RESERVED` và tạo booking.*
  - *Lưu ý là `RLock` chỉ làm nhiệm vụ bắt các luồng đến cùng lúc phải xếp hàng lần lượt từng người một; sau khi luồng đầu giữ xe xong và nhả khóa, luồng thứ hai bước vào kiểm tra thấy trạng thái xe khác `AVAILABLE` thì code nghiệp vụ mới báo `VEHICLE_CONFLICT`.*
  - *Trên terminal, `scripts/race_demo.py` dùng `threading.Barrier(2)` ép 2 luồng `SV_A` và `SV_B` bắn cùng 1 lúc... Kết quả luôn đảm bảo **chỉ duy nhất 1 người đặt được**."*

---

### Slide 8 — Kỹ thuật lõi #2 & #3: Lọc gói trễ & Cô lập What-if (`1:45` — **Tấn Phát**)
- **[Thao tác]:**
  1. Trên **Terminal 2**, chạy tiếp:
     ```powershell
     python scripts/packet_demo.py
     ```
  2. Chỉ JSON kết quả (`"ok": true`, `"updated": false`, `"reason": "OUTDATED_PACKET"`), rồi chuyển sang tab `/operator/overview` chỉ bảng **`PACKET_LOG`** vừa thêm dòng `2020-01-01T08:00:00`.
  3. Chỉ tổng số xe sẵn sàng trên `/operator/overview` (không đổi dù vừa chạy What-if ở Slide 6).
- **Lời thoại:**
  - *"Cơ chế thứ hai ở **UC16** giúp chống ghi đè dữ liệu cũ từ mạng IoT. Khi em chạy `scripts/packet_demo.py` để gửi một gói tin của xe `EB-201` mang mốc thời gian cũ năm `2020`, API vẫn tiếp nhận hợp lệ (`ok: true`) nhưng trả về `updated: false` với lý do `OUTDATED_PACKET` vì timestamp cũ hơn dữ liệu đang lưu. Gói bị loại được ghi thẳng vào bảng `PACKET_LOG` trên Dashboard để truy vết mà dữ liệu thực của xe không hề bị ghi đè ngược.*
  - *Cơ chế thứ ba ở **UC14** là **cô lập môi trường mô phỏng**: hàm `initVirtualEnvironment()` tạo bản sao độc lập bằng `copy.deepcopy(db.snapshot())`. Như thầy thấy, dù vừa nãy nhóm chạy What-if với kịch bản mưa lớn thay đổi mạnh cung–cầu, nhưng khi quay lại `/operator/overview`, toàn bộ số liệu vận hành thật vẫn giữ nguyên 100%.*
  - *Phần cuối về quá trình phát triển và tổng kết, xin mời bạn **Huy Phong**."*

---

### Slide 9 — Điểm đáng chú ý trong quá trình phát triển (`1:15` — **Huy Phong**)
- **Lời thoại:**
  - *"Trong quá trình phát triển và kiểm thử chéo thực tế, nhóm tự phát hiện và xử lý 4 bài toán nổi bật, được kiểm chứng lại bằng **87/87 test tự động (`pytest`)**:*
  - *Thứ nhất, khi bản đồ OpenStreetMap chập chờn và CARTO đột ngột siết API key, nhóm tự viết **bộ nạp bản đồ 3 lớp (`map_tiles.js`)** kết hợp Dual-CDN, tự failover Esri/OSM và lớp nền vector khu vực ĐHQG-HCM để không bao giờ bị nền xám.*
  - *Thứ hai, khi test tay đặt chỗ đỗ, nhóm phát hiện **lỗi lệch múi giờ UTC+7** khiến lịch đặt hợp lệ bị báo quá khứ và đã chuẩn hóa quy đổi giờ bằng `.astimezone()`.*
  - *Thứ ba, khi mở rộng dữ liệu lên **700 xe**, nhóm bổ sung khung cuộn bảng, tìm kiếm tức thì, phân tầng tải 5 Hub và tách gọn Dual-Portal Login.*
  - *Thứ tư là giữ kỷ luật Git 5 nhánh riêng với **hợp đồng dữ liệu `DATA_CONTRACT.md`** để tích hợp mượt mà code của 5 thành viên."*

---

### Slide 10 — Khai báo AI, Bài học & Hướng phát triển (`1:00` — **Huy Phong**)
- **Lời thoại:**
  - *"Về khai báo Generative AI, cả 5 thành viên đều dùng ChatGPT và Claude minh bạch ở vai trò hỗ trợ dựng khung, gợi ý test case, rà lỗi và biên tập tài liệu; toàn bộ code, giao diện và kết quả test cuối cùng đều được nhóm tự đối chiếu mockup, tự chạy kiểm chứng và chỉnh sửa bằng tay.*
  - *Qua đồ án này, nhóm rút ra 3 bài học lớn: thành thạo quy trình làm việc nhóm trên GitHub, biết cách phối hợp và rà soát code giữa các thành viên, và tận dụng AI có kiểm soát. Về hướng phát triển, nhờ tầng `data/` đã tách riêng, hệ thống sẵn sàng nâng cấp lên PostgreSQL/Redis, WebSocket realtime và SSO ĐHQG-HCM thực tế."*

---

### Slide 11 — Cảm ơn & Q&A (`0:15` — **Huy Phong**)
- *"Phần trình bày và demo của Nhóm 09 đến đây là kết thúc. Em xin cảm ơn Thầy đã lắng nghe và rất mong nhận được câu hỏi góp ý từ Thầy ạ."*

---

## 4. Chuẩn bị nhanh cho phần Q&A (Nếu thầy hỏi sâu)

| Câu hỏi dễ gặp | Hướng trả lời ngắn gọn (15–20 giây) | Người phụ trách chính |
|---|---|---|
| **`DATA_LOCK = threading.RLock()` hoạt động thế nào?** | Khóa bắt các luồng vào kiểm tra/đặt xe tuần tự; dùng `RLock` để cùng 1 luồng gọi lồng hàm không bị deadlock; chính dòng `if status != "AVAILABLE"` mới là chỗ trả `VEHICLE_CONFLICT`. | **Tấn Phát (TV4)** |
| **Tại sao `packet_demo` trả `ok: true` mà `updated: false`?** | Gói JSON hợp lệ về định dạng nên server xử lý bình thường (`ok: true`), nhưng theo luật `isOutdatedPacket` gói cũ hơn `lastUpdatedAt` nên không cập nhật xe (`updated: false`) và ghi vào `PACKET_LOG`. | **Tấn Phát (TV4)** |
| **8 trường ĐHQG và >32.000 SV nội trú mà chỉ có 5 Hub, 700 xe?** | Giai đoạn Pilot tập trung 5 nút gom lưu lượng lõi; 700 xe quay vòng 4–5 lượt/sáng đáp ứng ~3.000 lượt (san tải 50–60 chuyến buýt); dư +130 chỗ đỗ đệm tránh đầy trạm lệch chiều; 220 cổng tạo bài toán lập lịch sạc. | **Tiến Thành (TV3)** |
| **Tại sao chọn Flask mà không dùng Django hoặc FastAPI?** | Bản demo cần chạy nhẹ tức thì trên máy sạch (2 lệnh) và gộp chung Jinja2 UI + REST API trong 1 repo, không cần cài CSDL nặng như Django hay tách frontend riêng như FastAPI. | **Tiến Thành (TV3)** |
| **Kiểm thử tự động `pytest` test những gì? Có test UI không?** | `pytest` kiểm tra **87 case** cho toàn bộ logic `services/`, API/RBAC và đồng bộ `323` khóa i18n (bật **Slide 9 / `tests/`** nếu cần); còn UI, bản đồ và Chart.js được kiểm thử thủ công theo 66 test case trong `TEST_MATRIX.md`. | **Huy Phong (TV5) & Mạnh Phát (TV2)** |
| **Hỏi chi tiết luồng Sinh viên / bản đồ 3 lớp?** | Giải thích đường đi bộ BK CS2 (`UC1–UC4`), chuỗi nhận–trả–sạc (`UC5–UC7`), và cơ chế Dual-CDN + failover Esri/OSM + nền vector ở `map_tiles.js`. | **Khang Kỳ (TV1) & Mạnh Phát (TV2)** |

