"""Web Dashboard của Đơn vị vận hành (UC8–UC14). Mọi route đều yêu cầu vai trò OPERATOR."""
from flask import Blueprint, abort, render_template

from services import monitor_service
from services.auth_service import loginRequired

bp = Blueprint("operator", __name__)


# ---------- UC8 (Hình 15) – bản cơ bản đã chạy, TV3 làm đẹp theo Figma ----------
@bp.route("/")
@loginRequired("OPERATOR")
def overview():
    return render_template("operator/overview.html", overview=monitor_service.getNetworkOverview())


# ---------- Các màn hình còn lại: mới có khung ----------
PAGES = {
    "resources":  "operator/resources.html",        # UC9  – Hình 16
    "alerts":     "operator/alerts.html",           # UC10 – Hình 17
    "incidents":  "operator/incidents.html",        # UC12 – Hình 18
    "incident":   "operator/incident_detail.html",  # UC12 – Hình 19
    "dispatch":   "operator/dispatch.html",         # UC11 – Hình 20
    "simulation": "operator/simulation.html",       # UC14 – Hình 21
    "schedule":   "operator/schedule.html",         # UC13 – chưa có mockup
}


@bp.route("/<page>")
@loginRequired("OPERATOR")
def page(page):
    if page not in PAGES:
        abort(404)
    return render_template(PAGES[page])
    # TODO(TV3/TV4): tách thành route riêng, gọi service tương ứng rồi truyền dữ liệu vào template.
