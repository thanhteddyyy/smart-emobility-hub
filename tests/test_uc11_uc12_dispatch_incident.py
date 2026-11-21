"""Test cho UC11 (Điều phối phương tiện) và UC12 (Xử lý sự cố)."""
import pytest

from data import mock_data as db
from services import dispatch_service, incident_service
from services.errors import DISPATCH_CONFLICT, HUB_FULL, ServiceError


def test_dispatch_success():
    """TC_UC11_01 – Normal Flow: Điều phối xe AVAILABLE sang Hub đích còn chỗ."""
    available = [v for v in db.VEHICLES if v["hubId"] == "H1" and v["status"] == "AVAILABLE"]
    assert len(available) >= 1
    vid = available[0]["id"]
    order = dispatch_service.processDispatch("OP001", "H1", "H2", [vid])
    assert order["status"] == "PENDING"
    assert db.getVehicle(vid) is not None


def test_dispatch_vehicle_conflict():
    """TC_UC11_02 – EX1: Xe không còn AVAILABLE bị từ chối với DISPATCH_CONFLICT."""
    v = db.VEHICLES[0]
    v["status"] = "RESERVED"
    with pytest.raises(ServiceError) as exc:
        dispatch_service.processDispatch("OP001", v["hubId"], "H2", [v["id"]])
    assert exc.value.code == DISPATCH_CONFLICT


def test_dispatch_destination_hub_full():
    """TC_UC11_03 – EX2: Hub đích hết chỗ đỗ báo HUB_FULL."""
    for spot in db.PARKING_SPOTS:
        if spot["hubId"] == "H2":
            spot["status"] = "OCCUPIED"
    available = [v for v in db.VEHICLES if v["hubId"] == "H1" and v["status"] == "AVAILABLE"]
    with pytest.raises(ServiceError) as exc:
        dispatch_service.processDispatch("OP001", "H1", "H2", [available[0]["id"]])
    assert exc.value.code == HUB_FULL


def test_cancel_pending_dispatch_order():
    """TC_UC11_04 – AF2: Hủy lệnh điều phối đang ở trạng thái PENDING."""
    db.DISPATCH_ORDERS.append({
        "id": "DSP-TEST-01",
        "fromHubId": "H1",
        "toHubId": "H2",
        "vehicleIds": ["EB-101"],
        "status": "PENDING",
    })
    cancelled = dispatch_service.cancelDispatchOrder("OP001", "DSP-TEST-01")
    assert cancelled["status"] == "CANCELLED"


def test_incident_pause_resource_and_audit():
    """TC_UC12_01 – Normal Flow: Tạm ngưng tài nguyên chuyển sự cố sang IN_PROGRESS và ghi AuditLog."""
    inc = db.INCIDENTS[0]
    before_logs = len(db.AUDIT_LOGS)
    updated = incident_service.handlePauseResource("OP001", inc["id"], "Kiểm tra pin", "Tạm ngưng")
    assert updated["status"] == "IN_PROGRESS"
    assert len(db.AUDIT_LOGS) > before_logs


def test_incident_complete_restores_resource():
    """TC_UC12_02 – AF1: Hoàn tất xử lý sự cố và khôi phục trạng thái tài nguyên."""
    inc = db.INCIDENTS[0]
    updated = incident_service.completeIncident("OP001", inc["id"], "AVAILABLE", "Đã sửa xong")
    assert updated["status"] == "RESOLVED"


def test_incident_isolate_disconnected_hub():
    """TC_UC12_03 – EX1/NFR05: Cô lập Hub mất kết nối mà không làm gián đoạn Hub khác."""
    hub = incident_service.isolateDisconnectedHub("H3")
    assert hub["status"] == "OFFLINE"
    assert db.getHub("H1")["status"] != "OFFLINE"


def test_incident_rbac_student_denied(client, loginAs):
    """TC_UC12_04 – NFR10: Sinh viên cố truy cập xử lý sự cố bị từ chối."""
    loginAs("student@hcmut.edu.vn")
    res = client.get("/operator/incidents")
    assert res.status_code == 302
    assert "/denied" in res.headers["Location"]
