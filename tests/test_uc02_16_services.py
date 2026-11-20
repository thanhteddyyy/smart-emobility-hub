"""Service tests for use cases UC2 through UC16.

UC15 is a frontend-only theme/language use case and has no service module.
Strict xfails document behavior that is explicitly still TODO in the services.
"""
from datetime import datetime, timedelta

import pytest

from data import mock_data as db
from services import (
    alert_service,
    booking_service,
    charging_service,
    dispatch_service,
    incident_service,
    monitor_service,
    realtime_service,
    schedule_service,
    simulation_service,
    status_service,
    trip_service,
)
from services.errors import (
    ACCESS_DENIED,
    BOOKING_NOT_FOUND,
    DISPATCH_CONFLICT,
    HUB_FULL,
    INVALID_PARAMETERS,
    NO_PORT_AVAILABLE,
    RESOURCE_NOT_FOUND,
    ServiceError,
)


def test_uc02_status_staleness_boundary():
    now = datetime(2026, 11, 19, 12, 0, 0)
    threshold = timedelta(seconds=60)

    assert not status_service.isStatusStale(
        (now - threshold).isoformat(), now=now
    )
    assert status_service.isStatusStale(
        (now - threshold - timedelta(seconds=1)).isoformat(), now=now
    )


def test_uc02_build_hub_status_counts_resources():
    hub = db.getHub("H1")

    result = status_service.buildHubStatus(hub)

    assert result["hubId"] == "H1"
    assert result["availableVehicles"] == sum(
        vehicle["status"] == "AVAILABLE" for vehicle in db.vehiclesOfHub("H1")
    )
    assert result["emptySpots"] == sum(
        spot["status"] == "FREE" for spot in db.spotsOfHub("H1")
    )
    assert result["availablePorts"] == sum(
        port["status"] == "AVAILABLE" for port in db.portsOfHub("H1")
    )


def test_uc02_missing_hub_raises_service_error():
    with pytest.raises(ServiceError) as error:
        status_service.getResourceStatus("HUB", "missing")

    assert error.value.code == RESOURCE_NOT_FOUND


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC2 vehicle status is TODO")
def test_uc02_build_vehicle_status_contract():
    vehicle = db.getVehicle("EB-201")

    result = status_service.buildVehicleStatus(vehicle)

    assert result["id"] == vehicle["id"]
    assert result["model"] == vehicle["model"]
    assert result["type"] == vehicle["type"]
    assert result["batteryLevel"] == vehicle["batteryLevel"]
    assert result["hubId"] == vehicle["hubId"]
    assert "isStale" in result


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC2 vehicle lookup is TODO")
def test_uc02_get_vehicle_status_contract():
    result = status_service.getResourceStatus("VEHICLE", "EB-201")

    assert result["id"] == "EB-201"


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC3 booking is TODO")
def test_uc03_book_vehicle_reserves_vehicle_and_creates_holding_booking():
    booking = booking_service.bookVehicle("2413148", "EB-201")

    assert db.getVehicle("EB-201")["status"] == "RESERVED"
    assert booking["userId"] == "2413148"
    assert booking["vehicleId"] == "EB-201"
    assert booking["status"] == "HOLDING"
    assert booking in db.BOOKINGS


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC3 booking is TODO")
def test_uc03_booking_same_vehicle_twice_returns_vehicle_conflict():
    booking_service.bookVehicle("2413148", "EB-201")

    with pytest.raises(ServiceError) as error:
        booking_service.bookVehicle("another-user", "EB-201")

    assert error.value.code == "VEHICLE_CONFLICT"


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC4 parking booking is TODO")
def test_uc04_book_parking_creates_holding_booking():
    booking = booking_service.bookParking("2413148", "H1", "18:00")

    assert booking["type"] == "PARKING"
    assert booking["hubId"] == "H1"
    assert booking["timeSlot"] == "18:00"
    assert booking["status"] == "HOLDING"


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC3/UC4 cancellation is TODO")
def test_uc04_cancel_booking_releases_reserved_resource():
    booking = {
        "id": "BK-TEST",
        "type": "VEHICLE",
        "userId": "2413148",
        "vehicleId": "EB-201",
        "hubId": "H1",
        "status": "HOLDING",
    }
    db.BOOKINGS.append(booking)
    db.getVehicle("EB-201")["status"] = "RESERVED"

    result = booking_service.cancelBooking("2413148", "BK-TEST")

    assert result["status"] == "CANCELLED"
    assert db.getVehicle("EB-201")["status"] == "AVAILABLE"


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC3 booking validity is TODO")
def test_uc03_expired_booking_is_not_valid():
    booking = {
        "status": "HOLDING",
        "expiresAt": (datetime.now() - timedelta(minutes=1)).isoformat(),
    }

    with pytest.raises(ServiceError) as error:
        booking_service.isBookingValid(booking)

    assert error.value.code == "HOLD_EXPIRED"


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="UC5 pickup confirmation is TODO")
def test_uc05_confirm_pickup_activates_booking_and_vehicle():
    db.BOOKINGS.append({
        "id": "BK-TEST",
        "type": "VEHICLE",
        "userId": "2413148",
        "vehicleId": "EB-201",
        "hubId": "H1",
        "status": "HOLDING",
        "expiresAt": (datetime.now() + timedelta(minutes=10)).isoformat(),
    })
    db.getVehicle("EB-201")["status"] = "RESERVED"

    result = trip_service.confirmPickup("2413148", "BK-TEST")

    assert result["status"] == "ACTIVE"
    assert db.getVehicle("EB-201")["status"] == "IN_USE"


