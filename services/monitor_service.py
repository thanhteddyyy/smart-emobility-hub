"""UC8 – Giám sát mạng lưới Mobility Hub (Submission 3, mục 2.6)."""
from datetime import datetime

import config
from data import mock_data as db
from services import status_service
from services.errors import ACCESS_DENIED, SESSION_EXPIRED, ServiceError


def validateOperatorAccess(session):
    if not session or not session.get("user"):
        raise ServiceError(SESSION_EXPIRED, "Phiên đăng nhập đã hết hạn.")
    if session["user"]["role"] != "OPERATOR":
        raise ServiceError(ACCESS_DENIED, "Chỉ Đơn vị vận hành được truy cập.")


def computeHubUsage(hub):
    """Tỉ lệ sử dụng = số chỗ đang bị chiếm / tổng số chỗ, kèm mức cảnh báo an toàn."""
    overview = status_service.buildHubStatus(hub)
    total = overview["totalSpots"]
    usageRate = round((total - overview["emptySpots"]) / total, 2) if total else 0
    overview["usageRate"] = usageRate
    overview["usagePercent"] = int(round(usageRate * 100))
    if usageRate >= config.OVERLOAD_CRITICAL_RATE:
        overview["safetyWarning"] = "Overload"
    elif usageRate >= config.OVERLOAD_WARNING_RATE:
        overview["safetyWarning"] = "Danger"
    else:
        overview["safetyWarning"] = "Safe"
    return overview


def applyOverviewFilter(hubs, filter):
    """Lọc theo q, area, operationStatus, safetyWarning, minUsageRate.
    Không khớp Hub nào -> trả list rỗng (AF5)."""
    if not filter:
        return hubs
    query = (filter.get("q") or "").strip().lower()
    area = (filter.get("area") or "").strip()
    opStatus = (filter.get("operationStatus") or "").strip().upper()
    safetyWarning = (filter.get("safetyWarning") or "").strip()
    minUsageRate = filter.get("minUsageRate")

    filtered = []
    for hub in hubs:
        if query and query not in hub["name"].lower() and query not in hub["hubId"].lower():
            continue
        if area and hub["area"] != area:
            continue
        if opStatus and hub["status"] != opStatus:
            continue
        if safetyWarning and hub["safetyWarning"] != safetyWarning:
            continue
        if minUsageRate is not None and hub["usageRate"] < float(minUsageRate):
            continue
        filtered.append(hub)
    return filtered


def getNetworkOverview(filter=None):
    """Trả dữ liệu tổng quan mạng lưới và trạng thái realtime cho các trang Operator."""
    now = datetime.now().isoformat(timespec="seconds")
    hubs = applyOverviewFilter([computeHubUsage(h) for h in db.HUBS], filter or {})
    hubNameById = {h["id"]: h["name"] for h in db.HUBS}
    hubUpdatedById = {h["id"]: h["lastUpdatedAt"] for h in db.HUBS}

    vehiclesMap = {
        v["id"]: {
            "batteryLevel": v["batteryLevel"],
            "status": v["status"],
            "hubId": v["hubId"],
            "hubName": hubNameById.get(v["hubId"], v["hubId"]),
            "lastUpdatedAt": v.get("lastUpdatedAt", now),
            "isLowBattery": (v["status"] == "AVAILABLE" and v["batteryLevel"] < 20),
        }
        for v in db.VEHICLES
    }

    resourcesMap = {}
    for v in db.VEHICLES:
        resourcesMap[v["id"]] = {
            "status": v["status"],
            "lastUpdatedAt": v.get("lastUpdatedAt", now),
        }
    for p in db.CHARGING_PORTS:
        resourcesMap[p["id"]] = {
            "status": p["status"],
            "lastUpdatedAt": p.get("lastUpdatedAt", hubUpdatedById.get(p["hubId"], now)),
        }
    for s in db.PARKING_SPOTS:
        resourcesMap[s["id"]] = {
            "status": s["status"],
            "lastUpdatedAt": s.get("lastUpdatedAt", hubUpdatedById.get(s["hubId"], now)),
        }

    incidentsMap = {
        inc["id"]: {
            "status": inc["status"],
            "priority": inc["priority"],
            "operator": inc.get("operator") or "None",
        }
        for inc in db.INCIDENTS
    }

    return {
        "activeHubCount": sum(h["status"] == "ACTIVE" for h in hubs),
        "totalHubs": len(db.HUBS),
        "totalVehicles": len(db.VEHICLES),
        "availableVehicles": sum(v["status"] == "AVAILABLE" for v in db.VEHICLES),
        "inUseVehicles": sum(v["status"] == "IN_USE" for v in db.VEHICLES),
        "chargingVehicles": sum(v["status"] == "CHARGING" for v in db.VEHICLES),
        "maintenanceVehicles": sum(v["status"] == "MAINTENANCE" for v in db.VEHICLES),
        "reservedVehicles": sum(v["status"] == "RESERVED" for v in db.VEHICLES),
        "availablePorts": sum(p["status"] == "AVAILABLE" for p in db.CHARGING_PORTS),
        "totalPorts": len(db.CHARGING_PORTS),
        "emptySpots": sum(s["status"] == "FREE" for s in db.PARKING_SPOTS),
        "totalSpots": len(db.PARKING_SPOTS),
        "openIncidents": sum(i["status"] != "RESOLVED" for i in db.INCIDENTS),
        "vehicles": vehiclesMap,
        "resources": resourcesMap,
        "incidents": incidentsMap,
        "hubs": hubs,
        "updatedAt": now,
    }
