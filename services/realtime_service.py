"""UC16 – Cập nhật trạng thái tài nguyên (Submission 3, mục 2.14).

Đã có: bộ giả lập IoT đơn giản (đổi pin, chỗ đỗ mỗi vài giây) để giao diện thấy số liệu thay đổi.
Còn TODO: xử lý gói tin đúng đặc tả + DEMO BẮT BUỘC "lọc gói dữ liệu trễ".
"""
import random
import threading
import time
from datetime import datetime

import config
from data import mock_data as db
from services.errors import ServiceError, INVALID_PARAMETERS
from copy import deepcopy

PACKET_LOG = [
    {
        "packet": {
            "resourceType": "VEHICLE",
            "resourceId": "EB-201",
            "timestamp": "2026-11-17T07:55:00",
            "status": "AVAILABLE",
        },
        "reason": "OUTDATED_PACKET",
        "receivedAt": "2026-11-20T20:16:00",
        "demo": True,
    }
]          # log các gói bị loại, hiển thị trên dashboard khi demo
_simulatorStarted = False

RESOURCE_COLLECTIONS = {
    "HUB": db.HUBS,
    "VEHICLE": db.VEHICLES,
    "CHARGING_PORT": db.CHARGING_PORTS
}

VALID_STATUSES = {
    "HUB": ["ACTIVE", "OFFLINE"],
    "VEHICLE": [
        "AVAILABLE", "RESERVED", "IN_USE",
        "CHARGING", "MAINTENANCE"
    ],
    "CHARGING_PORT": ["AVAILABLE", "IN_USE", "OUT_OF_ORDER"]
}

def isOutdatedPacket(packetTimestamp, currentTimestamp):
    """True nếu gói tin cũ hơn (hoặc bằng) trạng thái đang lưu."""
    return datetime.fromisoformat(packetTimestamp) <= datetime.fromisoformat(currentTimestamp)


def validatePacket(packet):
    """UC16: Validate incoming telemetry packet."""

    if not isinstance(packet, dict):
        raise ServiceError(INVALID_PARAMETERS)

    requiredFields = ["resourceType", "resourceId", "timestamp", "status"]

    for field in requiredFields:
        if field not in packet or packet[field] is None:
            raise ServiceError(INVALID_PARAMETERS)

    resourceType = packet["resourceType"]

    if resourceType not in RESOURCE_COLLECTIONS:
        raise ServiceError(INVALID_PARAMETERS)

    if not isinstance(packet["resourceId"], str) or not packet["resourceId"].strip():
        raise ServiceError(INVALID_PARAMETERS)

    if not isinstance(packet["status"], str):
        raise ServiceError(INVALID_PARAMETERS)

    if packet["status"] not in VALID_STATUSES[resourceType]:
        raise ServiceError(INVALID_PARAMETERS)

    # Timestamp must be a valid ISO 8601 datetime.
    if not isinstance(packet["timestamp"], str):
        raise ServiceError(INVALID_PARAMETERS)

    try:
        datetime.fromisoformat(packet["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        raise ServiceError(INVALID_PARAMETERS)

    # Optional vehicle battery level must be between 0 and 100.
    if "batteryLevel" in packet:
        batteryLevel = packet["batteryLevel"]

        if (
            resourceType != "VEHICLE"
            or isinstance(batteryLevel, bool)
            or not isinstance(batteryLevel, (int, float))
            or not 0 <= batteryLevel <= 100
        ):
            raise ServiceError(INVALID_PARAMETERS)

    return True


def upsertSimulatedState(packet):
    """UC16: Update simulated resource state."""

    with db.DATA_LOCK:
        collection = RESOURCE_COLLECTIONS[packet["resourceType"]]

        resource = db.findById(collection, packet["resourceId"])

        if not resource:
            raise ServiceError("RESOURCE_NOT_FOUND")

        resource["status"] = packet["status"]
        resource["lastUpdatedAt"] = packet["timestamp"]

        if packet["resourceType"] == "VEHICLE":
            if "batteryLevel" in packet:
                resource["batteryLevel"] = packet["batteryLevel"]

        return resource


def ingestResourceStatus(packet):
    """UC16: Validate, filter outdated packets, and update resource state."""

    validatePacket(packet)

    with db.DATA_LOCK:
        collection = RESOURCE_COLLECTIONS[packet["resourceType"]]

        resource = db.findById(collection, packet["resourceId"])

        if not resource:
            raise ServiceError("RESOURCE_NOT_FOUND")

        currentTimestamp = resource["lastUpdatedAt"]

        if isOutdatedPacket(packet["timestamp"], currentTimestamp):
            PACKET_LOG.append({
                "packet": deepcopy(packet),
                "reason": "OUTDATED_PACKET",
                "receivedAt": datetime.now().isoformat(timespec="seconds")
            })

            return {
                "updated": False,
                "reason": "OUTDATED_PACKET",
                "resourceId": packet["resourceId"]
            }

        updatedResource = upsertSimulatedState(packet)

        return {
            "updated": True,
            "resource": updatedResource
        }


def receiveTelemetryPacket(packet):
    """UC16: Entry point for /api/telemetry."""

    return ingestResourceStatus(packet)


# ---------- Bộ giả lập IoT (đã chạy được) ----------
def simulateTick():
    """Một nhịp giả lập: đổi pin vài xe, đổi trạng thái một chỗ đỗ, cập nhật mốc thời gian Hub."""
    now = datetime.now().isoformat(timespec="seconds")
    with db.DATA_LOCK:
        for vehicle in random.sample(db.VEHICLES, k=min(5, len(db.VEHICLES))):
            if vehicle["status"] == "CHARGING":
                vehicle["batteryLevel"] = min(100, vehicle["batteryLevel"] + 2)
            elif vehicle["status"] == "IN_USE":
                vehicle["batteryLevel"] = max(0, vehicle["batteryLevel"] - 1)
            vehicle["lastUpdatedAt"] = now
        spot = random.choice(db.PARKING_SPOTS)
        if spot["status"] in ("FREE", "OCCUPIED") and random.random() < 0.5:
            spot["status"] = "OCCUPIED" if spot["status"] == "FREE" else "FREE"
        for hub in db.HUBS:
            if hub["status"] == "ACTIVE":
                hub["lastUpdatedAt"] = now


def startSimulator():
    global _simulatorStarted
    if _simulatorStarted:
        return
    _simulatorStarted = True

    def loop():
        while True:
            simulateTick()
            time.sleep(config.SIMULATOR_INTERVAL_SECONDS)

    threading.Thread(target=loop, daemon=True, name="iot-simulator").start()
