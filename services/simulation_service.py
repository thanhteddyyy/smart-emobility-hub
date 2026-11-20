"""UC14 – Mô phỏng và phân tích kịch bản What-if (Submission 3, mục 2.12).

DEMO BẮT BUỘC – cô lập dữ liệu (NFR07): mô phỏng CHỈ được chạy trên bản sao
`db.snapshot()`, tuyệt đối không sửa db.HUBS / db.VEHICLES thật.
Cách chứng minh: chạy mô phỏng xong, số liệu dashboard UC8 không đổi.
"""
from data import mock_data as db
from services.errors import INVALID_PARAMETERS, ServiceError

_REPORTS = {}

_WEATHER_FACTORS = {
    "HEAVY_RAIN": (1.25, 5),
    "LIGHT_RAIN": (1.10, 2),
    "CLEAR": (1.00, 0),
    "EXTREME_HEAT": (1.15, 3),
}


def initVirtualEnvironment():
    """Trả bản sao độc lập của toàn bộ dữ liệu để cô lập mô phỏng (NFR07)."""
    return db.snapshot()


def validateParameters(params):
    """Kiểm tra tham số mô phỏng: studentDemandPercent, availableEvDelta, weather."""
    if not isinstance(params, dict) or not params:
        raise ServiceError(INVALID_PARAMETERS, "Thiếu tham số mô phỏng.")
    try:
        demandPct = int(params.get("studentDemandPercent", 20))
        evDelta = int(params.get("availableEvDelta", -15))
    except (TypeError, ValueError) as exc:
        raise ServiceError(INVALID_PARAMETERS, "Tham số số lượng phải là số nguyên hợp lệ.") from exc

    weather = (params.get("weather") or "HEAVY_RAIN").upper()
    timeFrame = (params.get("timeFrame") or "09:00-18:00")
    scenario = (params.get("scenario") or "STANDARD").upper()
    if not (-50 <= demandPct <= 100):
        raise ServiceError(INVALID_PARAMETERS, "Biến động nhu cầu phải trong khoảng -50% đến +100%.")
    if not (-50 <= evDelta <= 50):
        raise ServiceError(INVALID_PARAMETERS, "Biến động số xe sẵn sàng phải trong khoảng -50 đến +50.")
    if weather not in _WEATHER_FACTORS:
        raise ServiceError(INVALID_PARAMETERS, "Điều kiện thời tiết không hợp lệ.")

    return {
        "studentDemandPercent": demandPct,
        "availableEvDelta": evDelta,
        "weather": weather,
        "timeFrame": timeFrame,
        "scenario": scenario,
    }


