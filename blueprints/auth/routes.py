"""UC17 – màn hình đăng nhập SSO giả lập (Hình 13, 14)."""
from flask import Blueprint, redirect, render_template, request, session, url_for

from services import auth_service
from services.errors import ServiceError

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            user = auth_service.authenticate(request.form.get("email", ""), request.form.get("password", ""))
            session["user"] = user
            fallback = url_for("operator.overview") if user["role"] == "OPERATOR" else url_for("student.search")
            return redirect(request.args.get("next") or fallback)
        except ServiceError as e:
            error = e          # template dựa vào error.code để hiện đúng kiểu lỗi
    return render_template("auth/login.html", error=error)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("student.search"))


@bp.route("/denied")
def denied():
    return render_template("auth/denied.html"), 403
