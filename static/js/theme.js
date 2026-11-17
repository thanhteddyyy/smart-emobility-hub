// UC15 – đổi giao diện Sáng/Tối KHÔNG tải lại trang (NFR13), nên dữ liệu form giữ nguyên.
// Cách dùng trong HTML:  <button data-theme-set="dark">…</button>
(function () {
  const KEY = "ehub-theme";

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    document.documentElement.setAttribute("data-bs-theme", theme); // để Bootstrap đổi theo
    document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.themeSet === theme);
    });
  }

  function savePreference(theme) {
    try { localStorage.setItem(KEY, theme); }
    catch (e) { handleSaveError(e); }   // UC15 EX1: không lưu được vẫn giữ giao diện hiện tại
  }

  function handleSaveError(e) { console.warn("Không lưu được tùy chọn giao diện:", e); }

  let saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  applyTheme(saved || "light");

  document.addEventListener("click", function (ev) {
    const btn = ev.target.closest("[data-theme-set]");
    if (!btn) return;
    applyTheme(btn.dataset.themeSet);
    savePreference(btn.dataset.themeSet);
  });
  window.EHubTheme = { applyTheme: applyTheme };
})();
