"""UC17 – Xác thực người dùng (SSO giả lập) + decorator phân quyền (NFR10)."""
from functools import wraps

from flask import redirect, request, session, url_for

from data import mock_data as db
from services.errors import ACCESS_DENIED, INVALID_CREDENTIALS, SSO_UNAVAILABLE, ServiceError

ALLOWED_ROLES = ("STUDENT", "OPERATOR")
SSO_AVAILABLE = True   # đổi thành False để demo lỗi SSO không khả dụng (Hình 14)


def authenticate(email, password):
    """Bản cơ bản đã chạy được. TODO(UC17): ghi AuditLog, xử lý AF1 (phiên còn hiệu lực)."""
    if not SSO_AVAILABLE:
        raise ServiceError(SSO_UNAVAILABLE, "Dịch vụ xác thực hiện không khả dụng. Vui lòng thử lại sau.")
    user = next((u for u in db.USERS if u["email"] == email and u["password"] == password), None)
    if not user:
        raise ServiceError(INVALID_CREDENTIALS, "Sai email hoặc mật khẩu.")
    if user["role"] not in ALLOWED_ROLES:
        raise ServiceError(ACCESS_DENIED, "Không đủ quyền truy cập. Vui lòng liên hệ Đơn vị vận hành.")
    return {"id": user["id"], "name": user["name"], "role": user["role"]}


def loginRequired(role=None):
    """Dùng trên route:  @loginRequired()  hoặc  @loginRequired("OPERATOR")"""
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = session.get("user")
            if not user:
                loginEndpoint = "auth.operatorLogin" if role == "OPERATOR" else "auth.login"
                return redirect(url_for(loginEndpoint, next=request.path))
            if role and user["role"] != role:
                return redirect(url_for("auth.denied"))
            return view(*args, **kwargs)
        return wrapper
    return decorator
