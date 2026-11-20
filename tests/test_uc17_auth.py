"""Test mẫu cho UC17 + phân quyền (NFR10) + 2 cổng đăng nhập riêng (Student & Operator)."""


def test_operator_page_requires_login(client):
    response = client.get("/operator/")
    assert response.status_code == 302
    assert "/operator/login" in response.headers["Location"]


def test_student_cannot_open_dashboard(client, loginAs):
    loginAs("student@hcmut.edu.vn")
    response = client.get("/operator/")
    assert response.status_code == 302 and "/denied" in response.headers["Location"]


def test_operator_can_open_dashboard(client, loginAs):
    loginAs("operator@ehub.vn")
    assert client.get("/operator/").status_code == 200


def test_wrong_password_shows_error(client, loginAs):
    assert "Sai email" in loginAs("student@hcmut.edu.vn", "sai").get_data(as_text=True)


def test_operator_login_page_renders_desktop_portal(client):
    response = client.get("/operator/login")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "op-auth-card" in html
    assert "/student/search" in html


def test_student_rejected_on_operator_login_portal(client):
    response = client.post(
        "/operator/login",
        data={"email": "student@hcmut.edu.vn", "password": "123456"},
    )
    assert response.status_code == 200
    assert "Đơn vị vận hành" in response.get_data(as_text=True)
    # Phiên không được thiết lập: mở /operator/ vẫn bị đẩy về /operator/login
    dash = client.get("/operator/")
    assert dash.status_code == 302 and "/operator/login" in dash.headers["Location"]


def test_operator_login_and_logout_stay_in_operator_portal(client):
    loginRes = client.post(
        "/operator/login",
        data={"email": "operator@ehub.vn", "password": "123456"},
    )
    assert loginRes.status_code == 302
    assert "/operator/overview" in loginRes.headers["Location"]
    assert client.get("/operator/").status_code == 200

    logoutRes = client.get("/logout")
    assert logoutRes.status_code == 302
    assert "/operator/login" in logoutRes.headers["Location"]


def test_student_can_browse_without_login_and_protected_pages_require_student_login(client, loginAs):
    assert client.get("/student/search").status_code == 200
    assert client.get("/student/resource").status_code == 200

    protected = client.get("/student/ride")
    assert protected.status_code == 302
    assert "/login" in protected.headers["Location"]
    assert "/operator/login" not in protected.headers["Location"]

    loginAs("student@hcmut.edu.vn")
    logoutRes = client.get("/logout")
    assert logoutRes.status_code == 302
    assert "/student/search" in logoutRes.headers["Location"]
