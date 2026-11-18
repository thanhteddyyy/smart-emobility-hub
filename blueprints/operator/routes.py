"""Web Dashboard của Đơn vị vận hành (UC8–UC14). Mọi route đều yêu cầu vai trò OPERATOR."""
from flask import Blueprint, redirect, render_template, request, session, url_for

from services import alert_service, dispatch_service, incident_service, monitor_service, simulation_service
from services.auth_service import loginRequired
from services.errors import ServiceError

bp = Blueprint("operator", __name__)


def _currentOperator():
    return session.get("user") or {"id": "OP001", "name": "Matthew", "role": "OPERATOR"}


# ---------- UC8: Tổng quan mạng lưới (OverviewDashboard) ----------
@bp.route("/")
@bp.route("/overview")
@loginRequired("OPERATOR")
def overview():
    filterCriteria = {
        "q": request.args.get("q", ""),
        "operationStatus": request.args.get("operationStatus", ""),
        "safetyWarning": request.args.get("safetyWarning", ""),
        "area": request.args.get("area", ""),
    }
    overviewData = monitor_service.getNetworkOverview(filterCriteria)
    alerts = alert_service.evaluateHubLoad()
    return render_template(
        "operator/overview.html",
        overview=overviewData,
        alerts=alerts,
        filter=filterCriteria,
    )


# ---------- UC9: Theo dõi tài nguyên một Hub (ResourceDashboard) ----------
@bp.route("/resources")
@bp.route("/resources/<hubId>")
@loginRequired("OPERATOR")
def resources(hubId="H1"):
    resourceData, error = None, None
    try:
        resourceData = alert_service.getHubResources(hubId)
    except ServiceError as e:
        error = e
    return render_template(
        "operator/resources.html",
        data=resourceData,
        hubId=hubId,
        error=error,
    )


# ---------- UC10: Cảnh báo quá tải (AlertDashboard) ----------
@bp.route("/alerts", methods=["GET", "POST"])
@loginRequired("OPERATOR")
def alerts():
    error = None
    if request.method == "POST":
        alertId = request.form.get("alertId")
        try:
            alert_service.resolveAlert(_currentOperator()["name"], alertId)
            return redirect(url_for("operator.alerts", alertId=alertId, resolved="1"))
        except ServiceError as e:
            error = e

    alertsList = alert_service.evaluateHubLoad()
    selectedId = request.args.get("alertId")
    selectedAlert = next((a for a in alertsList if a["id"] == selectedId), None)
    if not selectedAlert and alertsList:
        selectedAlert = alertsList[0]

    return render_template(
        "operator/alerts.html",
        alerts=alertsList,
        selectedAlert=selectedAlert,
        resolved=request.args.get("resolved") == "1",
        error=error,
    )


# ---------- UC12: Danh sách sự cố (IncidentModal1) ----------
@bp.route("/incidents")
@loginRequired("OPERATOR")
def incidents():
    incidentsList = incident_service.getPrioritizedIncidents()
    return render_template("operator/incidents.html", incidents=incidentsList)


# ---------- UC12: Chi tiết & xử lý sự cố (IncidentModal2 - trang riêng) ----------
@bp.route("/incidents/<incidentId>", methods=["GET", "POST"])
@loginRequired("OPERATOR")
def incidentDetail(incidentId):
    error, savedMessage = None, None
    if request.method == "POST":
        action = request.form.get("action")
        operatorName = _currentOperator()["name"]
        try:
            if action == "pause":
                incident_service.handlePauseResource(
                    operatorName,
                    incidentId,
                    request.form.get("reason", ""),
                    request.form.get("fixingMethod", ""),
                )
                savedMessage = "paused"
            elif action == "update":
                incident_service.completeIncident(
                    operatorName,
                    incidentId,
                    request.form.get("resourceStatus", "AVAILABLE"),
                    request.form.get("updateDetails", ""),
                )
                savedMessage = "updated"
        except ServiceError as e:
            error = e

    incident = None
    try:
        incident = incident_service.getIncidentById(incidentId)
    except ServiceError as e:
        error = e

    return render_template(
        "operator/incident_detail.html",
        incident=incident,
        error=error,
        savedMessage=savedMessage,
    )


# ---------- UC11: Điều phối phương tiện (Dispatch) ----------
@bp.route("/dispatch", methods=["GET", "POST"])
@loginRequired("OPERATOR")
def dispatch():
    sourceHubId = request.values.get("sourceHubId") or ""
    destHubId = request.values.get("destHubId") or ""
    error, successMessage = None, None

    if request.method == "POST":
        action = request.form.get("action", "dispatch")
        operatorId = _currentOperator()["id"]
        try:
            if action == "cancel":
                orderId = request.form.get("orderId")
                dispatch_service.cancelDispatchOrder(operatorId, orderId)
                successMessage = f"Đã hủy lệnh điều phối {orderId}."
            else:
                vehicleIds = request.form.getlist("vehicleIds")
                order = dispatch_service.processDispatch(operatorId, sourceHubId, destHubId, vehicleIds)
                successMessage = f"Đã tạo lệnh điều phối {order['id']} ({len(order['vehicleIds'])} xe)."
        except ServiceError as e:
            error = e

    dispatchData = dispatch_service.getDispatchHubData(sourceHubId or None, destHubId or None)
    return render_template(
        "operator/dispatch.html",
        data=dispatchData,
        error=error,
        successMessage=successMessage,
    )


# ---------- UC14: Mô phỏng What-if (Simulation) ----------
@bp.route("/simulation", methods=["GET", "POST"])
@loginRequired("OPERATOR")
def simulation():
    params = {
        "studentDemandPercent": request.form.get("studentDemandPercent", 20),
        "availableEvDelta": request.form.get("availableEvDelta", -15),
        "weather": request.form.get("weather", "HEAVY_RAIN"),
    }
    report, error = None, None
    try:
        report = simulation_service.runSimulation(params)
    except ServiceError as e:
        error = e
        report = simulation_service.runSimulation({})

    return render_template(
        "operator/simulation.html",
        params=report["params"] if report else params,
        report=report,
        error=error,
    )


@bp.route("/simulation/apply", methods=["POST"])
@loginRequired("OPERATOR")
def applySimulation():
    rec = simulation_service.applyRecommendation(request.form.get("reportId"))
    return redirect(
        url_for("operator.dispatch", sourceHubId=rec["sourceHubId"], destHubId=rec["destHubId"])
    )


# ---------- UC13: Lịch sạc (chưa có mockup Figma — placeholder) ----------
@bp.route("/schedule")
@loginRequired("OPERATOR")
def schedule():
    return render_template("operator/schedule.html")
