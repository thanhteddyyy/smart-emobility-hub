"""Các màn hình mobile của Sinh viên (UC1–UC7).

Mẫu chuẩn của một route:  nhận yêu cầu -> gọi service -> render_template.
Route KHÔNG chứa logic nghiệp vụ; logic nằm trong services/.
"""
from flask import Blueprint, abort, render_template, request

import config
from services import search_service
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


@bp.route("/<page>")
def page(page):
    if page not in PAGES:
        abort(404)
    template, needLogin = PAGES[page]
    view = lambda: render_template(template)
    return loginRequired("STUDENT")(view)() if needLogin else view()
    # TODO(TV1/TV2): khi làm thật, tách mỗi màn hình thành một route riêng như search() ở trên.
