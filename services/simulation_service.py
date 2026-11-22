"""UC14 – Mô phỏng và phân tích kịch bản What-if (Submission 3, mục 2.12).

DEMO BẮT BUỘC – cô lập dữ liệu (NFR07): mô phỏng CHỈ được chạy trên bản sao
`db.snapshot()`, tuyệt đối không sửa db.HUBS / db.VEHICLES thật.
Cách chứng minh: chạy mô phỏng xong, số liệu dashboard UC8 không đổi.
"""
from data import mock_data as db
from services.errors import INVALID_PARAMETERS, ServiceError

_REPORTS = {}

_WEATHER_FACTORS = {
    "HEAVY_RAIN": (1.22, 0.06),
    "LIGHT_RAIN": (1.10, 0.02),
    "CLEAR": (0.98, 0.00),
    "EXTREME_HEAT": (1.15, 0.04),
}

_VALID_TIME_FRAMES = ("09:00-18:00", "06:00-12:00", "12:00-18:00")

_SCENARIO_FACTORS = {
    "STANDARD": (1.00, 0.00),
    "HUB_FULL": (1.15, 0.02),
    "WEATHER_ALERT": (1.12, 0.05),
    "LOW_SUPPLY": (1.05, 0.12),
}


def initVirtualEnvironment():
    """Trả bản sao độc lập của toàn bộ dữ liệu để cô lập mô phỏng (NFR07)."""
    return db.snapshot()


def validateParameters(params):
    """Kiểm tra tham số mô phỏng: studentDemandPercent, availableEvDelta, weather, timeFrame, scenario."""
    if not isinstance(params, dict) or not params:
        raise ServiceError(INVALID_PARAMETERS, "Thiếu tham số mô phỏng.")
    try:
        demandPct = int(params.get("studentDemandPercent", 20))
        evDelta = int(params.get("availableEvDelta", -15))
    except (TypeError, ValueError) as exc:
        raise ServiceError(INVALID_PARAMETERS, "Tham số số lượng phải là số nguyên hợp lệ.") from exc

    weather = (params.get("weather") or "HEAVY_RAIN").upper()
    timeFrame = params.get("timeFrame") or "09:00-18:00"
    scenario = (params.get("scenario") or "STANDARD").upper()

    if not (-50 <= demandPct <= 100):
        raise ServiceError(INVALID_PARAMETERS, "Biến động nhu cầu phải trong khoảng -50% đến +100%.")
    if not (-100 <= evDelta <= 100):
        raise ServiceError(INVALID_PARAMETERS, "Biến động số xe sẵn sàng phải trong khoảng -100 đến +100.")
    if weather not in _WEATHER_FACTORS:
        raise ServiceError(INVALID_PARAMETERS, "Điều kiện thời tiết không hợp lệ.")
    if timeFrame not in _VALID_TIME_FRAMES:
        raise ServiceError(INVALID_PARAMETERS, "Khung giờ mô phỏng không hợp lệ.")
    if scenario not in _SCENARIO_FACTORS:
        raise ServiceError(INVALID_PARAMETERS, "Kịch bản mô phỏng không hợp lệ.")

    return {
        "studentDemandPercent": demandPct,
        "availableEvDelta": evDelta,
        "weather": weather,
        "timeFrame": timeFrame,
        "scenario": scenario,
    }


