"""Test mẫu cho UC17 + phân quyền (NFR10)."""


def test_operator_page_requires_login(client):
    assert client.get("/operator/").status_code == 302


def test_student_cannot_open_dashboard(client, loginAs):
    loginAs("student@hcmut.edu.vn")
    response = client.get("/operator/")
    assert response.status_code == 302 and "/denied" in response.headers["Location"]


def test_operator_can_open_dashboard(client, loginAs):
    loginAs("operator@ehub.vn")
    assert client.get("/operator/").status_code == 200


def test_wrong_password_shows_error(client, loginAs):
    assert "Sai email" in loginAs("student@hcmut.edu.vn", "sai").get_data(as_text=True)
