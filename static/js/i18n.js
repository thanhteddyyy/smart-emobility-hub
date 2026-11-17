// UC15 – đổi ngôn ngữ VN/EN không tải lại trang.
// Cách dùng trong HTML:
//   <span data-i18n="search.title">Tìm Hub</span>            -> đổi nội dung chữ
//   <input data-i18n-placeholder="search.placeholder">        -> đổi placeholder
//   <button data-lang-set="en">EN</button>                    -> nút chuyển ngôn ngữ
// Từ điển: static/i18n/vi.json và en.json (TV5 quản lý danh sách key).
(function () {
  const KEY = "ehub-lang";
  const cache = {};

  async function loadDictionary(lang) {
    if (!cache[lang]) {
      const res = await fetch("/static/i18n/" + lang + ".json");
      cache[lang] = await res.json();
    }
    return cache[lang];
  }

  async function applyLanguage(lang) {
    const dict = await loadDictionary(lang);
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      if (dict[el.dataset.i18n]) el.textContent = dict[el.dataset.i18n];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      if (dict[el.dataset.i18nPlaceholder]) el.placeholder = dict[el.dataset.i18nPlaceholder];
    });
    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.langSet === lang);
    });
  }

  let saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  applyLanguage(saved || "vi");

  document.addEventListener("click", function (ev) {
    const btn = ev.target.closest("[data-lang-set]");
    if (!btn) return;
    applyLanguage(btn.dataset.langSet);
    try { localStorage.setItem(KEY, btn.dataset.langSet); } catch (e) {}
  });
  window.EHubI18n = { applyLanguage: applyLanguage };
})();
