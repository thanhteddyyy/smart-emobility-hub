# Tổng hợp công việc còn lại — Mốc cuối (21/11 – 22/11/2026)

> **Trạng thái tổng quan (tính đến T7 21/11/2026):**
> - Đã hợp nhất đủ 5 nhánh (`TV1`, `TV2`, `TV3`, `TV4`, `TV5`) trên nhánh `main`.
> - Kiểm thử tự động: **`87 passed, 0 failed`** (`pytest`).
> - Song ngữ: đồng bộ **`323/323` khóa** (`static/i18n/vi.json`, `static/i18n/en.json`), hỗ trợ Sáng/Tối toàn hệ thống.
> - Đạt đủ **3 demo bắt buộc**: chống race condition đặt chỗ (`scripts/race_demo.py`), lọc gói dữ liệu trễ (`scripts/packet_demo.py` / UC16), cô lập dữ liệu mô phỏng What-if (UC14).
> - Hoàn thành toàn bộ 21 đầu mục sửa lỗi `#0 – #20` trong `fix_error.md`.

---

## 1. Bảng tóm tắt tiến độ & đầu việc còn lại (TV1 – TV5)

| Thành viên | Vai trò chính | Đã hoàn thành | Còn làm T7 (21/11) | Còn làm CN (22/11) |
|---|---|---|---|---|
| **TV1 (Khang Kỳ)** | UI Sinh viên H1–H5, H13–H14 & Backend UC1–UC5 | Layout mobile + Responsive Web/Mobile; H1 bản đồ Leaflet (5 trạm, chấm BK CS2, vẽ đường, chỉ đường Google Maps); H2–H5 modal đặt xe/chỗ (chặn giờ quá khứ); H13–H14 SSO; backend UC1–UC5 | Test tay toàn bộ luồng Sinh viên trên bản 700 xe; điền `docs/AI_USAGE.md` | Giải nén `.zip` trên máy sạch & chạy 2 lệnh trong `README.md` |
| **TV2 (Mạnh Phát)** | UI Sinh viên H6–H12, UC2 & Chụp ảnh kiểm thử | Đủ 8 màn hình (`resource`, `pickup`, `ride`, `return`, `returned`, `charging_slot`, `charging_review`, `charging_suggest`); thông luồng `H6→H7→H8→H9` và `H10→H11→H12`; khung cuộn xe (`#10`), pin realtime (`#16`), Sáng/Tối & VN/EN | Chạy test tay cùng TV5 chốt `docs/TEST_MATRIX.md`; chụp chuỗi ảnh UC1–UC17; điền `docs/AI_USAGE.md` | Rà soát file PDF báo cáo cuối cùng trước khi nộp |
| **TV3 (Operator)** | Web Dashboard Operator (H15–H21, UC13) | Đủ 7 màn hình Dashboard + `/operator/login`; khung cuộn 700 xe (`#19`); sự cố & chip gợi ý lý do (`#14`); 3 cấp cảnh báo (`#9`); What-if động (`#12`); `PACKET_LOG` song ngữ (`#15`); gộp xong 5 nhánh (`87/87 passed`) | **Ngay lập tức**: `git commit --no-edit && git push origin main`; test tay 7 trang Dashboard (Sáng/Tối, VN/EN) + `scripts/packet_demo.py`; điền `docs/AI_USAGE.md` | Phối hợp cùng TV5 quay video demo phần Operator |
| **TV4 (Tấn Phát)** | Logic, Dữ liệu, API, 3 Demo bắt buộc & Đóng gói | `services/` UC1–UC17, `blueprints/`, `data/seed.json` (700 xe / 830 chỗ / 220 cổng, 5 Hub tải khác nhau), `docs/ARCHITECTURE.md`, `README.md`, đạt 3 demo bắt buộc | Test chéo **Student ↔ Operator** realtime; ngồi cùng TV5 30 phút đọc `services/`; điền `docs/AI_USAGE.md` | Dọn file thừa/nội bộ, chốt `README.md` và đóng gói `.zip` nộp bài |
| **TV5 (Huy Phong)** | Tài liệu, Ma trận Test, Slide, Video & PDF cuối | Bản nền `docs/UI_GUIDE.md`, `docs/TEST_MATRIX.md`, `docs/DEMO_SCRIPT.md` và 22 test tự động cho UC8–UC16 | Cập nhật 3 file docs (`TEST_MATRIX.md`, `DEMO_SCRIPT.md`, `UI_GUIDE.md`) cho khớp code mới; tổng hợp `docs/AI_USAGE.md`; làm slide; học `services/` cùng TV4 (30 phút); chạy nháp demo ≥ 2 lần | Quay video demo 8–10 phút (cùng TV3), gắn link công khai, rà soát gộp Submission 1–2–3 & xuất PDF cuối |

