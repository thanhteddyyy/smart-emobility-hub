"""UC3 – Đặt xe, UC4 – Đặt chỗ đỗ (Submission 3, mục 2.3).

DEMO BẮT BUỘC – race condition: hai yêu cầu cùng đặt một xe, chỉ MỘT yêu cầu thành công.
Gợi ý: bọc toàn bộ bước "kiểm tra xe còn trống -> đổi trạng thái -> tạo booking" trong
`with db.DATA_LOCK:`. Thử bằng scripts/race_demo.py.
"""
from data import mock_data as db
from services.errors import HUB_FULL, VEHICLE_CONFLICT, ServiceError


def bookVehicle(userId, vehicleId):
    """TODO(UC3): Xe không còn AVAILABLE -> ServiceError(VEHICLE_CONFLICT) (Hình 3).
    Thành công: xe -> RESERVED, thêm booking {id, type:'VEHICLE', userId, vehicleId, hubId, status:'HOLDING', expiresAt}
    với expiresAt = bây giờ + config.HOLD_TIME_MINUTES."""
    raise NotImplementedError("UC3 bookVehicle")


def bookParking(userId, hubId, timeSlot):
    """TODO(UC4): Hub hết chỗ FREE -> ServiceError(HUB_FULL) kèm gợi ý Hub thay thế (Hình 4)."""
    raise NotImplementedError("UC4 bookParking")


def cancelBooking(userId, bookingId):
    """TODO(UC3/UC4): Hủy booking, trả tài nguyên về trạng thái trống."""
    raise NotImplementedError("UC3/UC4 cancelBooking")


def isBookingValid(booking):
    """TODO(UC3): Booking.isValid(): còn hạn giữ và chưa bị hủy. Hết hạn -> HOLD_EXPIRED (Hình 5)."""
    raise NotImplementedError("UC3 isBookingValid")
