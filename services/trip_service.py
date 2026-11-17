"""UC5 – Nhận phương tiện, UC6 – Trả phương tiện (Submission 3, mục 2.3.7, 2.4)."""
from data import mock_data as db
from services.errors import BOOKING_NOT_FOUND, HOLD_EXPIRED, HUB_FULL, ServiceError


def confirmPickup(userId, bookingId):
    """TODO(UC5): Kiểm tra booking còn hạn -> xe chuyển IN_USE, booking chuyển ACTIVE."""
    raise NotImplementedError("UC5 confirmPickup")


def returnVehicle(userId, bookingId, hubId):
    """TODO(UC6): Hub trả hết chỗ -> ServiceError(HUB_FULL) + gợi ý Hub khác.
    Thành công: xe -> AVAILABLE tại hubId, chiếm 1 chỗ đỗ, booking -> COMPLETED."""
    raise NotImplementedError("UC6 returnVehicle")