def test_uc06_return_vehicle_completes_trip_and_occupies_spot():
    booking = {
        "id": "BK-ACTIVE",
        "type": "VEHICLE",
        "userId": "2413148",
        "vehicleId": "EB-201",
        "hubId": "H1",
        "status": "ACTIVE",
    }
    db.BOOKINGS.append(booking)
    db.getVehicle("EB-201")["status"] = "IN_USE"

    result = trip_service.returnVehicle("2413148", "BK-ACTIVE", "H2")

    assert result["booking"]["status"] == "COMPLETED"
    assert result["vehicle"]["status"] == "AVAILABLE"
    assert result["vehicle"]["hubId"] == "H2"
    assert result["parkingSpot"]["status"] == "OCCUPIED"


def test_uc06_return_vehicle_rejects_full_hub():
    db.BOOKINGS.append({
        "id": "BK-ACTIVE",
        "type": "VEHICLE",
        "userId": "2413148",
        "vehicleId": "EB-201",
        "hubId": "H1",
        "status": "ACTIVE",
    })
    for spot in db.spotsOfHub("H2"):
        spot["status"] = "OCCUPIED"

    with pytest.raises(ServiceError) as error:
        trip_service.returnVehicle("2413148", "BK-ACTIVE", "H2")

    assert error.value.code == HUB_FULL


def test_uc06_return_vehicle_rejects_booking_owned_by_another_user():
    with pytest.raises(ServiceError) as error:
        trip_service.returnVehicle("not-the-owner", "BK-MISSING", "H2")

    assert error.value.code == BOOKING_NOT_FOUND


def test_uc07_register_charging_reserves_available_port():
    registration = charging_service.registerCharging(
        "2413148", "H1", "H1-C01", "2026-11-20T09:00", 30
    )

    assert registration["portId"] == "H1-C01"
    assert registration["batteryLevel"] == 30
    assert registration["status"] == "ACTIVE"
    assert registration in db.CHARGING_REGISTRATIONS


def test_uc07_duplicate_port_and_slot_are_rejected():
    charging_service.registerCharging(
        "2413148", "H1", "H1-C01", "2026-11-20T09:00", 30
    )

    with pytest.raises(ServiceError) as error:
        charging_service.registerCharging(
            "another-user", "H1", "H1-C01", "2026-11-20T09:00", 40
        )

    assert error.value.code == NO_PORT_AVAILABLE


def test_uc07_invalid_battery_level_is_rejected():
    with pytest.raises(ServiceError) as error:
        charging_service.registerCharging(
            "2413148", "H1", "H1-C01", "2026-11-20T09:00", 101
        )

    assert error.value.code == INVALID_PARAMETERS


def test_uc07_suggest_nearest_hub_with_available_port():
    suggested_hub = charging_service.suggestNearestHubWithPort("H1")

    assert suggested_hub["id"] == "H5"


def test_uc08_operator_access_validation():
    monitor_service.validateOperatorAccess({"user": {"role": "OPERATOR"}})

    with pytest.raises(ServiceError) as error:
        monitor_service.validateOperatorAccess({"user": {"role": "STUDENT"}})

    assert error.value.code == ACCESS_DENIED


def test_uc08_overview_summarizes_seeded_network():
    overview = monitor_service.getNetworkOverview()

    assert overview["activeHubCount"] == len(db.HUBS)
    assert overview["totalVehicles"] == len(db.VEHICLES)
    assert overview["availableVehicles"] == sum(
        vehicle["status"] == "AVAILABLE" for vehicle in db.VEHICLES
    )
    assert len(overview["hubs"]) == len(db.HUBS)


def test_uc08_overview_filter_limits_hubs_by_area():
    overview = monitor_service.getNetworkOverview({"area": "Metro"})

    assert [hub["hubId"] for hub in overview["hubs"]] == ["H1"]


