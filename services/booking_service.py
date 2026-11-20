"""UC3 – Đặt xe, UC4 – Đặt chỗ đỗ (Submission 3, mục 2.3).

DEMO BẮT BUỘC – race condition: hai yêu cầu cùng đặt một xe, chỉ MỘT yêu cầu thành công.
Toàn bộ bước kiểm tra -> đổi trạng thái -> tạo booking được bọc trong `with db.DATA_LOCK:`.
Thử bằng: python scripts/race_demo.py
"""
from datetime import datetime, timedelta

import config
from data import mock_data as db
from services import audit_service
from services.errors import (
    BOOKING_NOT_FOUND,
    HOLD_EXPIRED,
    HUB_FULL,
    INVALID_PARAMETERS,
    RESOURCE_NOT_FOUND,
    VEHICLE_CONFLICT,
    ServiceError,
)


def isBookingValid(booking):
    """UC3: Booking.isValid() – còn hạn giữ và chưa bị hủy. Hết hạn -> HOLD_EXPIRED (Hình 5)."""
    if not booking:
        raise ServiceError(BOOKING_NOT_FOUND, "Không tìm thấy lượt đặt.")
    if booking.get("status") in ("CANCELLED", "EXPIRED", "COMPLETED"):
        raise ServiceError(HOLD_EXPIRED, "Lượt đặt không còn hiệu lực.")
    expiresAt = booking.get("expiresAt")
    if expiresAt and datetime.now() > datetime.fromisoformat(expiresAt):
        with db.DATA_LOCK:
            booking["status"] = "EXPIRED"
            if booking.get("type") == "VEHICLE" and booking.get("vehicleId"):
                vehicle = db.getVehicle(booking["vehicleId"])
                if vehicle and vehicle["status"] == "RESERVED":
                    vehicle["status"] = "AVAILABLE"
            elif booking.get("type") == "PARKING" and booking.get("spotId"):
                spot = db.findById(db.PARKING_SPOTS, booking["spotId"])
                if spot and spot["status"] == "RESERVED":
                    spot["status"] = "FREE"
        raise ServiceError(HOLD_EXPIRED, "Đã hết thời gian giữ xe (15 phút).")
    return True


def bookVehicle(userId, vehicleId):
    """UC3: Xe không còn AVAILABLE -> ServiceError(VEHICLE_CONFLICT) (Hình 3).
    Thành công: xe -> RESERVED, thêm booking HOLDING với expiresAt = now + HOLD_TIME_MINUTES."""
    with db.DATA_LOCK:
        vehicle = db.getVehicle(vehicleId)
        if not vehicle:
            raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy phương tiện.")
        if vehicle["status"] != "AVAILABLE":
            raise ServiceError(VEHICLE_CONFLICT, "Xe vừa được người khác đặt hoặc không sẵn sàng.")

        now = datetime.now()
        vehicle["status"] = "RESERVED"
        vehicle["lastUpdatedAt"] = now.isoformat(timespec="seconds")

        booking = {
            "id": f"BK-{len(db.BOOKINGS) + 1:04d}",
            "type": "VEHICLE",
            "userId": userId,
            "vehicleId": vehicle["id"],
            "hubId": vehicle["hubId"],
            "status": "HOLDING",
            "createdAt": now.isoformat(timespec="seconds"),
            "expiresAt": (now + timedelta(minutes=config.HOLD_TIME_MINUTES)).isoformat(timespec="seconds"),
        }
        db.BOOKINGS.append(booking)

    audit_service.record(userId, "BOOK_VEHICLE", booking["id"], f"vehicle={vehicle['id']} hub={vehicle['hubId']}")
    return booking


def bookParking(userId, hubId, timeSlot):
    """UC4: Hub hết chỗ FREE -> ServiceError(HUB_FULL) (Hình 4)."""
    if not timeSlot:
        raise ServiceError(INVALID_PARAMETERS, "Thiếu thời gian đặt chỗ.")
    try:
        slotText = str(timeSlot).strip()
        if len(slotText) == 5 and slotText[2] == ":":
            datetime.strptime(slotText, "%H:%M")
            slotTime = None
        else:
            slotTime = datetime.fromisoformat(slotText.replace("Z", "+00:00"))
        if slotTime is not None and slotTime.tzinfo:
            slotTime = slotTime.replace(tzinfo=None)
        if slotTime is not None and slotTime < datetime.now():
            raise ServiceError(INVALID_PARAMETERS, "Không thể đặt chỗ trong quá khứ.")
    except ValueError:
        raise ServiceError(INVALID_PARAMETERS, "Thời gian đặt chỗ không hợp lệ.")
    with db.DATA_LOCK:
        hub = db.getHub(hubId)
        if not hub or hub["status"] != "ACTIVE":
            raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy Hub đang hoạt động.")

        freeSpot = next((s for s in db.spotsOfHub(hubId) if s["status"] == "FREE"), None)
        if not freeSpot:
            raise ServiceError(HUB_FULL, "Trạm hiện đã hết chỗ đỗ xe trống.")

        now = datetime.now()
        freeSpot["status"] = "RESERVED"

        booking = {
            "id": f"BK-{len(db.BOOKINGS) + 1:04d}",
            "type": "PARKING",
            "userId": userId,
            "hubId": hubId,
            "spotId": freeSpot["id"],
            "timeSlot": timeSlot,
            "status": "HOLDING",
            "createdAt": now.isoformat(timespec="seconds"),
            "expiresAt": (now + timedelta(minutes=config.HOLD_TIME_MINUTES)).isoformat(timespec="seconds"),
        }
        db.BOOKINGS.append(booking)

    audit_service.record(userId, "BOOK_PARKING", booking["id"], f"hub={hubId} spot={freeSpot['id']} slot={timeSlot}")
    return booking


def cancelBooking(userId, bookingId):
    """UC3/UC4: Hủy booking, trả tài nguyên về trạng thái trống."""
    with db.DATA_LOCK:
        booking = next(
            (b for b in db.BOOKINGS if b["id"] == bookingId and b["userId"] == userId),
            None,
        )
        if not booking:
            raise ServiceError(BOOKING_NOT_FOUND, "Không tìm thấy lượt đặt.")

        if booking["status"] == "HOLDING":
            if booking.get("type") == "VEHICLE" and booking.get("vehicleId"):
                vehicle = db.getVehicle(booking["vehicleId"])
                if vehicle and vehicle["status"] == "RESERVED":
                    vehicle["status"] = "AVAILABLE"
                    vehicle["lastUpdatedAt"] = datetime.now().isoformat(timespec="seconds")
            elif booking.get("type") == "PARKING" and booking.get("spotId"):
                spot = db.findById(db.PARKING_SPOTS, booking["spotId"])
                if spot and spot["status"] == "RESERVED":
                    spot["status"] = "FREE"

        booking["status"] = "CANCELLED"

    audit_service.record(userId, "CANCEL_BOOKING", bookingId)
    return booking
