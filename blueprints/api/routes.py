"""API trả JSON: dùng cho cập nhật realtime và các nút bấm không tải lại trang.

Quy ước trả về:
  thành công: {"ok": true, ...dữ liệu}
  lỗi nghiệp vụ: HTTP 400 {"ok": false, "error": "MÃ_LỖI", "message": "..."}
  chưa làm:      HTTP 501 {"ok": false, "error": "NOT_IMPLEMENTED", ...}
"""
from flask import Blueprint, jsonify, request, session

from services import booking_service, monitor_service, realtime_service, trip_service, charging_service, dispatch_service, incident_service, schedule_service, simulation_service

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
    vehicles = overview.get("vehicles")
    return jsonify({"ok": True, "network": overview, "hubs": hubs, "vehicles": vehicles})


# ---------- UC16: nhận gói tin IoT giả lập (demo lọc gói trễ) ----------
@bp.route("/telemetry", methods=["POST"])
def telemetry():
    result = realtime_service.receiveTelemetryPacket(request.get_json(force=True))
    return jsonify({"ok": True, "result": result})


@bp.route("/telemetry/packet-log")
def packetLog():
    return jsonify({"ok": True, "packetLog": realtime_service.PACKET_LOG[-50:]})


# ---------- UC3: ví dụ API cho nút "Confirm Booking" ----------
@bp.route("/bookings/vehicle", methods=["POST"])
def bookVehicle():
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    data = request.get_json(silent=True) or {}
    booking = booking_service.bookVehicle(user["id"], data.get("vehicleId"))
    return jsonify({"ok": True, "booking": booking})


# ---------- UC4: Đặt chỗ và huỷ lượt đặt ----------
@bp.route("/bookings/hub", methods=["POST"])
@bp.route("/bookings/parking", methods=["POST"])
def bookParking():
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    
    data = request.get_json(silent=True) or {}
    hubId = data.get("hubId")
    timeSlot = data.get("timeSlot")
    if not (hubId and timeSlot):
        return jsonify({"ok": False, "error": "MISSING_FIELDS", "message": "Thiếu thông tin đặt chỗ."}), 400
    try: 
        booking = booking_service.bookParking(user["id"], hubId, timeSlot)
        return jsonify({"ok": True, "booking": booking})
    except ServiceError as e:
        status_code = 409 if e.code == "HUB_FULL" else 400
        return jsonify(e.toDict()), status_code

@bp.route("/bookings/<bookingId>", methods=["DELETE"])
def cancelBooking(bookingId):
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    try:
        booking_service.cancelBooking(user["id"], bookingId)
        return jsonify({"ok": True, "message": "Huỷ lượt đặt thành công"})
    except ServiceError as e:
        status_code = 404 if e.code == "BOOKING_NOT_FOUND" else 400
        return jsonify(e.toDict()), status_code

#---------- UC5: Nhận phương tiện" ----------
@bp.route("/trips/<bookingId>/confirm-pickup", methods=["POST"])
def confirmPickup(bookingId):
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    try:
        trip_service.confirmPickup(user["id"], bookingId)
        return jsonify({"ok": True, "message": "Phương tiện đã được nhận."})
    except ServiceError as e:
        status_code = 400
        if e.code == "BOOKING_NOT_FOUND":
            status_code = 404
        elif e.code == "HOLD_EXPIRED":
            status_code = 409
        return jsonify(e.toDict()), status_code

#---------- UC6: Trả phương tiện" ----------
@bp.route("/trips/<bookingId>/return-vehicle", methods=["POST"])
def returnVehicle(bookingId):
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    data = request.get_json(silent=True) or {}
    hubId = data.get("hubId")
    if not hubId:
        return jsonify({"ok": False, "error": "MISSING_HUB_ID", "message": "Thiếu thông tin Hub."}), 400
    try:
        trip_service.returnVehicle(user["id"], bookingId, hubId)
        return jsonify({"ok": True, "message": "Trả xe thành công."})
    except ServiceError as e:
        status_code = 400
        if e.code == "BOOKING_NOT_FOUND":
            status_code = 404
        elif e.code == "HUB_FULL":
            status_code = 409
        return jsonify(e.toDict()), status_code

