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
      if (!res.ok) throw new Error("HTTP " + res.status);
      const state = await res.json();
      document.querySelectorAll("[data-rt]").forEach(function (el) {
        const value = pick(state, el.dataset.rt);
        if (value !== undefined) el.textContent = value;
      });
      document.dispatchEvent(new CustomEvent("ehub:state", { detail: state }));
      const warning = document.getElementById("realtimeConnectionWarning");
      if (warning) warning.hidden = true;
    } catch (e) {
      console.warn("Mất kết nối realtime:", e);
      let warning = document.getElementById("realtimeConnectionWarning");
      if (!warning) {
        warning = document.createElement("div");
        warning.id = "realtimeConnectionWarning";
        warning.className = "alert-x danger";
        warning.setAttribute("role", "alert");
        warning.style.position = "fixed";
        warning.style.bottom = "1rem";
        warning.style.left = "50%";
        warning.style.transform = "translateX(-50%)";
        warning.style.zIndex = "9999";
        warning.textContent = "Mất kết nối realtime. Đang thử cập nhật lại...";
        document.body.appendChild(warning);
      }
      warning.hidden = false;
    }
  }

  setInterval(refresh, interval);
})();