---

## 2. Chi tiết checklist theo từng thành viên (TV1 – TV5)

### 2.1. TV1 (Khang Kỳ) — UI Sinh viên H1–H5, H13–H14 & Backend UC1–UC5
- **Đã hoàn thành**:
  - Layout mobile + Responsive Web/Mobile (`student_web.css`, `student_view.js`, thanh điều hướng `.web-navbar`).
  - H1 bản đồ Leaflet (5 trạm, chấm vị trí BK CS2, vẽ đường đi, chỉ đường Google Maps).
  - H2–H5 modal đặt xe/chỗ đỗ (có kiểm tra chặn giờ quá khứ).
  - H13–H14 đăng nhập SSO và toàn bộ backend UC1–UC5.
- **Việc cần làm T7 (21/11)**:
  - [ ] Bấm kiểm tra tay toàn bộ luồng Sinh viên trên bản đã gộp 700 xe (từ tìm trạm H1 đến modal đặt xe/chỗ, đăng nhập SSO `/login`).
  - [ ] Điền phần khai báo sử dụng AI của bản thân vào `docs/AI_USAGE.md` (công cụ, phạm vi, mức độ đóng góp, phần đã tự chỉnh sửa/kiểm tra).
- **Việc cần làm CN (22/11)**:
  - [ ] Giải nén file `.zip` nộp bài cuối cùng trên một máy/thư mục sạch hoàn toàn.
  - [ ] Chạy thử đúng 2 lệnh hướng dẫn trong `README.md` (`pip install -r requirements.txt` → `python app.py`) để xác nhận không lỗi môi trường hay thiếu file phụ thuộc.

---

### 2.2. TV2 (Mạnh Phát) — UI Sinh viên H6–H12, UC2 & Chụp ảnh kiểm thử
- **Đã hoàn thành**:
  - Đủ 8 màn hình (`resource`, `pickup`, `ride`, `return`, `returned`, `charging_slot`, `charging_review`, `charging_suggest`).
  - Nối thông luồng `H6→H7→H8→H9` (mượn–nhận–chạy–trả xe) và `H10→H11→H12` (gợi ý–chọn cổng–xác nhận sạc).
  - Khung cuộn danh sách xe (`#10`), pin cập nhật realtime (`#16`), hỗ trợ đầy đủ Sáng/Tối & VN/EN.
- **Việc cần làm T7 (21/11)**:
  - [ ] Chạy toàn bộ test case thủ công trên bản web thật cùng TV5 để chốt trạng thái `Passed/Failed` trong `docs/TEST_MATRIX.md`.
  - [ ] Chụp chuỗi ảnh màn hình theo từng Use Case (`UC1–UC17`, tối thiểu 1 ảnh/UC) gửi cho TV5 đưa vào chương Demo của báo cáo PDF.
  - [ ] Điền phần khai báo sử dụng AI của bản thân vào `docs/AI_USAGE.md`.
- **Việc cần làm CN (22/11)**:
  - [ ] Rà soát lại toàn bộ file PDF báo cáo cuối cùng trước khi nộp (kiểm tra bố cục, chính tả, ảnh minh chứng, link video).

---

