"""UC9 – Theo dõi tài nguyên, UC10 – Xem cảnh báo quá tải (Submission 3, mục 2.7, 2.8)."""
import config
from data import mock_data as db
from services import audit_service, monitor_service, status_service
from services.errors import RESOURCE_NOT_FOUND, ServiceError

_VEHICLE_STATUS_DISPLAY = {
    "AVAILABLE": "Available",
    "RESERVED": "Occupied",
    "IN_USE": "Occupied",
    "CHARGING": "Occupied",
    "MAINTENANCE": "Faulty",
}

_PORT_STATUS_DISPLAY = {
    "AVAILABLE": "Available",
    "IN_USE": "Occupied",
    "OUT_OF_ORDER": "Faulty",
}

_SPOT_STATUS_DISPLAY = {
    "FREE": "Available",
    "OCCUPIED": "Occupied",
    "RESERVED": "Occupied",
}


def getHubResources(hubId):
    """Trả thông tin tổng hợp của một Hub và danh sách tài nguyên (xe, cổng sạc, chỗ đỗ)."""
    hub = db.getHub(hubId)
    if not hub:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy Hub.")

    hubStatus = status_service.buildHubStatus(hub)
    resources = []

    for v in db.vehiclesOfHub(hubId):
        resources.append({
            "id": v["id"],
            "category": "VEHICLE",
            "typeLabel": "Vehicle",
            "name": f"{v['id']} — {v['model']} ({v['batteryLevel']}%)",
            "status": v["status"],
            "displayStatus": _VEHICLE_STATUS_DISPLAY.get(v["status"], v["status"]),
            "batteryLevel": v["batteryLevel"],
            "lastUpdatedAt": v.get("lastUpdatedAt", hub["lastUpdatedAt"]),
        })

    for p in db.portsOfHub(hubId):
        resources.append({
            "id": p["id"],
            "category": "CHARGING_PORT",
            "typeLabel": "Charging Port",
            "name": f"{p['id']} ({p['powerKw']} kW)",
            "status": p["status"],
            "displayStatus": _PORT_STATUS_DISPLAY.get(p["status"], p["status"]),
            "batteryLevel": None,
            "lastUpdatedAt": p.get("lastUpdatedAt", hub["lastUpdatedAt"]),
        })

    for s in db.spotsOfHub(hubId):
        resources.append({
            "id": s["id"],
            "category": "PARKING_SPOT",
            "typeLabel": "Parking Spot",
            "name": s["id"],
            "status": s["status"],
            "displayStatus": _SPOT_STATUS_DISPLAY.get(s["status"], s["status"]),
            "batteryLevel": None,
            "lastUpdatedAt": s.get("lastUpdatedAt", hub["lastUpdatedAt"]),
        })

    return {
        "hub": hubStatus,
        "resources": resources,
        "allHubs": list(db.HUBS),
    }


def evaluateHubLoad():
    """Kết hợp dữ liệu từ db.ALERTS và mức sử dụng thực tế của các Hub."""
    liveHubUsage = {
        h["id"]: monitor_service.computeHubUsage(h)
        for h in db.HUBS
    }
    alerts = []
    for alert in db.ALERTS:
        item = dict(alert)
        hubUsage = liveHubUsage.get(item["hubId"])
        if hubUsage:
            item["hubName"] = hubUsage["name"]
            if item.get("utilizationType") == "Parking spots":
                item["utilization"] = hubUsage["usagePercent"]
                if hubUsage["usageRate"] >= config.OVERLOAD_CRITICAL_RATE:
                    item["dangerLevel"] = "HIGH"
        alerts.append(item)

    statusOrder = {"ACTIVE": 0, "RESOLVED": 1}
    dangerOrder = {"HIGH": 0, "MEDIUM": 1}
    alerts.sort(key=lambda a: (
        statusOrder.get(a.get("status", "ACTIVE"), 9),
        dangerOrder.get(a.get("dangerLevel", "MEDIUM"), 9),
        a.get("id", ""),
    ))
    return alerts


def resolveAlert(operatorId, alertId):
    """Đánh dấu cảnh báo đã xử lý và ghi AuditLog."""
    alert = db.findById(db.ALERTS, alertId)
    if not alert:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy cảnh báo.")
    with db.DATA_LOCK:
        alert["status"] = "RESOLVED"
    audit_service.record(operatorId, "RESOLVE_ALERT", alertId, "Đã xử lý cảnh báo quá tải")
    return alert
