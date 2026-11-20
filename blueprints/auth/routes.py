"""UC17 – màn hình đăng nhập SSO giả lập (2 cổng riêng: Sinh viên /login & Vận hành /operator/login)."""
from flask import Blueprint, redirect, render_template, request, session, url_for

from services import auth_service
from services.errors import ACCESS_DENIED, ServiceError

bp = Blueprint("auth", __name__)


def _safeNextUrl(nextUrl, allowedPrefix=None):
    if not nextUrl or not nextUrl.startswith("/") or nextUrl.startswith("//"):
        return None
    if allowedPrefix and not nextUrl.startswith(allowedPrefix):
        return None
    return nextUrl


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Cổng đăng nhập Mobile SSO dành cho Sinh viên (vẫn giữ tương thích test khi Operator POST /login)."""
    error = None
    if request.method == "POST":
        try:
            user = auth_service.authenticate(
                request.form.get("email", "").strip(),
                request.form.get("password", ""),
            )
            session["user"] = user
            if user["role"] == "OPERATOR":
                target = _safeNextUrl(request.args.get("next"), "/operator") or url_for("operator.overview")
            else:
                target = _safeNextUrl(request.args.get("next"), "/student") or url_for("student.search")
            return redirect(target)
        except ServiceError as e:
            error = e          # template dựa vào error.code để hiện đúng kiểu lỗi
    return render_template("auth/login.html", error=error)


@bp.route("/operator/login", methods=["GET", "POST"])
def operatorLogin():
    """Cổng đăng nhập Desktop riêng dành cho Đơn vị vận hành (chỉ chấp nhận role OPERATOR)."""
    current = session.get("user")
    if request.method == "GET" and current and current.get("role") == "OPERATOR" and request.args.get("ui") != "H14":
        target = _safeNextUrl(request.args.get("next"), "/operator") or url_for("operator.overview")
        return redirect(target)

    error = None
    if request.method == "POST":
        try:
            user = auth_service.authenticate(
                request.form.get("email", "").strip(),
                request.form.get("password", ""),
            )
            if user["role"] != "OPERATOR":
                raise ServiceError(
                    ACCESS_DENIED,
                    "Cổng quản trị chỉ dành cho tài khoản Đơn vị vận hành.",
                )
            session["user"] = user
            target = _safeNextUrl(request.args.get("next"), "/operator") or url_for("operator.overview")
            return redirect(target)
        except ServiceError as e:
            error = e
    return render_template("auth/operator_login.html", error=error)


@bp.route("/logout")
def logout():
    user = session.get("user")
    isOperator = (user and user.get("role") == "OPERATOR") or request.args.get("portal") == "operator"
    session.clear()
    if isOperator:
        return redirect(url_for("auth.operatorLogin"))
    return redirect(url_for("student.search"))


@bp.route("/denied")
def denied():
    return render_template("auth/denied.html"), 403
