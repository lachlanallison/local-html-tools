(function () {
  const CATEGORY_LABELS = {
    images: "Images & design",
    "text-data": "Text & data",
    developer: "Developer",
    productivity: "Productivity",
    education: "Education",
    "audio-video": "Audio & video",
    utilities: "Utilities",
    other: "Other",
  };

  const state = {
    data: null,
    query: "",
    category: "",
    limit: 12,
  };

  const els = {};
  let sentinelObs = null;

  function $(id) {
    return document.getElementById(id);
  }

  function formatAuthors(authors) {
    return authors
      .map((a) => {
        if (a.url) {
          const safe = escapeAttr(a.url);
          return `<span class="author"><a href="${safe}" target="_blank" rel="noopener noreferrer">${escapeHtml(a.name)}</a></span>`;
        }
        return `<span class="author">${escapeHtml(a.name)}</span>`;
      })
      .join(" &middot; ");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeAttr(s) {
    return escapeHtml(s).replace(/'/g, "&#39;");
  }

  function runtimeBadge(tool) {
    const r = tool.runtime || {};
    const parts = [];
    if (r.single_file) parts.push("single-file");
    if (r.offline === "yes") parts.push("offline OK");
    else if (r.offline === "partial") parts.push("partial offline");
    else if (r.offline === "no") parts.push("needs network");
    if (r.needs_network) parts.push("API/remote");
    return parts.length ? `<span class="badge-runtime">${parts.map(escapeHtml).join(" &middot; ")}</span>` : "";
  }

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function matches(tool) {
    const q = state.query.trim().toLowerCase();
    if (state.category && !(tool.categories || []).includes(state.category)) return false;
    if (!q) return true;
    const blob = [
      tool.name,
      tool.summary,
      (tool.tags || []).join(" "),
      (tool.authors || []).map((a) => a.name).join(" "),
    ]
      .join(" ")
      .toLowerCase();
    return blob.includes(q);
  }

  function loadMore() {
    state.limit += 12;
    renderList();
  }

  function observeSentinel() {
    if (sentinelObs) sentinelObs.disconnect();
    const sentinel = document.getElementById("scroll-sentinel");
    if (!sentinel) return;
    sentinelObs = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) loadMore();
    }, { rootMargin: "200px" });
    sentinelObs.observe(sentinel);
  }

  function renderList() {
    const grid = els.grid;
    const tools = (state.data.tools || []).filter(matches);
    if (!tools.length) {
      grid.innerHTML = `<p class="empty-state" role="status">No tools match your filters.</p>`;
      return;
    }
    const limit = state.limit || tools.length;
    const show = tools.slice(0, limit);
    const ghMark = `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.4.6.1.82-.26.82-.58 0-.28-.01-1.04-.02-2.04-3.34.72-4.04-1.61-4.04-1.61-.55-1.4-1.34-1.77-1.34-1.77-1.1-.75.08-.74.08-.74 1.22.09 1.86 1.25 1.86 1.25 1.08 1.85 2.83 1.32 3.52 1.01.11-.79.42-1.32.77-1.62-2.69-.31-5.53-1.35-5.53-6 0-1.33.47-2.41 1.24-3.26-.13-.31-.54-1.56.12-3.25 0 0 1.01-.32 3.3 1.24.96-.27 1.98-.4 3-.4s2.04.13 3 .4c2.29-1.56 3.3-1.24 3.3-1.24.66 1.69.25 2.94.12 3.25.77.85 1.24 1.93 1.24 3.26 0 4.66-2.84 5.69-5.54 5.99.44.38.83 1.13.83 2.27 0 1.64-.02 2.96-.02 3.36 0 .32.22.7.83.58C20.56 21.8 24 17.3 24 12 24 5.37 18.63 0 12 0z"/></svg>`;
    const extLink = `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M21 13v10H3V4h12v2H5v15h14v-8h2zm3-12H13l4 4-8 8 2 2 8-8 4 4V1z"/></svg>`;
    let html = show.map((tool) => {
      const detailUrl = escapeAttr(`tool/${tool.id}/`);
      const url = escapeAttr(tool.url);
      const source = tool.source_url ? escapeAttr(tool.source_url) : null;
      const cats = (tool.categories || [])
        .map((c) => `<span class="cat">${escapeHtml(CATEGORY_LABELS[c] || c)}</span>`)
        .join("");
      const runtime = runtimeBadge(tool);
      return `
        <article class="tool-card" data-id="${escapeAttr(tool.id)}">
          <div>
            <h2><a href="${detailUrl}">${escapeHtml(tool.name)}</a></h2>
            <p class="summary">${escapeHtml(tool.summary)}</p>
            <div class="meta-row">
              ${formatAuthors(tool.authors)}
              ${runtime ? `<span aria-hidden="true">&middot;</span>${runtime}` : ""}
            </div>
          </div>
          <div class="cats">${cats}</div>
          <div class="tool-actions">
            <a href="${detailUrl}" class="btn btn-secondary btn-small">Details</a>
            <a href="${url}" class="btn btn-primary btn-small" target="_blank" rel="noopener noreferrer">${extLink} Open</a>
            ${source ? `<a href="${source}" class="btn btn-secondary btn-small" target="_blank" rel="noopener noreferrer">${ghMark} Source</a>` : ""}
          </div>
        </article>`;
    }).join("");

    if (tools.length > limit) {
      html += '<div id="scroll-sentinel" class="scroll-sentinel"></div>';
    }

    grid.innerHTML = html;
    observeSentinel();
  }

  function injectJsonLd() {
    const base = state.data.meta?.site_url || window.location.origin;
    const baseSlash = base.endsWith("/") ? base : base + "/";
    const list = (state.data.tools || []).map((tool, i) => ({
      "@type": "ListItem",
      position: i + 1,
      url: baseSlash + "tool/" + tool.id + "/",
      name: tool.name,
    }));
    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "ItemList",
      name: state.data.meta?.title || "Local HTML Tools",
      description: state.data.meta?.description || "",
      url: baseSlash,
      numberOfItems: list.length,
      itemListElement: list,
    });
    document.head.appendChild(script);
  }

  function setMeta() {
    if (!state.data?.meta) return;
    const m = state.data.meta;
    document.title = m.title;
    const desc = document.querySelector('meta[name="description"]');
    if (desc && m.description) desc.setAttribute("content", m.description);
  }

  async function load() {
    els.grid = $("tool-grid");
    els.search = $("q");
    els.category = $("category");

    try {
      const res = await fetch("data/tools.json", { cache: "no-store" });
      if (!res.ok) throw new Error("Failed to load directory data");
      state.data = await res.json();
      shuffle(state.data.tools);
      setMeta();
      injectJsonLd();
    } catch (err) {
      const isFile = window.location.protocol === "file:";
      const hint = isFile
        ? "Opening <code>index.html</code> directly blocks <code>fetch()</code>. Run a tiny server instead: <code>python -m http.server 8000</code> then open <a href='http://127.0.0.1:8000/'>http://127.0.0.1:8000/</a>."
        : '<a href=".">Retry</a>';
      els.grid.innerHTML = `<p class="empty-state" role="alert">Unable to load directory data. ${hint}</p>`;
      if (typeof console !== "undefined") console.error(err);
      return;
    }

    els.search.addEventListener("input", () => {
      state.query = els.search.value;
      state.limit = 12;
      if (sentinelObs) sentinelObs.disconnect();
      renderList();
    });
    els.category.addEventListener("change", () => {
      state.category = els.category.value;
      state.limit = 12;
      if (sentinelObs) sentinelObs.disconnect();
      renderList();
    });

    renderList();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();

