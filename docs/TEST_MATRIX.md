# Ma trận kiểm thử _(TV5 + TV2)_

Tổng hợp toàn bộ **66 test case** từ Submission 3, ánh xạ với màn hình / hàm xử lý, test tự động (`pytest`) và kết quả chạy thực tế.

> **Trạng thái kiểm thử tự động hiện tại (`pytest -v`):** **33 passed** trên các Use Case đã hoàn thiện backend (`UC1, UC8, UC9, UC10, UC11, UC12, UC14, UC15, UC16 một phần, UC17`). Các UC còn lại (`UC2–UC7, UC13, UC16 receiveTelemetryPacket`) đang ở trạng thái `Pending` chờ TV4/TV1 hoàn tất tầng `services/`.

## 1. Bảng Test Case tổng hợp (Submission 3)

| Test Case ID | Use Case | Mô tả kịch bản | Màn hình / Hàm xử lý | Test tự động (`tests/`) | Kết quả | Ảnh minh chứng |
|---|---|---|---|---|---|---|
| TC_UC01_01 | UC1 | Không có kết quả phù hợp tiêu chí | `/student/search` · `searchVehicleAndHub` | `test_uc01_search.py::test_no_result_returns_empty_list` | Passed | |
| TC_UC01_02 | UC1 | Không xác định được vị trí tìm kiếm | `resolveSearchLocation` | `test_uc01_search.py::test_location_unavailable` | Passed | |
| TC_UC01_03 | UC1 | Tiêu chí tìm kiếm không hợp lệ (bán kính) | `validateSearchCriteria` | `test_uc01_search.py::test_invalid_radius` | Passed | |
| TC_UC01_04 | UC1 | Map API không khả dụng (fallback danh sách) | `/student/search` | _Manual / Browser_ | Pending | |
| TC_UC01_05 | UC1 | Không truy xuất được dữ liệu phương tiện/Hub | `searchVehicleAndHub` | _Manual / Mock fault_ | Pending | |
| TC_UC02_01 | UC2 | Tài nguyên không tồn tại / ngừng hoạt động | `/student/resource` · `getResourceStatus` | _Chờ `status_service.py` (TODO)_ | Pending | |
| TC_UC02_02 | UC2 | Chưa chọn tài nguyên hợp lệ | `/student/resource` | _Chờ `status_service.py` (TODO)_ | Pending | |
| TC_UC02_03 | UC2 | Không truy xuất được dữ liệu trạng thái | `getResourceStatus` | _Chờ `status_service.py` (TODO)_ | Pending | |
| TC_UC02_04 | UC2 | Biên: dữ liệu trạng thái quá cũ (`isStatusStale`) | `status_service.isStatusStale` | _Chờ `getResourceStatus` (TODO)_ | Pending | |
| TC_UC02_05 | UC2 | Biên: tài nguyên đang không khả dụng | `/student/resource` | _Chờ `status_service.py` (TODO)_ | Pending | |
| TC_UC03_01 | UC3 | Đặt xe thành công (tạo booking, giữ 15 phút) | `_booking_modal.html` · `bookVehicle` | _Chờ `booking_service.py` (TODO)_ | Pending | |
| TC_UC03_02 | UC3 | Hủy trước khi xác nhận đặt xe | `_booking_modal.html` · `cancelBooking` | _Chờ `booking_service.py` (TODO)_ | Pending | |
| TC_UC03_03 | UC3 | **BẮT BUỘC:** Nhiều người cùng đặt một xe (Race condition) | `bookVehicle` (`threading.Lock`) | `scripts/race_demo.py` | Pending | |
| TC_UC03_04 | UC3 | Lỗi khi lưu đơn đặt xe | `bookVehicle` | _Chờ `booking_service.py` (TODO)_ | Pending | |
| TC_UC04_01 | UC4 | Đặt chỗ đỗ thành công | `_booking_modal.html` · `bookParking` | _Chờ `booking_service.py` (TODO)_ | Pending | |
| TC_UC04_02 | UC4 | Khoảng thời gian đặt chỗ không hợp lệ | `bookParking` | _Chờ `booking_service.py` (TODO)_ | Pending | |
| TC_UC04_03 | UC4 | Đặt chỗ đỗ đồng thời bị trùng / Hub đầy | `bookParking` (`HUB_FULL`) | _Chờ `booking_service.py` (TODO)_ | Pending | |
| TC_UC04_04 | UC4 | Chưa đăng nhập hoặc không có quyền đặt chỗ | `/api/bookings/vehicle` | _Chờ tích hợp UC3/UC4_ | Pending | |
| TC_UC05_01 | UC5 | Nhận xe thành công | `/student/pickup` · `confirmPickup` | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC05_02 | UC5 | Đơn không hợp lệ hoặc thuộc người khác | `confirmPickup` (`BOOKING_NOT_FOUND`) | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC05_03 | UC5 | Kiểm tra thời hạn giữ xe (`HOLD_EXPIRED`) | `confirmPickup` · `isBookingValid` | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC05_04 | UC5 | Lỗi cập nhật sau thao tác nhận xe | `confirmPickup` | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC06_01 | UC6 | Trả xe pin thấp, chuyển trạng thái chờ sạc | `/student/return` · `returnVehicle` | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC06_02 | UC6 | Xe không có lượt mượn hợp lệ | `returnVehicle` | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC06_03 | UC6 | Gửi thông báo thất bại nhưng trả xe vẫn thành công | `returnVehicle` | _Chờ `trip_service.py` (TODO)_ | Pending | |
| TC_UC07_01 | UC7 | Khung giờ sạc đã được người khác đặt | `/student/charging` · `registerCharging` | _Chờ `charging_service.py` (TODO)_ | Pending | |
| TC_UC07_02 | UC7 | Race condition: 2 SV đăng ký cùng cổng sạc | `registerCharging` | _Chờ `charging_service.py` (TODO)_ | Pending | |
| TC_UC07_03 | UC7 | Đăng ký cổng sạc còn trống thành công | `registerCharging` | _Chờ `charging_service.py` (TODO)_ | Pending | |
| TC_UC08_01 | UC8 | Biên: một Hub có dữ liệu cấu hình không hợp lệ | `monitor_service.computeHubUsage` | _Manual / Unit_ | Pending | |
| TC_UC08_02 | UC8 | Không có Hub phù hợp với bộ lọc | `/operator/overview` · `getNetworkOverview` | `test_uc08_uc09_uc10_monitor.py::test_overview_filter_no_match` | Passed | |
| TC_UC08_03 | UC8 | Người dùng không đủ quyền truy cập dashboard | `/operator/overview` | `test_uc08_uc09_uc10_monitor.py::test_overview_rbac_student_denied` | Passed | |
| TC_UC08_04 | UC8 | Không truy xuất được dữ liệu giám sát | `getNetworkOverview` | _Manual / Mock fault_ | Pending | |
| TC_UC08_05 | UC8 | Một Hub mất kết nối, các Hub khác vẫn hoạt động | `isolateDisconnectedHub` · `getNetworkOverview` | `test_uc08_uc09_uc10_monitor.py::test_overview_isolated_offline_hub` | Passed | |
| TC_UC09_01 | UC9 | Biên: dòng tài nguyên có timestamp quá cũ | `/operator/resources/<hubId>` · `getHubResources` | `test_uc08_uc09_uc10_monitor.py::test_resources_stale_timestamp_detected` | Passed | |
| TC_UC09_02 | UC9 | Không truy xuất được dữ liệu tài nguyên Hub | `getHubResources` | `test_uc08_uc09_uc10_monitor.py::test_resources_hub_not_found` | Passed | |
| TC_UC10_01 | UC10 | Quá tải vượt ngưỡng, gọi nhiều lần không tạo trùng | `/operator/alerts` · `evaluateHubLoad` | `test_uc08_uc09_uc10_monitor.py::test_overload_alert_no_duplicate` | Passed | |
| TC_UC10_02 | UC10 | Biên: mức sử dụng thấp hơn ngưỡng, không cảnh báo | `evaluateHubLoad` | `test_uc08_uc09_uc10_monitor.py::test_low_usage_no_overload_alert` | Passed | |
| TC_UC10_03 | UC10 | Ngoại lệ: dữ liệu quá cũ, không tạo cảnh báo | `evaluateHubLoad` | `test_uc08_uc09_uc10_monitor.py::test_stale_hub_does_not_generate_new_alert` | Passed | |
| TC_UC11_01 | UC11 | Điều phối xe AVAILABLE sang Hub đích còn chỗ | `/operator/dispatch` · `processDispatch` | `test_uc11_uc12_dispatch_incident.py::test_dispatch_success` | Passed | |
| TC_UC11_02 | UC11 | Xe vừa bị đặt trước khi Operator xác nhận | `processDispatch` (`DISPATCH_CONFLICT`) | `test_uc11_uc12_dispatch_incident.py::test_dispatch_vehicle_conflict` | Passed | |
| TC_UC11_03 | UC11 | Hub đích không đủ chỗ đỗ trống (`HUB_FULL`) | `processDispatch` | `test_uc11_uc12_dispatch_incident.py::test_dispatch_destination_hub_full` | Passed | |
| TC_UC11_04 | UC11 | Hủy lệnh điều phối đang ở trạng thái PENDING | `cancelDispatchOrder` | `test_uc11_uc12_dispatch_incident.py::test_cancel_pending_dispatch_order` | Passed | |
| TC_UC12_01 | UC12 | Tạm ngưng tài nguyên, chuyển IN_PROGRESS, ghi AuditLog | `/operator/incidents/<id>` · `handlePauseResource` | `test_uc11_uc12_dispatch_incident.py::test_incident_pause_resource_and_audit` | Passed | |
| TC_UC12_02 | UC12 | Hoàn tất sửa chữa và khôi phục trạng thái tài nguyên | `completeIncident` | `test_uc11_uc12_dispatch_incident.py::test_incident_complete_restores_resource` | Passed | |
| TC_UC12_03 | UC12 | Cô lập Hub mất kết nối không làm gián đoạn Hub khác | `isolateDisconnectedHub` | `test_uc11_uc12_dispatch_incident.py::test_incident_isolate_disconnected_hub` | Passed | |
| TC_UC12_04 | UC12 | Tài khoản Sinh viên gọi chức năng sự cố bị từ chối | `/operator/incidents` | `test_uc11_uc12_dispatch_incident.py::test_incident_rbac_student_denied` | Passed | |
| TC_UC13_01 | UC13 | Tạo lịch sạc phù hợp và phê duyệt, lưu lịch | `/operator/schedule` · `generateSchedule` | _Chờ `schedule_service.py` (TODO)_ | Pending | |
| TC_UC13_02 | UC13 | Operator chỉnh sửa lịch sạc đề xuất trước khi duyệt | `editSchedule` | _Chờ `schedule_service.py` (TODO)_ | Pending | |
| TC_UC13_03 | UC13 | Tự động phê duyệt lịch sạc khi hợp lệ | `approveSchedule` | _Chờ `schedule_service.py` (TODO)_ | Pending | |
| TC_UC13_04 | UC13 | Phát hiện xung đột trụ sạc / khung giờ / Hub quá tải | `validateSchedule` | _Chờ `schedule_service.py` (TODO)_ | Pending | |
| TC_UC13_05 | UC13 | Xử lý lỗi đồng bộ khi lưu lịch sạc | `saveSchedule` | _Chờ `schedule_service.py` (TODO)_ | Pending | |
| TC_UC14_01 | UC14 | **BẮT BUỘC:** Chạy mô phỏng What-if cô lập DB thật | `/operator/simulation` · `runSimulation` | `test_uc14_uc15_uc16_simulation_i18n.py::test_simulation_isolates_operational_db` | Passed | |
| TC_UC14_02 | UC14 | Chuyển tiếp áp dụng đề xuất mô phỏng sang Điều phối | `applyRecommendation` | `test_uc14_uc15_uc16_simulation_i18n.py::test_simulation_apply_recommendation` | Passed | |
| TC_UC14_03 | UC14 | Nhập tham số mô phỏng không hợp lệ | `validateParameters` | `test_uc14_uc15_uc16_simulation_i18n.py::test_simulation_invalid_parameters` | Passed | |
| TC_UC14_04 | UC14 | Không thể khởi tạo môi trường mô phỏng | `initVirtualEnvironment` | _Manual / Mock fault_ | Pending | |
| TC_UC15_01 | UC15 | Chuyển đổi giao diện Sáng ↔ Tối (`tokens.css`) | `static/js/theme.js` | _Manual / Browser_ | Pending | |
| TC_UC15_02 | UC15 | Đổi ngôn ngữ VN ↔ EN khi đang nhập form (không mất dữ liệu) | `static/js/i18n.js`, `vi.json`, `en.json` | `test_uc14_uc15_uc16_simulation_i18n.py::test_i18n_json_valid_and_synced` | Passed (JSON) | |
| TC_UC15_03 | UC15 | Lỗi khi lưu tùy chọn giao diện (localStorage bị chặn) | `theme.js`, `i18n.js` | _Manual / Browser_ | Pending | |
| TC_UC16_01 | UC16 | Tiếp nhận gói dữ liệu mới hợp lệ, đẩy realtime `/api/state` | `/api/state`, `simulateTick` | `test_uc14_uc15_uc16_simulation_i18n.py::test_api_state_endpoint` | Passed | |
| TC_UC16_02 | UC16 | **BẮT BUỘC:** Lọc / loại bỏ gói dữ liệu trễ (NFR08) | `isOutdatedPacket` / `ingestResourceStatus` | `test_uc14_uc15_uc16_simulation_i18n.py::test_realtime_outdated_packet_detected` | Passed (helper) / Pending (endpoint) | |
| TC_UC16_03 | UC16 | Gói tin sai định dạng hoặc `resourceId` không tồn tại | `validatePacket` | _Chờ `realtime_service.py` (TODO)_ | Pending | |
| TC_UC16_04 | UC16 | Gói tin gắn cờ What-if chỉ ghi vào môi trường ảo | `ingestResourceStatus` | _Chờ `realtime_service.py` (TODO)_ | Pending | |
| TC_UC17_01 | UC17 | Đăng nhập SSO thành công (Operator / Student) | `/login` · `authenticate` | `test_uc17_auth.py::test_operator_can_open_dashboard` | Passed | |
| TC_UC17_02 | UC17 | Hủy đăng nhập giữa chừng | `/login` | _Manual / Browser_ | Pending | |
| TC_UC17_03 | UC17 | Sai mật khẩu hoặc tài khoản không hợp lệ | `/login` · `authenticate` | `test_uc17_auth.py::test_wrong_password_shows_error` | Passed | |
| TC_UC17_04 | UC17 | Dịch vụ SSO không phản hồi (`SSO_UNAVAILABLE`) | `hinh14_SSOUnavailable.html` | _Manual / Mock fault_ | Pending | |

---

## 2. Checklist 3 Test Bắt Buộc Theo Phân Công Nhóm
- [ ] **UC3/UC4 – Race condition khi đặt chỗ** (`scripts/race_demo.py`): Hiện `bookVehicle` chưa được hiện thực (`TODO(UC3)`), script trả về `CHƯA ĐẠT`. Cần test lại ngay khi TV4/TV1 hoàn thành `bookVehicle`.
- [ ] **UC16 – Lọc / loại bỏ gói dữ liệu trễ**: Hàm `isOutdatedPacket` đã hoạt động (`Passed`), cần TV4 hoàn thành `validatePacket` và `ingestResourceStatus` cho `/api/telemetry` để demo end-to-end.
- [x] **UC14 – Cô lập dữ liệu mô phỏng**: Đã chứng minh qua `test_simulation_isolates_operational_db` — chạy What-if xong, `db.HUBS`, `db.VEHICLES`, `db.PARKING_SPOTS` giữ nguyên 100%.
