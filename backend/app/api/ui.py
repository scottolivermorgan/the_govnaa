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
      --bg: #f6f7f9;
      --panel: #ffffff;
      --panel-soft: #f0f3f6;
      --text: #15202b;
      --muted: #5e6b78;
      --line: #d8dee6;
      --accent: #0d766e;
      --accent-dark: #075f59;
      --warn: #8a5a00;
      --danger: #a13a3a;
      --ok: #176a3a;
      font-family:
        Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
    }

    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      padding: 18px 28px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }

    h1, h2 { margin: 0; letter-spacing: 0; }
    h1 { font-size: 1.25rem; }
    h2 { font-size: 1rem; }

    main {
      width: min(1440px, 100%);
      margin: 0 auto;
      padding: 24px;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }

    button {
      min-height: 38px;
      border: 1px solid var(--accent);
      border-radius: 6px;
      background: var(--accent);
      color: white;
      font: inherit;
      font-weight: 650;
      padding: 0 14px;
      cursor: pointer;
    }

    button.secondary {
      background: var(--panel);
      color: var(--accent-dark);
    }

    button:disabled {
      border-color: #aeb8c2;
      background: #aeb8c2;
      cursor: wait;
    }

    .status {
      min-height: 22px;
      color: var(--muted);
      font-size: 0.9rem;
    }

    .summary {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 20px;
    }

    .metric, section {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }

    .metric {
      padding: 14px;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
      text-transform: uppercase;
    }

    .metric strong {
      display: block;
      margin-top: 6px;
      font-size: 1.5rem;
    }

    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
    }

    section header {
      padding: 13px 16px;
      border-bottom: 1px solid var(--line);
      background: var(--panel-soft);
      border-radius: 8px 8px 0 0;
    }

    .table-wrap {
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }

    th, td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      white-space: nowrap;
    }

    td.path, td.reason {
      white-space: normal;
      overflow-wrap: anywhere;
      min-width: 260px;
    }

    th {
      color: var(--muted);
      font-weight: 700;
      font-size: 0.78rem;
      text-transform: uppercase;
      background: #fbfcfd;
    }

    tr:last-child td { border-bottom: 0; }

    .pill {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 999px;
      padding: 2px 9px;
      font-size: 0.78rem;
      font-weight: 700;
      background: #e7edf3;
      color: var(--text);
    }

    .pill.pending_review { background: #dff3ef; color: var(--accent-dark); }
    .pill.needs_classification { background: #fff1cf; color: var(--warn); }
    .pill.completed { background: #e1f4e8; color: var(--ok); }
    .pill.failed { background: #ffe1e1; color: var(--danger); }

    @media (max-width: 900px) {
      header { align-items: flex-start; flex-direction: column; }
      main { padding: 16px; }
      .summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 560px) {
      .summary { grid-template-columns: 1fr; }
      .actions, button { width: 100%; }
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Data Governor</h1>
      <div class="status" id="status">Ready</div>
    </div>
    <div class="actions">
      <button id="scan-button" type="button">Scan Test Media</button>
      <button id="proposal-button" class="secondary" type="button">Generate Proposals</button>
      <button id="refresh-button" class="secondary" type="button">Refresh</button>
    </div>
  </header>

  <main>
    <div class="summary">
      <div class="metric"><span>Scans</span><strong id="scan-count">0</strong></div>
      <div class="metric"><span>Assets</span><strong id="asset-count">0</strong></div>
      <div class="metric"><span>Proposals</span><strong id="proposal-count">0</strong></div>
      <div class="metric"><span>Pending Review</span><strong id="pending-count">0</strong></div>
    </div>

    <div class="grid">
      <section>
        <header><h2>Proposals</h2></header>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Status</th><th>Operation</th><th>Source</th><th>Target</th><th>Confidence</th><th>Reason</th>
              </tr>
            </thead>
            <tbody id="proposal-rows"></tbody>
          </table>
        </div>
      </section>

      <section>
        <header><h2>Assets</h2></header>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Path</th><th>Extension</th><th>Size</th><th>Status</th></tr></thead>
            <tbody id="asset-rows"></tbody>
          </table>
        </div>
      </section>

      <section>
        <header><h2>Scans</h2></header>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Status</th><th>Started</th><th>Seen</th><th>New</th><th>Changed</th><th>Ignored</th><th>Proposals</th>
              </tr>
            </thead>
            <tbody id="scan-rows"></tbody>
          </table>
        </div>
      </section>
    </div>
  </main>

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
      document.querySelector("#scan-count").textContent = state.scans.length;
      document.querySelector("#asset-count").textContent = state.assets.length;
      document.querySelector("#proposal-count").textContent = state.proposals.length;
      document.querySelector("#pending-count").textContent = state.proposals
        .filter((proposal) => proposal.status === "pending_review").length;

      renderRows("#proposal-rows", state.proposals, proposalRow);
      renderRows("#asset-rows", state.assets, assetRow);
      renderRows("#scan-rows", state.scans, scanRow);
    }

    function renderRows(selector, rows, rowRenderer) {
      document.querySelector(selector).innerHTML = rows.length
        ? rows.map(rowRenderer).join("")
        : `<tr><td colspan="8">No records</td></tr>`;
    }

    function proposalRow(proposal) {
      return `<tr>
        <td>${pill(proposal.status)}</td>
        <td>${escapeHtml(proposal.operation)}</td>
        <td class="path">${escapeHtml(proposal.source_relative_path)}</td>
        <td class="path">${escapeHtml(proposal.target_relative_path)}</td>
        <td>${Math.round(proposal.confidence * 100)}%</td>
        <td class="reason">${escapeHtml(proposal.reason)}</td>
      </tr>`;
    }

    function assetRow(asset) {
      return `<tr>
        <td class="path">${escapeHtml(asset.relative_path)}</td>
        <td>${escapeHtml(asset.extension)}</td>
        <td>${asset.size_bytes}</td>
        <td>${pill(asset.status)}</td>
      </tr>`;
    }

    function scanRow(scan) {
      return `<tr>
        <td>${pill(scan.status)}</td>
        <td>${formatDate(scan.started_at)}</td>
        <td>${scan.files_seen}</td>
        <td>${scan.files_new}</td>
        <td>${scan.files_changed}</td>
        <td>${scan.files_ignored}</td>
        <td>${scan.proposals_created}</td>
      </tr>`;
    }

    function pill(value) {
      return `<span class="pill ${escapeHtml(value)}">${escapeHtml(value.replaceAll("_", " "))}</span>`;
    }

    function formatDate(value) {
      return new Intl.DateTimeFormat(undefined, {
        dateStyle: "short",
        timeStyle: "short",
      }).format(new Date(value));
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
