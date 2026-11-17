"""DEMO BẮT BUỘC – race condition khi đặt xe (UC3).

Hai luồng cùng đặt MỘT xe ở cùng thời điểm. Kết quả đúng: đúng 1 thành công, 1 nhận VEHICLE_CONFLICT.
Chạy từ thư mục gốc:  python scripts/race_demo.py
(Chạy được sau khi TV4 hoàn thành booking_service.bookVehicle.)
"""
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data import mock_data as db                 # noqa: E402
from services import booking_service             # noqa: E402
from services.errors import ServiceError         # noqa: E402

VEHICLE_ID = next(v["id"] for v in db.VEHICLES if v["status"] == "AVAILABLE")
results = {}
barrier = threading.Barrier(2)   # giữ 2 luồng lại rồi thả cùng lúc


def tryBook(userId):
    barrier.wait()
    try:
        booking_service.bookVehicle(userId, VEHICLE_ID)
        results[userId] = "THÀNH CÔNG"
    except ServiceError as e:
        results[userId] = f"THẤT BẠI ({e.code})"
    except NotImplementedError:
        results[userId] = "bookVehicle chưa được hiện thực"


threads = [threading.Thread(target=tryBook, args=(uid,)) for uid in ("SV_A", "SV_B")]
[t.start() for t in threads]
[t.join() for t in threads]

print(f"Hai sinh viên cùng đặt xe {VEHICLE_ID}:")
for userId, outcome in results.items():
    print(f"  {userId}: {outcome}")
successCount = sum(o == "THÀNH CÔNG" for o in results.values())
print("=> ĐẠT: chỉ 1 người đặt được." if successCount == 1 else "=> CHƯA ĐẠT.")
