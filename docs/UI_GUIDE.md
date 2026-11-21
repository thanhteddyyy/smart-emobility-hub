# Quy ước giao diện _(TV5 hoàn thiện)_

## Tên thương hiệu
Mockup đang dùng lẫn `E-HUB`, `E-Mobility`, `E-Hub`. Nhóm thống nhất chốt tên:
- [x] Tên chốt: **`E-Hub`** (đã cấu hình `BRAND_NAME = "E-Hub"` trong `config.py`).

---

## Bảng màu Sáng / Tối (`static/css/tokens.css`)
Lấy từ Figma Light & Dark Mode (Free Figma Admin Dashboard UI Kit). Mọi file CSS/HTML bắt buộc dùng `var(--...)`, không hardcode mã màu.

| Biến | Dùng cho | Sáng (`:root`) | Tối (`[data-theme="dark"]`) |
|---|---|---|---|
| `--color-primary` | Nút chính, điểm nhấn | `#548afe` | `#548afe` |
| `--color-primary-strong` | Hover nút chính | `#3b6fe8` | `#6e9eff` |
| `--color-primary-soft` | Nền nhấn nhẹ | `rgba(93, 135, 255, 0.1)` | `rgba(93, 135, 255, 0.15)` |
| `--color-secondary` | Điểm nhấn phụ | `#49beff` | `#49beff` |
| `--color-bg` | Nền trang | `#f8fafc` | `#2a3447` |
| `--color-surface` | Nền thẻ / card | `#ffffff` | `#2a3547` |
| `--color-surface-elevated` | Nền nổi (modal, dropdown) | `#ffffff` | `#202936` |
| `--color-text` | Chữ chính | `#2a3547` | `#ffffff` |
| `--color-text-strong` | Tiêu đề đậm | `#000000` | `#ffffff` |
| `--color-muted` | Chữ phụ | `rgba(42, 53, 71, 0.6)` | `rgba(255, 255, 255, 0.6)` |
| `--color-border` | Viền thẻ / bảng | `rgba(42, 53, 71, 0.1)` | `rgba(255, 255, 255, 0.1)` |
| `--color-success` / `--color-success-strong` | Trạng thái tốt / hoàn tất | `#13deb9` / `#14ae5c` | `#13deb9` / `#14ae5c` |
| `--color-warning` | Cảnh báo | `#ffae1f` | `#ffae1f` |
| `--color-danger` / `--color-error` | Lỗi / nguy hiểm | `#fa896b` / `#ff383c` | `#fa896b` / `#ff383c` |
| `--color-info` | Thông tin | `#539bff` | `#539bff` |
| `--color-shadow` | Đổ bóng thẻ | `rgba(70, 109, 174, 0.08)` | `rgba(0, 0, 0, 0.25)` |

---

## Chữ & Bo góc
- **Font nội dung (`--font`)**: `"DM Sans", "Be Vietnam Pro", system-ui, -apple-system, "Segoe UI", sans-serif`
- **Font tiêu đề (`--font-display`)**: `"Plus Jakarta Sans", "Be Vietnam Pro", system-ui, sans-serif`
- **Cỡ chữ tham chiếu**: Tiêu đề trang `1.25rem–1.5rem` (bold), tiêu đề thẻ `1rem` (semibold), nội dung `0.875rem–0.95rem`, chú thích/badge `0.75rem–0.8rem`.
- **Bo góc chuẩn (`--radius`)**: `12px` cho thẻ/panel; `8px` cho nút bấm; `999px` cho pill/segmented control.

---

## Thành phần dùng lại (class có sẵn trong `tokens.css`)
- Thẻ: `card-x`
- Nút: `btn-primary-x`, `btn-outline-x`
- Nhãn trạng thái: `badge-ok`, `badge-warn`, `badge-danger`, `badge-info-x`
- Thông báo: `alert-x danger`, `alert-x success`
- Nút gạt (Theme/Ngôn ngữ): `seg` (với `button.active`)

---

## Song ngữ (`static/i18n/vi.json`, `static/i18n/en.json`)
- Key đặt dạng `nhóm.tên`: ví dụ `search.placeholder`, `action.book`, `dash.overview`, `sim.paramsTitle`, `tv.VEHICLE_CONFLICT`.
- Mọi chữ hiển thị trên UI gắn `data-i18n="group.key"` (hoặc `data-i18n-placeholder` cho ô nhập).
- Đảm bảo **cả hai** file `vi.json` và `en.json` luôn có cùng tập key (hiện đã đồng bộ 194 key, hợp lệ JSON).
- Khi đổi Sáng/Tối hoặc VN/EN (UC15), `theme.js` và `i18n.js` cập nhật trực tiếp DOM và lưu `localStorage`, không reload trang nên không mất dữ liệu đang nhập trong form.

---

## Lệch giữa mockup Submission 2 và bản code (ghi lại để đưa vào báo cáo)
- Hình 20–21 dùng sidebar khác → code dùng chung `templates/base_dashboard.html` để thống nhất điều hướng Operator.
- Hình 5–12 chỉ có bản sáng → bản tối được sinh tự động thông qua biến CSS trong `static/css/tokens.css`.
- Form đăng nhập email/mật khẩu là trang SSO giả lập (UC17); bỏ nút Sign up để đúng phạm vi tài khoản ĐHQG/Vận hành.