### 2.3. TV3 (Operator Dashboard H15–H21, UC13)
- **Đã hoàn thành**:
  - Toàn bộ 7 màn hình Dashboard Operator + cổng đăng nhập riêng `/operator/login`.
  - Khung cuộn bảng 700 xe có tìm kiếm & bộ đếm (`#19`), sự cố đa dạng & chip gợi ý lý do (`#14`), 3 cấp cảnh báo `HIGH/MEDIUM/LOW` (`#9`).
  - Trang mô phỏng What-if động theo khung giờ & kịch bản (`#12`), bảng `PACKET_LOG` song ngữ (`#15`).
  - Hợp nhất xong toàn bộ 5 nhánh trên `main` (`87/87 passed`).
- **Việc cần làm ngay lập tức**:
  - [ ] Chạy `git commit --no-edit && git push origin main` để hoàn tất đẩy bản merge TV5 lên GitHub.
  - [ ] Nhắn cả nhóm chạy `git pull origin main` để đồng bộ bản chuẩn `87/87 passed`.
- **Việc cần làm T7 (21/11)**:
  - [ ] Bấm kiểm tra tay toàn bộ 7 trang Dashboard Operator ở cả chế độ Sáng/Tối và ngôn ngữ VN/EN.
  - [ ] Chạy thử `python scripts/packet_demo.py` và kiểm tra bảng `PACKET_LOG` cập nhật realtime trên trang `/operator/overview`.
  - [ ] Điền phần khai báo sử dụng AI của bản thân vào `docs/AI_USAGE.md`.
- **Việc cần làm CN (22/11)**:
  - [ ] Phối hợp cùng TV5 quay video demo phần giao diện và nghiệp vụ Operator.

---

### 2.4. TV4 (Tấn Phát) — Logic, Dữ liệu, API, 3 Demo bắt buộc & Đóng gói
- **Đã hoàn thành**:
  - Toàn bộ tầng `services/` cho UC1–UC17, `blueprints/`, `data/seed.json` quy mô lớn (700 xe / 830 chỗ đỗ / 220 cổng sạc, 5 Hub mức tải khác nhau).
  - Hoàn thiện `docs/ARCHITECTURE.md`, `README.md` và đạt đủ 3 demo bắt buộc (`scripts/race_demo.py`, `scripts/packet_demo.py`, cô lập What-if).
- **Việc cần làm T7 (21/11)**:
  - [ ] Thực hiện test chéo luồng xuyên phân hệ **Student ↔ Operator**: Sinh viên thực hiện đặt/nhận/trả xe ở cổng Student và kiểm tra số liệu, cảnh báo, lịch sử nhảy realtime trên Dashboard Operator.
  - [ ] Ngồi cùng TV5 khoảng 30 phút đọc qua cấu trúc và luồng xử lý trong `services/` để TV5 nắm chắc kiến thức kỹ thuật trả lời giảng viên.
  - [ ] Điền phần khai báo sử dụng AI của bản thân vào `docs/AI_USAGE.md`.
- **Việc cần làm CN (22/11)**:
  - [ ] Dọn sạch toàn bộ file thừa/nội bộ trước khi nén gói nộp bài (loại bỏ `.venv/`, `.pytest_cache/`, `__pycache__/`, `assign_task_last_submission.pdf`, `fix_error.md`, `Last_task_21-11.md`).
  - [ ] Rà soát và chốt lần cuối nội dung `README.md`.
  - [ ] Đóng gói file `.zip` nộp bài chuẩn chỉnh.

---

### 2.5. TV5 (Huy Phong) — Tài liệu, Ma trận Test, Slide, Video & PDF cuối
- **Đã hoàn thành**:
  - Bản nền `docs/UI_GUIDE.md`, `docs/TEST_MATRIX.md`, `docs/DEMO_SCRIPT.md` và 22 test tự động cho UC8–UC16.
