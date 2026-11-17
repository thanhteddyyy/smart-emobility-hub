"""API trả JSON: dùng cho cập nhật realtime và các nút bấm không tải lại trang.

Quy ước trả về:
  thành công: {"ok": true, ...dữ liệu}
  lỗi nghiệp vụ: HTTP 400 {"ok": false, "error": "MÃ_LỖI", "message": "..."}
  chưa làm:      HTTP 501 {"ok": false, "error": "NOT_IMPLEMENTED", ...}
"""
from flask import Blueprint, jsonify, request, session

from services import booking_service, monitor_service, realtime_service
from services.errors import ServiceError

bp = Blueprint("api", __name__)


@bp.errorhandler(ServiceError)
def handleServiceError(e):
    return jsonify(e.toDict()), 400


@bp.errorhandler(NotImplementedError)
def handleNotImplemented(e):
    return jsonify({"ok": False, "error": "NOT_IMPLEMENTED", "message": f"Chưa làm: {e}"}), 501


# ---------- UC16: trạng thái mới nhất cho static/js/realtime.js ----------
@bp.route("/state")
def state():
    overview = monitor_service.getNetworkOverview()
    hubs = {h["hubId"]: h for h in overview.pop("hubs")}
    return jsonify({"ok": True, "network": overview, "hubs": hubs})


# ---------- UC16: nhận gói tin IoT giả lập (demo lọc gói trễ) ----------
@bp.route("/telemetry", methods=["POST"])
def telemetry():
    result = realtime_service.receiveTelemetryPacket(request.get_json(force=True))
    return jsonify({"ok": True, "result": result})


# ---------- UC3: ví dụ API cho nút "Confirm Booking" ----------
@bp.route("/bookings/vehicle", methods=["POST"])
def bookVehicle():
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    booking = booking_service.bookVehicle(user["id"], request.get_json(force=True).get("vehicleId"))
    return jsonify({"ok": True, "booking": booking})

# TODO(TV4): thêm API cho UC4, UC5, UC6, UC7, UC11, UC12, UC13, UC14 theo cùng kiểu.
