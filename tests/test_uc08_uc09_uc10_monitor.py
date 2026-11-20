"""Test cho UC8 (Tổng quan mạng lưới), UC9 (Tài nguyên Hub), UC10 (Cảnh báo quá tải)."""
from datetime import datetime, timedelta, timezone

import pytest

import config
from data import mock_data as db
from services import alert_service, incident_service, monitor_service
from services.errors import RESOURCE_NOT_FOUND, ServiceError


def test_overview_filter_no_match():
    """TC_UC08_02 – AF5: Không có Hub phù hợp với bộ lọc."""
    overview = monitor_service.getNetworkOverview({"q": "KHONG_TON_TAI_XYZ"})
    assert overview["hubs"] == []


def test_overview_rbac_student_denied(client, loginAs):
    """TC_UC08_03 – EX1: Sinh viên không đủ quyền truy cập dashboard."""
    loginAs("student@hcmut.edu.vn")
    res = client.get("/operator/overview")
    assert res.status_code == 302
    assert "/denied" in res.headers["Location"]


def test_overview_isolated_offline_hub():
    """TC_UC08_05 – EX3/NFR05: Một Hub mất kết nối, các Hub khác vẫn hoạt động."""
    incident_service.isolateDisconnectedHub("H1")
    overview = monitor_service.getNetworkOverview()
    hubs = {h["hubId"]: h for h in overview["hubs"]}
    assert hubs["H1"]["status"] == "OFFLINE"
    assert hubs["H2"]["status"] != "OFFLINE"
    assert overview["totalHubs"] == len(db.HUBS)


def test_resources_stale_timestamp_detected():
    """TC_UC09_01 – Biên: tài nguyên có timestamp quá cũ được gắn cờ stale."""
    old_ts = (datetime.now(timezone.utc) - timedelta(seconds=config.STALE_THRESHOLD_SECONDS + 30)).isoformat()
    db.HUBS[0]["lastUpdated"] = old_ts
    data = alert_service.getHubResources(db.HUBS[0]["id"])
    assert data["hub"]["isStale"] is True


def test_resources_hub_not_found():
    """TC_UC09_02 – EX1: Hub không tồn tại báo RESOURCE_NOT_FOUND."""
    with pytest.raises(ServiceError) as exc:
        alert_service.getHubResources("H999")
    assert exc.value.code == RESOURCE_NOT_FOUND


def test_overload_alert_no_duplicate():
    """TC_UC10_01 – Quá tải: gọi nhiều lần không tạo cảnh báo trùng cho cùng Hub."""
    hub_id = "H1"
    for spot in db.PARKING_SPOTS:
        if spot["hubId"] == hub_id:
            spot["status"] = "OCCUPIED"
    first = alert_service.evaluateHubLoad()
    second = alert_service.evaluateHubLoad()
    h1_first = [a for a in first if a["hubId"] == hub_id and a["status"] == "ACTIVE"]
    h1_second = [a for a in second if a["hubId"] == hub_id and a["status"] == "ACTIVE"]
    assert len(h1_first) >= 1
    assert len(h1_first) == len(h1_second)


def test_low_usage_no_overload_alert():
    """TC_UC10_02 – Biên: mức sử dụng thấp hơn ngưỡng không sinh cảnh báo mới."""
    db.ALERTS.clear()
    for spot in db.PARKING_SPOTS:
        spot["status"] = "FREE"
    alerts = alert_service.evaluateHubLoad()
    assert alerts == []


def test_stale_hub_does_not_generate_new_alert():
    """TC_UC10_03 – Ngoại lệ: dữ liệu quá cũ không tạo cảnh báo quá tải mới."""
    db.ALERTS.clear()
    old_ts = (datetime.now(timezone.utc) - timedelta(seconds=config.STALE_THRESHOLD_SECONDS + 120)).isoformat()
    for h in db.HUBS:
        h["lastUpdated"] = old_ts
    for spot in db.PARKING_SPOTS:
        spot["status"] = "OCCUPIED"
    alerts = alert_service.evaluateHubLoad()
    assert alerts == []
