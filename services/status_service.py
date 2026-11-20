"""UC2 – Xem trạng thái phương tiện và Hub (Submission 3, mục 2.2)."""
from datetime import datetime

import config
from data import mock_data as db
from services.errors import RESOURCE_NOT_FOUND, ServiceError


def isStatusStale(lastUpdatedAt, now=None):
    """True nếu dữ liệu cũ hơn STALE_THRESHOLD_SECONDS."""
    now = now or datetime.now()
    age = (now - datetime.fromisoformat(lastUpdatedAt)).total_seconds()
    return age > config.STALE_THRESHOLD_SECONDS


def buildHubStatus(hub):
    """Tóm tắt trạng thái một Hub. (Đã làm – nhiều màn hình dùng chung.)"""
    vehicles = db.vehiclesOfHub(hub["id"])
    spots = db.spotsOfHub(hub["id"])
    ports = db.portsOfHub(hub["id"])
    return {
        "hubId": hub["id"], "name": hub["name"], "area": hub["area"],
        "lat": hub["lat"], "lng": hub["lng"], "status": hub["status"],
        "availableVehicles": sum(v["status"] == "AVAILABLE" for v in vehicles),
        "totalVehicles": len(vehicles),
        "emptySpots": sum(s["status"] == "FREE" for s in spots),
        "totalSpots": len(spots),
        "availablePorts": sum(p["status"] == "AVAILABLE" for p in ports),
        "totalPorts": len(ports),
        "lastUpdatedAt": hub["lastUpdatedAt"],
        "isStale": isStatusStale(hub["lastUpdatedAt"]),
    }


def buildVehicleStatus(vehicle):
    """UC2: trả dict trạng thái xe: id, model, type, batteryLevel, status, hubId,
    lastUpdatedAt, isStale."""
    return {
        "id": vehicle["id"],
        "model": vehicle["model"],
        "type": vehicle["type"],
        "batteryLevel": vehicle["batteryLevel"],
        "status": vehicle["status"],
        "hubId": vehicle["hubId"],
        "lastUpdatedAt": vehicle["lastUpdatedAt"],
        "isStale": isStatusStale(vehicle["lastUpdatedAt"]),
    }


def getResourceStatus(resourceType, resourceId):
    """UC2: resourceType là 'VEHICLE' hoặc 'HUB'.
    Không tìm thấy -> ServiceError(RESOURCE_NOT_FOUND)."""
    if resourceType == "HUB":
        hub = db.getHub(resourceId)
        if not hub:
            raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy Hub.")
        return buildHubStatus(hub)
    if resourceType == "VEHICLE":
        vehicle = db.getVehicle(resourceId)
        if not vehicle:
            raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy phương tiện.")
        return buildVehicleStatus(vehicle)
    raise ServiceError(RESOURCE_NOT_FOUND, "Loại tài nguyên không hợp lệ.")
