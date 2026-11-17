# Ma trận kiểm thử  _(TV5 + TV2)_

Chép toàn bộ test case từ Submission 3 vào bảng. Sau khi chạy trên bản web, đổi `Pending` thành `Passed` / `Failed`.

| Test Case ID | Use case | Màn hình / hàm | Test tự động | Kết quả | Ảnh minh chứng |
|---|---|---|---|---|---|
| TC_UC01_01 | UC1 | `/student/search` | `tests/test_uc01_search.py::test_no_result_returns_empty_list` | Pending | |
| TC_UC01_02 | UC1 | `resolveSearchLocation` | `tests/test_uc01_search.py::test_location_unavailable` | Pending | |
| _TODO: các test case còn lại_ | | | | | |

Test bắt buộc theo phân công nhóm:
- [ ] UC3/UC4 – race condition khi đặt chỗ (`scripts/race_demo.py`)
- [ ] UC16 – lọc / loại bỏ gói dữ liệu trễ
- [ ] UC14 – cô lập dữ liệu mô phỏng