def _selectCurveProfile(timeFrame, weather, scenario):
    """Chọn nhãn giờ và đường cong tỷ trọng nhu cầu/cung biến thiên theo khung giờ, thời tiết và kịch bản."""
    if timeFrame == "06:00-12:00":
        hours = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00"]
        supplyRatios = [0.04, 0.02, -0.02, -0.04, 0.00, 0.03]
        byScenario = {
            "HUB_FULL": [0.50, 0.68, 0.80, 0.86, 0.90, 0.96],
            "WEATHER_ALERT": [0.44, 0.60, 0.78, 0.88, 0.95, 0.84],
            "LOW_SUPPLY": [0.48, 0.70, 0.90, 0.84, 0.74, 0.66],
        }
        byWeather = {
            "CLEAR": [0.36, 0.62, 0.86, 0.74, 0.60, 0.52],
            "LIGHT_RAIN": [0.42, 0.68, 0.82, 0.88, 0.72, 0.62],
            "HEAVY_RAIN": [0.48, 0.72, 0.86, 0.94, 0.80, 0.70],
            "EXTREME_HEAT": [0.40, 0.56, 0.72, 0.82, 0.92, 0.86],
        }
        demandRatios = byScenario.get(scenario) or byWeather[weather]
        return hours, demandRatios, supplyRatios

    if timeFrame == "12:00-18:00":
        hours = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        supplyRatios = [-0.04, -0.02, 0.01, 0.02, -0.01, -0.03]
        byScenario = {
            "HUB_FULL": [0.96, 0.86, 0.74, 0.70, 0.82, 0.88],
            "WEATHER_ALERT": [0.72, 0.78, 0.84, 0.90, 0.96, 0.82],
            "LOW_SUPPLY": [0.80, 0.92, 0.82, 0.72, 0.66, 0.60],
        }
        byWeather = {
            "CLEAR": [0.64, 0.56, 0.58, 0.68, 0.82, 0.88],
            "LIGHT_RAIN": [0.70, 0.64, 0.66, 0.78, 0.89, 0.80],
            "HEAVY_RAIN": [0.84, 0.93, 0.95, 0.82, 0.74, 0.66],
            "EXTREME_HEAT": [0.92, 0.88, 0.78, 0.70, 0.64, 0.58],
        }
        demandRatios = byScenario.get(scenario) or byWeather[weather]
        return hours, demandRatios, supplyRatios

    # Mặc định khung 9 giờ (08:00 - 16:00)
    hours = [
        "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00", "16:00",
    ]
    supplyRatios = [0.05, 0.03, 0.01, -0.02, -0.04, -0.03, 0.01, 0.02, 0.00]
    byScenario = {
        "HUB_FULL": [0.56, 0.68, 0.78, 0.88, 0.98, 0.86, 0.76, 0.70, 0.64],
        "WEATHER_ALERT": [0.46, 0.56, 0.64, 0.72, 0.78, 0.84, 0.90, 0.97, 0.82],
        "LOW_SUPPLY": [0.52, 0.68, 0.82, 0.92, 0.84, 0.76, 0.68, 0.62, 0.56],
    }
    byWeather = {
        "CLEAR": [0.44, 0.54, 0.62, 0.68, 0.64, 0.58, 0.68, 0.78, 0.87],
        "LIGHT_RAIN": [0.52, 0.74, 0.88, 0.76, 0.68, 0.62, 0.66, 0.72, 0.64],
        "HEAVY_RAIN": [0.48, 0.60, 0.70, 0.78, 0.84, 0.94, 0.82, 0.72, 0.60],
        "EXTREME_HEAT": [0.46, 0.58, 0.72, 0.84, 0.92, 0.82, 0.74, 0.66, 0.56],
    }
    demandRatios = byScenario.get(scenario) or byWeather[weather]
    return hours, demandRatios, supplyRatios


def calculateImpact(virtualData, params):
    """Tính chuỗi cung/cầu trên bản sao virtualData tương xứng quy mô đội xe hiện tại."""
    vehicles = virtualData["vehicles"]
    hubs = virtualData["hubs"]
    spots = virtualData["parkingSpots"]

    baseAvailable = max(10, sum(1 for v in vehicles if v["status"] == "AVAILABLE"))
    weatherFactor, weatherPenaltyRate = _WEATHER_FACTORS[params["weather"]]
    scenarioFactor, scenarioPenaltyRate = _SCENARIO_FACTORS[params["scenario"]]

    hours, demandRatios, supplyRatios = _selectCurveProfile(
        params.get("timeFrame", "09:00-18:00"),
        params["weather"],
        params.get("scenario", "STANDARD"),
    )

    demandMultiplier = (1.0 + params["studentDemandPercent"] / 100.0) * weatherFactor * scenarioFactor
    supplyPenalty = round(baseAvailable * (weatherPenaltyRate + scenarioPenaltyRate))
    effectiveSupplyBase = max(4, baseAvailable + params["availableEvDelta"] - supplyPenalty)

    demandSeries = [max(0, round(baseAvailable * ratio * demandMultiplier)) for ratio in demandRatios]
    availableSeries = [max(0, effectiveSupplyBase + round(baseAvailable * off)) for off in supplyRatios]
    deficits = [dem - avail for avail, dem in zip(availableSeries, demandSeries)]

    peakShortageIdx = deficits.index(max(deficits))
    maxDeficit = deficits[peakShortageIdx]

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
    recommendedCount = min(30, max(5, deficit // 4)) if deficit > 0 else 0
    sourceHub = impact["sourceHub"]
    destHub = impact["destHub"]

    if deficit > 0:
        recText = (
            f"Pre-dispatch {recommendedCount} EVs from {sourceHub['name']} "
            f"to {destHub['name']} before {impact['peakShortageTime']}"
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
        "sourceHubName": sourceHub["name"],
        "destHubId": destHub["hubId"],
        "destHubName": destHub["name"],
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
