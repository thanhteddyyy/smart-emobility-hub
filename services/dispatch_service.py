"""UC11 – Điều phối phương tiện (Submission 3, mục 2.9)."""
from datetime import datetime

import config
from data import mock_data as db
from services import audit_service, status_service
from services.errors import DISPATCH_CONFLICT, HUB_FULL, INVALID_PARAMETERS, RESOURCE_NOT_FOUND, ServiceError


def getDispatchHubData(sourceHubId=None, destHubId=None):
    """Trả thống kê xe, bản đồ Hub (Leaflet) và danh sách xe kèm cờ Low Battery tính toán động."""
    hubStatuses = [status_service.buildHubStatus(h) for h in db.HUBS]
    hubNameById = {h["hubId"]: h["name"] for h in hubStatuses}

    selectedSourceHubId = sourceHubId or ""
    selectedDestHubId = destHubId or (hubStatuses[0]["hubId"] if hubStatuses else "")

    vehicles = []
    for v in db.VEHICLES:
        if selectedSourceHubId and v["hubId"] != selectedSourceHubId:
            continue
        item = dict(v)
        item["hubName"] = hubNameById.get(v["hubId"], v["hubId"])
        # Low Battery là cảnh báo tính toán, KHÔNG ghi đè trạng thái gốc v['status']
        item["isLowBattery"] = (v["status"] == "AVAILABLE" and v["batteryLevel"] < 20)
        vehicles.append(item)

    stats = {
        "totalVehicles": len(db.VEHICLES),
        "available": sum(v["status"] == "AVAILABLE" for v in db.VEHICLES),
        "inUse": sum(v["status"] == "IN_USE" for v in db.VEHICLES),
        "charging": sum(v["status"] == "CHARGING" for v in db.VEHICLES),
        "maintenance": sum(v["status"] == "MAINTENANCE" for v in db.VEHICLES),
    }

    mapView = {
        "center": config.DEFAULT_LOCATION,
        "markers": [
            {
                "hubId": h["hubId"],
                "name": h["name"],
                "lat": h["lat"],
                "lng": h["lng"],
                "availableVehicles": h["availableVehicles"],
                "emptySpots": h["emptySpots"],
                "availablePorts": h["availablePorts"],
                "status": h["status"],
            }
            for h in hubStatuses
        ],
    }

    availableSourceVehicles = [v for v in vehicles if v["status"] == "AVAILABLE"]
    destFreeSpots = (
        [s for s in db.spotsOfHub(selectedDestHubId) if s["status"] == "FREE"]
        if selectedDestHubId
        else [s for s in db.PARKING_SPOTS if s["status"] == "FREE"]
    )

    return {
        "stats": stats,
        "hubs": hubStatuses,
        "selectedSourceHubId": selectedSourceHubId,
        "selectedDestHubId": selectedDestHubId,
        "vehicles": vehicles,
        "Available vehicles": availableSourceVehicles,
        "Available parking spots": destFreeSpots,
        "mapView": mapView,
        "orders": list(reversed(db.DISPATCH_ORDERS)),
    }


def processDispatch(operatorId, sourceHubId, destHubId, vehicleIds):
    """Điều phối các xe AVAILABLE sang Hub đích; kiểm tra xung đột xe và chỗ trống."""
    destHub = db.getHub(destHubId)
    if not destHub:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy Hub đích.")
    if not vehicleIds:
        raise ServiceError(INVALID_PARAMETERS, "Vui lòng chọn ít nhất một phương tiện để điều phối.")

    now = datetime.now().isoformat(timespec="seconds")
    with db.DATA_LOCK:
        selectedVehicles = []
        for vid in vehicleIds:
            vehicle = db.getVehicle(vid)
            if not vehicle:
                raise ServiceError(RESOURCE_NOT_FOUND, f"Không tìm thấy xe {vid}.")
            if vehicle["status"] != "AVAILABLE":
                raise ServiceError(DISPATCH_CONFLICT, f"Xe {vid} đang ở trạng thái {vehicle['status']}, không thể điều phối.")
            if vehicle["hubId"] == destHubId:
                raise ServiceError(DISPATCH_CONFLICT, f"Xe {vid} đã đang ở Hub đích.")
            selectedVehicles.append(vehicle)

        destFreeSpots = [s for s in db.spotsOfHub(destHubId) if s["status"] == "FREE"]
        if len(destFreeSpots) < len(selectedVehicles):
            raise ServiceError(HUB_FULL, "Hub đích không đủ chỗ đỗ trống cho số xe đã chọn.")

        for idx, vehicle in enumerate(selectedVehicles):
            oldHubId = vehicle["hubId"]
            occupiedSource = next(
                (s for s in db.spotsOfHub(oldHubId) if s["status"] == "OCCUPIED"),
                None,
            )
            if occupiedSource:
                occupiedSource["status"] = "FREE"
            destFreeSpots[idx]["status"] = "OCCUPIED"
            vehicle["hubId"] = destHubId
            vehicle["lastUpdatedAt"] = now

        order = {
            "id": f"DSP-{len(db.DISPATCH_ORDERS) + 1:03d}",
            "operatorId": operatorId,
            "sourceHubId": sourceHubId or selectedVehicles[0]["hubId"],
            "destHubId": destHubId,
            "vehicleIds": list(vehicleIds),
            "status": "PENDING",
            "createdAt": now,
        }
        db.DISPATCH_ORDERS.append(order)

    audit_service.record(
        operatorId,
        "CREATE_DISPATCH_ORDER",
        destHubId,
        f"Điều phối {', '.join(vehicleIds)} -> {destHubId}",
    )
    return order


def cancelDispatchOrder(operatorId, orderId):
    """Chỉ hủy được lệnh điều phối đang ở trạng thái PENDING."""
    order = db.findById(db.DISPATCH_ORDERS, orderId)
    if not order:
        raise ServiceError(RESOURCE_NOT_FOUND, "Không tìm thấy lệnh điều phối.")
    if order["status"] != "PENDING":
        raise ServiceError(DISPATCH_CONFLICT, "Chỉ có thể hủy lệnh đang PENDING.")

    with db.DATA_LOCK:
        order["status"] = "CANCELLED"
    audit_service.record(operatorId, "CANCEL_DISPATCH_ORDER", orderId, "Hủy lệnh điều phối")
    return order
