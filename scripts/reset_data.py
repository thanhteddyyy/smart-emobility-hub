"""Hỗ trợ kịch bản reset/demo theo dữ liệu seed."""
import argparse

parser = argparse.ArgumentParser(description="Hiển thị hướng dẫn reset dữ liệu demo.")
parser.add_argument("--scenario", choices=["default", "hub_full"], default="default")
args = parser.parse_args()

if args.scenario == "hub_full":
    print("Dùng kịch bản hub_full: khởi động server mới rồi demo đặt chỗ H1;")
    print("trong seed gốc H1 có chỗ trống; cần cập nhật trạng thái chỗ H1 qua /api/telemetry.")
else:
    print("Khởi động lại server (Ctrl+C rồi python app.py) để dữ liệu quay về data/seed.json.")