- **Việc cần làm T7 (21/11)**:
  - [ ] Cập nhật `docs/TEST_MATRIX.md` cho khớp bản code mới nhất:
    - Đổi dòng trạng thái tổng từ `33 passed` → **`87 passed`**.
    - Cập nhật loạt dòng `Pending (chờ TODO)` ở `UC2–UC7`, `UC13`, `UC16` sang **`Passed`**.
    - Tick `[x]` đầy đủ cả 3 demo bắt buộc (bổ sung kết quả đạt cho `scripts/race_demo.py` và `scripts/packet_demo.py`).
    - Điền kết quả test thủ công và tên file ảnh minh chứng sau khi test cùng TV2.
  - [ ] Cập nhật `docs/DEMO_SCRIPT.md`:
    - Sửa Phần 1: bỏ bước "lọc bán kính 2 km" (đã loại bỏ theo `#4`), thay bằng tìm kiếm trong 5 trạm + chấm gốc BK CS2 + vẽ đường.
    - Nêu rõ cơ chế Dual-Portal Login (`/login` cho Sinh viên và `/operator/login` cho Nhân viên vận hành).
    - Bổ sung lệnh chạy `python scripts/packet_demo.py` vào Phần 8.
  - [ ] Cập nhật `docs/UI_GUIDE.md`:
    - Cập nhật số khóa song ngữ từ `194` → **`323 key`**.
    - Bổ sung mục Dual-Portal Login (`/login` & `/operator/login`) và ghi chú chế độ Responsive Web/Mobile cho cổng Sinh viên.
  - [ ] Tổng hợp nội dung `docs/AI_USAGE.md` từ cả 5 thành viên (hiện file vẫn đang để `_TODO_`).
  - [ ] Hoàn thiện slide thuyết trình (đảm bảo có phần bài học kinh nghiệm rút ra).
  - [ ] Ngồi cùng TV4 khoảng 30 phút để nắm vững luồng code trong `services/`.
  - [ ] Chạy nháp toàn bộ kịch bản demo trực tiếp ít nhất 2 lần để tránh sự cố khi quay/báo cáo.
- **Việc cần làm CN (22/11)**:
  - [ ] Quay video demo hoàn chỉnh thời lượng 8–10 phút (phối hợp cùng TV3 quay phần Operator) và gắn link công khai vào báo cáo.
  - [ ] Rà soát bản hợp nhất báo cáo **Submission 1–2–3**: kiểm tra đã sửa header/footer cũ còn ghi `"Mạng Máy Tính"`, đảm bảo đủ ít nhất 1 ảnh minh chứng cho từng UC (`UC1–UC17`) và đầy đủ bảng Khai báo AI.
  - [ ] Xuất file PDF báo cáo cuối cùng.

---

## 3. Checklist chốt nộp bài CN (22/11)

- [ ] **Mã nguồn `.zip` sạch & chạy được ngay**:
  - TV1 giải nén trên máy sạch, chạy đúng 2 lệnh trong `README.md` (`pip install -r requirements.txt` → `python app.py`) thành công không lỗi.
  - Bộ test tự động `pytest` đạt **87/87 passed, 0 failed**.
  - Không dính các thư mục/file tạm & ghi chú nội bộ: `.venv/`, `.pytest_cache/`, `__pycache__/`, `assign_task_last_submission.pdf`, `fix_error.md`, `Last_task_21-11.md`.
- [ ] **Báo cáo PDF hợp nhất (Submission 1–2–3)**:
  - Đã xóa/sửa sạch header/footer cũ ghi `"Mạng Máy Tính"`.
  - Chương Demo có đủ ảnh chụp màn hình cho toàn bộ **UC1–UC17** (tối thiểu 1 ảnh/UC) và gắn **link video demo công khai**.
  - Chương Khai báo sử dụng Generative AI đầy đủ đóng góp của cả **5 thành viên** (khớp `docs/AI_USAGE.md`).
- [ ] **Slide, Video & 3 Demo bắt buộc**:
  - Hoàn chỉnh slide thuyết trình (có mục bài học kinh nghiệm).
  - Video demo 8–10 phút rõ nét, đủ cả luồng Student & Operator.
  - Sẵn sàng chạy trực tiếp 3 demo bắt buộc: `python scripts/race_demo.py`, `python scripts/packet_demo.py`, và mô phỏng What-if cô lập dữ liệu thật (UC14).

