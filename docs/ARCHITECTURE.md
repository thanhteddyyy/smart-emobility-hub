# Kiến trúc: code ↔ thiết kế Submission 3

## Thư mục ↔ Implementation view

| Tầng (Submission 3) | Thư mục | Ghi chú |
|---|---|---|
| Presentation | `templates/`, `static/`, `blueprints/auth|student|operator/` | Web Client (mobile) + Web Dashboard |
| API | `blueprints/api/` | REST trả JSON; realtime làm bằng polling `/api/state` thay cho WebSocket |
| Business | `services/` | Mỗi file ứng với một nhóm Control |
| Data Access | `data/mock_data.py`, `data/seed.json` | Thay PostgreSQL bằng dữ liệu trong bộ nhớ |
| Integration | `services/auth_service.py` (SSO giả lập), `services/realtime_service.py` (Data Simulator), Leaflet/OpenStreetMap (Map API) | |

## Service ↔ Use case ↔ Control class

| File | Use case | Lớp Control trong Class diagram |
|---|---|---|
| `search_service.py` | UC1 | SearchController |
| `status_service.py` | UC2 | ResourceStatusController |
| `booking_service.py` | UC3, UC4 | BookingController |
| `trip_service.py` | UC5, UC6 | TripController |
| `charging_service.py` | UC7 | _TODO: điền tên lớp_ |
| `monitor_service.py` | UC8 | NetworkMonitorController |
| `alert_service.py` | UC9, UC10 | _TODO_ |
| `dispatch_service.py` | UC11 | DispatchController |
| `incident_service.py` | UC12 | _TODO_ |
| `schedule_service.py` | UC13 | _TODO_ |
| `simulation_service.py` | UC14 | _TODO_ |
| `static/js/theme.js`, `i18n.js` | UC15 | _TODO_ |
| `realtime_service.py` | UC16 | _TODO_ |
| `auth_service.py` | UC17 | AuthController |
| `audit_service.py` | NFR11 | AuditLog |

## Khác biệt giữa MVP và thiết kế (ghi vào báo cáo)

_TODO(TV4): hoàn thiện._
- Không có database, Load Balancer; chạy 1 tiến trình Flask.
- Realtime dùng polling 5 giây thay cho WebSocket/SSE (vẫn đạt NFR02 ≤ 15 giây).
- SSO, Notification, IoT là giả lập.
- Entity là `dict` đọc từ JSON thay cho class.
