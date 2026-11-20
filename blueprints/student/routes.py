"""Các màn hình mobile / responsive web của Sinh viên (UC1–UC7).

Mẫu chuẩn của một route: nhận yêu cầu -> gọi service -> render_template.
Route KHÔNG chứa logic nghiệp vụ; logic nằm trong services/.
"""
from datetime import datetime, timedelta
from math import asin, cos, radians, sin, sqrt

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

import config
from data import mock_data as db
from services import (
    booking_service,
    charging_service,
    search_service,
    status_service,
    trip_service,
)
from services.auth_service import loginRequired
from services.errors import ServiceError

bp = Blueprint("student", __name__)

CHARGING_TIME_SLOTS = [
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "14:00 - 15:00",
    "16:00 - 17:00",
]


def _distanceKm(lat1, lng1, lat2, lng2):
    dLat = radians(lat2 - lat1)
    dLng = radians(lng2 - lng1)
    a = sin(dLat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLng / 2) ** 2
    return round(2 * 6371 * asin(sqrt(a)), 2)


def _findUserVehicleBooking(userId, status, bookingId=None):
    if bookingId:
        found = next(
            (b for b in db.BOOKINGS if b["id"] == bookingId and b["userId"] == userId),
            None,
        )
        if found and (status is None or found.get("status") == status):
            return found
    for booking in reversed(db.BOOKINGS):
        if booking.get("userId") == userId and booking.get("type") == "VEHICLE" and booking.get("status") == status:
            return booking
    return None


# ---------- UC1 (Hình 1) ----------
@bp.route("/search")
def search():
    criteria = {
        "radiusKm": request.args.get("radiusKm", config.DEFAULT_RADIUS_KM, type=float),
        "vehicleType": request.args.get("vehicleType") or None,
        "minBatteryLevel": request.args.get("minBatteryLevel", 0, type=int),
    }
    results, mapView, error = [], None, None
    try:
        location = search_service.resolveSearchLocation(None, config.DEFAULT_LOCATION)
        results = search_service.searchVehicleAndHub(location, **criteria)
        mapView = search_service.displayResultsOnMap(results, location)
    except ServiceError as e:
        error = e
    return render_template(
        "student/search.html",
        criteria=criteria,
        results=results,
        mapView=mapView,
        error=error,
    )


# Fallback map tên trang -> (endpoint, cần đăng nhập?)
PAGES = {
    "resource": ("student.resource", False),
    "pickup": ("student.pickup", True),
    "ride": ("student.ride", True),
    "return": ("student.returnPage", True),
    "returned": ("student.returned", True),
    "charging": ("student.charging", True),
    "charging-review": ("student.chargingReview", True),
    "charging-suggest": ("student.chargingSuggest", True),
}


# ---------- UC2 - Chi tiết xe / Hub ----------
@bp.route("/resource")
def resource():
    hubId = request.args.get("hubId") or (db.HUBS[0]["id"] if db.HUBS else "H1")
    vehicleId = request.args.get("vehicleId")
    hubStatus, selectedVehicle, vehicles, error = None, None, [], None

    try:
        hubStatus = status_service.getResourceStatus("HUB", hubId)
        vehicles = [status_service.buildVehicleStatus(v) for v in db.vehiclesOfHub(hubId)]
        if vehicleId:
            selectedVehicle = status_service.getResourceStatus("VEHICLE", vehicleId)
        elif vehicles:
            selectedVehicle = next((v for v in vehicles if v["status"] == "AVAILABLE"), vehicles[0])
    except ServiceError as e:
        error = e

    isStale = bool(
        (hubStatus and hubStatus.get("isStale"))
        or (selectedVehicle and selectedVehicle.get("isStale"))
    )
    return render_template(
        "student/resource.html",
        hubStatus=hubStatus,
        selectedVehicle=selectedVehicle,
        vehicles=vehicles,
        allHubs=db.HUBS,
        isStale=isStale,
        error=error,
    )


# ---------- UC5 - Nhận xe (Hình 6) ----------
@bp.route("/pickup", methods=["GET", "POST"])
@loginRequired("STUDENT")
def pickup():
    user = session.get("user")
    error = None

    if request.method == "POST":
        action = request.form.get("action", "confirm")
        bookingId = request.form.get("bookingId")
        try:
            if action == "cancel":
                booking_service.cancelBooking(user["id"], bookingId)
                return redirect(url_for("student.search"))
            trip_service.confirmPickup(user["id"], bookingId)
            return redirect(url_for("student.ride", bookingId=bookingId))
        except ServiceError as e:
            error = e

    booking = _findUserVehicleBooking(user["id"], "HOLDING", request.args.get("bookingId"))
    vehicle = db.getVehicle(booking["vehicleId"]) if booking else None
    hub = db.getHub(booking["hubId"]) if booking else None
    activeBooking = _findUserVehicleBooking(user["id"], "ACTIVE")

    return render_template(
        "student/pickup.html",
        booking=booking,
        vehicle=vehicle,
        hub=hub,
        activeBooking=activeBooking,
        error=error,
    )


