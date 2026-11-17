"""UC9 – Theo dõi tài nguyên, UC10 – Xem cảnh báo quá tải (Submission 3, mục 2.7, 2.8)."""
import config
from data import mock_data as db


def getHubResources(hubId):
    """TODO(UC9): Trả danh sách xe + cổng sạc của một Hub cho bảng Hình 16."""
    raise NotImplementedError("UC9 getHubResources")


def evaluateHubLoad():
    """TODO(UC10): Với mỗi Hub: usageRate >= config.OVERLOAD_CRITICAL_RATE -> mức CRITICAL,
    >= config.OVERLOAD_WARNING_RATE -> mức WARNING. Trả danh sách cảnh báo (Hình 17)."""
    raise NotImplementedError("UC10 evaluateHubLoad")
