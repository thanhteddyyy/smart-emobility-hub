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
      if (!state.ok) throw new Error("Invalid state");

      const studentWarning = document.getElementById("connectionWarning");
      if (studentWarning) studentWarning.hidden = true;
      const floatingWarning = document.getElementById("realtimeConnectionWarning");
      if (floatingWarning) floatingWarning.hidden = true;

      document.querySelectorAll("[data-rt]").forEach(function (el) {
        const value = pick(state, el.dataset.rt);
        if (value === undefined) return;
        const prefix = el.dataset.rtI18nPrefix;
        if (prefix) {
          const i18nKey = prefix + value;
          el.dataset.i18n = i18nKey;
          el.textContent = window.EHubI18n && window.EHubI18n.t
            ? window.EHubI18n.t(i18nKey, value)
            : value;
        } else {
          el.textContent = value;
        }
      });
      document.dispatchEvent(new CustomEvent("ehub:state", { detail: state }));
    } catch (e) {
      console.warn("Mất kết nối realtime:", e);
      const studentWarning = document.getElementById("connectionWarning");
      if (studentWarning) {
        studentWarning.hidden = false;
      } else {
        let floatingWarning = document.getElementById("realtimeConnectionWarning");
        if (!floatingWarning) {
          floatingWarning = document.createElement("div");
          floatingWarning.id = "realtimeConnectionWarning";
          floatingWarning.className = "alert-x danger";
          floatingWarning.setAttribute("role", "alert");
          floatingWarning.style.position = "fixed";
          floatingWarning.style.bottom = "1rem";
          floatingWarning.style.left = "50%";
          floatingWarning.style.transform = "translateX(-50%)";
          floatingWarning.style.zIndex = "9999";
          floatingWarning.dataset.i18n = "tv.connection";
          floatingWarning.textContent = window.EHubI18n && window.EHubI18n.t
            ? window.EHubI18n.t("tv.connection", "Mất kết nối realtime. Đang thử cập nhật lại...")
            : "Mất kết nối realtime. Đang thử cập nhật lại...";
          document.body.appendChild(floatingWarning);
        }
        floatingWarning.hidden = false;
      }
    }
  }

  setInterval(refresh, interval);
})();