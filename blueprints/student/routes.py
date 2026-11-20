"""Các màn hình mobile của Sinh viên (UC1–UC7).

Mẫu chuẩn của một route:  nhận yêu cầu -> gọi service -> render_template.
Route KHÔNG chứa logic nghiệp vụ; logic nằm trong services/.
"""
from flask import Blueprint, abort, redirect, render_template, request, session, url_for

import config
from data import mock_data as db
from services import search_service, trip_service, charging_service
from services.auth_service import loginRequired
from services.errors import ServiceError

bp = Blueprint("student", __name__)


# ---------- UC1 (Hình 1) – MÀN HÌNH MẪU ĐÃ LÀM XONG ----------
@bp.route("/search")
def search():
    criteria = {
        "radiusKm": request.args.get("radiusKm", config.DEFAULT_RADIUS_KM, type=float),
        "vehicleType": request.args.get("vehicleType") or None,
        "minBatteryLevel": request.args.get("minBatteryLevel", 0, type=int),
    }
    results, mapView, error = [], None, None
    try:
        location = search_service.resolveSearchLocation(None, config.DEFAULT_LOCATION)
        results = search_service.searchVehicleAndHub(location, **criteria)
        mapView = search_service.displayResultsOnMap(results, location)
    except ServiceError as e:
        error = e
    return render_template("student/search.html", criteria=criteria, results=results,
                           mapView=mapView, error=error)


# ---------- Các màn hình còn lại: mới có khung, TV1/TV2 hoàn thiện ----------
# tên trang -> (template, cần đăng nhập?)
PAGES = {
    "resource":        ("student/resource.html", False),          # UC2
    "pickup":          ("student/pickup.html", True),             # UC5 – Hình 6
    "ride":            ("student/ride.html", True),               # UC5 – Hình 7
    "return":          ("student/return.html", True),             # UC6 – Hình 8
    "returned":        ("student/returned.html", True),           # UC6 – Hình 9
    "charging":        ("student/charging_slot.html", True),      # UC7 – Hình 10
    "charging-review": ("student/charging_review.html", True),    # UC7 – Hình 11
    "charging-suggest": ("student/charging_suggest.html", True),  # UC7 – Hình 12
}


# ---------- UC2 - Resource details ----------
@bp.route("/resource")
def resource():
    return render_template("student/resource.html")


# ---------- UC5 - Pickup (Hình 6) ----------
@bp.route("/pickup")
@loginRequired("STUDENT")
def pickup():
    return render_template("student/pickup.html")


# ---------- UC5 - Ride (Hình 7) ----------
@bp.route("/ride")
@loginRequired("STUDENT")
def ride():
    return render_template("student/ride.html")


# ---------- UC6 - Return (Hình 8) ----------
@bp.route("/return", methods=["GET", "POST"])
@loginRequired("STUDENT")
def returnPage():
    user = session.get("user")
    error = None
    result = None

    if request.method == "POST":
        bookingId = request.form.get("bookingId")
        hubId = request.form.get("hubId")

        try:
            result = trip_service.returnVehicle(
                user["id"], bookingId, hubId
            )
            return redirect(url_for("student.returned"))
        except ServiceError as e:
            error = e

    return render_template(
        "student/return.html",
        error=error,
        result=result
    )


# ---------- UC6 - Returned (Hình 9) ----------
@bp.route("/returned")
@loginRequired("STUDENT")
def returned():
    return render_template("student/returned.html")


# ---------- UC7 - Charging slot (Hình 10) ----------
@bp.route("/charging")
@loginRequired("STUDENT")
def charging():
    return render_template("student/charging_slot.html")


# ---------- UC7 - Charging review (Hình 11) ----------
@bp.route("/charging-review", methods=["GET", "POST"])
@loginRequired("STUDENT")
def chargingReview():
    user = session.get("user")
    error = None
    registration = None

    if request.method == "POST":
        hubId = request.form.get("hubId")
        portId = request.form.get("portId")
        timeSlot = request.form.get("timeSlot")
        batteryLevel = request.form.get("batteryLevel", type=int)

        try:
            registration = charging_service.registerCharging(
                user["id"], hubId, portId, timeSlot, batteryLevel
            )
            return render_template(
                "student/charging_review.html",
                registration=registration,
                error=None
            )
        except ServiceError as e:
            error = e

    return render_template(
        "student/charging_review.html",
        registration=registration,
        error=error
    )


# ---------- UC7 - Charging suggestion (Hình 12) ----------
@bp.route("/charging-suggest")
@loginRequired("STUDENT")
def chargingSuggest():
    hubId = request.args.get("hubId")
    suggestedHub = None
    error = None

    try:
        suggestedHub = charging_service.suggestNearestHubWithPort(hubId)
    except ServiceError as e:
        error = e

    return render_template(
        "student/charging_suggest.html",
        suggestedHub=suggestedHub,
        error=error
    )


@bp.route("/<page>")
def page(page):
    if page not in PAGES:
        abort(404)
    template, needLogin = PAGES[page]
    view = lambda: render_template(template)
    return loginRequired("STUDENT")(view)() if needLogin else view()