# ---------- UC5 - Đang đi (Hình 7) ----------
@bp.route("/ride")
@loginRequired("STUDENT")
def ride():
    user = session.get("user")
    booking = _findUserVehicleBooking(user["id"], "ACTIVE", request.args.get("bookingId"))
    pendingBooking = _findUserVehicleBooking(user["id"], "HOLDING")
    vehicle = db.getVehicle(booking["vehicleId"]) if booking else None
    hub = db.getHub(booking["hubId"]) if booking else None
    activeHubs = [h for h in db.HUBS if h.get("status") == "ACTIVE"]
    destHub = next((h for h in activeHubs if not hub or h["id"] != hub["id"]), hub)

    return render_template(
        "student/ride.html",
        booking=booking,
        pendingBooking=pendingBooking,
        vehicle=vehicle,
        hub=hub,
        destHub=destHub,
        activeHubs=activeHubs,
    )


# ---------- UC6 - Trả xe (Hình 8) ----------
@bp.route("/return", methods=["GET", "POST"])
@loginRequired("STUDENT")
def returnPage():
    user = session.get("user")
    error = None
    suggestedHub = None
    booking = _findUserVehicleBooking(user["id"], "ACTIVE", request.values.get("bookingId"))
    activeHubStatuses = [
        status_service.buildHubStatus(h) for h in db.HUBS if h.get("status") == "ACTIVE"
    ]

    if request.method == "POST":
        bookingId = request.form.get("bookingId") or (booking["id"] if booking else None)
        hubId = request.form.get("hubId")
        try:
            trip_service.returnVehicle(user["id"], bookingId, hubId)
            return redirect(url_for("student.returned", bookingId=bookingId, hubId=hubId))
        except ServiceError as e:
            error = e
            if e.code == "HUB_FULL":
                suggestedHub = next((h for h in activeHubStatuses if h["emptySpots"] > 0 and h["hubId"] != hubId), None)

    vehicle = db.getVehicle(booking["vehicleId"]) if booking else None
    selectedHubId = request.values.get("hubId") or (booking["hubId"] if booking else (activeHubStatuses[0]["hubId"] if activeHubStatuses else "H1"))
    hub = db.getHub(selectedHubId)

    return render_template(
        "student/return.html",
        booking=booking,
        vehicle=vehicle,
        hub=hub,
        activeHubs=activeHubStatuses,
        selectedHubId=selectedHubId,
        suggestedHub=suggestedHub,
        error=error,
    )


# ---------- UC6 - Trả xe thành công (Hình 9) ----------
@bp.route("/returned")
@loginRequired("STUDENT")
def returned():
    user = session.get("user")
    booking = _findUserVehicleBooking(user["id"], "COMPLETED", request.args.get("bookingId"))
    vehicle = db.getVehicle(booking["vehicleId"]) if booking else None
    hubId = request.args.get("hubId") or (vehicle["hubId"] if vehicle else None)
    hub = db.getHub(hubId) if hubId else None

    return render_template(
        "student/returned.html",
        booking=booking,
        vehicle=vehicle,
        hub=hub,
    )


# ---------- UC7 - Chọn khung giờ sạc (Hình 10) ----------
@bp.route("/charging")
@loginRequired("STUDENT")
def charging():
    user = session.get("user")
    activeHubs = [h for h in db.HUBS if h.get("status") == "ACTIVE"] or list(db.HUBS)
    hubId = request.args.get("hubId") or activeHubs[0]["id"]
    hub = db.getHub(hubId) or activeHubs[0]

    bookedPairs = {
        (r["portId"], r["timeSlot"])
        for r in db.CHARGING_REGISTRATIONS
        if r.get("status") in ("ACTIVE", "REGISTERED", "APPROVED")
    }
    availablePorts = [p for p in db.portsOfHub(hub["id"]) if p.get("status") == "AVAILABLE"]

    slots = []
    now = datetime.now()
    selectedDate = now.date()
    futureSlots = []
    for slotIndex, timeSlot in enumerate(CHARGING_TIME_SLOTS):
        startText = timeSlot.split(" - ", 1)[0]
        try:
            slotStart = datetime.strptime(f"{selectedDate.isoformat()} {startText}", "%Y-%m-%d %H:%M")
        except ValueError:
            slotStart = now
        if slotStart > now:
            futureSlots.append((timeSlot, slotStart))

    if not futureSlots:
        selectedDate = (now + timedelta(days=1)).date()
        for timeSlot in CHARGING_TIME_SLOTS:
            startText = timeSlot.split(" - ", 1)[0]
            slotStart = datetime.strptime(f"{selectedDate.isoformat()} {startText}", "%Y-%m-%d %H:%M")
            futureSlots.append((timeSlot, slotStart))

    for timeSlot, slotStart in futureSlots:
        isoTimeSlot = slotStart.isoformat(timespec="minutes")
        for port in availablePorts:
            if (port["id"], isoTimeSlot) not in bookedPairs:
                slots.append({
                    "id": f"{port['id']}|{isoTimeSlot}",
                    "portId": port["id"],
                    "time": timeSlot,
                    "selected": len(slots) == 0,
                })
                break

    activeBooking = _findUserVehicleBooking(user["id"], "ACTIVE")
    activeVehicle = db.getVehicle(activeBooking["vehicleId"]) if activeBooking else None
    currentDate = selectedDate.strftime("%d/%m/%Y")

    return render_template(
        "student/charging_slot.html",
        hub=hub,
        allHubs=activeHubs,
        slots=slots,
        currentDate=currentDate,
        activeVehicle=activeVehicle,
    )


