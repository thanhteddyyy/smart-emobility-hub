"""Lỗi nghiệp vụ dùng chung.

Service KHÔNG tự hiển thị lỗi. Service ném ServiceError(code, message);
route bắt lỗi và giao diện quyết định hiện thế nào (vd. VEHICLE_CONFLICT -> hộp thoại đỏ Hình 3).
Danh sách mã lỗi: docs/DATA_CONTRACT.md
"""


class ServiceError(Exception):
    def __init__(self, code, message=""):
        super().__init__(message or code)
        self.code = code
        self.message = message or code

    def toDict(self):
        return {"ok": False, "error": self.code, "message": self.message}


# Mã lỗi (hằng số ALL_CAPS)
INVALID_CRITERIA = "INVALID_CRITERIA"            # UC1
LOCATION_UNAVAILABLE = "LOCATION_UNAVAILABLE"    # UC1
RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"        # UC2
VEHICLE_CONFLICT = "VEHICLE_CONFLICT"            # UC3 – xe vừa bị người khác đặt (Hình 3)
HUB_FULL = "HUB_FULL"                            # UC4, UC6 – Hub hết chỗ (Hình 4)
HOLD_EXPIRED = "HOLD_EXPIRED"                    # UC3, UC5 – hết thời gian giữ xe (Hình 5)
BOOKING_NOT_FOUND = "BOOKING_NOT_FOUND"          # UC5
NO_PORT_AVAILABLE = "NO_PORT_AVAILABLE"          # UC7 (Hình 12)
INVALID_CREDENTIALS = "INVALID_CREDENTIALS"      # UC17 EX1
SSO_UNAVAILABLE = "SSO_UNAVAILABLE"              # UC17 EX2 (Hình 14)
ACCESS_DENIED = "ACCESS_DENIED"                  # UC17 EX3, UC8
SESSION_EXPIRED = "SESSION_EXPIRED"              # UC8, UC11
DISPATCH_CONFLICT = "DISPATCH_CONFLICT"          # UC11
INCIDENT_NOT_FOUND = "INCIDENT_NOT_FOUND"        # UC12
INVALID_PARAMETERS = "INVALID_PARAMETERS"        # UC14
OUTDATED_PACKET = "OUTDATED_PACKET"              # UC16
