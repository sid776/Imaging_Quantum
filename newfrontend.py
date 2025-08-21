<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Data Counts</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 24px; }
    h1 { margin: 0 0 16px; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 12px; background: #fff; }
    .controls { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 8px; border-bottom: 1px solid #eee; text-align: left; }
    th { background: #fafafa; }
    .muted { color: #666; }
    .pill { display:inline-block; padding:2px 8px; border-radius:999px; background:#f3f3f3; }
  </style>
</head>
<body>
  <h1>Data Counts</h1>

  <div class="controls">
    <label for="cob">COB Date (optional):</label>
    <input id="cob" type="date" />
    <button id="refresh">Refresh</button>
    <span id="status" class="muted"></span>
  </div>

  <div class="row">
    <div class="card">
      <h3>Valuation — Book Counts</h3>
      <table id="tbl-books">
        <thead><tr><th>Book</th><th>Count</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>

    <div class="card">
      <h3>Risk Factor Shocks — Counts</h3>
      <table id="tbl-shocks">
        <thead><tr><th>Risk Factor</th><th>Curve</th><th>Count</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <div class="row">
    <div class="card">
      <h3>Sensitivities — Book Counts</h3>
      <table id="tbl-sens">
        <thead><tr><th>Book</th><th>Count</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>

    <div class="card">
      <h3>Valuation — Run Count</h3>
      <div id="run-count" class="pill">loading…</div>
      <div class="muted" style="margin-top:8px;">Latest COB if date not provided.</div>
    </div>
  </div>

<script>
(async function () {
  const elStatus = document.getElementById('status');
  const elCob    = document.getElementById('cob');
  const elBtn    = document.getElementById('refresh');

  // Update these paths if you mounted your routers under a different prefix
  const API = {
    books:      '/api/valuation/book_counts',
    shocks:     '/api/riskshocks/counts',
    sensBooks:  '/api/sensitivities/book_counts',
    runCounts:  '/api/valuation/run_counts'
  };

  function q(el){return document.querySelector(el)}
  function fillTable(tbodySel, rows, cols){
    const tb = q(tbodySel);
    tb.innerHTML = rows.map(r => `<tr>${cols.map(c => `<td>${r[c] ?? ''}</td>`).join('')}</tr>`).join('') || `<tr><td colspan="${cols.length}" class="muted">No data</td></tr>`;
  }

  async function getJSON(url){
    const r = await fetch(url, {headers:{'Accept':'application/json'}});
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  }

  function withCob(url){
    const v = elCob.value?.trim();
    if(!v) return url;
    const sep = url.includes('?') ? '&' : '?';
    // the param name must match what your endpoints expect; if they
    // don’t accept a date, leaving it off will use latest COB.
    return `${url}${sep}cob_date=${v}`;
  }

  async function load(){
    try{
      elStatus.textContent = 'Loading…';
      const [books, shocks, sens, run] = await Promise.all([
        getJSON(withCob(API.books)),
        getJSON(withCob(API.shocks)),
        getJSON(withCob(API.sensBooks)),
        getJSON(withCob(API.runCounts))
      ]);

      fillTable('#tbl-books tbody', books, ['book','count']);
      fillTable('#tbl-shocks tbody', shocks, ['risk_factor','curve','count']);
      fillTable('#tbl-sens tbody', sens, ['book','count']);
      q('#run-count').textContent = (run?.run_count ?? '0');

      elStatus.textContent = 'Done';
      setTimeout(()=>elStatus.textContent='', 1200);
    }catch(e){
      console.error(e);
      elStatus.textContent = 'Error loading data (see console)';
    }
  }

  elBtn.addEventListener('click', load);
  await load();
})();
</script>
</body>
</html>
