"""UC8 – Giám sát mạng lưới Mobility Hub (Submission 3, mục 2.6)."""
from datetime import datetime

from data import mock_data as db
from services import status_service
from services.errors import ACCESS_DENIED, SESSION_EXPIRED, ServiceError


def validateOperatorAccess(session):
    if not session or not session.get("user"):
        raise ServiceError(SESSION_EXPIRED, "Phiên đăng nhập đã hết hạn.")
    if session["user"]["role"] != "OPERATOR":
        raise ServiceError(ACCESS_DENIED, "Chỉ Đơn vị vận hành được truy cập.")


def computeHubUsage(hub):
    """Tỉ lệ sử dụng = số chỗ đang bị chiếm / tổng số chỗ."""
    overview = status_service.buildHubStatus(hub)
    total = overview["totalSpots"]
    overview["usageRate"] = round((total - overview["emptySpots"]) / total, 2) if total else 0
    return overview


def applyOverviewFilter(hubs, filter):
    """TODO(UC8): lọc theo filter['area'], filter['operationStatus'], filter['minUsageRate'].
    Không khớp Hub nào -> trả list rỗng (AF5)."""
    return hubs


def getNetworkOverview(filter=None):
    """Bản cơ bản đã chạy được. TODO(UC8): đánh dấu Hub lỗi dữ liệu, ghi AuditLog."""
    hubs = applyOverviewFilter([computeHubUsage(h) for h in db.HUBS], filter or {})
    return {
        "activeHubCount": sum(h["status"] == "ACTIVE" for h in hubs),
        "totalVehicles": len(db.VEHICLES),
        "availableVehicles": sum(v["status"] == "AVAILABLE" for v in db.VEHICLES),
        "availablePorts": sum(p["status"] == "AVAILABLE" for p in db.CHARGING_PORTS),
        "emptySpots": sum(s["status"] == "FREE" for s in db.PARKING_SPOTS),
        "openIncidents": sum(i["status"] != "RESOLVED" for i in db.INCIDENTS),
        "hubs": hubs,
        "updatedAt": datetime.now().isoformat(timespec="seconds"),
    }
