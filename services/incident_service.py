"""UC12 – Xử lý các sự cố (Submission 3, mục 2.10)."""
from data import mock_data as db
from services.errors import INCIDENT_NOT_FOUND, ServiceError


def getPrioritizedIncidents():
    """TODO(UC12): Sắp xếp HIGH -> MEDIUM -> LOW, sự cố chưa xử lý lên trước."""
    raise NotImplementedError("UC12 getPrioritizedIncidents")


def handlePauseResource(operatorId, incidentId, reason, fixingMethod):
    """TODO(UC12): Tạm ngưng tài nguyên liên quan, sự cố -> IN_PROGRESS, hủy các đặt chỗ bị ảnh hưởng."""
    raise NotImplementedError("UC12 handlePauseResource")


def completeIncident(operatorId, incidentId):
    """TODO(UC12): Sự cố -> RESOLVED, tài nguyên hoạt động lại."""
    raise NotImplementedError("UC12 completeIncident")


def isolateDisconnectedHub(hubId):
    """TODO(UC12): Hub mất kết nối: status -> OFFLINE, không nhận đặt chỗ mới (NFR05)."""
    raise NotImplementedError("UC12 isolateDisconnectedHub")
