"""UC5 – Nhận phương tiện, UC6 – Trả phương tiện (Submission 3, mục 2.3.7, 2.4)."""
from datetime import datetime

from data import mock_data as db
from services.errors import BOOKING_NOT_FOUND, HOLD_EXPIRED, HUB_FULL, ServiceError


def confirmPickup(userId, bookingId):
    """TODO(UC5): Kiểm tra booking còn hạn -> xe chuyển IN_USE, booking chuyển ACTIVE."""
    raise NotImplementedError("UC5 confirmPickup")


def returnVehicle(userId, bookingId, hubId):
    """TODO(UC6): Hub trả hết chỗ -> ServiceError(HUB_FULL) + gợi ý Hub khác.
    Thành công: xe -> AVAILABLE tại hubId, chiếm 1 chỗ đỗ, booking -> COMPLETED."""
    with db.DATA_LOCK:
        booking = next((b for b in db.BOOKINGS if b["id"] == bookingId and b["userId"] == userId),
            None)
        if not booking:
            raise ServiceError("BOOKING_NOT_FOUND")
        if booking["type"] != "VEHICLE" or booking["status"] != "ACTIVE":
            raise ServiceError("INVALID_BOOKING")
        vehicle = db.getVehicle(booking["vehicleId"])
        hub = db.getHub(hubId)
        if not vehicle:
            raise ServiceError("RESOURCE_NOT_FOUND")
        if not hub or hub["status"] != "ACTIVE":
            raise ServiceError("HUB_NOT_FOUND")

        freeSpot = next(
            (s for s in db.PARKING_SPOTS if s["hubId"] == hubId and s["status"] == "FREE"), None)

        if not freeSpot:
            raise ServiceError("HUB_FULL")

        freeSpot["status"] = "OCCUPIED"
        vehicle["hubId"] = hubId
        vehicle["status"] = "AVAILABLE"
        vehicle["lastUpdatedAt"] = datetime.now().isoformat(timespec="seconds")

        booking["status"] = "COMPLETED"

        return {"booking": booking, "vehicle": vehicle, "parkingSpot": freeSpot}
