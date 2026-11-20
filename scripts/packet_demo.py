"""Gửi một gói telemetry có timestamp cũ để demo PACKET_LOG trên Dashboard."""
import json
import sys
from urllib.request import Request, urlopen

baseUrl = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:5000"

packet = {
    "resourceType": "VEHICLE",
    "resourceId": "EB-201",
    "timestamp": "2020-01-01T08:00:00",
    "status": "IN_USE",
    "batteryLevel": 45,
}

request = Request(
    baseUrl + "/api/telemetry",
    data=json.dumps(packet).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urlopen(request, timeout=5) as response:
    result = json.loads(response.read().decode("utf-8"))

print(json.dumps(result, ensure_ascii=False, indent=2))