def test_uc09_get_hub_resources_returns_vehicles_and_ports():
    resources = alert_service.getHubResources("H1")

    assert resources["hub"]["id"] == "H1"
    assert resources["vehicles"] == db.vehiclesOfHub("H1")
    assert resources["chargingPorts"] == db.portsOfHub("H1")


def test_uc09_missing_hub_raises_service_error():
    with pytest.raises(ServiceError) as error:
        alert_service.getHubResources("missing")

    assert error.value.code == RESOURCE_NOT_FOUND


def test_uc10_critical_hub_load_creates_critical_alert():
    hub = db.getHub("H1")
    vehicles_at_hub = [
        vehicle for vehicle in db.VEHICLES if vehicle["hubId"] == "H1"
        and vehicle["status"] in ("AVAILABLE", "CHARGING")
    ]
    hub["parkingCapacity"] = len(vehicles_at_hub)
    db.HUBS[:] = [hub]

    alerts = alert_service.evaluateHubLoad()

    assert len(alerts) == 1
    assert alerts[0]["hubId"] == "H1"
    assert alerts[0]["severity"] == "CRITICAL"


def test_uc10_hubs_below_warning_threshold_produce_no_alerts():
    alerts = alert_service.evaluateHubLoad()

    assert alerts == []


def test_uc11_dispatch_data_contains_available_vehicles_and_free_spots():
    data = dispatch_service.getDispatchHubData("H1", "H2")

    assert data["Available vehicles"]
    assert all(vehicle["status"] == "AVAILABLE" for vehicle in data["Available vehicles"])
    assert all(spot["status"] == "FREE" for spot in data["Available parking spots"])


def test_uc11_process_dispatch_creates_order_and_audit_entry():
    order = dispatch_service.processDispatch("OP001", "H1", "H2", ["EB-201"])

    assert order["status"] == "PENDING"
    assert order["vehicleIds"] == ["EB-201"]
    assert order in db.DISPATCH_ORDERS
    assert db.AUDIT_LOGS[-1]["action"] == "CREATE_DISPATCH_ORDER"


def test_uc11_dispatch_rejects_vehicle_not_available_at_source():
    with pytest.raises(ServiceError) as error:
        dispatch_service.processDispatch("OP001", "H1", "H2", ["EB-203"])

    assert error.value.code == DISPATCH_CONFLICT


def test_uc11_cancel_dispatch_order_changes_status_and_logs_action():
    order = dispatch_service.processDispatch("OP001", "H1", "H2", ["EB-201"])

    cancelled = dispatch_service.cancelDispatchOrder("OP001", order["id"])

    assert cancelled["status"] == "CANCELLED"
    assert db.AUDIT_LOGS[-1]["action"] == "CANCEL_DISPATCH_ORDER"


def test_uc12_incidents_are_ordered_by_status_then_priority():
    incidents = incident_service.getPrioritizedIncidents()

    assert [incident["id"] for incident in incidents[:4]] == [
        "INC-001", "INC-004", "INC-002", "INC-006"
    ]


def test_uc12_handling_vehicle_incident_changes_resource_and_logs_action():
    incident = db.findById(db.INCIDENTS, "INC-003")
    vehicle = db.getVehicle(incident["resourceId"])
    vehicle["status"] = "AVAILABLE"

    result = incident_service.handlePauseResource(
        "OP001", incident["id"], "GPS issue", "Inspect vehicle"
    )

    assert result["status"] == "IN_PROGRESS"
    assert vehicle["status"] == "MAINTENANCE"
    assert db.AUDIT_LOGS[-1]["action"] == "HANDLE_INCIDENT"


def test_uc12_complete_incident_restores_charging_port():
    incident = db.findById(db.INCIDENTS, "INC-001")
    port = next(port for port in db.CHARGING_PORTS if port["id"] == incident["resourceId"])

    result = incident_service.completeIncident("OP001", incident["id"])

    assert result["status"] == "RESOLVED"
    assert port["status"] == "AVAILABLE"
    assert db.AUDIT_LOGS[-1]["action"] == "RESOLVE_INCIDENT"


def test_uc12_isolate_hub_marks_it_offline_and_cancels_related_booking():
    db.BOOKINGS.append({
        "id": "BK-H1",
        "hubId": "H1",
        "status": "HOLDING",
    })

    hub = incident_service.isolateDisconnectedHub("H1")

    assert hub["status"] == "OFFLINE"
    assert db.BOOKINGS[0]["status"] == "CANCELLED"
    assert db.AUDIT_LOGS[-1]["action"] == "ISOLATE_HUB"


