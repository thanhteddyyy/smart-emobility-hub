"""Test mẫu cho UC1. Mỗi hàm test ứng với một test case trong Submission 3 (ghi mã TC trong docstring).
Chạy: pytest      TV4/TV5 viết thêm test_ucXX_*.py theo kiểu này."""
import pytest

import config
from data import mock_data as db
from services import search_service
from services.errors import INVALID_CRITERIA, LOCATION_UNAVAILABLE, ServiceError


def test_search_returns_hubs_sorted_by_distance():
    results = search_service.searchVehicleAndHub(config.DEFAULT_LOCATION, 2.0)
    assert results
    assert [r["distanceKm"] for r in results] == sorted(r["distanceKm"] for r in results)


def test_no_result_returns_empty_list():
    """TC_UC01_01 – AF3: không có kết quả phù hợp."""
    for vehicle in db.VEHICLES:
        vehicle["batteryLevel"] = 10
    results = search_service.searchVehicleAndHub(config.DEFAULT_LOCATION, 2.0,
                                                 searchType="VEHICLE", minBatteryLevel=90)
    assert results == []


def test_location_unavailable():
    """TC_UC01_02 – EX1: không xác định được vị trí tìm kiếm."""
    with pytest.raises(ServiceError) as e:
        search_service.resolveSearchLocation(None, None)
    assert e.value.code == LOCATION_UNAVAILABLE


@pytest.mark.parametrize("radiusKm", [0, -1, 999])
def test_invalid_radius(radiusKm):
    with pytest.raises(ServiceError) as e:
        search_service.searchVehicleAndHub(config.DEFAULT_LOCATION, radiusKm)
    assert e.value.code == INVALID_CRITERIA


def test_search_page_opens_without_login(client):
    """UC1 không bắt buộc đăng nhập."""
    assert client.get("/student/search").status_code == 200
