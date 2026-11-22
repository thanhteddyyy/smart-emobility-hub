// UC15 – đổi ngôn ngữ VN/EN không tải lại trang.
// Cách dùng trong HTML:
//   <span data-i18n="search.title">Tìm Hub</span>            -> đổi nội dung chữ
//   <input data-i18n-placeholder="search.placeholder">        -> đổi placeholder
//   <button data-lang-set="en">EN</button>                    -> nút chuyển ngôn ngữ
// Từ điển: static/i18n/vi.json và en.json (TV5 quản lý danh sách key).
(function () {
  const KEY = "ehub-lang";
  const cache = {};
  let currentLang = "vi";
  let currentDict = {};

  async function loadDictionary(lang) {
    if (!cache[lang]) {
      const res = await fetch("/static/i18n/" + lang + ".json");
      cache[lang] = await res.json();
    }
    return cache[lang];
  }

  function t(key, fallback) {
    if (key && currentDict && Object.prototype.hasOwnProperty.call(currentDict, key) && currentDict[key] !== "") {
      return currentDict[key];
    }
    return fallback !== undefined ? fallback : key;
  }

  function getLang() {
    return currentLang;
  }

  function applyDomTranslations(dict) {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      const k = el.dataset.i18n;
      if (k && Object.prototype.hasOwnProperty.call(dict, k) && dict[k]) {
        el.textContent = dict[k];
      }
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      const k = el.dataset.i18nPlaceholder;
      if (k && Object.prototype.hasOwnProperty.call(dict, k) && dict[k]) {
        el.placeholder = dict[k];
      }
    });
    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      const k = el.dataset.i18nTitle;
      if (k && Object.prototype.hasOwnProperty.call(dict, k) && dict[k]) {
        el.title = dict[k];
        if (el.hasAttribute("aria-label")) {
          el.setAttribute("aria-label", dict[k]);
        }
      }
    });
  }

  async function applyLanguage(lang) {
    const targetLang = lang === "en" ? "en" : "vi";
    const dict = await loadDictionary(targetLang);
    currentLang = targetLang;
    currentDict = dict;
    document.documentElement.lang = targetLang;
    applyDomTranslations(dict);
    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.langSet === targetLang);
    });
    document.dispatchEvent(
      new CustomEvent("ehub:langchange", {
        detail: { lang: targetLang, dict: dict },
      })
    );
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
  window.EHubI18n = {
    applyLanguage: applyLanguage,
    t: t,
    getLang: getLang,
  };
})();
