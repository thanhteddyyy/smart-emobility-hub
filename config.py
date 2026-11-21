"""Hằng số cấu hình dùng chung. Quy ước: hằng số viết ALL_CAPS."""

BRAND_NAME = "E-Hub"            # TV5 chốt tên thương hiệu thống nhất rồi sửa ở đây
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
SECRET_KEY = "dev-only-secret"  # chỉ dùng cho demo

# UC16 / NFR02 – cập nhật gần thời gian thực
POLL_INTERVAL_SECONDS = 5       # trình duyệt gọi /api/state mỗi 5 giây
SIMULATOR_INTERVAL_SECONDS = 5  # bộ giả lập IoT đổi dữ liệu mỗi 5 giây
SIMULATOR_ENABLED = True

# UC2 – dữ liệu cũ hơn ngưỡng này thì hiện cảnh báo "dữ liệu cũ"
STALE_THRESHOLD_SECONDS = 60

# UC1 – giới hạn tiêu chí tìm kiếm
MIN_RADIUS_KM = 0.1
MAX_RADIUS_KM = 10.0
DEFAULT_RADIUS_KM = 10.0
DEFAULT_LOCATION = {"lat": 10.8806, "lng": 106.8054}  # Bách khoa CS2

# UC3 – thời gian giữ xe sau khi đặt
HOLD_TIME_MINUTES = 15

# UC10 – ngưỡng cảnh báo mức sử dụng Hub
OVERLOAD_WARNING_RATE = 0.8
OVERLOAD_CRITICAL_RATE = 0.95
