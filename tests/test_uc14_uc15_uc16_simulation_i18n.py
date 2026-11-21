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
