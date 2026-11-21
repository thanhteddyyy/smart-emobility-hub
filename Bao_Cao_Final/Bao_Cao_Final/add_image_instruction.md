# Hướng dẫn đặt tên & phân công thêm ảnh minh chứng Demo (`Images/demo/`)

> Tài liệu này hướng dẫn toàn nhóm quy chuẩn chụp ảnh màn hình chạy thật (**Submission 4 — `A working demonstration (by sequence of screens)`**), đặt tên file theo chuẩn `/folder/function` và phân công rõ từng thành viên phụ trách để ghép vào `Contents/TrienKhai.tex` và xuất PDF cuối từ `main.tex`.

---

## 1. Quy ước thư mục & đặt tên ảnh (`/folder/function`)

- **Thư mục gốc lưu ảnh demo:** `bao_cao_final/Bao_Cao_Final/Images/demo/`
- **Quy tắc đường dẫn chuẩn trong LaTeX:** `Images/demo/<folder>/<function>.png`
  - Viết thường toàn bộ, **không dấu tiếng Việt**, **không khoảng trắng**, dùng dấu gạch dưới `_` nếu tên chức năng có nhiều từ.
  - **Ví dụ:**
    - UC1 (`/student/search`) → lưu tại `Images/demo/student/search.png`
    - UC8 (`/operator/overview`) → lưu tại `Images/demo/operator/overview.png`
    - UC17 (`/auth/login_student`) → lưu tại `Images/demo/auth/login_student.png`
- **5 thư mục con chuẩn bên trong `Images/demo/`:**
  1. `student/` — các màn hình phân hệ Sinh viên (`H1–H12`)
  2. `operator/` — các màn hình Web Dashboard Operator (`H15–H21`)
  3. `auth/` — các màn hình đăng nhập Dual-Portal SSO & từ chối truy cập (`UC17`)
  4. `shared/` — các màn hình minh họa Sáng/Tối & song ngữ Việt/Anh (`UC15`)
  5. `tests/` — ảnh chụp terminal chạy 2 demo script bắt buộc & `pytest`
- **Yêu cầu khi chụp ảnh:**
  - Chụp trực tiếp trên ứng dụng web chạy thật tại `http://127.0.0.1:5000` (**không** dùng lại ảnh mockup Figma của Submission 2).
  - Lưu định dạng `.png`, chữ rõ nét, không che mất thông tin quan trọng.
  - Màn hình Sinh viên (Mobile / Responsive Web) chụp gọn theo khung điện thoại hoặc chế độ Web rõ nét để dễ xếp 2–3 ảnh cạnh nhau trong PDF.

---

## 2. Bảng phân công chụp & thêm ảnh chi tiết (UC1 – UC17)

