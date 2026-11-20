"""UC13 – Xây dựng lịch sạc thông minh (Submission 3, mục 2.11)."""
from data import mock_data as db
from services import audit_service
from services.errors import ServiceError


def generateSchedule(hubId):
    """TODO(UC13): Xếp xe pin thấp / có lịch sử dụng gần lên trước, chia vào các cổng AVAILABLE theo khung giờ."""
    with db.DATA_LOCK:
        hub = db.getHub(hubId)
        if not hub:
            raise ServiceError("HUB_NOT_FOUND")
        ports = [p for p in db.CHARGING_PORTS if p["hubId"] == hubId and p["status"] == "AVAILABLE"]

        if not ports:
            return []
        vehicles = [v for v in db.VEHICLES if v["hubId"] == hubId and v["status"] in ["AVAILABLE", "CHARGING"]]
        vehicles.sort(key=lambda v: v["batteryLevel"])
        schedule = []
        for i, vehicle in enumerate(vehicles):
            port = ports[i % len(ports)]
            schedule.append({
                "id": f"REG-{len(db.CHARGING_REGISTRATIONS) + i + 1:04d}",
                "userId": None,
                "hubId": hubId,
                "portId": port["id"],
                "vehicleId": vehicle["id"],
                "timeSlot": f"SLOT-{i // len(ports) + 1}",
                "batteryLevel": vehicle["batteryLevel"],
                "status": "PENDING"
            })
        if not validateSchedule(schedule):
            raise ServiceError("INVALID_SCHEDULE")
        return schedule


def validateSchedule(schedule):
    """TODO(UC13): Không trùng cổng trong cùng khung giờ, không dùng cổng OUT_OF_ORDER."""
    with db.DATA_LOCK:
        usedPorts = set()
        for item in schedule:
            port = db.findById(db.CHARGING_PORTS, item["portId"])
            if not port:
                return False
            if port["status"] == "OUT_OF_ORDER":
                return False
            if port["status"] != "AVAILABLE":
                return False
            if item["hubId"] != port["hubId"]:
                return False
            key = (item["portId"], item["timeSlot"])
            if key in usedPorts:
                return False
            usedPorts.add(key)
        return True


def editSchedule(schedule, changes):
    """TODO(UC13): Áp dụng chỉnh sửa của Operator rồi validateSchedule lại."""
    with db.DATA_LOCK:
        updatedSchedule = [item.copy() for item in schedule]
        for change in changes:
            registrationId = change.get("id")
            registration = next((item for item in updatedSchedule if item["id"] == registrationId), None)
            if not registration:
                raise ServiceError("RESOURCE_NOT_FOUND")
            for field in ["portId", "timeSlot"]:
                if field in change:
                    registration[field] = change[field]
        if not validateSchedule(updatedSchedule):
            raise ServiceError("INVALID_SCHEDULE")
        return updatedSchedule


def approveSchedule(operatorId, schedule):
    """TODO(UC13): Phê duyệt và gọi saveSchedule."""
    with db.DATA_LOCK:
        if not validateSchedule(schedule):
            raise ServiceError("INVALID_SCHEDULE")
        approvedSchedule = [item.copy() for item in schedule]
        for item in approvedSchedule:
            item["status"] = "APPROVED"
        savedSchedule = saveSchedule(approvedSchedule)
        audit_service.record(
            operatorId,
            "APPROVE_CHARGING_SCHEDULE",
            savedSchedule[0]["hubId"] if savedSchedule else "",
            f"Operator {operatorId} approved charging schedule"
        )
        return savedSchedule



def saveSchedule(schedule):
    """TODO(UC13): Lưu lịch đã duyệt."""
    with db.DATA_LOCK:
        if not validateSchedule(schedule):
            raise ServiceError("INVALID_SCHEDULE")
        for item in schedule:
            if item["status"] != "APPROVED":
                raise ServiceError("INVALID_SCHEDULE")
        for item in schedule:
            db.CHARGING_REGISTRATIONS.append(item.copy())
        return schedule
