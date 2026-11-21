import json
import random
from pathlib import Path

specs = {
    "H1": ("Ga Metro ĐHQG", "Metro", 10.8664, 106.8010, 180, 200, 50),
    "H2": ("KTX Khu A", "Ký túc xá", 10.8783, 106.8063, 150, 180, 45),
    "H3": ("KTX Khu B", "Ký túc xá", 10.8826, 106.7825, 120, 160, 40),
    "H4": ("ĐH Bách khoa CS2", "Trường đại học", 10.8806, 106.8054, 110, 140, 40),
    "H5": ("Nhà văn hóa Sinh viên", "Dịch vụ", 10.8752, 106.8007, 140, 150, 45),
}

hubs = []
vehicles = []
spots = []
ports = []
vehicle_number = 241
legacy_numbers = {
    "H1": range(201, 211),
    "H2": range(211, 220),
    "H3": range(220, 224),
    "H4": range(224, 228),
    "H5": range(228, 241),
}

for hub_id, (name, area, lat, lng, vehicle_count, parking_count, port_count) in specs.items():
    hubs.append({
        "id": hub_id,
        "name": name,
        "area": area,
        "lat": lat,
        "lng": lng,
        "parkingCapacity": parking_count,
        "status": "ACTIVE",
        "lastUpdatedAt": "2026-11-17T08:00:00",
    })
    statuses = ["AVAILABLE", "AVAILABLE", "AVAILABLE", "CHARGING", "IN_USE", "RESERVED", "MAINTENANCE"]
    for legacy_number in legacy_numbers[hub_id]:
        index = legacy_number - legacy_numbers[hub_id].start
        vehicle_type = "E_SCOOTER" if index % 3 else "E_BIKE"
        model = "Xiaomi Scooter 4" if vehicle_type == "E_SCOOTER" else "VinFast Feliz S"
        status = "AVAILABLE"
        if legacy_number in (203, 213, 216, 219):
            status = "CHARGING"
        elif legacy_number in (209, 221):
            status = "MAINTENANCE"
        elif legacy_number == 212:
            status = "RESERVED"
        battery = 62 if legacy_number == 201 else 38 if legacy_number == 202 else 15 if legacy_number == 203 else 28 if legacy_number == 212 else 40
        vehicles.append({
            "id": f"EB-{legacy_number}",
            "type": vehicle_type,
            "model": model,
            "batteryLevel": battery,
            "status": status,
            "hubId": hub_id,
            "lastUpdatedAt": "2026-11-17T08:00:00",
        })
    for index in range(vehicle_count - len(legacy_numbers[hub_id])):
        vehicle_type = "E_SCOOTER" if index % 3 else "E_BIKE"
        model = "Xiaomi Scooter 4" if vehicle_type == "E_SCOOTER" else "VinFast Feliz S"
        battery = random.Random(vehicle_number).randint(12, 100)
        status = statuses[index % len(statuses)]
        vehicles.append({
            "id": f"EB-{vehicle_number}",
            "type": vehicle_type,
            "model": model,
            "batteryLevel": battery,
            "status": status,
            "hubId": hub_id,
            "lastUpdatedAt": "2026-11-17T08:00:00",
        })
        vehicle_number += 1
    for index in range(1, parking_count + 1):
        status = "FREE" if index % 5 in (1, 2) else ("RESERVED" if index % 17 == 0 else "OCCUPIED")
        spots.append({
            "id": f"{hub_id}-P{index:02d}",
            "hubId": hub_id,
            "status": status,
            "lastUpdatedAt": "2026-11-17T08:00:00",
        })
    for index in range(1, port_count + 1):
        status = "AVAILABLE" if index % 4 in (1, 2) else ("OUT_OF_ORDER" if index % 11 == 0 else "IN_USE")
        ports.append({
            "id": f"{hub_id}-C{index:02d}",
            "hubId": hub_id,
            "powerKw": 7.4 if index % 3 == 0 else 3.3,
            "status": status,
            "lastUpdatedAt": "2026-11-17T08:00:00",
        })