def test_uc13_generate_schedule_uses_low_battery_vehicles_first():
    schedule = schedule_service.generateSchedule("H1")

    assert schedule
    assert schedule[0]["batteryLevel"] <= schedule[-1]["batteryLevel"]
    assert schedule_service.validateSchedule(schedule)


def test_uc13_validate_schedule_rejects_duplicate_port_and_slot():
    schedule = schedule_service.generateSchedule("H1")
    schedule[1]["portId"] = schedule[0]["portId"]
    schedule[1]["timeSlot"] = schedule[0]["timeSlot"]

    assert not schedule_service.validateSchedule(schedule)


def test_uc13_edit_schedule_applies_valid_changes():
    schedule = schedule_service.generateSchedule("H1")
    replacement_port = next(
        port["id"] for port in db.portsOfHub("H1")
        if port["status"] == "AVAILABLE" and port["id"] != schedule[0]["portId"]
    )

    edited = schedule_service.editSchedule(
        schedule,
        [{"id": schedule[0]["id"], "portId": replacement_port, "timeSlot": "SLOT-TEST"}],
    )

    assert edited[0]["portId"] == replacement_port
    assert edited[0]["timeSlot"] == "SLOT-TEST"
    assert schedule[0]["portId"] != replacement_port


def test_uc13_approve_schedule_persists_approved_registrations():
    schedule = schedule_service.generateSchedule("H1")

    approved = schedule_service.approveSchedule("OP001", schedule)

    assert approved
    assert all(item["status"] == "APPROVED" for item in approved)
    assert db.CHARGING_REGISTRATIONS == approved
    assert db.AUDIT_LOGS[-1]["action"] == "APPROVE_CHARGING_SCHEDULE"


def test_uc14_virtual_environment_is_an_isolated_snapshot():
    virtual_data = simulation_service.initVirtualEnvironment()
    initial_status = virtual_data["vehicles"][0]["status"]

    virtual_data["vehicles"][0]["status"] = "MAINTENANCE"

    assert db.VEHICLES[0]["status"] == initial_status


def test_uc14_invalid_simulation_parameters_raise_service_error():
    with pytest.raises(ServiceError) as error:
        simulation_service.validateParameters({})

    assert error.value.code == INVALID_PARAMETERS


def test_uc16_packet_validation_accepts_valid_vehicle_packet():
    packet = {
        "resourceType": "VEHICLE",
        "resourceId": "EB-201",
        "timestamp": "2026-11-20T08:00:00",
        "status": "IN_USE",
        "batteryLevel": 45,
    }

    assert realtime_service.validatePacket(packet)


@pytest.mark.parametrize(
    "packet",
    [
        None,
        {},
        {"resourceType": "UNKNOWN", "resourceId": "x", "timestamp": "2026-11-20T08:00:00", "status": "ACTIVE"},
        {"resourceType": "VEHICLE", "resourceId": "EB-201", "timestamp": "bad-date", "status": "IN_USE"},
        {"resourceType": "VEHICLE", "resourceId": "EB-201", "timestamp": "2026-11-20T08:00:00", "status": "IN_USE", "batteryLevel": 101},
    ],
)
def test_uc16_invalid_telemetry_packet_is_rejected(packet):
    with pytest.raises(ServiceError) as error:
        realtime_service.validatePacket(packet)

    assert error.value.code == INVALID_PARAMETERS


def test_uc16_newer_packet_updates_resource_status():
    packet = {
        "resourceType": "VEHICLE",
        "resourceId": "EB-201",
        "timestamp": "2026-11-20T08:00:00",
        "status": "IN_USE",
        "batteryLevel": 45,
    }

    result = realtime_service.receiveTelemetryPacket(packet)

    assert result["updated"] is True
    assert result["resource"]["status"] == "IN_USE"
    assert result["resource"]["batteryLevel"] == 45


def test_uc16_outdated_packet_is_logged_and_does_not_update_resource():
    realtime_service.PACKET_LOG.clear()
    vehicle = db.getVehicle("EB-201")
    previous_status = vehicle["status"]
    packet = {
        "resourceType": "VEHICLE",
        "resourceId": "EB-201",
        "timestamp": "2026-11-16T08:00:00",
        "status": "IN_USE",
    }

    result = realtime_service.receiveTelemetryPacket(packet)

    assert result == {
        "updated": False,
        "reason": "OUTDATED_PACKET",
        "resourceId": "EB-201",
    }
    assert vehicle["status"] == previous_status
    assert realtime_service.PACKET_LOG[-1]["packet"] == packet
    assert realtime_service.PACKET_LOG[-1]["reason"] == "OUTDATED_PACKET"
