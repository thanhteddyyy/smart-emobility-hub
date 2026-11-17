"""AuditLog dùng chung (NFR11) – Submission 3, mục 2.15.7."""
from datetime import datetime

from data import mock_data as db


def record(actorId, action, targetId, details=""):
    """Đã làm: ghi một dòng nhật ký thao tác."""
    entry = {"id": f"LOG-{len(db.AUDIT_LOGS) + 1:04d}", "actorId": actorId, "action": action,
             "targetId": targetId, "details": details,
             "timestamp": datetime.now().isoformat(timespec="seconds")}
    with db.DATA_LOCK:
        db.AUDIT_LOGS.append(entry)
    return entry
