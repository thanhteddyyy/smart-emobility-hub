// UC16 – cập nhật gần thời gian thực bằng cách gọi /api/state định kỳ (NFR02: ≤ 15 giây).
// Cách dùng trong HTML: gắn data-rt="đường.dẫn.tới.giá.trị", ví dụ
//   <span data-rt="hubs.H1.availableVehicles">7</span>
//   <span data-rt="network.availableVehicles">30</span>
// Màn hình cần xử lý riêng (vẽ lại bản đồ, bảng) thì nghe sự kiện:
//   document.addEventListener("ehub:state", (e) => { console.log(e.detail); });
(function () {
  const interval = (window.EHUB_POLL_INTERVAL_SECONDS || 5) * 1000;

  function pick(obj, path) {
    return path.split(".").reduce(function (o, k) { return o == null ? undefined : o[k]; }, obj);
  }

  async function refresh() {
    try {
      const res = await fetch("/api/state");
      const state = await res.json();
      document.querySelectorAll("[data-rt]").forEach(function (el) {
        const value = pick(state, el.dataset.rt);
        if (value !== undefined) el.textContent = value;
      });
      document.dispatchEvent(new CustomEvent("ehub:state", { detail: state }));
    } catch (e) {
      console.warn("Mất kết nối realtime:", e); // TODO(TV4): hiện cảnh báo mất kết nối (NFR05)
    }
  }

  setInterval(refresh, interval);
})();