incidents = [
    ("INC-001", "H1", "CHARGING_PORT", "H1-C02", "Cổng sạc mất kết nối", "Mất kết nối IoT", "HIGH", "OPEN", None),
    ("INC-002", "H1", "HUB", "H1", "Hub sắp quá tải", "Quá tải trạm", "HIGH", "IN_PROGRESS", "Matthew"),
    ("INC-003", "H3", "VEHICLE", "EB-221", "GPS lệch vị trí", "GPS lệch vị trí", "LOW", "RESOLVED", "Liam"),
    ("INC-004", "H4", "CHARGING_PORT", "H4-C01", "Cổng sạc lỗi chập chờn", "Hỏng cổng sạc", "MEDIUM", "OPEN", None),
    ("INC-005", "H2", "VEHICLE", "EB-213", "Mất tín hiệu GPS", "Lỗi pin", "LOW", "RESOLVED", "Liam"),
    ("INC-006", "H5", "HUB", "H5", "Hub mất kết nối chập chờn", "Mất kết nối IoT", "MEDIUM", "IN_PROGRESS", "Jack"),
]

seed = {
    "hubs": hubs,
    "vehicles": vehicles,
    "parkingSpots": spots,
    "chargingPorts": ports,
    "incidents": [
        {
            "id": incident_id,
            "hubId": hub_id,
            "resourceType": resource_type,
            "resourceId": resource_id,
            "description": description,
            "reason": reason,
            "fixingMethod": "Kiểm tra tài nguyên, thay thế linh kiện hoặc reconnect thiết bị.",
            "priority": priority,
            "status": status,
            "operator": operator,
            "createdAt": "2026-11-17T08:00:00",
        }
        for incident_id, hub_id, resource_type, resource_id, description, reason, priority, status, operator in incidents
    ],
    "users": [
        {"id": "2413148", "name": "Sinh viên Demo", "email": "student@hcmut.edu.vn", "password": "123456", "role": "STUDENT"},
        {"id": "OP001", "name": "Matthew", "email": "operator@ehub.vn", "password": "123456", "role": "OPERATOR"},
        {"id": "G001", "name": "Khách", "email": "guest@gmail.com", "password": "123456", "role": "GUEST"},
    ],
    "alerts": [
        {"id": "ALT-001", "hubId": "H1", "hubName": "Ga Metro ĐHQG", "utilizationType": "Parking spots", "utilization": 95, "threshold": 75, "dangerLevel": "HIGH", "location": "Ga Metro ĐHQG - Cửa Đông", "expectedCause": "Rush hour", "status": "ACTIVE", "createdAt": "2026-11-17T09:46:00"},
        {"id": "ALT-002", "hubId": "H2", "hubName": "KTX Khu A", "utilizationType": "Charging ports", "utilization": 90, "threshold": 80, "dangerLevel": "MEDIUM", "location": "KTX Khu A - Cổng chính", "expectedCause": "Peak charging demand", "status": "ACTIVE", "createdAt": "2026-11-17T09:36:00"},
        {"id": "ALT-003", "hubId": "H4", "hubName": "ĐH Bách khoa CS2", "utilizationType": "Parking spots", "utilization": 93, "threshold": 75, "dangerLevel": "HIGH", "location": "ĐH Bách khoa CS2 - Nhà xe A", "expectedCause": "Class dismissal peak", "status": "ACTIVE", "createdAt": "2026-11-17T09:26:00"},
        {"id": "ALT-004", "hubId": "H3", "hubName": "KTX Khu B", "utilizationType": "Parking spots", "utilization": 85, "threshold": 80, "dangerLevel": "MEDIUM", "location": "KTX Khu B - Khu B2", "expectedCause": "Evening return traffic", "status": "ACTIVE", "createdAt": "2026-11-17T09:10:00"},
        {"id": "ALT-005", "hubId": "H5", "hubName": "Nhà văn hóa Sinh viên", "utilizationType": "Charging ports", "utilization": 82, "threshold": 75, "dangerLevel": "MEDIUM", "location": "Nhà văn hóa Sinh viên - Sảnh B", "expectedCause": "Student event surge", "status": "RESOLVED", "createdAt": "2026-11-17T09:05:00"},
    ],
}

Path(__file__).resolve().parents[1].joinpath("data", "seed.json").write_text(
    json.dumps(seed, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
)
