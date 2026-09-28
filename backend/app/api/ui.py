from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Data Governor</title>
  <style>
    :root {
      color-scheme: light;
      --page: #e8f7f3;
      --shell: #f8fbfa;
      --panel: #ffffff;
      --text: #172326;
      --muted: #718188;
      --line: #dbe8e5;
      --accent: #3aa99b;
      --accent-dark: #137669;
      --accent-soft: #d9f2ed;
      --amber: #d9901d;
      --amber-soft: #fff0d4;
      --danger: #aa4545;
      --shadow: 0 18px 55px rgba(31, 78, 73, 0.12);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      background: radial-gradient(circle at top left, rgba(255, 255, 255, 0.95), transparent 34rem), var(--page);
      color: var(--text);
    }

    .app-shell {
      display: grid;
      grid-template-columns: 224px minmax(0, 1fr);
      width: min(1320px, calc(100% - 32px));
      min-height: calc(100vh - 32px);
      margin: 16px auto;
      border: 1px solid rgba(255, 255, 255, 0.78);
      border-radius: 18px;
      background: rgba(248, 251, 250, 0.94);
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .sidebar {
      padding: 26px 18px;
      border-right: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.74), rgba(232, 247, 243, 0.58));
    }

    .brand {
      display: flex;
      gap: 2px;
      margin: 0 0 24px;
      font-size: 1.22rem;
      font-weight: 850;
      letter-spacing: 0;
    }

    .brand span { color: var(--accent-dark); }

    nav { display: grid; gap: 7px; }

    .nav-item {
      display: grid;
      grid-template-columns: 24px 1fr;
      align-items: center;
      gap: 10px;
      min-height: 42px;
      border-radius: 7px;
      padding: 0 12px;
      color: #405056;
      font-size: 0.92rem;
      font-weight: 650;
    }

    .nav-item.active {
      background: var(--accent-soft);
      color: var(--accent-dark);
    }

    .icon {
      display: inline-grid;
      width: 22px;
      height: 22px;
      place-items: center;
      border: 1.5px solid currentColor;
      border-radius: 6px;
      font-size: 0.75rem;
      line-height: 1;
    }

    .content {
      display: grid;
      grid-template-rows: auto 1fr;
      min-width: 0;
      background: linear-gradient(90deg, rgba(255, 255, 255, 0.84), rgba(255, 255, 255, 0.58)), var(--shell);
    }

    .topbar {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: center;
      gap: 16px;
      padding: 18px 24px;
      border-bottom: 1px solid var(--line);
    }

    .search {
      display: flex;
      align-items: center;
      max-width: 520px;
      min-height: 42px;
      border-radius: 8px;
      padding: 0 14px;
      background: #f2f7f6;
      color: var(--muted);
      font-size: 0.9rem;
    }

    .avatar {
      display: grid;
      width: 42px;
      height: 42px;
      place-items: center;
      border-radius: 50%;
      background: #9dded4;
      color: #075e54;
      font-weight: 850;
    }

    main {
      min-width: 0;
      padding: 34px 42px;
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 18px;
      margin-bottom: 26px;
    }

    h1, h2, p { margin: 0; letter-spacing: 0; }
    h1 { font-size: clamp(1.55rem, 3vw, 2.15rem); line-height: 1.05; }
    h2 { font-size: 1rem; }
    .subtitle { margin-top: 8px; color: var(--muted); font-size: 0.98rem; }

    .actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 10px;
    }

    button {
      min-height: 38px;
      border: 1px solid var(--accent);
      border-radius: 7px;
      background: var(--accent);
      color: white;
      font: inherit;
      font-size: 0.86rem;
      font-weight: 750;
      padding: 0 13px;
      cursor: pointer;
    }

    button.secondary {
      background: #fff;
      color: var(--accent-dark);
    }

    button:disabled {
      border-color: #aebbb8;
      background: #aebbb8;
      cursor: wait;
    }

    .status {
      min-height: 22px;
      margin-top: 8px;
      color: var(--muted);
      font-size: 0.92rem;
    }

    .summary {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 18px;
      margin-bottom: 26px;
    }

    .metric {
      display: grid;
      grid-template-columns: 42px 1fr;
      align-items: center;
      gap: 14px;
      min-height: 104px;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 18px;
      background: rgba(255, 255, 255, 0.78);
      box-shadow: 0 8px 24px rgba(41, 77, 72, 0.05);
    }

    .metric-icon {
      display: grid;
      width: 42px;
      height: 42px;
      place-items: center;
      border: 2px solid var(--accent);
      border-radius: 8px;
      color: var(--accent-dark);
      font-weight: 850;
    }

    .metric.warning .metric-icon {
      border-color: var(--amber);
      color: var(--amber);
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.86rem;
    }

    .metric strong {
      display: block;
      font-size: 1.6rem;
      line-height: 1;
      margin-bottom: 5px;
    }

    .workbench { display: grid; gap: 18px; }

    section {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.82);
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(41, 77, 72, 0.05);
    }

    section header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--line);
      background: #fbfdfc;
    }

    .table-wrap { overflow-x: auto; }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }

    th, td {
      padding: 13px 16px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: middle;
      white-space: nowrap;
    }

    th {
      color: var(--muted);
      font-size: 0.74rem;
      font-weight: 850;
      text-transform: uppercase;
    }

    tr:last-child td { border-bottom: 0; }

    td.path, td.reason {
      min-width: 250px;
      white-space: normal;
      overflow-wrap: anywhere;
    }

    .path-muted {
      color: var(--muted);
      font-size: 0.82rem;
    }

    .arrow {
      color: var(--muted);
      font-weight: 850;
      text-align: center;
      min-width: 32px;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      min-height: 27px;
      border-radius: 6px;
      padding: 3px 10px;
      font-size: 0.78rem;
      font-weight: 850;
      background: #e9f0ef;
      color: var(--text);
    }

    .pill.pending_review { background: #d7f1eb; color: var(--accent-dark); }
    .pill.needs_classification { background: var(--amber-soft); color: #8a5a00; }
    .pill.blocked { background: #ffe1e1; color: var(--danger); }
    .pill.completed { background: #dff3e6; color: #176a3a; }
    .pill.failed { background: #ffe1e1; color: var(--danger); }

    .secondary-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
      gap: 18px;
    }

    @media (max-width: 980px) {
      .app-shell { grid-template-columns: 1fr; }
      .sidebar { display: none; }
      main { padding: 24px; }
      .hero { flex-direction: column; }
      .actions { justify-content: flex-start; }
      .summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .secondary-grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 560px) {
      .app-shell {
        width: 100%;
        min-height: 100vh;
        margin: 0;
        border-radius: 0;
      }

      .topbar { padding: 14px; }
      main { padding: 18px 14px; }
      .summary { grid-template-columns: 1fr; }
      .actions, button { width: 100%; }
    }
  </style>
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">Data<span>Governor</span></div>
      <nav>
        <div class="nav-item active"><span class="icon">S</span><span>Scan</span></div>
        <div class="nav-item"><span class="icon">R</span><span>Review</span></div>
        <div class="nav-item"><span class="icon">O</span><span>Organise</span></div>
        <div class="nav-item"><span class="icon">Q</span><span>Search</span></div>
        <div class="nav-item"><span class="icon">G</span><span>Settings</span></div>
      </nav>
    </aside>

    <div class="content">
      <div class="topbar">
        <div class="search">Search assets and proposals...</div>
        <div class="avatar">DG</div>
      </div>

      <main>
        <div class="hero">
          <div>
            <h1 id="page-title">Scan Ready</h1>
            <p class="subtitle" id="page-subtitle">Run a scan to catalogue the test media root.</p>
            <div class="status" id="status">Ready</div>
          </div>
          <div class="actions">
            <button id="scan-button" type="button">Scan Test Media</button>
            <button id="proposal-button" class="secondary" type="button">Generate Proposals</button>
            <button id="refresh-button" class="secondary" type="button">Refresh</button>
          </div>
        </div>

        <div class="summary">
          <div class="metric">
            <div class="metric-icon">M</div>
            <div><strong id="pending-count">0</strong><span>Rename / Move</span></div>
          </div>
          <div class="metric">
            <div class="metric-icon">A</div>
            <div><strong id="asset-count">0</strong><span>Assets</span></div>
          </div>
          <div class="metric warning">
            <div class="metric-icon">!</div>
            <div><strong id="review-count">0</strong><span>Needs Review</span></div>
          </div>
          <div class="metric">
            <div class="metric-icon">S</div>
            <div><strong id="scan-count">0</strong><span>Scans</span></div>
          </div>
        </div>

        <div class="workbench">
          <section>
            <header>
              <h2>Review Queue</h2>
              <span class="path-muted" id="proposal-count">0 proposals</span>
            </header>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Source</th><th></th><th>Target</th><th>Status</th><th>Confidence</th>
                  </tr>
                </thead>
                <tbody id="proposal-rows"></tbody>
              </table>
            </div>
          </section>

          <div class="secondary-grid">
            <section>
              <header><h2>Assets</h2></header>
              <div class="table-wrap">
                <table>
                  <thead><tr><th>Path</th><th>Extension</th><th>Status</th></tr></thead>
                  <tbody id="asset-rows"></tbody>
                </table>
              </div>
            </section>

            <section>
              <header><h2>Scan History</h2></header>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Status</th><th>Seen</th><th>New</th><th>Ignored</th><th>Proposals</th>
                    </tr>
                  </thead>
                  <tbody id="scan-rows"></tbody>
                </table>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  </div>

  <script>
    const state = { scans: [], assets: [], proposals: [] };
    const statusEl = document.querySelector("#status");
    const buttons = [...document.querySelectorAll("button")];

    function setBusy(message) {
      statusEl.textContent = message;
      buttons.forEach((button) => button.disabled = true);
    }

    function setReady(message = "Ready") {
      statusEl.textContent = message;
      buttons.forEach((button) => button.disabled = false);
    }

    async function request(path, options = {}) {
      const response = await fetch(path, options);
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`${response.status} ${body}`);
      }
      return response.json();
    }

    async function refresh(message = "Ready") {
      const [scans, assets, proposals] = await Promise.all([
        request("/scans"),
        request("/assets"),
        request("/proposals"),
      ]);
      state.scans = scans;
      state.assets = assets;
      state.proposals = proposals;
      render();
      setReady(message);
    }

    async function scan() {
      setBusy("Scanning test media...");
      try {
        await request("/scans/test-media", { method: "POST" });
        await refresh("Scan complete");
      } catch (error) {
        setReady(`Scan failed: ${error.message}`);
      }
    }

    async function generateProposals() {
      if (state.scans.length === 0) {
        setReady("Run a scan first");
        return;
      }
      setBusy("Generating proposals...");
      try {
        await request(`/scans/${state.scans[0].id}/proposals`, { method: "POST" });
        await refresh("Proposals updated");
      } catch (error) {
        setReady(`Proposal generation failed: ${error.message}`);
      }
    }

    function render() {
      const pendingMoves = state.proposals.filter((proposal) => proposal.status === "pending_review");
      const needsReview = state.proposals.filter(
        (proposal) => proposal.status === "needs_classification" || proposal.status === "blocked"
      );

      document.querySelector("#scan-count").textContent = state.scans.length;
      document.querySelector("#asset-count").textContent = state.assets.length;
      document.querySelector("#pending-count").textContent = pendingMoves.length;
      document.querySelector("#review-count").textContent = needsReview.length;
      document.querySelector("#proposal-count").textContent = `${state.proposals.length} proposals`;
      document.querySelector("#page-title").textContent = state.scans.length ? "Scan Complete" : "Scan Ready";
      document.querySelector("#page-subtitle").textContent = state.proposals.length
        ? `Found ${state.proposals.length} items to review.`
        : state.scans.length
          ? `Found ${state.assets.length} catalogue assets.`
          : "Run a scan to catalogue the test media root.";

      renderRows("#proposal-rows", state.proposals, proposalRow, 5);
      renderRows("#asset-rows", state.assets, assetRow, 3);
      renderRows("#scan-rows", state.scans, scanRow, 5);
    }

    function renderRows(selector, rows, rowRenderer, colspan) {
      document.querySelector(selector).innerHTML = rows.length
        ? rows.map(rowRenderer).join("")
        : `<tr><td colspan="${colspan}">No records</td></tr>`;
    }

    function proposalRow(proposal) {
      const detail = proposal.validation_message || proposal.reason;
      return `<tr>
        <td class="path">${escapeHtml(proposal.source_relative_path)}</td>
        <td class="arrow">-&gt;</td>
        <td class="path">
          <div>${escapeHtml(proposal.target_relative_path)}</div>
          <div class="path-muted">${escapeHtml(detail)}</div>
        </td>
        <td>${pill(proposal.status)}</td>
        <td>${Math.round(proposal.confidence * 100)}%</td>
      </tr>`;
    }

    function assetRow(asset) {
      return `<tr>
        <td class="path">${escapeHtml(asset.relative_path)}</td>
        <td>${escapeHtml(asset.extension)}</td>
        <td>${pill(asset.status)}</td>
      </tr>`;
    }

    function scanRow(scan) {
      return `<tr>
        <td>${pill(scan.status)}</td>
        <td>${scan.files_seen}</td>
        <td>${scan.files_new}</td>
        <td>${scan.files_ignored}</td>
        <td>${scan.proposals_created}</td>
      </tr>`;
    }

    function pill(value) {
      return `<span class="pill ${escapeHtml(value)}">${escapeHtml(value.replaceAll("_", " "))}</span>`;
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    document.querySelector("#scan-button").addEventListener("click", scan);
    document.querySelector("#proposal-button").addEventListener("click", generateProposals);
    document.querySelector("#refresh-button").addEventListener("click", () => refresh("Refreshed"));

    refresh();
  </script>
</body>
</html>
"""
