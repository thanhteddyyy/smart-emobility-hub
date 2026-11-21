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
    hubStatus["id"] = hub["id"]
    vehicles = db.vehiclesOfHub(hubId)
    chargingPorts = db.portsOfHub(hubId)
    resources = []

    for v in vehicles:
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

    for p in chargingPorts:
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
        "vehicles": vehicles,
        "chargingPorts": chargingPorts,
        "resources": resources,
        "allHubs": list(db.HUBS),
    }


def evaluateHubLoad(includeSeeded=False):
    """Đánh giá tải của từng Hub theo ngưỡng WARNING/CRITICAL.
    includeSeeded=True kết hợp thêm dữ liệu cảnh báo mẫu từ db.ALERTS cho màn hình Dashboard."""
    if includeSeeded:
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
                elif item.get("utilizationType") == "Charging ports":
                    ports = db.portsOfHub(item["hubId"])
                    occupied = sum(p["status"] in ("IN_USE", "OUT_OF_ORDER") for p in ports)
                    item["utilization"] = int(round(occupied * 100 / len(ports))) if ports else 0
            utilization = item.get("utilization", 0)
            if utilization >= int(round(config.OVERLOAD_CRITICAL_RATE * 100)):
                item["dangerLevel"] = "HIGH"
                item["severity"] = "CRITICAL"
            elif utilization >= int(round(config.OVERLOAD_WARNING_RATE * 100)):
                item["dangerLevel"] = "MEDIUM"
                item["severity"] = "WARNING"
            else:
                item["dangerLevel"] = "LOW"
                item["severity"] = "SAFE"
            alerts.append(item)

        statusOrder = {"ACTIVE": 0, "RESOLVED": 1}
        dangerOrder = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        alerts.sort(key=lambda a: (
            statusOrder.get(a.get("status", "ACTIVE"), 9),
            dangerOrder.get(a.get("dangerLevel", "MEDIUM"), 9),
            a.get("id", ""),
        ))
        return alerts

    dynamicAlerts = []
    for hub in db.HUBS:
        capacity = hub.get("parkingCapacity") or 0
        if capacity <= 0:
            continue
        activeVehiclesAtHub = [
            v for v in db.VEHICLES
            if v["hubId"] == hub["id"] and v["status"] in ("AVAILABLE", "CHARGING")
        ]
        loadRate = len(activeVehiclesAtHub) / capacity
        if loadRate >= config.OVERLOAD_CRITICAL_RATE:
            severity = "CRITICAL"
            dangerLevel = "HIGH"
        elif loadRate >= config.OVERLOAD_WARNING_RATE:
            severity = "WARNING"
            dangerLevel = "MEDIUM"
        else:
            continue

        dynamicAlerts.append({
            "id": f"LOAD-{hub['id']}",
            "hubId": hub["id"],
            "hubName": hub["name"],
            "utilizationType": "Parking spots",
            "utilization": int(round(loadRate * 100)),
            "threshold": int(round(config.OVERLOAD_WARNING_RATE * 100)),
            "severity": severity,
            "dangerLevel": dangerLevel,
            "location": hub.get("area", ""),
            "expectedCause": "High vehicle density",
            "status": "ACTIVE",
            "createdAt": hub.get("lastUpdatedAt", ""),
        })

    return dynamicAlerts


def resolveAlert(operatorId, alertId):
    """Đánh dấu cảnh báo đã xử lý và ghi AuditLog."""
    alert = db.findById(db.ALERTS, alertId)
    if not alert:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy cảnh báo.")
    with db.DATA_LOCK:
        alert["status"] = "RESOLVED"
    audit_service.record(operatorId, "RESOLVE_ALERT", alertId, "Đã xử lý cảnh báo quá tải")
    return alert
