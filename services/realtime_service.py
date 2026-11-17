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

PACKET_LOG = []          # log các gói bị loại, hiển thị trên dashboard khi demo
_simulatorStarted = False


def isOutdatedPacket(packetTimestamp, currentTimestamp):
    """True nếu gói tin cũ hơn (hoặc bằng) trạng thái đang lưu."""
    return datetime.fromisoformat(packetTimestamp) <= datetime.fromisoformat(currentTimestamp)


def validatePacket(packet):
    """TODO(UC16): kiểm tra packet có đủ resourceType, resourceId, timestamp và giá trị hợp lệ."""
    raise NotImplementedError("UC16 validatePacket")


def upsertSimulatedState(packet):
    """TODO(UC16): ghi trạng thái mới vào mock_data (nhớ dùng `with db.DATA_LOCK:`)."""
    raise NotImplementedError("UC16 upsertSimulatedState")


def ingestResourceStatus(packet):
    """TODO(UC16) – DEMO BẮT BUỘC lọc gói trễ:
    1. validatePacket(packet)
    2. Nếu isOutdatedPacket(packet['timestamp'], <lastUpdatedAt hiện tại>) -> thêm vào PACKET_LOG, bỏ qua
    3. Ngược lại upsertSimulatedState(packet)
    """
    raise NotImplementedError("UC16 ingestResourceStatus")


def receiveTelemetryPacket(packet):
    """TODO(UC16): điểm nhận gói tin từ /api/telemetry -> gọi ingestResourceStatus."""
    raise NotImplementedError("UC16 receiveTelemetryPacket")


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