#---------- UC7: Đăng ký sạc" ----------
@bp.route("/charging/register", methods=["POST"])
def registerCharging():
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    data = request.get_json(silent=True) or {}
    hubId = data.get("hubId")
    portId = data.get("portId")
    timeSlot = data.get("timeSlot")
    batteryLevel = data.get("batteryLevel")
    if not (hubId and portId and timeSlot and batteryLevel is not None):
        return jsonify({"ok": False, "error": "MISSING_FIELDS", "message": "Thiếu thông tin đặt sạc."}), 400
    try:
        registration = charging_service.registerCharging(user["id"], hubId, portId, timeSlot, batteryLevel)
        return jsonify({"ok": True, "registration": registration})
    except ServiceError as e:
        status_code = 409 if e.code == "NO_PORT_AVAILABLE" else 400
        return jsonify(e.toDict()), status_code



#---------- UC11: Điều phối phương tiện" ----------
@bp.route("/dispatch/hub-data", methods=["GET"])
def getDispatchHubData():
    sourceHubId = request.args.get("sourceHubId")
    destHubId = request.args.get("destHubId")
    if not sourceHubId or not destHubId:
        return jsonify({"ok": False, "error": "MISSING_FIELDS", "message": "Thiếu Hub nguồn hoặc Hub đích."}), 400
    try:
        result = dispatch_service.getDispatchHubData(sourceHubId, destHubId)
        return jsonify({"ok": True, "data": result})
    except ServiceError as e:
        status_code = 404 if e.code == "HUB_NOT_FOUND" else 400
        return jsonify(e.toDict()), status_code

@bp.route("/dispatch-orders", methods=["POST"])
def processDispatch():
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    if user["role"] != "OPERATOR":
        return jsonify({"ok": False, "error": "FORBIDDEN", "message": "Không có quyền truy cập."}), 403
    data = request.get_json(silent=True) or {}
    sourceHubId = data.get("sourceHubId")
    destHubId = data.get("destHubId")
    vehicleIds = data.get("vehicleIds")
    if not sourceHubId or not destHubId or not vehicleIds:
        return jsonify({"ok": False, "error": "MISSING_FIELDS", "message": "Thiếu thông tin điều phối."}), 400
    try:
        result = dispatch_service.processDispatch(user["id"], sourceHubId, destHubId, vehicleIds)
        return jsonify({"ok": True, "data": result})
    except ServiceError as e:
        status_code = 400
        if e.code == "DISPATCH_CONFLICT" or e.code == "HUB_FULL":
            status_code = 409
        return jsonify(e.toDict()), status_code

@bp.route("/dispatch-orders/<orderId>", methods=["DELETE"])
def cancelDispatchOrder(orderId):
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    if user["role"] != "OPERATOR":
        return jsonify({"ok": False, "error": "FORBIDDEN", "message": "Không có quyền truy cập."}), 403
    try:
        dispatch_service.cancelDispatchOrder(user["id"], orderId)
        return jsonify({"ok": True, "message": "Huỷ lệnh thành công"})
    except ServiceError as e:
        status_code = 409 if e.code == "DISPATCH_CONFLICT" else 400
        return jsonify(e.toDict()), status_code

#---------- UC12: Điều phối phương tiện" ----------

@bp.route("/incidents/<incidentId>/handling", methods = ["POST"])
def handlePauseResource(incidentId):
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    if user["role"] != "OPERATOR":
        return jsonify({"ok": False, "error": "FORBIDDEN", "message": "Không có quyền truy cập."}), 403
    data = request.get_json(silent=True) or {}
    reason = data.get("reason")
    fixingMethod = data.get("fixingMethod")
    if not reason or not fixingMethod:
        return jsonify({"ok": False, "error": "MISSING_FIELDS", "message": "Thiếu thông tin sửa lỗi."}), 400
    try:
        handling = incident_service.handlePauseResource(user["id"], incidentId, reason, fixingMethod)
        return jsonify({"ok": True, "handling": handling})
    except ServiceError as e:
        status_code = 404 if e.code == "INCIDENT_NOT_FOUND" else 400
        return jsonify(e.toDict()), status_code

