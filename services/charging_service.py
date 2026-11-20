"""UC7 – Đăng ký sạc (Submission 3, mục 2.5)."""
import math

from data import mock_data as db
from services.errors import INVALID_PARAMETERS, NO_PORT_AVAILABLE, RESOURCE_NOT_FOUND, ServiceError


def _distanceKm(a, b):
    lat1, lng1, lat2, lng2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def registerCharging(userId, hubId, portId, timeSlot, batteryLevel):
    """Đăng ký cổng sạc tại Hub theo khung giờ. Trùng cổng/khung giờ hoặc cổng lỗi -> NO_PORT_AVAILABLE."""
    if not userId or not hubId or not portId or not timeSlot:
        raise ServiceError(INVALID_PARAMETERS, "Thiếu thông tin đăng ký sạc.")
    if not isinstance(batteryLevel, (int, float)) or isinstance(batteryLevel, bool) or not (0 <= batteryLevel <= 100):
        raise ServiceError(INVALID_PARAMETERS, "Mức pin phải nằm trong khoảng 0 đến 100.")

    hub = db.getHub(hubId)
    if not hub:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy Hub.")

    with db.DATA_LOCK:
        port = next((p for p in db.portsOfHub(hubId) if p["id"] == portId), None)
        if not port or port["status"] != "AVAILABLE":
            raise ServiceError(NO_PORT_AVAILABLE, "Cổng sạc không khả dụng.")

        duplicate = any(
            reg.get("portId") == portId
            and reg.get("timeSlot") == timeSlot
            and reg.get("status") != "CANCELLED"
            for reg in db.CHARGING_REGISTRATIONS
        )
        if duplicate:
            raise ServiceError(NO_PORT_AVAILABLE, "Cổng sạc đã có người đăng ký trong khung giờ này.")

        registration = {
            "id": f"CHG-{len(db.CHARGING_REGISTRATIONS) + 1:03d}",
            "userId": userId,
            "hubId": hubId,
            "portId": portId,
            "timeSlot": timeSlot,
            "batteryLevel": int(batteryLevel),
            "status": "ACTIVE",
        }
        db.CHARGING_REGISTRATIONS.append(registration)

    return registration


def suggestNearestHubWithPort(hubId):
    """Trả Hub gần hubId nhất còn cổng sạc AVAILABLE, hoặc None."""
    originHub = db.getHub(hubId)
    if not originHub:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy Hub.")

    candidates = [
        h for h in db.HUBS
        if h["id"] != hubId
        and h.get("status") == "ACTIVE"
        and any(p["status"] == "AVAILABLE" for p in db.portsOfHub(h["id"]))
    ]
    if not candidates:
        return None

    candidates.sort(key=lambda h: _distanceKm(originHub, h))
    return candidates[0]
