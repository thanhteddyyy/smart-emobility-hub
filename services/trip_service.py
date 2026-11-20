"""UC5 – Nhận phương tiện, UC6 – Trả phương tiện (Submission 3, mục 2.3.7, 2.4)."""
from datetime import datetime

from data import mock_data as db
from services import audit_service, booking_service
from services.errors import BOOKING_NOT_FOUND, HOLD_EXPIRED, HUB_FULL, RESOURCE_NOT_FOUND, ServiceError


def confirmPickup(userId, bookingId):
    """UC5: Kiểm tra booking còn hạn -> xe chuyển IN_USE, booking chuyển ACTIVE."""
    with db.DATA_LOCK:
        booking = next(
            (b for b in db.BOOKINGS if b["id"] == bookingId and b["userId"] == userId),
            None,
        )
        if not booking:
            raise ServiceError(BOOKING_NOT_FOUND, "Không tìm thấy lượt đặt xe.")

        booking_service.isBookingValid(booking)

        if booking.get("type") != "VEHICLE" or booking.get("status") != "HOLDING":
            raise ServiceError(HOLD_EXPIRED, "Lượt đặt không ở trạng thái chờ nhận xe.")

        vehicle = db.getVehicle(booking.get("vehicleId"))
        if not vehicle:
            raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy phương tiện.")

        now = datetime.now().isoformat(timespec="seconds")
        vehicle["status"] = "IN_USE"
        vehicle["lastUpdatedAt"] = now

        booking["status"] = "ACTIVE"
        booking["startedAt"] = now

    audit_service.record(userId, "CONFIRM_PICKUP", bookingId, f"vehicle={vehicle['id']}")
    return booking


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
