"""UC14 – Mô phỏng và phân tích kịch bản What-if (Submission 3, mục 2.12).

DEMO BẮT BUỘC – cô lập dữ liệu (NFR07): mô phỏng CHỈ được chạy trên bản sao
`db.snapshot()`, tuyệt đối không sửa db.HUBS / db.VEHICLES thật.
Cách chứng minh: chạy mô phỏng xong, số liệu dashboard UC8 không đổi.
"""
from data import mock_data as db
from services.errors import INVALID_PARAMETERS, ServiceError


def initVirtualEnvironment():
    """TODO(UC14): return db.snapshot()  – bản sao độc lập của dữ liệu hiện tại."""
    raise NotImplementedError("UC14 initVirtualEnvironment")


def validateParameters(params):
    """TODO(UC14): params: studentDemandPercent, availableEvPercent, weather... Sai -> INVALID_PARAMETERS."""
    raise NotImplementedError("UC14 validateParameters")


def calculateImpact(virtualData, params):
    """TODO(UC14): Tính trên virtualData: giờ thiếu xe cao điểm, số xe thiếu, Hub quá tải."""
    raise NotImplementedError("UC14 calculateImpact")


def generateReport(impact):
    """TODO(UC14): Trả dữ liệu cho biểu đồ Chart.js + khuyến nghị (Hình 21)."""
    raise NotImplementedError("UC14 generateReport")


def runSimulation(params):
    """TODO(UC14): validateParameters -> initVirtualEnvironment -> calculateImpact -> generateReport."""
    raise NotImplementedError("UC14 runSimulation")


def applyRecommendation(reportId):
    """TODO(UC14): Trả dữ liệu điền sẵn cho màn hình UC11 hoặc UC13."""
    raise NotImplementedError("UC14 applyRecommendation")
