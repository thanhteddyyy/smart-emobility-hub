# Hợp đồng dữ liệu

Tên trường và mã trạng thái mà giao diện (TV1–TV3) và logic (TV4) cùng dùng.
**Không đổi tên trường sau khi đã chốt.** Nếu buộc phải đổi, báo cả nhóm.

## 1. Dữ liệu gốc (`data/seed.json`)

### Hub
| Trường | Kiểu | Ví dụ | Ghi chú |
|---|---|---|---|
| id | string | `H1` | |
| name | string | `Ga Metro ĐHQG` | |
| area | string | `Metro` | Metro / Ký túc xá / Trường đại học / Dịch vụ |
| lat, lng | number | `10.8664`, `106.801` | Tọa độ gần đúng, chỉ để demo |
| parkingCapacity | int | `20` | |
| status | string | `ACTIVE` | `ACTIVE`, `OFFLINE` |
| lastUpdatedAt | string | `2026-11-17T08:00:00` | ISO 8601 |

### Vehicle (xe)
| Trường | Kiểu | Ví dụ | Ghi chú |
|---|---|---|---|
| id | string | `EB-204` | |
| type | string | `E_BIKE` | `E_BIKE`, `E_SCOOTER` |
| model | string | `VinFast Feliz S` | |
| batteryLevel | int | `90` | 0–100 |
| status | string | `AVAILABLE` | `AVAILABLE`, `RESERVED`, `IN_USE`, `CHARGING`, `MAINTENANCE` |
| hubId | string | `H2` | |
| lastUpdatedAt | string | | |

### ParkingSpot (chỗ đỗ)
`id` (`H1-P01`), `hubId`, `status`: `FREE`, `OCCUPIED`, `RESERVED`

### ChargingPort (cổng sạc)
`id` (`H1-C01`), `hubId`, `powerKw`, `status`: `AVAILABLE`, `IN_USE`, `OUT_OF_ORDER`

### Incident (sự cố)
`id` (`INC-001`), `hubId`, `resourceType` (`HUB`, `VEHICLE`, `CHARGING_PORT`), `resourceId`, `description`,
`priority` (`HIGH`, `MEDIUM`, `LOW`), `status` (`OPEN`, `IN_PROGRESS`, `RESOLVED`), `operator`, `createdAt`

### User
`id`, `name`, `email`, `password`, `role` (`STUDENT`, `OPERATOR`; `GUEST` chỉ để demo lỗi không đủ quyền)

Trong session: `session["user"] = {id, name, role}`. Trong template: biến `currentUser`.

## 2. Dữ liệu sinh ra khi chạy (TV4 chốt khi hiện thực)

| Bảng | Trường đề xuất |
|---|---|
| `BOOKINGS` | id, type (`VEHICLE`/`PARKING`), userId, vehicleId, hubId, status (`HOLDING`, `ACTIVE`, `COMPLETED`, `CANCELLED`, `EXPIRED`), createdAt, expiresAt |
| `CHARGING_REGISTRATIONS` | id, userId, hubId, portId, timeSlot, batteryLevel, status |
| `DISPATCH_ORDERS` | id, operatorId, sourceHubId, destHubId, vehicleIds, status (`PENDING`, `COMPLETED`, `CANCELLED`), createdAt |
| `AUDIT_LOGS` | id, actorId, action, targetId, details, timestamp |

## 3. Dữ liệu service trả cho giao diện

### Trạng thái Hub – `status_service.buildHubStatus(hub)`
`hubId, name, area, lat, lng, status, availableVehicles, emptySpots, totalSpots, availablePorts, totalPorts, lastUpdatedAt, isStale`

### Kết quả tìm kiếm – `search_service.searchVehicleAndHub(...)`
Danh sách "Trạng thái Hub", mỗi phần tử thêm: `distanceKm, walkMinutes, matchingVehicles` (danh sách Vehicle)

### Tổng quan mạng lưới – `monitor_service.getNetworkOverview()`
`activeHubCount, totalVehicles, availableVehicles, availablePorts, emptySpots, openIncidents, updatedAt, hubs`
Mỗi phần tử `hubs` = "Trạng thái Hub" + `usageRate` (0–1)

### `/api/state` (dùng cho `data-rt`)
```json
{ "ok": true,
  "network": { "availableVehicles": 30, "emptySpots": 15, "...": "..." },
  "hubs": { "H1": { "availableVehicles": 7, "emptySpots": 2, "usageRate": 0.9, "...": "..." } } }
```

## 4. Mã lỗi (`services/errors.py`)

| Mã | Use case | Giao diện hiển thị |
|---|---|---|
| `INVALID_CRITERIA` | UC1 | Thông báo đỏ dưới form tìm kiếm |
| `LOCATION_UNAVAILABLE` | UC1 | Yêu cầu nhập vị trí thủ công |
| `RESOURCE_NOT_FOUND` | UC2 | Thông báo không tìm thấy |
| `VEHICLE_CONFLICT` | UC3 | Hình 3 |
| `HUB_FULL` | UC4, UC6, UC11 | Hình 4 + gợi ý Hub thay thế |
| `HOLD_EXPIRED` | UC3, UC5 | Hình 5 |
| `BOOKING_NOT_FOUND` | UC5 | Thông báo lỗi |
| `NO_PORT_AVAILABLE` | UC7 | Hình 12 |
| `INVALID_CREDENTIALS` | UC17 | Thông báo dưới form đăng nhập |
| `SSO_UNAVAILABLE` | UC17 | Hình 14 |
| `ACCESS_DENIED` | UC17, UC8 | Trang "Không đủ quyền truy cập" |
| `SESSION_EXPIRED` | UC8, UC11 | Chuyển về đăng nhập |
| `DISPATCH_CONFLICT` | UC11 | Thông báo trên màn hình điều phối |
| `INCIDENT_NOT_FOUND` | UC12 | Thông báo lỗi |
| `INVALID_PARAMETERS` | UC14 | Đánh dấu tham số sai |
| `OUTDATED_PACKET` | UC16 | Ghi log, không hiện cho người dùng |

API trả lỗi dạng: `{"ok": false, "error": "MÃ_LỖI", "message": "..."}` (HTTP 400).
