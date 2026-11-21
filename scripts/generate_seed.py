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

# Tỷ lệ phân bổ riêng biệt cho từng Hub để phản ánh đúng kích thước & mức độ quá tải khác nhau:
# H1: 96% chỗ đỗ (Overload/HIGH) | H2: 75% chỗ đỗ, 84% cổng sạc (Danger/MEDIUM)
# H3: 60% chỗ đỗ (Safe/LOW)      | H4: 89% chỗ đỗ (Danger/MEDIUM) | H5: 48% chỗ đỗ (Safe/LOW)
spotProfiles = {
    "H1": (8, 4),
    "H2": (45, 5),
    "H3": (64, 4),
    "H4": (16, 4),
    "H5": (78, 4),
}
portAvailableCount = {
    "H1": 12,
    "H2": 7,
    "H3": 22,
    "H4": 20,
    "H5": 27,
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

    freeCount, reservedCount = spotProfiles[hub_id]
    for index in range(1, parking_count + 1):
        if index <= freeCount:
            status = "FREE"
        elif index <= freeCount + reservedCount:
            status = "RESERVED"
        else:
            status = "OCCUPIED"
        spots.append({
            "id": f"{hub_id}-P{index:02d}",
            "hubId": hub_id,
            "status": status,
            "lastUpdatedAt": "2026-11-17T08:00:00",
        })

    availTarget = portAvailableCount[hub_id]
    availAssigned = 0
    for index in range(1, port_count + 1):
        if hub_id == "H1" and index == 2:
            status = "OUT_OF_ORDER"
        elif index % 15 == 0:
            status = "OUT_OF_ORDER"
        elif availAssigned < availTarget:
            status = "AVAILABLE"
            availAssigned += 1
        else:
            status = "IN_USE"
        ports.append({
            "id": f"{hub_id}-C{index:02d}",
            "hubId": hub_id,
            "powerKw": 7.4 if index % 3 == 0 else 3.3,
            "status": status,
            "lastUpdatedAt": "2026-11-17T08:00:00",
        })

incidents = [
    ("INC-001", "H1", "CHARGING_PORT", "H1-C02", "Cổng sạc mất kết nối", "Mất kết nối IoT", "HIGH", "OPEN", None),
    ("INC-002", "H1", "HUB", "H1", "Hub sắp quá tải giờ cao điểm", "Quá tải trạm", "HIGH", "IN_PROGRESS", "Matthew"),
    ("INC-003", "H3", "VEHICLE", "EB-221", "GPS lệch vị trí khỏi trạm", "GPS lệch vị trí", "LOW", "RESOLVED", "Liam"),
    ("INC-004", "H4", "CHARGING_PORT", "H4-C01", "Cổng sạc lỗi chập chờn điện áp", "Hỏng cổng sạc", "MEDIUM", "OPEN", None),
    ("INC-005", "H2", "VEHICLE", "EB-213", "Pin sụt nhanh bất thường", "Lỗi pin / sụt áp", "LOW", "RESOLVED", "Liam"),
    ("INC-006", "H5", "HUB", "H5", "Hub mất tín hiệu định kỳ", "Mất kết nối IoT", "MEDIUM", "IN_PROGRESS", "Jack"),
    ("INC-007", "H2", "VEHICLE", "EB-209", "Phanh trước bị bó nhẹ cần bảo trì", "Hỏng phanh / lốp xe", "MEDIUM", "RESOLVED", "Jack"),
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
        {"id": "ALT-001", "hubId": "H1", "hubName": "Ga Metro ĐHQG", "utilizationType": "Parking spots", "utilization": 96, "threshold": 75, "dangerLevel": "HIGH", "location": "Ga Metro ĐHQG - Cửa Đông", "expectedCause": "Rush hour", "status": "ACTIVE", "createdAt": "2026-11-17T09:46:00"},
        {"id": "ALT-002", "hubId": "H2", "hubName": "KTX Khu A", "utilizationType": "Charging ports", "utilization": 84, "threshold": 80, "dangerLevel": "MEDIUM", "location": "KTX Khu A - Cổng chính", "expectedCause": "Peak charging demand", "status": "ACTIVE", "createdAt": "2026-11-17T09:36:00"},
        {"id": "ALT-003", "hubId": "H4", "hubName": "ĐH Bách khoa CS2", "utilizationType": "Parking spots", "utilization": 89, "threshold": 75, "dangerLevel": "MEDIUM", "location": "ĐH Bách khoa CS2 - Nhà xe A", "expectedCause": "Class dismissal peak", "status": "ACTIVE", "createdAt": "2026-11-17T09:26:00"},
        {"id": "ALT-004", "hubId": "H3", "hubName": "KTX Khu B", "utilizationType": "Parking spots", "utilization": 60, "threshold": 80, "dangerLevel": "LOW", "location": "KTX Khu B - Khu B2", "expectedCause": "Normal evening traffic", "status": "ACTIVE", "createdAt": "2026-11-17T09:10:00"},
        {"id": "ALT-005", "hubId": "H5", "hubName": "Nhà văn hóa Sinh viên", "utilizationType": "Charging ports", "utilization": 40, "threshold": 75, "dangerLevel": "LOW", "location": "Nhà văn hóa Sinh viên - Sảnh B", "expectedCause": "Off-peak charging window", "status": "RESOLVED", "createdAt": "2026-11-17T09:05:00"},
    ],
}

Path(__file__).resolve().parents[1].joinpath("data", "seed.json").write_text(
    json.dumps(seed, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
)
print("Generated data/seed.json successfully.")
