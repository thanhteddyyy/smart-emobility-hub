"""Test cho UC14 (Mô phỏng What-if), UC15 (Đa ngôn ngữ/UI), UC16 (Realtime/Gói trễ)."""
import copy
import json
import pathlib
import re

import pytest

from data import mock_data as db
from services import realtime_service, simulation_service
from services.errors import INVALID_PARAMETERS, ServiceError


def test_simulation_isolates_operational_db():
    """TC_UC14_01 – DEMO BẮT BUỘC: Chạy What-if trên bản sao độc lập, không làm đổi dữ liệu gốc."""
    before_hubs = copy.deepcopy(db.HUBS)
    before_vehicles = copy.deepcopy(db.VEHICLES)
    before_spots = copy.deepcopy(db.PARKING_SPOTS)

    report = simulation_service.runSimulation({
        "studentDemandPercent": 40,
        "availableEvDelta": -5,
        "weather": "HEAVY_RAIN",
    })
    assert "availableSeries" in report
    assert "demandSeries" in report
    assert db.HUBS == before_hubs
    assert db.VEHICLES == before_vehicles
    assert db.PARKING_SPOTS == before_spots


def test_simulation_apply_recommendation():
    """TC_UC14_02 – AF1: Áp dụng đề xuất mô phỏng trả dữ liệu điền sẵn cho điều phối."""
    report = simulation_service.runSimulation({
        "studentDemandPercent": 50,
        "availableEvDelta": -4,
        "weather": "LIGHT_RAIN",
    })
    rec = simulation_service.applyRecommendation(report["reportId"])
    assert "sourceHubId" in rec
    assert "destHubId" in rec
    assert "recommendedCount" in rec


def test_simulation_invalid_parameters():
    """TC_UC14_03 – EX1: Tham số mô phỏng ngoài ngưỡng hợp lệ báo INVALID_PARAMETERS."""
    with pytest.raises(ServiceError) as exc:
        simulation_service.validateParameters({
            "studentDemandPercent": 999,
            "availableEvDelta": 0,
            "weather": "CLEAR",
        })
    assert exc.value.code == INVALID_PARAMETERS


def test_i18n_json_valid_and_synced():
    """TC_UC15_02 – Kiểm tra từ điển vi.json và en.json hợp lệ JSON và đồng bộ key."""
    root = pathlib.Path(__file__).resolve().parent.parent
    vi = json.loads((root / "static/i18n/vi.json").read_text(encoding="utf-8"))
    en = json.loads((root / "static/i18n/en.json").read_text(encoding="utf-8"))
    assert set(vi.keys()) == set(en.keys())
    assert len(vi) > 0


def test_realtime_outdated_packet_detected():
    """TC_UC16_02 – NFR08: Phát hiện gói dữ liệu có timestamp cũ hơn trạng thái hiện tại."""
    assert realtime_service.isOutdatedPacket("2026-11-20T10:00:00+00:00", "2026-11-20T10:05:00+00:00") is True
    assert realtime_service.isOutdatedPacket("2026-11-20T10:05:00+00:00", "2026-11-20T10:05:00+00:00") is True
    assert realtime_service.isOutdatedPacket("2026-11-20T10:06:00+00:00", "2026-11-20T10:05:00+00:00") is False


def test_api_state_endpoint(client):
    """TC_UC16_01 – API /api/state trả về JSON hợp lệ cho realtime.js."""
    res = client.get("/api/state")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    assert "hubs" in payload


def test_simulation_uses_24h_labels_and_positive_deficit_sign():
    """UC14 – Trục thời gian 24h (không AM/PM) và dấu mức thiếu hụt = demand - available."""
    for tf in ("09:00-18:00", "06:00-12:00", "12:00-18:00"):
        shortage_report = simulation_service.runSimulation({
            "studentDemandPercent": 80,
            "availableEvDelta": -50,
            "weather": "HEAVY_RAIN",
            "timeFrame": tf,
        })
        assert all("AM" not in h and "PM" not in h for h in shortage_report["hours"])
        assert "AM" not in shortage_report["peakShortageTime"]
        assert "PM" not in shortage_report["peakShortageTime"]

        expected_max = max(
            dem - avail
            for avail, dem in zip(shortage_report["availableSeries"], shortage_report["demandSeries"])
        )
        assert shortage_report["maxVehicleDeficit"] == expected_max
        assert shortage_report["maxVehicleDeficit"] > 0
        assert shortage_report["recommendedCount"] > 0

    surplus_report = simulation_service.runSimulation({
        "studentDemandPercent": -50,
        "availableEvDelta": 100,
        "weather": "CLEAR",
        "timeFrame": "09:00-18:00",
    })
    assert surplus_report["maxVehicleDeficit"] < 0
    assert surplus_report["recommendedCount"] == 0


def test_schedule_single_item_approve_keeps_unselected_pending():
    """UC13 – Duyệt đơn lẻ 1 phần tử chỉ lưu phần tử đó, không ghi đè toàn bộ lịch."""
    from services import schedule_service

    schedule = schedule_service.generateSchedule("H1")
    assert len(schedule) >= 2
    before_len = len(db.CHARGING_REGISTRATIONS)
    approved_single = schedule_service.approveSchedule("OP001", [schedule[0]])
    assert len(approved_single) == 1
    assert approved_single[0]["id"] == schedule[0]["id"]
    assert approved_single[0]["status"] == "APPROVED"
    assert len(db.CHARGING_REGISTRATIONS) == before_len + 1


def test_schedule_custom_edit_overwrite_and_reload(client):
    """UC13 – Cho phép tùy chỉnh cổng/khung giờ, lưu đè đúng bản ghi, nạp lại và xóa qua API."""
    from services import schedule_service

    with client.session_transaction() as sess:
        sess["user"] = {"id": "OP001", "name": "Thành", "email": "op@bk.edu.vn", "role": "OPERATOR"}

    schedule = schedule_service.generateSchedule("H1")
    item = dict(schedule[0])
    item["timeSlot"] = "14:00-15:00"
    res1 = client.post("/api/charging-schedule/approve", json={"schedule": [item]})
    assert res1.status_code == 200
    assert res1.get_json()["ok"] is True

    # Operator chỉnh sửa lại khung giờ cho chính item đó rồi lưu lại -> không nhân bản
    item["timeSlot"] = "16:00-17:00"
    res2 = client.post("/api/charging-schedule/approve", json={"schedule": [item]})
    assert res2.status_code == 200

    res_get = client.get("/api/hubs/H1/charging-schedule")
    assert res_get.status_code == 200
    payload = res_get.get_json()
    assert payload["ok"] is True
    assert len(payload["availablePorts"]) > 0
    matched = [r for r in payload["data"] if r["id"] == item["id"]]
    assert len(matched) == 1
    assert matched[0]["timeSlot"] == "16:00-17:00"

    res_del = client.delete(f"/api/charging-schedule/{item['id']}")
    assert res_del.status_code == 200
    assert res_del.get_json()["removed"] is True
    res_get2 = client.get("/api/hubs/H1/charging-schedule")
    assert all(r["id"] != item["id"] for r in res_get2.get_json()["data"])
