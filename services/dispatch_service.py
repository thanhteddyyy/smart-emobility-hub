"""UC11 – Điều phối phương tiện (Submission 3, mục 2.9)."""
from data import mock_data as db
from services.errors import DISPATCH_CONFLICT, HUB_FULL, ServiceError


def getDispatchHubData(sourceHubId, destHubId):
    """TODO(UC11): Trả số xe khả dụng ở Hub nguồn và số chỗ trống ở Hub đích."""
    raise NotImplementedError("UC11 getDispatchHubData")


def processDispatch(operatorId, sourceHubId, destHubId, vehicleIds):
    """TODO(UC11): Xe đang bận -> DISPATCH_CONFLICT; Hub đích không đủ chỗ -> HUB_FULL.
    Thành công: tạo lệnh trong db.DISPATCH_ORDERS, ghi AuditLog."""
    raise NotImplementedError("UC11 processDispatch")


def cancelDispatchOrder(operatorId, orderId):
    """TODO(UC11): Chỉ hủy được lệnh đang PENDING."""
    raise NotImplementedError("UC11 cancelDispatchOrder")