@bp.route("/incidents/<incidentId>/completion", methods = ["POST"])
def completeIncident(incidentId):
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    if user["role"] != "OPERATOR":
        return jsonify({"ok": False, "error": "FORBIDDEN", "message": "Không có quyền truy cập."}), 403
    try:
        incident_service.completeIncident(user["id"], incidentId)
        return jsonify({"ok": True, "message": "Sự cố đã được xử lý hoàn tất."})
    except ServiceError as e:
        status_code = 404 if e.code == "INCIDENT_NOT_FOUND" else 400
        return jsonify(e.toDict()), status_code

@bp.route("/incidents/hubs/<hubId>/isolate", methods=["POST"])
def isolateDisconnectedHub(hubId):
    try:
        incident_service.isolateDisconnectedHub(hubId)
        return jsonify({"ok": True, "message": "Hub đã bị cô lập."})
    except ServiceError as e:
        status_code = 404 if e.code == "HUB_NOT_FOUND" else 400
        return jsonify(e.toDict()), status_code 

#---------- UC13: Lịch sạc thông minh ----------
@bp.route("/hubs/<hubId>/charging-schedules/generate", methods=["POST"])
@bp.route("/hubs/<hubId>/charging-schedule/generate", methods=["POST"])
def generateSchedule(hubId):
    try:
        result = schedule_service.generateSchedule(hubId)
        return jsonify({"ok": True, "data": result})
    except ServiceError as e:
        status_code = 404 if e.code in ("HUB_NOT_FOUND", "RESOURCE_NOT_FOUND") else 400
        return jsonify(e.toDict()), status_code


@bp.route("/charging-schedules/validate", methods=["POST"])
@bp.route("/charging-schedule/validate", methods=["POST"])
def validateSchedule():
    data = request.get_json(silent=True) or {}
    schedule = data.get("schedule") or []
    isValid = schedule_service.validateSchedule(schedule)
    if not isValid:
        return jsonify({"ok": False, "error": "INVALID_SCHEDULE", "message": "Lịch sạc bị trùng cổng/khung giờ hoặc cổng lỗi."}), 400
    return jsonify({"ok": True, "message": "Lịch sạc hợp lệ."})


@bp.route("/charging-schedules/change", methods=["PATCH"])
@bp.route("/charging-schedule/edit", methods=["PATCH"])
def editSchedule():
    data = request.get_json(silent=True) or {}
    schedule = data.get("schedule")
    changes = data.get("changes")
    if not changes:
        return jsonify({"ok": False, "error": "CHANGE_NOT_FOUND", "message": "Thiếu thông tin thay đổi."}), 400
    try:
        edited = schedule_service.editSchedule(schedule, changes)
        return jsonify({"ok": True, "data": edited, "message": "Đã thay đổi lịch sạc."})
    except ServiceError as e:
        return jsonify(e.toDict()), 400


@bp.route("/charging-schedules/approve", methods=["POST"])
@bp.route("/charging-schedule/approve", methods=["POST"])
def approveSchedule():
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "error": "LOGIN_REQUIRED", "message": "Cần đăng nhập."}), 401
    if user["role"] != "OPERATOR":
        return jsonify({"ok": False, "error": "FORBIDDEN", "message": "Không có quyền truy cập."}), 403
    data = request.get_json(silent=True) or {}
    schedule = data.get("schedule")
    try:
        approved = schedule_service.approveSchedule(user["id"], schedule)
        return jsonify({"ok": True, "data": approved, "message": "Lịch sạc đã được xác nhận."})
    except ServiceError as e:
        return jsonify(e.toDict()), 400

#---------- UC14: Mô phỏng và phân tích kịch bản What-if" ----------
@bp.route("/what-if/simulate", methods=["POST"])
def simulateWhatIf():
    data = request.get_json(silent=True) or {}
    params = data.get("params")
    if not params:
        return jsonify({"ok": False, "error": "MISSING_PARAMS", "message": "Thiếu thông số mô phỏng."}), 400
    try:
        simulation_service.validateParameters(params)
        virtualData = simulation_service.initVirtualEnvironment()
        impact = simulation_service.calculateImpact(virtualData, params)
        report = simulation_service.generateReport(impact)
        return jsonify({"ok": True, "data": report})
    except ServiceError as e:
        status_code = 409 if e.code == "INVALID_PARAMETERS" else 400
        return jsonify(e.toDict()), status_code
