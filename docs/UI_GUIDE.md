# Quy ước giao diện  _(TV5 hoàn thiện trong ngày đầu)_

## Tên thương hiệu
Mockup đang dùng lẫn `E-HUB`, `E-Mobility`, `E-Hub`. **Chốt một tên**, rồi sửa `BRAND_NAME` trong `config.py`.
- [ ] Tên chốt: ______

## Màu (lấy từ Figma → tab Inspect), sửa trong `static/css/tokens.css`
| Biến | Dùng cho | Sáng | Tối |
|---|---|---|---|
| `--color-primary` | Nút chính, điểm nhấn | _TODO_ | _TODO_ |
| `--color-bg` | Nền trang | | |
| `--color-surface` | Nền thẻ | | |
| `--color-text` / `--color-muted` | Chữ chính / chữ phụ | | |
| `--color-danger` / `--color-warning` | Lỗi / cảnh báo | | |

## Chữ
- Font: _TODO (theo Figma)_ · Cỡ tiêu đề / nội dung / chú thích: _TODO_

## Thành phần dùng lại (class có sẵn trong `tokens.css`)
`card-x` (thẻ) · `btn-primary-x`, `btn-outline-x` (nút) · `badge-ok|warn|danger` · `alert-x danger` · `seg` (nút gạt)

## Song ngữ
- Key đặt dạng `nhóm.tên`: `search.title`, `action.book`, `dash.overview`.
- Thêm key vào **cả** `static/i18n/vi.json` và `en.json`.

## Lệch giữa mockup và bản code (ghi lại để đưa vào báo cáo)
- Hình 20–21 dùng sidebar khác → code dùng chung `base_dashboard.html`.
- Hình 5–12 chỉ có bản sáng → bản tối sinh từ `tokens.css`.
- Form đăng nhập email/mật khẩu = trang SSO giả lập; bỏ nút Sign up.
