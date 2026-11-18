"""Tầng Data Access (giả lập). Thay cho database: mọi dữ liệu nằm trong bộ nhớ.

- Dữ liệu gốc đọc từ data/seed.json. Tắt server là quay về trạng thái ban đầu.
- services/ đọc và sửa trực tiếp các list bên dưới.
- Khi SỬA dữ liệu từ nhiều luồng (đặt xe, giả lập IoT) hãy dùng `with DATA_LOCK:`.
- Mô tả từng trường: docs/DATA_CONTRACT.md
"""
import copy
import json
import threading
from pathlib import Path

SEED_PATH = Path(__file__).with_name("seed.json")
DATA_LOCK = threading.RLock()

HUBS = []
VEHICLES = []
PARKING_SPOTS = []
CHARGING_PORTS = []
INCIDENTS = []
ALERTS = []
USERS = []

# Dữ liệu sinh ra khi chạy (ban đầu rỗng)
BOOKINGS = []                # UC3, UC4
CHARGING_REGISTRATIONS = []  # UC7
DISPATCH_ORDERS = []         # UC11
AUDIT_LOGS = []              # NFR11

_TABLES = {
    "hubs": HUBS, "vehicles": VEHICLES, "parkingSpots": PARKING_SPOTS,
    "chargingPorts": CHARGING_PORTS, "incidents": INCIDENTS, "alerts": ALERTS,
    "users": USERS,
}


def resetData():
    """Nạp lại dữ liệu gốc. Dùng trong test và trước khi quay video."""
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    with DATA_LOCK:
        for key, table in _TABLES.items():
            table[:] = seed.get(key, [])  # sửa tại chỗ để các module khác vẫn giữ đúng list
        for table in (BOOKINGS, CHARGING_REGISTRATIONS, DISPATCH_ORDERS, AUDIT_LOGS):
            table.clear()


def snapshot():
    """Bản sao độc lập của toàn bộ dữ liệu – dùng cho mô phỏng What-if (UC14, NFR07)."""
    with DATA_LOCK:
        return copy.deepcopy({key: table for key, table in _TABLES.items()})


def findById(table, itemId):
    return next((item for item in table if item["id"] == itemId), None)


def getHub(hubId):
    return findById(HUBS, hubId)


def getVehicle(vehicleId):
    return findById(VEHICLES, vehicleId)


def vehiclesOfHub(hubId):
    return [v for v in VEHICLES if v["hubId"] == hubId]


def spotsOfHub(hubId):
    return [s for s in PARKING_SPOTS if s["hubId"] == hubId]


def portsOfHub(hubId):
    return [p for p in CHARGING_PORTS if p["hubId"] == hubId]


resetData()