| UC | Nội dung cần chụp (theo `Contents/TrienKhai.tex`) | Đường dẫn chuẩn (`/folder/function`) | File lưu trong `Images/demo/` | Người phụ trách |
|---|---|---|---|---|
| **UC1** | Bản đồ 5 trạm, chấm vị trí BK CS2, vẽ đường đi bộ đến trạm | `/student/search` | `Images/demo/student/search.png` | **TV1 (Nguyễn Khang Kỳ)** |
| **UC2** | Chi tiết trạm & danh sách xe + cảnh báo dữ liệu cũ (stale) | `/student/resource`<br>`/student/resource_stale` | `Images/demo/student/resource.png`<br>`Images/demo/student/resource_stale.png` | **TV2 (Châu Mạnh Phát)** |
| **UC3** | Modal đặt xe thành công + lỗi `VEHICLE_CONFLICT` + demo terminal chống race condition | `/student/booking_vehicle_success`<br>`/student/booking_vehicle_conflict`<br>`/tests/race_demo` | `Images/demo/student/booking_vehicle_success.png`<br>`Images/demo/student/booking_vehicle_conflict.png`<br>`Images/demo/tests/race_demo.png` | **TV1 (Nguyễn Khang Kỳ)** _(UI)_<br>**TV4 (Võ Tấn Phát)** _(`race_demo`)_ |
| **UC4** | Modal đặt chỗ đỗ xe (kèm kiểm tra giờ quá khứ) + gợi ý Hub thay thế khi `HUB_FULL` | `/student/booking_parking`<br>`/student/booking_hub_full` | `Images/demo/student/booking_parking.png`<br>`Images/demo/student/booking_hub_full.png` | **TV1 (Nguyễn Khang Kỳ)** |
| **UC5** | Màn hình xác nhận nhận phương tiện | `/student/pickup` | `Images/demo/student/pickup.png` | **TV2 (Châu Mạnh Phát)** |
| **UC6** | Chuỗi màn hình đang đi (bản đồ + pin realtime), chọn trạm trả xe, trả xe thành công | `/student/ride`<br>`/student/return`<br>`/student/returned` | `Images/demo/student/ride.png`<br>`Images/demo/student/return.png`<br>`Images/demo/student/returned.png` | **TV2 (Châu Mạnh Phát)** |
| **UC7** | Chọn khung giờ sạc, xem lại/xác nhận đăng ký sạc, gợi ý trạm sạc khẩn cấp | `/student/charging_slot`<br>`/student/charging_review`<br>`/student/charging_suggest` | `Images/demo/student/charging_slot.png`<br>`Images/demo/student/charging_review.png`<br>`Images/demo/student/charging_suggest.png` | **TV2 (Châu Mạnh Phát)** |
| **UC8** | Dashboard Tổng quan mạng lưới Hub (KPI, biểu đồ / bảng trạng thái 5 Hub) | `/operator/overview` | `Images/demo/operator/overview.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC9** | Theo dõi tài nguyên phương tiện / bãi đỗ / cổng sạc theo Hub | `/operator/resources` | `Images/demo/operator/resources.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC10** | Màn hình cảnh báo quá tải 3 mức (`HIGH` / `MEDIUM` / `LOW`) | `/operator/alerts` | `Images/demo/operator/alerts.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC11** | Điều phối phương tiện trên bản đồ Leaflet & lệnh điều phối | `/operator/dispatch` | `Images/demo/operator/dispatch.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC12** | Danh sách sự cố & trang chi tiết xử lý sự cố | `/operator/incidents`<br>`/operator/incident_detail` | `Images/demo/operator/incidents.png`<br>`Images/demo/operator/incident_detail.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC13** | Lập lịch sạc thông minh cho các xe pin yếu | `/operator/schedule` | `Images/demo/operator/schedule.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC14** | Mô phỏng What-if với biểu đồ Chart.js & khuyến nghị (không đổi DB thật) | `/operator/simulation` | `Images/demo/operator/simulation.png` | **TV3 (Hoàng Phạm Tiến Thành)** |
| **UC15** | So sánh chuyển đổi giao diện Sáng/Tối & song ngữ Việt/Anh | `/shared/theme_light_dark`<br>`/shared/lang_vi_en` | `Images/demo/shared/theme_light_dark.png`<br>`Images/demo/shared/lang_vi_en.png` | **TV5 (Đào Huy Phong)** |
| **UC16** | Bảng `PACKET_LOG` trên Dashboard + kết quả chạy terminal `packet_demo.py` & `pytest` | `/operator/packet_log`<br>`/tests/packet_demo`<br>`/tests/pytest_summary` | `Images/demo/operator/packet_log.png`<br>`Images/demo/tests/packet_demo.png`<br>`Images/demo/tests/pytest_summary.png` | **TV3 (Hoàng Phạm Tiến Thành)** _(`packet_log`)_<br>**TV4 (Võ Tấn Phát)** _(scripts & `pytest`)_ |
| **UC17** | Xác thực SSO Dual-Portal (`/login`, `/operator/login`) & thông báo từ chối truy cập | `/auth/login_student`<br>`/auth/login_operator`<br>`/auth/denied` | `Images/demo/auth/login_student.png`<br>`Images/demo/auth/login_operator.png`<br>`Images/demo/auth/denied.png` | **TV1 (Nguyễn Khang Kỳ)** _(Student & denied)_<br>**TV3 (Hoàng Phạm Tiến Thành)** _(Operator login)_ |

---

## 3. Checklist nhanh theo từng thành viên (`TV1` – `TV5`)

### TV1 (Nguyễn Khang Kỳ) — 7 ảnh
- [ ] `Images/demo/student/search.png` *(UC1 — `/student/search`)*
- [ ] `Images/demo/student/booking_vehicle_success.png` *(UC3 — modal đặt xe thành công)*
- [ ] `Images/demo/student/booking_vehicle_conflict.png` *(UC3 — modal báo lỗi `VEHICLE_CONFLICT`)*
- [ ] `Images/demo/student/booking_parking.png` *(UC4 — modal đặt chỗ đỗ & chặn giờ quá khứ)*
- [ ] `Images/demo/student/booking_hub_full.png` *(UC4 — modal `HUB_FULL` kèm gợi ý trạm khác)*
- [ ] `Images/demo/auth/login_student.png` *(UC17 — cổng đăng nhập Sinh viên `/login`)*
- [ ] `Images/demo/auth/denied.png` *(UC17 — trang từ chối phân quyền khi sai role)*

