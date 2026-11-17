"""UC7 – Đăng ký sạc (Submission 3, mục 2.5)."""
from data import mock_data as db
from services.errors import NO_PORT_AVAILABLE, ServiceError


def registerCharging(userId, hubId, portId, timeSlot, batteryLevel):
    """TODO(UC7): Không còn cổng -> ServiceError(NO_PORT_AVAILABLE) + gợi ý Hub gần nhất còn cổng (Hình 12)."""
    raise NotImplementedError("UC7 registerCharging")


def suggestNearestHubWithPort(hubId):
    """TODO(UC7): Trả Hub gần hubId nhất còn cổng sạc AVAILABLE, hoặc None."""
    raise NotImplementedError("UC7 suggestNearestHubWithPort")
