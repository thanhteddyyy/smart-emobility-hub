// Chuyển đổi chế độ xem Web Desktop / App Mobile cho Cổng Sinh viên trên màn hình lớn (>= 900px).
// Trên màn hình nhỏ (< 900px) CSS tự động hiển thị giao diện App Mobile chuẩn Figma.
(function () {
  const KEY = "ehub-student-view";

  function applyView(mode) {
    const normalized = mode === "mobile" ? "mobile" : "web";
    document.documentElement.setAttribute("data-student-view", normalized);
    document.querySelectorAll("[data-view-set]").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.viewSet === normalized);
    });
    window.dispatchEvent(new CustomEvent("ehub:viewchange", { detail: { mode: normalized } }));
  }

  let saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  applyView(saved || "web");

  document.addEventListener("click", function (ev) {
    const btn = ev.target.closest("[data-view-set]");
    if (!btn) return;
    applyView(btn.dataset.viewSet);
    try { localStorage.setItem(KEY, btn.dataset.viewSet); } catch (e) {}
  });

  document.addEventListener("DOMContentLoaded", function () {
    applyView(document.documentElement.getAttribute("data-student-view") || "web");
  });

  window.EHubStudentView = {
    applyView: applyView,
    isDesktopWeb: function () {
      return window.innerWidth >= 900 && document.documentElement.getAttribute("data-student-view") !== "mobile";
    },
  };
})();

