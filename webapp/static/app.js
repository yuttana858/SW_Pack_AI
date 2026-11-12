"use strict";
// PACK AI web client. Vanilla JS, no build step. Talks to the JSON API in webapp/app.py.

const $ = (s, r = document) => r.querySelector(s);
const state = { token: null, me: null, config: null, plant: null, conversation: null, oidc: null };

const store = {
  get(k) { try { return sessionStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { v == null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v); } catch { /* storage blocked */ } },
};

// ---------- API ----------------------------------------------------------------------
async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  if (state.plant) headers["X-SWPack-Plant"] = state.plant;
  const res = await fetch(path, { ...opts, headers, body: opts.body ? JSON.stringify(opts.body) : undefined });
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 && !path.startsWith("/api/login")) { signOut(data.error || "Please sign in again."); throw new Error("unauthorized"); }
  if (!res.ok) throw new Error(data.error || data.detail || `Request failed (${res.status})`);
  return data;
}

// ---------- Markdown (safe subset: escape first, then format) ------------------------
function esc(s) { return s.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]); }
function inline(s) {
  return s.replace(/`([^`]+)`/g, "<code>$1</code>")
          .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
          .replace(/(^|[\s(])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
}
function markdown(src) {
  const lines = esc(src).split("\n"); const out = []; let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (/^```/.test(l)) { const buf = []; i++; while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]); i++; out.push(`<pre><code>${buf.join("\n")}</code></pre>`); continue; }
    if (/^#{1,3} /.test(l)) { const n = l.match(/^#+/)[0].length; out.push(`<h${n}>${inline(l.slice(n + 1))}</h${n}>`); i++; continue; }
    if (/^\|.*\|\s*$/.test(l)) {
      const rows = []; while (i < lines.length && /^\|.*\|\s*$/.test(lines[i])) rows.push(lines[i++]);
      const cells = r => r.trim().slice(1, -1).split("|").map(c => inline(c.trim()));
      const body = rows.filter(r => !/^\|[\s:|-]+\|\s*$/.test(r));
      out.push("<table><thead><tr>" + cells(body[0]).map(c => `<th>${c}</th>`).join("") + "</tr></thead><tbody>" +
        body.slice(1).map(r => "<tr>" + cells(r).map(c => `<td>${c}</td>`).join("") + "</tr>").join("") + "</tbody></table>");
      continue;
    }
    if (/^\s*([-*]|\d+\.) /.test(l)) {
      const ordered = /^\s*\d+\./.test(l); const items = [];
      while (i < lines.length && /^\s*([-*]|\d+\.) /.test(lines[i])) {
        let item = lines[i++].replace(/^\s*([-*]|\d+\.) /, "");
        while (i < lines.length && /^ {2,}\S/.test(lines[i]) && !/^\s*([-*]|\d+\.) /.test(lines[i])) item += " " + lines[i++].trim();
        items.push(item);
      }
      out.push(`<${ordered ? "ol" : "ul"}>` + items.map(x => `<li>${inline(x)}</li>`).join("") + `</${ordered ? "ol" : "ul"}>`);
      continue;
    }
    if (!l.trim()) { i++; continue; }
    const para = []; while (i < lines.length && lines[i].trim() && !/^(#{1,3} |```|\||\s*([-*]|\d+\.) )/.test(lines[i])) para.push(lines[i++]);
    out.push(`<p>${inline(para.join("<br>"))}</p>`);
  }
  return out.join("");
}

// ---------- Citations -----------------------------------------------------------------
const label = c => (c.heading && c.heading !== c.title ? `${c.title} › ${c.heading}` : c.title);
function renderAnswer(el, text, citations) {
  const order = new Map(); (citations || []).forEach((c, n) => order.set(c.id, { ...c, n: n + 1 }));
  let html = markdown(text);
  html = html.replace(/\[((?:kb|card|lib)\.[A-Za-z0-9_.:#/\-]+)\]/g, (m, id) => {
    const c = order.get(id);
    if (!c) return "";
    return `<button type="button" class="cite${c.found ? "" : " missing"}" data-chunk="${esc(c.chunk_id || id)}" title="${esc(c.found ? label(c) : `Not found: ${id}`)}">${c.n}</button>`;
  });
  el.innerHTML = html;
}

async function openSource(chunkId) {
  const panel = $("#source-panel");
  $("#src-title").textContent = "Loading…"; $("#src-meta").textContent = ""; $("#src-body").innerHTML = "";
  panel.hidden = false;
  try {
    const c = await api(`/api/chunk/${encodeURIComponent(chunkId)}`);
    $("#src-title").textContent = label(c);
    Object.assign($("#src-open-doc").dataset, { doc: c.doc_id || "", section: c.id || "" });
    $("#src-meta").textContent = `${c.kind === "card" ? "Data card" : "Corpus section"} · ${c.confidence} · ${c.status} · ${c.path}`;
    const cites = (c.citations || []).filter(x => x.url).map(x => `- [${x.id}] ${x.title} — ${x.url}`).join("\n");
    $("#src-body").innerHTML = markdown(c.text + (cites ? `\n\n**References**\n\n${cites}` : ""));
  } catch (e) { $("#src-title").textContent = "Source unavailable"; $("#src-body").textContent = e.message; }
}

// ---------- Thread --------------------------------------------------------------------
function addTurn(question, result) {
  $("#empty").hidden = true;
  const node = $("#tpl-turn").content.firstElementChild.cloneNode(true);
  $(".q", node).textContent = question;
  const ans = $(".answer", node);
  if (!result) { ans.innerHTML = '<p class="thinking">Working on it… searching the knowledge base and running calculators.</p>'; $(".feedback", node).hidden = true; }
  else fillTurn(node, result);
  $("#thread").appendChild(node);
  node.scrollIntoView({ block: "end", behavior: "smooth" });
  return node;
}

function fillTurn(node, r) {
  node.dataset.messageId = r.message_id || r.id;
  renderAnswer($(".answer", node), r.answer || (r.refusal ? "This request was declined." : "No answer."), r.citations);
  const warns = r.warnings || [];
  const w = $(".warnings", node);
  w.hidden = !warns.length;
  if (warns.length) w.innerHTML = "<strong>Check before relying on this answer</strong><ul>" + warns.map(x => `<li>${esc(x)}</li>`).join("") + "</ul>";
  const found = (r.citations || []).filter(c => c.found);
  const src = $(".sources", node); src.hidden = !found.length;
  $("ol", src).innerHTML = (r.citations || []).map(c => c.found
    ? `<li><a href="#" data-chunk="${esc(c.chunk_id)}">${esc(label(c))}</a>` +
      `<span class="tag ${c.status !== "approved" ? "draft" : ""}">${esc(c.status)}</span><span class="tag">${esc(c.confidence)}</span></li>`
    : `<li class="muted">${esc(c.id)} <span class="tag draft">not found</span></li>`).join("");
  const tools = r.tool_calls || [];
  const wk = $(".working", node); wk.hidden = !tools.length;
  $("summary", wk).textContent = `Working: ${tools.length} tool call${tools.length === 1 ? "" : "s"} · release ${r.release_id || ""}`;
  $("ul", wk).innerHTML = tools.map(t => `<li><strong>${esc(t.name)}</strong>${t.is_error ? ' <span class="tag draft">error</span>' : ""} <code>${esc(JSON.stringify(t.input))}</code></li>`).join("");
  $(".feedback", node).hidden = false;
  $(".correction-field", node).hidden = !state.me?.can_propose;
}

async function ask(question) {
  const btn = $("#btn-send"); btn.disabled = true;
  const node = addTurn(question, null);
  try {
    const effort = document.querySelector('input[name="effort"]:checked').value;
    const r = await api("/api/ask", { method: "POST", body: { question, conversation_id: state.conversation, effort } });
    state.conversation = r.conversation_id;
    fillTurn(node, r);
    loadConversations();
  } catch (e) {
    $(".answer", node).innerHTML = `<p class="error">${esc(e.message)}</p>`;
  } finally { btn.disabled = false; $("#question").focus(); }
}

async function openConversation(id) {
  const c = await api(`/api/conversations/${id}`);
  if (c.plant !== state.plant && c.plant) { state.plant = c.plant; $("#plant").value = c.plant; }
  state.conversation = id;
  $("#thread").querySelectorAll(".turn").forEach(n => n.remove());
  $("#empty").hidden = c.messages.length > 0;
  c.messages.forEach(m => addTurn(m.question, m));
  highlightConversation();
  showChat();
}

function newConversation() {
  state.conversation = null;
  $("#thread").querySelectorAll(".turn").forEach(n => n.remove());
  $("#empty").hidden = false; highlightConversation(); showChat(); $("#question").focus();
}

async function loadConversations() {
  const { conversations } = await api("/api/conversations");
  $("#conv-list").innerHTML = conversations.map(c =>
    `<li><button data-conv="${esc(c.id)}" title="${esc(c.title)}">${esc(c.title)}${c.plant ? `<span class="plant-tag">${esc(c.plant)}</span>` : ""}</button></li>`).join("");
  highlightConversation();
}
function highlightConversation() {
  document.querySelectorAll("#conv-list button").forEach(b => b.setAttribute("aria-current", String(b.dataset.conv === state.conversation)));
}

// ---------- Feedback & review --------------------------------------------------------
async function sendFeedback(node, rating, comment, correction) {
  const status = $(".fb-status", node);
  try {
    const r = await api("/api/feedback", { method: "POST", body: { message_id: node.dataset.messageId, rating, comment: comment || null, correction: correction || null } });
    status.textContent = r.proposal_id ? "Thanks — correction sent to the review queue." : "Thanks for the feedback.";
    node.querySelectorAll(".fb").forEach(b => b.setAttribute("aria-pressed", String((rating === 1) === b.classList.contains("up"))));
    if (r.proposal_id) refreshReviewCount();
  } catch (e) { status.textContent = e.message; }
}

function canReview() { return state.me && (state.me.roles.includes("steward") || state.me.roles.includes("plant-admin")); }

async function refreshReviewCount() {
  if (!canReview()) return;
  const { proposals } = await api("/api/proposals?status=open");
  $("#review-count").textContent = proposals.length || "";
}

async function showReview() {
  setView("review");
  const { proposals } = await api("/api/proposals?status=open");
  $("#proposal-list").innerHTML = proposals.length ? proposals.map(p => `
    <li class="proposal" data-id="${esc(p.id)}">
      <div class="muted small">${esc(p.kind)} · plant ${esc(p.plant || "—")} · by ${esc(p.created_by)} · ${new Date(p.created * 1000).toLocaleString()}</div>
      <div><span class="lbl">Question</span><blockquote>${esc(p.body.question || "")}</blockquote></div>
      <div><span class="lbl">Answer given</span><blockquote>${esc(p.body.answer || "")}</blockquote></div>
      <div><span class="lbl">Proposed correction</span><blockquote class="correction">${esc(p.body.correction || "")}</blockquote></div>
      ${p.body.comment ? `<div><span class="lbl">Comment</span><blockquote>${esc(p.body.comment)}</blockquote></div>` : ""}
      ${(p.body.cited_chunks || []).length ? `<div class="small muted">Cited: ${p.body.cited_chunks.map(esc).join(", ")}</div>` : ""}
      <label class="small">Decision note <textarea rows="2" name="note"></textarea></label>
      <div class="row"><button class="primary" data-decide="accepted">Accept</button><button class="ghost" data-decide="rejected">Reject</button></div>
    </li>`).join("") : '<li class="muted">No open proposals.</li>';
}

function showChat() { setView("chat"); }

// ---------- Views (top menu) ------------------------------------------------------------
function setView(view) {
  state.view = view;
  $("#chat-view").hidden = view !== "chat";
  $("#kb-view").hidden = view !== "kb";
  $("#review-view").hidden = view !== "review";
  $("#app").classList.toggle("no-sidebar", view !== "chat");
  document.querySelectorAll(".topnav [data-view]").forEach(b => { if (b.dataset.view === view) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current"); });
  if (view === "kb" && !state.kbLoaded) loadKB();
}

// ---------- Knowledge base browser ---------------------------------------------------------
const KB_GROUPS = {
  terminology: "Glossary", materials: "Materials & board grades", performance: "Strength & performance",
  dimensional: "Dimensions & tolerances", styles: "Box & carton styles", manufacturing: "Manufacturing & machines",
  testing: "Testing & standards", cushioning: "Cushioning", logistics: "Pallets & logistics", printing: "Printing",
  sustainability: "Sustainability & regulations", standards: "Freight rules (Item 222 / Rule 41)",
  reference: "Units & conversions", library: "Engineering library (data cards)", agent: "How SWIS answers",
};
const KB_ORDER = Object.keys(KB_GROUPS);
const RECORD_LABEL = { formula: "Formula", flute_profile: "Flute", grade_table: "Grade table", factor_set: "Strength factors",
  box_style: "Box style", tolerance_spec: "Tolerances", allowance_table: "Allowances", board_material: "Board", machine_spec: "Machine", plant: "Plant" };

function statusTag(status, confidence) {
  return `<span class="tag ${status !== "approved" ? "draft" : ""}">${esc(status || "")}</span>` + (confidence ? `<span class="tag">${esc(confidence)}</span>` : "");
}

async function loadKB() {
  const { documents } = await api("/api/kb/documents");
  state.kbLoaded = true; state.kbDocs = documents;
  const groups = {};
  documents.forEach(d => (groups[d.group] = groups[d.group] || []).push(d));
  const keys = Object.keys(groups).sort((a, b) => (KB_ORDER.indexOf(a) + 1 || 99) - (KB_ORDER.indexOf(b) + 1 || 99));
  $("#kb-count").textContent = `${documents.length} documents · ${documents.reduce((n, d) => n + d.sections, 0)} sections`;
  $("#kb-tree").innerHTML = keys.map(g => `
    <details${g === "library" ? "" : ""}>
      <summary>${esc(KB_GROUPS[g] || g)}<span class="n">${groups[g].length}</span></summary>
      <ul>${groups[g].map(d => `<li><button data-doc="${esc(d.id)}">${d.record_type ? `<span class="muted small">${esc(RECORD_LABEL[d.record_type] || d.record_type)} · </span>` : ""}${esc(d.title)}</button></li>`).join("")}</ul>
    </details>`).join("");
}

async function openDoc(docId, sectionId) {
  setView("kb");
  const art = $("#kb-doc");
  art.innerHTML = '<p class="muted">Loading…</p>';
  document.querySelectorAll("#kb-tree [data-doc]").forEach(b => b.setAttribute("aria-current", String(b.dataset.doc === docId)));
  try {
    const d = await api(`/api/kb/documents/${encodeURIComponent(docId)}`);
    const showToc = d.sections.length > 2;
    art.innerHTML = `
      <h1>${esc(d.title)}</h1>
      <div class="meta">${statusTag(d.status, d.confidence)}<span class="tag">${esc(d.kind === "card" ? "data card" : "reference document")}</span>${(d.material_family || []).map(f => `<span class="tag">${esc(f)}</span>`).join("")}</div>
      ${showToc ? `<nav class="toc" aria-label="Sections"><strong>Sections</strong><ol>${d.sections.map(x => `<li><a href="#" data-section="${esc(x.id)}">${esc(x.heading)}</a></li>`).join("")}</ol></nav>` : ""}
      ${d.sections.map(x => `<section class="part md" id="sec-${esc(x.id)}">${markdown(x.text.replace(/^# .*\n+/, ""))}</section>`).join("")}
      ${d.references.length ? `<section class="part refs"><h2>References</h2><ul>${d.references.map(r => `<li>[${esc(r.id)}] ${esc(r.title)}${r.url ? ` — <a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.url)}</a>` : ""}</li>`).join("")}</ul></section>` : ""}
      <p class="muted small">Source file: <code>${esc(d.path)}</code></p>`;
    art.scrollTop = 0;
    if (sectionId) scrollToSection(sectionId);
  } catch (e) { art.innerHTML = `<p class="error">${esc(e.message)}</p>`; }
}

function scrollToSection(sectionId) {
  const el = document.getElementById(`sec-${sectionId}`);
  if (!el) return;
  document.querySelectorAll("#kb-doc .part.hit").forEach(x => x.classList.remove("hit"));
  el.classList.add("hit"); el.scrollIntoView({ block: "start" });
}

let kbTimer = null;
function kbSearch(q) {
  clearTimeout(kbTimer);
  kbTimer = setTimeout(async () => {
    if (!q.trim()) { $("#kb-tree").hidden = false; $("#kb-results")?.remove(); return; }
    const { results } = await api(`/api/kb/search?q=${encodeURIComponent(q)}&k=20`);
    $("#kb-tree").hidden = true;
    let ul = $("#kb-results");
    if (!ul) { ul = document.createElement("ul"); ul.id = "kb-results"; ul.className = "kb-results"; $("#kb-tree").after(ul); }
    ul.innerHTML = results.length ? results.map(r => `<li><button data-doc="${esc(r.doc_id || "")}" data-section="${esc(r.id)}">
        <span class="h">${esc(r.heading)}</span><span class="s">${esc(r.title)}</span></button></li>`).join("")
      : '<li class="muted small">No matches.</li>';
  }, 250);
}

// ---------- Theme & user menu ----------------------------------------------------------------
function applyTheme(theme) {
  const t = theme === "light" || theme === "dark" ? theme : "system";
  if (t === "system") delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = t;
  try { localStorage.setItem("swpack_theme", t); } catch { /* storage blocked */ }
  document.querySelectorAll('input[name="theme"]').forEach(r => { r.checked = r.value === t; });
}
try { applyTheme(localStorage.getItem("swpack_theme")); } catch { /* storage blocked */ }

function toggleUserMenu(open) {
  const pop = $("#user-pop"), btn = $("#btn-user");
  const show = open ?? pop.hidden;
  pop.hidden = !show; btn.setAttribute("aria-expanded", String(show));
}

// ---------- Sign-in ------------------------------------------------------------------
async function signedIn() {
  state.me = await api("/api/me");
  $("#signin").hidden = true; $("#app").hidden = false;
  const roles = state.me.roles.filter(r => r !== "viewer").join(", ") || "viewer";
  $("#user-name").textContent = state.me.name;
  $("#pop-name").textContent = state.me.name; $("#pop-roles").textContent = roles;
  api("/api/prefs").then(p => applyTheme(p.theme)).catch(() => {});
  const badge = $("#mode-badge");
  badge.textContent = state.me.responder === "assistant" ? "AI assistant" : "Search-only mode";
  badge.className = `badge ${state.me.responder}`;
  $("#release").textContent = state.me.release_id || "";
  const plants = state.me.plants;
  $("#plant").innerHTML = plants.length ? plants.map(p => `<option>${esc(p)}</option>`).join("") : '<option value="">Library only</option>';
  $("#plant").disabled = plants.length < 2;
  state.plant = plants[0] || null;
  $("#nav-review").hidden = !canReview();
  state.kbLoaded = false; setView("chat");
  await loadConversations(); refreshReviewCount();
}

function signOut(message) {
  state.token = null; state.me = null; store.set("swpack_token", null);
  if (state.oidc && state.config?.auth.mode === "oidc") { state.oidc.removeUser(); }
  $("#app").hidden = true; $("#signin").hidden = false;
  $("#signin-error").textContent = message || "";
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script"); s.src = src; s.onload = resolve; s.onerror = reject; document.head.appendChild(s);
  });
}

async function initAuth() {
  state.config = await (await fetch("/api/config")).json();
  const a = state.config.auth;
  const frag = new URLSearchParams(location.hash.slice(1));
  if (frag.has("session") || frag.has("error")) history.replaceState({}, "", "/");   // never leave tokens in the address bar
  if (a.mode === "password") {
    $("#signin-password").hidden = false;
    const saved = store.get("swpack_token");
    if (saved) { state.token = saved; try { return await signedIn(); } catch { store.set("swpack_token", null); } }
    $("#signin").hidden = false;
    $("#username").focus();
    return;
  }
  if (a.mode === "github") {
    $("#signin-github").hidden = false;
    $("#github-org-note").textContent = a.org ? `Members of the ${a.org} GitHub organization` : "Approved GitHub accounts only";
    if (frag.get("error")) $("#signin-error").textContent = frag.get("error");
    const t = frag.get("session") || store.get("swpack_token");
    if (t) { state.token = t; store.set("swpack_token", t); try { return await signedIn(); } catch { store.set("swpack_token", null); } }
    $("#signin").hidden = false;
    return;
  }
  if (a.mode === "dev") {
    $("#signin-dev").hidden = false;
    $("#persona").innerHTML = Object.entries(a.personas).map(([k, p]) => `<option value="${esc(k)}">${esc(p.name)} (${esc(p.roles.join(", "))})</option>`).join("");
    const saved = store.get("swpack_token");
    if (saved) { state.token = saved; try { return await signedIn(); } catch { /* fall through to sign-in */ } }
    $("#signin").hidden = false;
    return;
  }
  // OIDC: Authorization Code + PKCE via oidc-client-ts, loaded only in this mode
  await loadScript("https://cdn.jsdelivr.net/npm/oidc-client-ts@3.1.0/dist/browser/oidc-client-ts.min.js")
    .catch(() => { throw new Error("Could not load the sign-in library. Check the network, or self-host oidc-client-ts in /static."); });
  state.oidc = new oidc.UserManager({ authority: a.authority, client_id: a.client_id, redirect_uri: location.origin + "/",
    post_logout_redirect_uri: location.origin + "/", response_type: "code", scope: a.scopes, automaticSilentRenew: true });
  $("#signin-oidc").hidden = false;
  if (new URLSearchParams(location.search).has("code")) {
    await state.oidc.signinRedirectCallback(); history.replaceState({}, "", "/");
  }
  const user = await state.oidc.getUser();
  if (user && !user.expired) { state.token = user.access_token || user.id_token; return signedIn(); }
  $("#signin").hidden = false;
}

// ---------- Wiring -------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  $("#btn-dev").onclick = async () => {
    try {
      const { token } = await api("/api/dev/login", { method: "POST", body: { persona: $("#persona").value } });
      state.token = token; store.set("swpack_token", token); await signedIn();
    } catch (e) { $("#signin-error").textContent = e.message; }
  };
  $("#btn-oidc").onclick = () => state.oidc.signinRedirect();
  $("#signin-password").onsubmit = async e => {
    e.preventDefault();
    const btn = $("#btn-login"); btn.disabled = true; $("#signin-error").textContent = "";
    try {
      const { token } = await api("/api/login", { method: "POST", body: { username: $("#username").value, password: $("#password").value } });
      $("#password").value = "";
      state.token = token; store.set("swpack_token", token); await signedIn();
    } catch (err) { $("#signin-error").textContent = err.message; }
    finally { btn.disabled = false; }
  };
  $("#btn-signout").onclick = () => signOut();
  $("#composer").onsubmit = e => { e.preventDefault(); const q = $("#question").value.trim(); if (!q) return; $("#question").value = ""; ask(q); };
  $("#question").addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("#composer").requestSubmit(); } });
  document.querySelectorAll(".example").forEach(b => b.onclick = () => ask(b.textContent));
  const closeMenu = () => $("#sidebar").classList.remove("open");
  $("#btn-new").onclick = () => { closeMenu(); newConversation(); };
  document.querySelectorAll(".topnav [data-view]").forEach(b => b.onclick = () => {
    closeMenu();
    if (b.dataset.view === "review") showReview(); else setView(b.dataset.view);
  });
  $("#btn-user").onclick = e => { e.stopPropagation(); toggleUserMenu(); };
  document.addEventListener("click", e => { if (!e.target.closest(".user-menu")) toggleUserMenu(false); });
  document.querySelectorAll('input[name="theme"]').forEach(r => r.onchange = () => {
    applyTheme(r.value);
    api("/api/prefs", { method: "PUT", body: { theme: r.value } }).catch(() => {});
  });
  $("#kb-q").addEventListener("input", e => kbSearch(e.target.value));
  $("#src-open-doc").onclick = e => { e.preventDefault(); const d = e.currentTarget.dataset; $("#source-panel").hidden = true; if (d.doc) openDoc(d.doc, d.section); };
  $("#btn-close-src").onclick = () => { $("#source-panel").hidden = true; };
  $("#btn-menu").onclick = () => $("#sidebar").classList.toggle("open");
  $("#plant").onchange = e => { state.plant = e.target.value || null; newConversation(); };
  document.addEventListener("keydown", e => { if (e.key === "Escape") { $("#source-panel").hidden = true; toggleUserMenu(false); } });

  document.body.addEventListener("click", async e => {
    const docBtn = e.target.closest("[data-doc]");
    if (docBtn && docBtn.dataset.doc) { e.preventDefault(); openDoc(docBtn.dataset.doc, docBtn.dataset.section); return; }
    const secLink = e.target.closest("#kb-doc [data-section]");
    if (secLink) { e.preventDefault(); scrollToSection(secLink.dataset.section); return; }
    const cite = e.target.closest("[data-chunk]");
    if (cite) { e.preventDefault(); openSource(cite.dataset.chunk); return; }
    const conv = e.target.closest("[data-conv]");
    if (conv) { $("#sidebar").classList.remove("open"); openConversation(conv.dataset.conv); return; }
    const turn = e.target.closest(".turn");
    if (turn && e.target.closest(".fb.up")) return sendFeedback(turn, 1);
    if (turn && e.target.closest(".fb.down")) { $(".fb-form", turn).hidden = false; return; }
    if (turn && e.target.closest(".fb-form .cancel")) { $(".fb-form", turn).hidden = true; return; }
    const decide = e.target.closest("[data-decide]");
    if (decide) {
      const li = decide.closest(".proposal");
      try {
        await api(`/api/proposals/${li.dataset.id}/decision`, { method: "POST", body: { status: decide.dataset.decide, note: $("textarea", li).value || null } });
        li.remove(); refreshReviewCount();
        if (!$("#proposal-list .proposal")) $("#proposal-list").innerHTML = '<li class="muted">No open proposals.</li>';
      } catch (err) { alert(err.message); }
    }
  });
  document.body.addEventListener("submit", e => {
    const form = e.target.closest(".fb-form"); if (!form) return;
    e.preventDefault();
    const turn = form.closest(".turn");
    sendFeedback(turn, -1, form.comment.value.trim(), form.correction.value.trim());
    form.hidden = true;
  });

  initAuth().catch(e => { $("#signin").hidden = false; $("#signin-error").textContent = e.message; });
});
