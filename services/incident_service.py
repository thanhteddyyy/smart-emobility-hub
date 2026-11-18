"""UC12 – Xử lý các sự cố (Submission 3, mục 2.10)."""
from data import mock_data as db
from services import audit_service
from services.errors import INCIDENT_NOT_FOUND, ServiceError

_STATUS_ORDER = {"OPEN": 0, "IN_PROGRESS": 1, "RESOLVED": 2}
_PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
_STATUS_DISPLAY = {"OPEN": "Unchecked", "IN_PROGRESS": "In Progress", "RESOLVED": "Done"}


def _resolveResourceStatus(incident):
    resourceType = incident.get("resourceType")
    resourceId = incident.get("resourceId")
    if resourceType == "VEHICLE":
        res = db.getVehicle(resourceId)
        return res["status"] if res else "UNKNOWN"
    if resourceType == "CHARGING_PORT":
        res = db.findById(db.CHARGING_PORTS, resourceId)
        return res["status"] if res else "UNKNOWN"
    if resourceType == "HUB":
        res = db.getHub(resourceId)
        return res["status"] if res else "UNKNOWN"
    return "UNKNOWN"


def _enrichIncident(incident):
    hub = db.getHub(incident.get("hubId"))
    item = dict(incident)
    item["hubName"] = hub["name"] if hub else incident.get("hubId", "")
    item["location"] = f"{hub['area']} ({incident.get('resourceId')})" if hub else incident.get("resourceId", "")
    item["resourceStatus"] = _resolveResourceStatus(incident)
    item["displayStatus"] = _STATUS_DISPLAY.get(incident.get("status"), incident.get("status"))
    item.setdefault("reason", "")
    item.setdefault("fixingMethod", "")
    item.setdefault("updateDetails", "")
    return item


def getPrioritizedIncidents():
    """Sắp xếp sự cố chưa xử lý lên trước và theo độ ưu tiên HIGH -> MEDIUM -> LOW."""
    enriched = [_enrichIncident(inc) for inc in db.INCIDENTS]
    enriched.sort(key=lambda inc: (
        _STATUS_ORDER.get(inc.get("status"), 9),
        _PRIORITY_ORDER.get(inc.get("priority"), 9),
        inc.get("id", ""),
    ))
    return enriched


def getIncidentById(incidentId):
    """Lấy chi tiết một sự cố kèm trạng thái tài nguyên liên quan."""
    inc = db.findById(db.INCIDENTS, incidentId)
    if not inc:
        raise ServiceError(INCIDENT_NOT_FOUND, "Không tìm thấy sự cố.")
    return _enrichIncident(inc)


def handlePauseResource(operatorId, incidentId, reason, fixingMethod):
    """Tạm ngưng tài nguyên liên quan, chuyển sự cố -> IN_PROGRESS, hủy đặt chỗ chờ."""
    inc = db.findById(db.INCIDENTS, incidentId)
    if not inc:
        raise ServiceError(INCIDENT_NOT_FOUND, "Không tìm thấy sự cố.")

    with db.DATA_LOCK:
        inc["status"] = "IN_PROGRESS"
        inc["operator"] = operatorId
        inc["reason"] = reason
        inc["fixingMethod"] = fixingMethod

        resType = inc.get("resourceType")
        resId = inc.get("resourceId")
        if resType == "VEHICLE":
            vehicle = db.getVehicle(resId)
            if vehicle:
                vehicle["status"] = "MAINTENANCE"
        elif resType == "CHARGING_PORT":
            port = db.findById(db.CHARGING_PORTS, resId)
            if port:
                port["status"] = "OUT_OF_ORDER"
        elif resType == "HUB":
            hub = db.getHub(resId)
            if hub:
                hub["status"] = "OFFLINE"

        for booking in db.BOOKINGS:
            if booking.get("status") == "HOLDING" and (
                booking.get("vehicleId") == resId or booking.get("hubId") == resId
            ):
                booking["status"] = "CANCELLED"

    audit_service.record(operatorId, "PAUSE_RESOURCE", incidentId, f"Tạm ngưng {resType}:{resId}")
    return _enrichIncident(inc)


def completeIncident(operatorId, incidentId, resourceStatus="AVAILABLE", updateDetails=""):
    """Cập nhật tiến độ xử lý sự cố và khôi phục/cập nhật trạng thái tài nguyên."""
    inc = db.findById(db.INCIDENTS, incidentId)
    if not inc:
        raise ServiceError(INCIDENT_NOT_FOUND, "Không tìm thấy sự cố.")

    normalizedStatus = (resourceStatus or "AVAILABLE").upper()
    with db.DATA_LOCK:
        inc["operator"] = operatorId
        inc["updateDetails"] = updateDetails

        resType = inc.get("resourceType")
        resId = inc.get("resourceId")
        if normalizedStatus == "AVAILABLE":
            if resType == "VEHICLE":
                vehicle = db.getVehicle(resId)
                if vehicle:
                    vehicle["status"] = "AVAILABLE"
            elif resType == "CHARGING_PORT":
                port = db.findById(db.CHARGING_PORTS, resId)
                if port:
                    port["status"] = "AVAILABLE"
            elif resType == "HUB":
                hub = db.getHub(resId)
                if hub:
                    hub["status"] = "ACTIVE"
            inc["status"] = "RESOLVED"
        else:
            if resType == "VEHICLE":
                vehicle = db.getVehicle(resId)
                if vehicle:
                    vehicle["status"] = "MAINTENANCE"
            elif resType == "CHARGING_PORT":
                port = db.findById(db.CHARGING_PORTS, resId)
                if port:
                    port["status"] = "OUT_OF_ORDER"
            elif resType == "HUB":
                hub = db.getHub(resId)
                if hub:
                    hub["status"] = "OFFLINE"
            inc["status"] = "IN_PROGRESS"

    audit_service.record(
        operatorId,
        "UPDATE_INCIDENT",
        incidentId,
        f"Trạng thái tài nguyên -> {normalizedStatus}",
    )
    return _enrichIncident(inc)


def isolateDisconnectedHub(hubId):
    """Hub mất kết nối: status -> OFFLINE, không nhận đặt chỗ mới (NFR05)."""
    hub = db.getHub(hubId)
    if not hub:
        raise ServiceError(INCIDENT_NOT_FOUND, "Không tìm thấy Hub.")
    with db.DATA_LOCK:
        hub["status"] = "OFFLINE"
    audit_service.record("SYSTEM", "ISOLATE_HUB", hubId, "Cô lập Hub mất kết nối")
    return hub
