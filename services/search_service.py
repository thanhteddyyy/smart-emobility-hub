"""UC1 – Tìm phương tiện và Hub phù hợp.  >>> FILE MẪU ĐÃ LÀM XONG – các service khác làm theo kiểu này <<<

Tên hàm đặt đúng theo Method description (Submission 3, mục 2.1).
"""
import math

import config
from data import mock_data as db
from services import status_service
from services.errors import INVALID_CRITERIA, LOCATION_UNAVAILABLE, ServiceError

SEARCH_TYPES = ("ALL", "VEHICLE", "HUB")


def resolveSearchLocation(gpsLocation, manualLocation):
    """Ưu tiên vị trí GPS; không có thì dùng vị trí nhập tay; không có cả hai -> lỗi (EX1)."""
    for location in (gpsLocation, manualLocation):
        if location and location.get("lat") is not None and location.get("lng") is not None:
            return {"lat": float(location["lat"]), "lng": float(location["lng"])}
    raise ServiceError(LOCATION_UNAVAILABLE, "Không xác định được vị trí tìm kiếm.")


def validateSearchCriteria(criteria):
    """Kiểm tra tiêu chí. Sai -> ServiceError(INVALID_CRITERIA)."""
    radiusKm = criteria.get("radiusKm")
    if radiusKm is None or not (config.MIN_RADIUS_KM <= radiusKm <= config.MAX_RADIUS_KM):
        raise ServiceError(INVALID_CRITERIA,
                           f"Bán kính phải từ {config.MIN_RADIUS_KM} đến {config.MAX_RADIUS_KM} km.")
    if criteria.get("searchType", "ALL") not in SEARCH_TYPES:
        raise ServiceError(INVALID_CRITERIA, "Loại tìm kiếm không hợp lệ.")
    minBattery = criteria.get("minBatteryLevel", 0)
    if not (0 <= minBattery <= 100):
        raise ServiceError(INVALID_CRITERIA, "Mức pin tối thiểu phải từ 0 đến 100.")


def searchVehicleAndHub(location, radiusKm, searchType="ALL", vehicleType=None, minBatteryLevel=0):
    """Trả về danh sách Hub trong bán kính, kèm số xe phù hợp, sắp xếp gần -> xa.

    Danh sách rỗng là kết quả hợp lệ (AF3): giao diện tự hiện "không có kết quả".
    """
    validateSearchCriteria({"radiusKm": radiusKm, "searchType": searchType,
                            "minBatteryLevel": minBatteryLevel})
    results = []
    for hub in db.HUBS:
        distanceKm = _distanceKm(location, hub)
        if distanceKm > radiusKm:
            continue
        matchingVehicles = [
            v for v in db.vehiclesOfHub(hub["id"])
            if v["status"] == "AVAILABLE"
            and v["batteryLevel"] >= minBatteryLevel
            and (not vehicleType or v["type"] == vehicleType)
        ]
        if searchType == "VEHICLE" and not matchingVehicles:
            continue
        hubStatus = status_service.buildHubStatus(hub)
        hubStatus["distanceKm"] = round(distanceKm, 2)
        hubStatus["walkMinutes"] = max(1, round(distanceKm / 5 * 60))   # đi bộ ~5 km/h
        hubStatus["matchingVehicles"] = matchingVehicles
        results.append(hubStatus)
    results.sort(key=lambda r: r["distanceKm"])
    return results


def displayResultsOnMap(results, searchLocation):
    """Gói dữ liệu cho bản đồ Leaflet: tâm bản đồ + danh sách marker."""
    return {
        "center": searchLocation,
        "markers": [{"hubId": r["hubId"], "name": r["name"], "lat": r["lat"], "lng": r["lng"],
                     "availableVehicles": r["availableVehicles"]} for r in results],
    }


def _distanceKm(a, b):
    """Khoảng cách đường chim bay (công thức Haversine)."""
    lat1, lng1, lat2, lng2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))