# ---------- UC7 - Xem lại & xác nhận sạc (Hình 11) ----------
@bp.route("/charging-review", methods=["GET", "POST"])
@loginRequired("STUDENT")
def chargingReview():
    user = session.get("user")
    error = None
    registration = None

    slotParam = request.values.get("charging_slot", "")
    portId = request.values.get("portId", "")
    timeSlot = request.values.get("timeSlot", "")
    if slotParam and "|" in slotParam and not (portId and timeSlot):
        portId, timeSlot = slotParam.split("|", 1)

    hubId = request.values.get("hubId") or (db.HUBS[0]["id"] if db.HUBS else "H1")
    hub = db.getHub(hubId)
    if not portId:
        firstPort = next((p for p in db.portsOfHub(hubId) if p.get("status") == "AVAILABLE"), None)
        portId = firstPort["id"] if firstPort else ""
    if not timeSlot:
        timeSlot = CHARGING_TIME_SLOTS[0]

    activeBooking = _findUserVehicleBooking(user["id"], "ACTIVE")
    activeVehicle = db.getVehicle(activeBooking["vehicleId"]) if activeBooking else None
    vehicleId = request.values.get("vehicleId") or (activeVehicle["id"] if activeVehicle else "EV-PERSONAL")
    defaultBattery = activeVehicle["batteryLevel"] if activeVehicle else 35
    batteryLevel = request.values.get("batteryLevel", defaultBattery, type=int)

    if request.method == "POST":
        try:
            registration = charging_service.registerCharging(
                user["id"], hubId, portId, timeSlot, batteryLevel
            )
        except ServiceError as e:
            error = e

    return render_template(
        "student/charging_review.html",
        hub=hub,
        hubId=hubId,
        portId=portId,
        timeSlot=timeSlot,
        vehicleId=vehicleId,
        batteryLevel=batteryLevel,
        currentDate=datetime.now().strftime("%d/%m/%Y"),
        registration=registration,
        error=error,
    )


# ---------- UC7 - Gợi ý trạm sạc khẩn cấp (Hình 12) ----------
@bp.route("/charging-suggest")
@loginRequired("STUDENT")
def chargingSuggest():
    user = session.get("user")
    activeBooking = _findUserVehicleBooking(user["id"], "ACTIVE")
    activeVehicle = db.getVehicle(activeBooking["vehicleId"]) if activeBooking else None

    hubId = request.args.get("hubId") or (activeBooking["hubId"] if activeBooking else (db.HUBS[0]["id"] if db.HUBS else "H1"))
    originHub = db.getHub(hubId)
    suggestedHub = None
    availablePort = None
    distanceKm = None
    error = None

    try:
        suggestedHub = charging_service.suggestNearestHubWithPort(hubId)
        availablePort = next(
            (p for p in db.portsOfHub(suggestedHub["id"]) if p.get("status") == "AVAILABLE"),
            None,
        )
        if originHub and suggestedHub:
            distanceKm = _distanceKm(originHub["lat"], originHub["lng"], suggestedHub["lat"], suggestedHub["lng"])
    except ServiceError as e:
        error = e

    return render_template(
        "student/charging_suggest.html",
        originHub=originHub,
        suggestedHub=suggestedHub,
        availablePort=availablePort,
        distanceKm=distanceKm,
        vehicle=activeVehicle,
        error=error,
    )


@bp.route("/<page>")
def page(page):
    if page not in PAGES:
        abort(404)
    endpoint, _ = PAGES[page]
    return redirect(url_for(endpoint, **request.args))