def calculateImpact(virtualData, params):
    """Tính chuỗi cung/cầu 9 giờ trên bản sao virtualData mà không đụng dữ liệu thật."""
    vehicles = virtualData["vehicles"]
    hubs = virtualData["hubs"]
    spots = virtualData["parkingSpots"]

    baseAvailable = sum(1 for v in vehicles if v["status"] == "AVAILABLE")
    demandFactor, supplyPenalty = _WEATHER_FACTORS[params["weather"]]

    fullHours = [
        "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM",
        "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM",
    ]
    baseDemandCurve = [18, 26, 36, 46, 56, 48, 38, 30, 22]
    baseSupplyOffsets = [8, 5, 2, -2, -5, -3, 1, 4, 6]
    frame = params.get("timeFrame", "09:00-18:00")
    if frame == "06:00-12:00":
        hours = ["06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM"]
        demandCurve = [10, 16, 28, 44, 38, 24]
        supplyOffsets = [10, 8, 4, -1, 2, 5]
    elif frame == "12:00-18:00":
        hours = ["12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"]
        demandCurve = [56, 48, 38, 30, 22, 18]
        supplyOffsets = [-5, -3, 1, 4, 6, 8]
    else:
        hours = fullHours
        demandCurve = baseDemandCurve
        supplyOffsets = baseSupplyOffsets

    scenario = params.get("scenario", "STANDARD")
    scenarioFactor = {"HUB_FULL": 1.35, "WEATHER_ALERT": 1.20, "LOW_SUPPLY": 1.15}.get(scenario, 1.0)
    demandCurve = [int(round(val * scenarioFactor)) for val in demandCurve]

    demandMultiplier = (1.0 + params["studentDemandPercent"] / 100.0) * demandFactor
    effectiveSupplyBase = max(4, baseAvailable + params["availableEvDelta"] - supplyPenalty)

    demandSeries = [max(0, round(val * demandMultiplier)) for val in demandCurve]
    availableSeries = [max(0, effectiveSupplyBase + off) for off in supplyOffsets]
    gaps = [avail - dem for avail, dem in zip(availableSeries, demandSeries)]

    peakShortageIdx = gaps.index(min(gaps))
    maxDeficit = gaps[peakShortageIdx]

    hubMetrics = []
    for h in hubs:
        hVehicles = [v for v in vehicles if v["hubId"] == h["id"] and v["status"] == "AVAILABLE"]
        hSpots = [s for s in spots if s["hubId"] == h["id"]]
        occupied = sum(1 for s in hSpots if s["status"] == "OCCUPIED")
        usageRate = (occupied / len(hSpots)) if hSpots else 0.0
        hubMetrics.append({
            "hubId": h["id"],
            "name": h["name"],
            "availableCount": len(hVehicles),
            "usageRate": usageRate,
        })

    sourceHub = max(hubMetrics, key=lambda item: item["availableCount"], default={"hubId": "H3", "name": "KTX Khu B"})
    destCandidates = [item for item in hubMetrics if item["hubId"] != sourceHub["hubId"]] or hubMetrics
    destHub = max(destCandidates, key=lambda item: item["usageRate"], default={"hubId": "H1", "name": "Ga Metro ĐHQG"})

    return {
        "params": params,
        "hours": hours,
        "availableSeries": availableSeries,
        "demandSeries": demandSeries,
        "peakShortageIndex": peakShortageIdx,
        "peakShortageTime": hours[peakShortageIdx],
        "maxVehicleDeficit": maxDeficit,
        "sourceHub": sourceHub,
        "destHub": destHub,
    }


def generateReport(impact):
    """Tạo báo cáo kết quả mô phỏng cho Chart.js và lưu tạm phục vụ Apply to Dispatch."""
    reportId = f"SIM-{len(_REPORTS) + 1:03d}"
    deficit = impact["maxVehicleDeficit"]
    recommendedCount = min(5, max(2, abs(deficit) // 8)) if deficit < 0 else 0
    sourceHub = impact["sourceHub"]
    destHub = impact["destHub"]

    if deficit < 0:
        recText = (
            f"Pre-dispatch {recommendedCount} EVs from {sourceHub['name']} "
            f"to {destHub['name']} before 11:00 AM"
        )
    else:
        recText = "Supply meets projected demand across all hubs."

    report = {
        "reportId": reportId,
        "params": impact["params"],
        "hours": impact["hours"],
        "availableSeries": impact["availableSeries"],
        "demandSeries": impact["demandSeries"],
        "peakShortageIndex": impact["peakShortageIndex"],
        "peakShortageTime": impact["peakShortageTime"],
        "maxVehicleDeficit": deficit,
        "recommendationText": recText,
        "sourceHubId": sourceHub["hubId"],
        "destHubId": destHub["hubId"],
        "recommendedCount": recommendedCount,
    }
    _REPORTS[reportId] = report
    return report


def runSimulation(params):
    """Chạy mô phỏng What-if hoàn chỉnh trên bản sao dữ liệu độc lập."""
    normalized = validateParameters(params)
    virtualData = initVirtualEnvironment()
    impact = calculateImpact(virtualData, normalized)
    return generateReport(impact)


def applyRecommendation(reportId=None):
    """Trả dữ liệu gợi ý để điền sẵn cho màn hình Điều phối phương tiện (UC11)."""
    report = _REPORTS.get(reportId) if reportId else None
    if not report:
        report = runSimulation({"studentDemandPercent": 20, "availableEvDelta": -15, "weather": "HEAVY_RAIN"})
    return {
        "sourceHubId": report["sourceHubId"],
        "destHubId": report["destHubId"],
        "recommendedCount": report["recommendedCount"],
    }
