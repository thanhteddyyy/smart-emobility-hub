"""UC13 – Xây dựng lịch sạc thông minh (Submission 3, mục 2.11)."""
from data import mock_data as db


def generateSchedule(hubId):
    """TODO(UC13): Xếp xe pin thấp / có lịch sử dụng gần lên trước, chia vào các cổng AVAILABLE theo khung giờ."""
    raise NotImplementedError("UC13 generateSchedule")


def validateSchedule(schedule):
    """TODO(UC13): Không trùng cổng trong cùng khung giờ, không dùng cổng OUT_OF_ORDER."""
    raise NotImplementedError("UC13 validateSchedule")


def editSchedule(schedule, changes):
    """TODO(UC13): Áp dụng chỉnh sửa của Operator rồi validateSchedule lại."""
    raise NotImplementedError("UC13 editSchedule")


def approveSchedule(operatorId, schedule):
    """TODO(UC13): Phê duyệt và gọi saveSchedule."""
    raise NotImplementedError("UC13 approveSchedule")


def saveSchedule(schedule):
    """TODO(UC13): Lưu lịch đã duyệt."""
    raise NotImplementedError("UC13 saveSchedule")
