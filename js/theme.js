(function () {
  const STORAGE_KEY = "lht-theme";
  const DEFAULT_MODE = "auto";

  function getSystemTheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function getEffectiveTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    const mode = ["auto", "light", "dark"].includes(saved) ? saved : DEFAULT_MODE;
    return mode === "auto" ? getSystemTheme() : mode;
  }

  function applyTheme(name) {
    document.documentElement.setAttribute("data-theme", name);
  }

  function setMode(mode) {
    localStorage.setItem(STORAGE_KEY, mode);
    const effective = mode === "auto" ? getSystemTheme() : mode;
    applyTheme(effective);

    const select = document.getElementById("theme-switcher");
    if (select) select.value = mode;
  }

  function init() {
    const saved = localStorage.getItem(STORAGE_KEY) || DEFAULT_MODE;
    applyTheme(getEffectiveTheme());

    const select = document.getElementById("theme-switcher");
    if (select) {
      select.value = saved;
      select.addEventListener("change", function () {
        setMode(select.value);
      });
    }

    // Re-evaluate when system preference changes while in auto mode
    const mql = window.matchMedia("(prefers-color-scheme: dark)");
    mql.addEventListener("change", function () {
      const currentMode = localStorage.getItem(STORAGE_KEY) || DEFAULT_MODE;
      if (currentMode === "auto") {
        applyTheme(getSystemTheme());
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