### TV2 (Châu Mạnh Phát) — 9 ảnh
- [ ] `Images/demo/student/resource.png` *(UC2 — `/student/resource`)*
- [ ] `Images/demo/student/resource_stale.png` *(UC2 — cảnh báo dữ liệu cũ)*
- [ ] `Images/demo/student/pickup.png` *(UC5 — `/student/pickup`)*
- [ ] `Images/demo/student/ride.png` *(UC6 — `/student/ride`)*
- [ ] `Images/demo/student/return.png` *(UC6 — `/student/return`)*
- [ ] `Images/demo/student/returned.png` *(UC6 — `/student/returned`)*
- [ ] `Images/demo/student/charging_slot.png` *(UC7 — `/student/charging`)*
- [ ] `Images/demo/student/charging_review.png` *(UC7 — `/student/charging-review`)*
- [ ] `Images/demo/student/charging_suggest.png` *(UC7 — `/student/charging-suggest`)*

### TV3 (Hoàng Phạm Tiến Thành) — 10 ảnh
- [ ] `Images/demo/operator/overview.png` *(UC8 — `/operator/overview`)*
- [ ] `Images/demo/operator/resources.png` *(UC9 — `/operator/resources`)*
- [ ] `Images/demo/operator/alerts.png` *(UC10 — `/operator/alerts` 3 mức)*
- [ ] `Images/demo/operator/dispatch.png` *(UC11 — `/operator/dispatch` bản đồ + danh sách điều phối)*
- [ ] `Images/demo/operator/incidents.png` *(UC12 — `/operator/incidents`)*
- [ ] `Images/demo/operator/incident_detail.png` *(UC12 — chi tiết & xử lý sự cố)*
- [ ] `Images/demo/operator/schedule.png` *(UC13 — `/operator/schedule`)*
- [ ] `Images/demo/operator/simulation.png` *(UC14 — `/operator/simulation` kèm biểu đồ Chart.js)*
- [ ] `Images/demo/operator/packet_log.png` *(UC16 — bảng `PACKET_LOG` minh họa lọc gói trễ trên `overview`)*
- [ ] `Images/demo/auth/login_operator.png` *(UC17 — cổng đăng nhập `/operator/login`)*

### TV4 (Võ Tấn Phát) — 3 ảnh
- [ ] `Images/demo/tests/race_demo.png` *(UC3 — terminal chạy `python scripts/race_demo.py` ra kết quả ĐẠT)*
- [ ] `Images/demo/tests/packet_demo.png` *(UC16 — terminal chạy `python scripts/packet_demo.py` lọc gói trễ)*
- [ ] `Images/demo/tests/pytest_summary.png` *(Tổng kết kiểm thử tự động `pytest -q` đạt `87 passed`)*

### TV5 (Đào Huy Phong) — 2 ảnh + Ghép báo cáo
- [ ] `Images/demo/shared/theme_light_dark.png` *(UC15 — so sánh Sáng/Tối)*
- [ ] `Images/demo/shared/lang_vi_en.png` *(UC15 — so sánh Việt/Anh)*
- [ ] Chèn toàn bộ ảnh vào `Contents/TrienKhai.tex` thay thế các dòng `\_TODO\_` và biên dịch lại `main.tex` ra `main.pdf`.

---

## 4. Mẫu chèn ảnh vào `Contents/TrienKhai.tex` (LaTeX)

- Với **màn hình Mobile Sinh viên** (khuyên dùng `width=0.45\textwidth`, có thể đặt 2 hình cạnh nhau bằng `minipage`):

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.45\textwidth]{Images/demo/student/search.png}
    \caption{UC1 --- Màn hình tìm kiếm trạm và bản đồ điều hướng (\texttt{/student/search})}
    \label{fig:demo_uc01_search}
\end{figure}
```

- Với **màn hình Web Dashboard Operator hoặc Terminal kiểm thử** (khuyên dùng `width=0.9\textwidth`):

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\textwidth]{Images/demo/operator/overview.png}
    \caption{UC8 --- Bảng điều khiển tổng quan mạng lưới Hub (\texttt{/operator/overview})}
    \label{fig:demo_uc08_overview}
\end{figure}
```

---

## 5. Các mục `_TODO_` khác còn thiếu trong `Bao_Cao_Final/`

Ngoài phần ảnh minh chứng ở `Contents/TrienKhai.tex`, nhóm lưu ý hoàn thiện nốt **3 chỗ còn `_TODO_`** trước khi xuất `main.pdf`:

1. **`Contents/TrienKhai.tex` (dòng 5):** Dán link video demo công khai (YouTube hoặc Google Drive) — **TV5**.
2. **`Contents/TongKet.tex` (dòng 15):** Bổ sung bài học kinh nghiệm sau buổi họp tổng kết và quay demo của nhóm — **TV5 + cả nhóm**.
3. **`Outro/PhuLuc.tex` (dòng 16, 17, 20):** Điền nốt bảng khai báo sử dụng Generative AI của **TV1 (Nguyễn Khang Kỳ)**, **TV2 (Châu Mạnh Phát)** và **TV5 (Đào Huy Phong)** *(TV3 và TV4 đã điền sẵn)*.

