"""Build the ActionableEvidence dashboard HTML file.

Reads results/verdicts.csv and results/summary.json, embeds them into
a single-file HTML dashboard with Plotly charts.
"""

import json
import csv
from pathlib import Path

RESULTS_DIR = Path("C:/Models/ActionableEvidence/results")
OUTPUT_PATH = Path("C:/Models/ActionableEvidence/dashboard.html")


def load_data():
    """Load verdicts and summary data."""
    with open(RESULTS_DIR / "summary.json", "r", encoding="utf-8") as f:
        summary = json.load(f)

    verdicts = []
    with open(RESULTS_DIR / "verdicts.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert types
            row["k"] = int(row["k"])
            row["total_n"] = int(row["total_n"])
            row["estimate"] = float(row["estimate"]) if row["estimate"] else None
            row["p_value"] = float(row["p_value"]) if row["p_value"] else None
            row["significant"] = row["significant"] == "True"
            row["pi_crosses_null"] = row["pi_crosses_null"] == "True"
            row["n_audit_fails"] = int(row["n_audit_fails"]) if row["n_audit_fails"] else None
            row["has_pub_bias"] = row["has_pub_bias"] == "True"
            verdicts.append(row)

    return summary, verdicts


def build_html(summary, verdicts):
    """Build the complete HTML dashboard."""
    verdicts_json = json.dumps(verdicts)
    summary_json = json.dumps(summary)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ActionableEvidence Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js"><""" + """/script>
<style>
:root {
    --green: #16a34a;
    --green-bg: #f0fdf4;
    --green-border: #bbf7d0;
    --grey: #6b7280;
    --grey-bg: #f9fafb;
    --grey-border: #e5e7eb;
    --red: #dc2626;
    --blue: #2563eb;
    --amber: #d97706;
    --bg: #ffffff;
    --text: #111827;
    --text-muted: #6b7280;
    --border: #e5e7eb;
    --surface: #f9fafb;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
}

header {
    text-align: center;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 2px solid var(--border);
}

header h1 {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
}

header p {
    color: var(--text-muted);
    font-size: 16px;
}

/* Tabs */
.tabs {
    display: flex;
    gap: 0;
    border-bottom: 2px solid var(--border);
    margin-bottom: 24px;
}

.tab-btn {
    padding: 12px 24px;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-muted);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
}

.tab-btn:hover { color: var(--text); }
.tab-btn:focus { outline: 2px solid var(--blue); outline-offset: -2px; }
.tab-btn.active {
    color: var(--green);
    border-bottom-color: var(--green);
    font-weight: 600;
}

.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* Hero cards */
.hero-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
}

.hero-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.hero-card .value {
    font-size: 36px;
    font-weight: 700;
    line-height: 1.2;
}

.hero-card .label {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.hero-card.green .value { color: var(--green); }
.hero-card.green { border-color: var(--green-border); background: var(--green-bg); }
.hero-card.grey .value { color: var(--grey); }
.hero-card.amber .value { color: var(--amber); }

/* Chart containers */
.chart-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 24px;
}

@media (max-width: 800px) {
    .chart-row { grid-template-columns: 1fr; }
}

.chart-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
}

.chart-box h3 {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--text);
}

.chart-full {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;
}

.chart-full h3 {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
}

/* Review explorer */
.search-bar {
    margin-bottom: 16px;
}

.search-bar input {
    width: 100%;
    padding: 10px 16px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 14px;
    outline: none;
}

.search-bar input:focus { border-color: var(--blue); }

.sort-controls {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}

.sort-btn {
    padding: 6px 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--bg);
    cursor: pointer;
    font-size: 13px;
    transition: all 0.15s;
}

.sort-btn:hover { background: var(--surface); }
.sort-btn.active { background: var(--green-bg); border-color: var(--green); color: var(--green); }

.review-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.review-table th {
    text-align: left;
    padding: 10px 12px;
    border-bottom: 2px solid var(--border);
    font-weight: 600;
    color: var(--text-muted);
    cursor: pointer;
    user-select: none;
}

.review-table th:hover { color: var(--text); }

.review-table td {
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
}

.review-table tr:hover { background: var(--surface); }

.review-table .expandable { cursor: pointer; }
.review-table .expand-icon { display: inline-block; width: 20px; transition: transform 0.2s; }

.verdict-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}

.verdict-badge.actionable { background: var(--green-bg); color: var(--green); border: 1px solid var(--green-border); }
.verdict-badge.not-yet { background: var(--grey-bg); color: var(--grey); border: 1px solid var(--grey-border); }

.detail-row { display: none; }
.detail-row.open { display: table-row; }

.detail-content {
    padding: 12px;
    background: var(--surface);
    font-size: 12px;
}

.detail-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
}

.detail-table th, .detail-table td {
    padding: 4px 8px;
    text-align: left;
    font-size: 12px;
    border-bottom: 1px solid var(--border);
}

.detail-table .fail { color: var(--red); font-weight: 600; }
.detail-table .pass { color: var(--green); }

.pct-bar-container {
    display: inline-block;
    width: 80px;
    height: 8px;
    background: var(--grey-bg);
    border-radius: 4px;
    overflow: hidden;
    vertical-align: middle;
    margin-right: 6px;
}

.pct-bar {
    height: 100%;
    background: var(--green);
    border-radius: 4px;
}

/* Sensitivity slider */
.sensitivity-controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

@media (max-width: 800px) {
    .sensitivity-controls { grid-template-columns: 1fr; }
}

.slider-group {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
}

.slider-group label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

.slider-group input[type="range"] {
    width: 100%;
    margin-bottom: 4px;
}

.slider-group .slider-value {
    font-size: 12px;
    color: var(--text-muted);
    text-align: center;
}

/* Methodology */
.methodology {
    max-width: 800px;
}

.methodology h3 {
    font-size: 18px;
    margin: 24px 0 12px;
    font-weight: 600;
}

.methodology h4 {
    font-size: 15px;
    margin: 16px 0 8px;
    font-weight: 600;
    color: var(--text);
}

.methodology p, .methodology li {
    font-size: 14px;
    color: var(--text);
    margin-bottom: 8px;
}

.methodology ul {
    padding-left: 20px;
}

.methodology .criterion-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

.methodology .criterion-card h4 {
    margin-top: 0;
}

.methodology .threshold {
    font-family: monospace;
    background: #e5e7eb;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 13px;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-top: 16px;
}

.pagination button {
    padding: 6px 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--bg);
    cursor: pointer;
    font-size: 13px;
}

.pagination button:disabled { opacity: 0.4; cursor: default; }
.pagination span { font-size: 13px; color: var(--text-muted); }
</style>
</head>
<body>
<div class="container">
<header>
    <h1>ActionableEvidence</h1>
    <p>GO / NO-GO verdicts for 6,229 Cochrane meta-analyses across 501 systematic reviews</p>
</header>

<div class="tabs" role="tablist">
    <button class="tab-btn active" role="tab" aria-selected="true" data-tab="overview" tabindex="0">Verdict Overview</button>
    <button class="tab-btn" role="tab" aria-selected="false" data-tab="explorer" tabindex="-1">Review Explorer</button>
    <button class="tab-btn" role="tab" aria-selected="false" data-tab="criteria" tabindex="-1">Criteria Deep Dive</button>
    <button class="tab-btn" role="tab" aria-selected="false" data-tab="methodology" tabindex="-1">Methodology</button>
</div>

<!-- Tab 1: Overview -->
<div class="tab-panel active" id="panel-overview" role="tabpanel">
    <div class="hero-cards" id="hero-cards"></div>
    <div class="chart-full">
        <h3>Evidence Funnel: Sequential Filtering of 6,229 Meta-Analyses</h3>
        <div id="waterfall-chart" style="height:400px;"></div>
    </div>
    <div class="chart-row">
        <div class="chart-box">
            <h3>Verdict Distribution</h3>
            <div id="donut-chart" style="height:320px;"></div>
        </div>
        <div class="chart-box">
            <h3>Criteria Failure Rates</h3>
            <div id="failure-bar-chart" style="height:320px;"></div>
        </div>
    </div>
    <div class="chart-full">
        <h3>Failed Criteria Combinations (Top 15)</h3>
        <div id="combo-chart" style="height:360px;"></div>
    </div>
</div>

<!-- Tab 2: Review Explorer -->
<div class="tab-panel" id="panel-explorer" role="tabpanel">
    <div class="search-bar">
        <input type="text" id="review-search" placeholder="Search by review ID (e.g., CD000028)..." aria-label="Search reviews">
    </div>
    <div class="sort-controls">
        <button class="sort-btn active" data-sort="pct_desc">% Actionable (high to low)</button>
        <button class="sort-btn" data-sort="pct_asc">% Actionable (low to high)</button>
        <button class="sort-btn" data-sort="n_mas_desc">Total MAs (high to low)</button>
        <button class="sort-btn" data-sort="review_id_asc">Review ID (A-Z)</button>
    </div>
    <table class="review-table" id="review-table">
        <thead>
            <tr>
                <th style="width:30px;"></th>
                <th>Review ID</th>
                <th># MAs</th>
                <th># Actionable</th>
                <th>% Actionable</th>
            </tr>
        </thead>
        <tbody id="review-tbody"></tbody>
    </table>
    <div class="pagination" id="review-pagination"></div>
</div>

<!-- Tab 3: Criteria Deep Dive -->
<div class="tab-panel" id="panel-criteria" role="tabpanel">
    <div class="chart-row">
        <div class="chart-box">
            <h3>Distribution of Study Count (k)</h3>
            <div id="hist-k" style="height:300px;"></div>
        </div>
        <div class="chart-box">
            <h3>Distribution of Total Sample Size (N)</h3>
            <div id="hist-n" style="height:300px;"></div>
        </div>
    </div>
    <div class="chart-row">
        <div class="chart-box">
            <h3>Distribution of P-values</h3>
            <div id="hist-p" style="height:300px;"></div>
        </div>
        <div class="chart-box">
            <h3>Audit Flag Burden</h3>
            <div id="hist-fails" style="height:300px;"></div>
        </div>
    </div>
    <div class="chart-full">
        <h3>Sensitivity Analysis: How Does Actionable % Change With Thresholds?</h3>
        <div class="sensitivity-controls">
            <div class="slider-group">
                <label>Min Studies (k): <span id="val-k">5</span></label>
                <input type="range" id="slider-k" min="2" max="15" value="5" step="1">
            </div>
            <div class="slider-group">
                <label>Min Sample Size (N): <span id="val-n">500</span></label>
                <input type="range" id="slider-n" min="100" max="2000" value="500" step="100">
            </div>
            <div class="slider-group">
                <label>Significance Alpha: <span id="val-alpha">0.05</span></label>
                <input type="range" id="slider-alpha" min="0.01" max="0.10" value="0.05" step="0.01">
            </div>
            <div class="slider-group">
                <label>Egger Min k: <span id="val-egger-k">10</span></label>
                <input type="range" id="slider-egger-k" min="5" max="20" value="10" step="1">
            </div>
        </div>
        <div id="sensitivity-result" style="text-align:center; font-size:18px; font-weight:600; padding:16px;"></div>
    </div>
</div>

<!-- Tab 4: Methodology -->
<div class="tab-panel" id="panel-methodology" role="tabpanel">
    <div class="methodology">
        <h3>Overview</h3>
        <p>ActionableEvidence applies 6 independent criteria to determine whether a Cochrane meta-analysis provides truly actionable evidence. <strong>ALL 6 criteria must pass</strong> for a verdict of ACTIONABLE; failure of any single criterion yields NOT YET.</p>
        <p>The corpus consists of <strong>6,229 meta-analyses</strong> from <strong>501 Cochrane systematic reviews</strong> in the Pairwise70 dataset. Each MA is recomputed from study-level data using REML random-effects models with Hartung-Knapp-Sidik-Jonkman (HKSJ) adjustment.</p>

        <h3>The 6 Criteria</h3>

        <div class="criterion-card">
            <h4>1. Statistical Significance</h4>
            <p>The pooled estimate must be statistically significant at <span class="threshold">p &lt; 0.05</span> with HKSJ adjustment.</p>
            <p>HKSJ provides more conservative inference than the standard DerSimonian-Laird approach, using a t-distribution with k-1 degrees of freedom and an inflated standard error when heterogeneity is present.</p>
        </div>

        <div class="criterion-card">
            <h4>2. Prediction Interval Concordance</h4>
            <p>The 95% prediction interval must <strong>not cross the null</strong> (zero on log-scale).</p>
            <p>The PI estimates the range of true effects expected in a new, similar study. Even if the pooled estimate is significant, a PI crossing zero means the effect may not generalize. Requires k &ge; 3 to compute (Higgins-Thompson-Spiegelhalter method); MAs with k &lt; 3 pass by default.</p>
        </div>

        <div class="criterion-card">
            <h4>3. Multiverse Robustness</h4>
            <p>The conclusion must survive multiverse analysis: classification of <span class="threshold">Robust</span> or <span class="threshold">Moderate</span> from the FragilityAtlas.</p>
            <p>Multiverse analysis varies the estimator, CI method, bias correction, and leave-one-out strategy. "Fragile" or "Unstable" results change direction or significance under reasonable analytic choices. FragilityAtlas covers 403 of 501 reviews; uncovered reviews receive benefit of doubt (pass).</p>
        </div>

        <div class="criterion-card">
            <h4>4. Low Audit Flag Burden</h4>
            <p>Must have <span class="threshold">0 FAIL-level flags</span> from the MetaAudit 11-detector suite.</p>
            <p>MetaAudit detectors include: prediction gap, model misspecification, fragility, underpowered, publication bias, small-study effect, excess significance, data integrity, study overlap, overclaiming, and certainty mismatch. WARN flags are allowed; FAIL and CRITICAL flags are not.</p>
        </div>

        <div class="criterion-card">
            <h4>5. Sufficient Evidence Volume</h4>
            <p>Must have <span class="threshold">k &ge; 5 studies</span> AND <span class="threshold">total N &ge; 500 participants</span>.</p>
            <p>Below these thresholds, heterogeneity estimates are unreliable (for tau-squared and I-squared) and random fluctuation dominates. The k &ge; 5 threshold aligns with common guidance for random-effects meta-analysis reliability.</p>
        </div>

        <div class="criterion-card">
            <h4>6. No Publication Bias Signal</h4>
            <p>Egger's test <span class="threshold">p &gt; 0.10</span> (no asymmetry detected), or <span class="threshold">k &lt; 10</span> (test not applicable, passes by default).</p>
            <p>Publication bias is assessed via the MetaAudit pub_bias module. Egger's regression test has low power below k=10, so small MAs are exempt. The threshold of p &gt; 0.10 is conventional for this exploratory test.</p>
        </div>

        <h3>Limitations</h3>
        <ul>
            <li>FragilityAtlas covers only 403 of 501 reviews (80.4%). The 98 uncovered reviews receive benefit-of-doubt for the robustness criterion, which inflates the ACTIONABLE count slightly.</li>
            <li>The robustness classification from FragilityAtlas is at the review level (primary analysis), not per-MA. All MAs within a review inherit the same robustness classification.</li>
            <li>Prediction intervals for k &lt; 3 and Egger's test for k &lt; 10 are not computable, so these criteria pass by default for small MAs. This is methodologically correct but means very small MAs face fewer hurdles.</li>
            <li>The 6 criteria are binary (pass/fail). A richer framework might weight criteria by importance or allow partial credit.</li>
            <li>This analysis uses recomputed effects from study-level data, which may differ from the original Cochrane analysis if different effect measures, subgroup selections, or fixed-effect models were used.</li>
        </ul>

        <h3>References</h3>
        <ul>
            <li>Hartung J, Knapp G (2001). A refined method for the meta-analysis of controlled clinical trials with binary outcome. <em>Statistics in Medicine</em>.</li>
            <li>Higgins JPT, Thompson SG, Spiegelhalter DJ (2009). A re-evaluation of random-effects meta-analysis. <em>JRSS-A</em>.</li>
            <li>IntHout J, Ioannidis JPA, Borm GF (2014). The Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian-Laird method. <em>BMC Medical Research Methodology</em>.</li>
            <li>Egger M et al. (1997). Bias in meta-analysis detected by a simple, graphical test. <em>BMJ</em>.</li>
        </ul>
    </div>
</div>

</div>

<script>
// ── Embedded data ─────────────────────────────────────────────────────
const VERDICTS = """ + verdicts_json + """;
const SUMMARY = """ + summary_json + """;

// ── Tab switching ─────────────────────────────────────────────────────
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');

function switchTab(tabId) {
    tabBtns.forEach(b => {
        const isActive = b.dataset.tab === tabId;
        b.classList.toggle('active', isActive);
        b.setAttribute('aria-selected', isActive);
        b.tabIndex = isActive ? 0 : -1;
    });
    tabPanels.forEach(p => {
        p.classList.toggle('active', p.id === 'panel-' + tabId);
    });
    // Trigger chart resize for Plotly
    setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
}

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    btn.addEventListener('keydown', (e) => {
        const btns = Array.from(tabBtns);
        const idx = btns.indexOf(btn);
        if (e.key === 'ArrowRight' && idx < btns.length - 1) {
            e.preventDefault();
            switchTab(btns[idx + 1].dataset.tab);
            btns[idx + 1].focus();
        } else if (e.key === 'ArrowLeft' && idx > 0) {
            e.preventDefault();
            switchTab(btns[idx - 1].dataset.tab);
            btns[idx - 1].focus();
        }
    });
});

// ── Hero cards ────────────────────────────────────────────────────────
function buildHeroCards() {
    const container = document.getElementById('hero-cards');
    const cards = [
        { value: SUMMARY.total_mas.toLocaleString(), label: 'Total Meta-Analyses', cls: '' },
        { value: SUMMARY.actionable, label: 'Actionable', cls: 'green' },
        { value: SUMMARY.actionable_pct + '%', label: 'Actionable Rate', cls: 'green' },
        { value: SUMMARY.reviews_with_any_actionable + ' / 501', label: 'Reviews With Any Actionable', cls: '' },
        { value: SUMMARY.most_common_single_failure.replace('_', ' '), label: 'Most Common Single Failure', cls: 'amber' },
    ];
    container.innerHTML = cards.map(c =>
        '<div class="hero-card ' + c.cls + '">' +
        '<div class="value">' + c.value + '</div>' +
        '<div class="label">' + c.label + '</div></div>'
    ).join('');
}

// ── Waterfall chart ───────────────────────────────────────────────────
function buildWaterfall() {
    const wf = SUMMARY.waterfall;
    const steps = [
        { label: 'Total MAs', val: wf.total },
        { label: '+ Significance', val: wf.after_significance },
        { label: '+ Prediction Interval', val: wf.after_prediction_interval },
        { label: '+ Robustness', val: wf.after_robustness },
        { label: '+ Audit Flags', val: wf.after_audit_flags },
        { label: '+ Evidence Volume', val: wf.after_evidence_volume },
        { label: '+ Pub Bias', val: wf.after_pub_bias },
    ];

    const labels = steps.map(s => s.label);
    const values = steps.map(s => s.val);
    const colors = values.map((v, i) => i === 0 ? '#6b7280' : (i === values.length - 1 ? '#16a34a' : '#3b82f6'));

    // Show drops as annotations
    const annotations = [];
    for (let i = 1; i < steps.length; i++) {
        const drop = values[i - 1] - values[i];
        if (drop > 0) {
            annotations.push({
                x: labels[i],
                y: values[i] + drop / 2,
                text: '-' + drop.toLocaleString(),
                showarrow: false,
                font: { size: 11, color: '#dc2626' },
            });
        }
    }

    Plotly.newPlot('waterfall-chart', [{
        type: 'bar',
        x: labels,
        y: values,
        marker: { color: colors, line: { width: 0 } },
        text: values.map(v => v.toLocaleString()),
        textposition: 'outside',
        textfont: { size: 13, color: '#111827' },
        hovertemplate: '%{x}: %{y:,}<extra></extra>',
    }], {
        margin: { t: 20, b: 80, l: 60, r: 20 },
        yaxis: { title: 'MAs remaining', gridcolor: '#e5e7eb' },
        xaxis: { tickangle: -30 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        annotations: annotations,
    }, { responsive: true });
}

// ── Donut chart ───────────────────────────────────────────────────────
function buildDonut() {
    Plotly.newPlot('donut-chart', [{
        type: 'pie',
        labels: ['ACTIONABLE', 'NOT YET'],
        values: [SUMMARY.actionable, SUMMARY.not_yet],
        hole: 0.55,
        marker: { colors: ['#16a34a', '#d1d5db'] },
        textinfo: 'label+value',
        textfont: { size: 13 },
        hovertemplate: '%{label}: %{value:,} (%{percent})<extra></extra>',
    }], {
        margin: { t: 10, b: 10, l: 10, r: 10 },
        showlegend: false,
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        annotations: [{
            text: SUMMARY.actionable_pct + '%',
            showarrow: false,
            font: { size: 28, color: '#16a34a', family: 'sans-serif' },
        }],
    }, { responsive: true });
}

// ── Failure bar chart ─────────────────────────────────────────────────
function buildFailureBar() {
    const rates = SUMMARY.criteria_failure_rates;
    const sorted = Object.entries(rates).sort((a, b) => b[1] - a[1]);
    const labels = sorted.map(([k]) => k.replace(/_/g, ' '));
    const values = sorted.map(([, v]) => v);

    Plotly.newPlot('failure-bar-chart', [{
        type: 'bar',
        x: values,
        y: labels,
        orientation: 'h',
        marker: { color: '#ef4444' },
        text: values.map(v => v + '%'),
        textposition: 'outside',
        textfont: { size: 12 },
        hovertemplate: '%{y}: %{x:.1f}%<extra></extra>',
    }], {
        margin: { t: 10, b: 30, l: 140, r: 60 },
        xaxis: { title: 'Failure rate (%)', range: [0, 100], gridcolor: '#e5e7eb' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
    }, { responsive: true });
}

// ── Failure combinations chart ────────────────────────────────────────
function buildComboChart() {
    const comboCounts = {};
    VERDICTS.forEach(v => {
        if (v.failed_criteria) {
            const key = v.failed_criteria;
            comboCounts[key] = (comboCounts[key] || 0) + 1;
        }
    });
    const sorted = Object.entries(comboCounts).sort((a, b) => b[1] - a[1]).slice(0, 15);
    const labels = sorted.map(([k]) => k.replace(/;/g, ' + ').replace(/_/g, ' '));
    const values = sorted.map(([, v]) => v);

    Plotly.newPlot('combo-chart', [{
        type: 'bar',
        x: values,
        y: labels,
        orientation: 'h',
        marker: { color: '#6366f1' },
        text: values.map(v => v.toLocaleString()),
        textposition: 'outside',
        textfont: { size: 11 },
        hovertemplate: '%{y}: %{x:,} MAs<extra></extra>',
    }], {
        margin: { t: 10, b: 30, l: 320, r: 60 },
        xaxis: { title: 'Number of MAs', gridcolor: '#e5e7eb' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
    }, { responsive: true });
}

// ── Review Explorer ───────────────────────────────────────────────────
function buildReviewData() {
    const byReview = {};
    VERDICTS.forEach(v => {
        if (!byReview[v.review_id]) {
            byReview[v.review_id] = { review_id: v.review_id, mas: [], n_actionable: 0 };
        }
        byReview[v.review_id].mas.push(v);
        if (v.verdict === 'ACTIONABLE') byReview[v.review_id].n_actionable++;
    });
    return Object.values(byReview).map(r => ({
        ...r,
        n_mas: r.mas.length,
        pct_actionable: r.n_mas > 0 ? Math.round(1000 * r.n_actionable / r.n_mas) / 10 : 0,
    }));
}

let reviewData = buildReviewData();
let currentSort = 'pct_desc';
let currentSearch = '';
let currentPage = 0;
const PAGE_SIZE = 30;

function sortReviews(data, sort) {
    const sorted = [...data];
    switch (sort) {
        case 'pct_desc': sorted.sort((a, b) => b.pct_actionable - a.pct_actionable || b.n_mas - a.n_mas); break;
        case 'pct_asc': sorted.sort((a, b) => a.pct_actionable - b.pct_actionable || a.n_mas - b.n_mas); break;
        case 'n_mas_desc': sorted.sort((a, b) => b.n_mas - a.n_mas); break;
        case 'review_id_asc': sorted.sort((a, b) => a.review_id.localeCompare(b.review_id)); break;
    }
    return sorted;
}

function renderReviewTable() {
    const filtered = reviewData.filter(r =>
        !currentSearch || r.review_id.toLowerCase().includes(currentSearch.toLowerCase())
    );
    const sorted = sortReviews(filtered, currentSort);
    const totalPages = Math.ceil(sorted.length / PAGE_SIZE);
    currentPage = Math.min(currentPage, Math.max(0, totalPages - 1));
    const start = currentPage * PAGE_SIZE;
    const page = sorted.slice(start, start + PAGE_SIZE);

    const tbody = document.getElementById('review-tbody');
    let html = '';
    page.forEach((r, idx) => {
        const rowId = 'review-row-' + (start + idx);
        const pctColor = r.pct_actionable > 0 ? 'var(--green)' : 'var(--grey)';
        html += '<tr class="expandable" data-row="' + rowId + '">';
        html += '<td><span class="expand-icon">&#9654;</span></td>';
        html += '<td><strong>' + r.review_id + '</strong></td>';
        html += '<td>' + r.n_mas + '</td>';
        html += '<td>' + r.n_actionable + '</td>';
        html += '<td><span class="pct-bar-container"><span class="pct-bar" style="width:' + r.pct_actionable + '%;"></span></span>' + r.pct_actionable + '%</td>';
        html += '</tr>';
        // Detail row
        html += '<tr class="detail-row" id="' + rowId + '"><td colspan="5"><div class="detail-content">';
        html += '<table class="detail-table"><thead><tr><th>MA ID</th><th>k</th><th>N</th><th>p-value</th><th>Verdict</th><th>Failed Criteria</th></tr></thead><tbody>';
        r.mas.forEach(m => {
            const badge = m.verdict === 'ACTIONABLE'
                ? '<span class="verdict-badge actionable">ACTIONABLE</span>'
                : '<span class="verdict-badge not-yet">NOT YET</span>';
            const failedHtml = m.failed_criteria
                ? m.failed_criteria.split(';').map(c => '<span class="fail">' + c.replace(/_/g, ' ') + '</span>').join(', ')
                : '<span class="pass">all passed</span>';
            const pStr = m.p_value !== null ? (m.p_value < 0.001 ? '&lt;0.001' : m.p_value.toFixed(3)) : 'N/A';
            html += '<tr><td>' + m.ma_id + '</td><td>' + m.k + '</td><td>' + m.total_n.toLocaleString() + '</td><td>' + pStr + '</td><td>' + badge + '</td><td>' + failedHtml + '</td></tr>';
        });
        html += '</tbody></table></div></td></tr>';
    });
    tbody.innerHTML = html;

    // Pagination
    const pagDiv = document.getElementById('review-pagination');
    pagDiv.innerHTML = '<button ' + (currentPage === 0 ? 'disabled' : '') + ' onclick="currentPage--;renderReviewTable();">Prev</button>' +
        '<span>Page ' + (currentPage + 1) + ' of ' + totalPages + ' (' + filtered.length + ' reviews)</span>' +
        '<button ' + (currentPage >= totalPages - 1 ? 'disabled' : '') + ' onclick="currentPage++;renderReviewTable();">Next</button>';

    // Click handlers for expand
    document.querySelectorAll('.expandable').forEach(tr => {
        tr.addEventListener('click', () => {
            const detailId = tr.dataset.row;
            const detail = document.getElementById(detailId);
            const icon = tr.querySelector('.expand-icon');
            if (detail.classList.contains('open')) {
                detail.classList.remove('open');
                icon.style.transform = 'rotate(0deg)';
            } else {
                detail.classList.add('open');
                icon.style.transform = 'rotate(90deg)';
            }
        });
    });
}

// Sort button handlers
document.querySelectorAll('.sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentSort = btn.dataset.sort;
        currentPage = 0;
        renderReviewTable();
    });
});

document.getElementById('review-search').addEventListener('input', (e) => {
    currentSearch = e.target.value;
    currentPage = 0;
    renderReviewTable();
});

// ── Criteria Deep Dive charts ─────────────────────────────────────────
function buildCriteriaCharts() {
    // k histogram
    const kVals = VERDICTS.map(v => v.k);
    const kColors = VERDICTS.map(v => v.k >= 5 ? '#16a34a' : '#ef4444');
    Plotly.newPlot('hist-k', [{
        type: 'histogram',
        x: kVals,
        nbinsx: 50,
        marker: { color: '#3b82f6', line: { width: 0.5, color: '#fff' } },
        hovertemplate: 'k=%{x}: %{y} MAs<extra></extra>',
    }], {
        margin: { t: 10, b: 40, l: 50, r: 20 },
        xaxis: { title: 'Number of studies (k)', range: [0, 80] },
        yaxis: { title: 'Count' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        shapes: [{ type: 'line', x0: 5, x1: 5, y0: 0, y1: 1, yref: 'paper', line: { color: '#ef4444', width: 2, dash: 'dash' } }],
        annotations: [{ x: 5, y: 1, yref: 'paper', text: 'k=5 threshold', showarrow: false, font: { color: '#ef4444', size: 11 }, yanchor: 'bottom' }],
    }, { responsive: true });

    // N histogram (log scale)
    const nVals = VERDICTS.map(v => v.total_n).filter(n => n > 0);
    Plotly.newPlot('hist-n', [{
        type: 'histogram',
        x: nVals.map(n => Math.log10(Math.max(1, n))),
        nbinsx: 50,
        marker: { color: '#3b82f6', line: { width: 0.5, color: '#fff' } },
        hovertemplate: 'log10(N)=%{x:.1f}: %{y} MAs<extra></extra>',
    }], {
        margin: { t: 10, b: 40, l: 50, r: 20 },
        xaxis: { title: 'log10(Total N)', tickvals: [1, 2, 2.7, 3, 4, 5], ticktext: ['10', '100', '500', '1K', '10K', '100K'] },
        yaxis: { title: 'Count' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        shapes: [{ type: 'line', x0: Math.log10(500), x1: Math.log10(500), y0: 0, y1: 1, yref: 'paper', line: { color: '#ef4444', width: 2, dash: 'dash' } }],
        annotations: [{ x: Math.log10(500), y: 1, yref: 'paper', text: 'N=500 threshold', showarrow: false, font: { color: '#ef4444', size: 11 }, yanchor: 'bottom' }],
    }, { responsive: true });

    // P-value histogram
    const pVals = VERDICTS.map(v => v.p_value).filter(p => p !== null);
    Plotly.newPlot('hist-p', [{
        type: 'histogram',
        x: pVals,
        nbinsx: 50,
        marker: { color: '#3b82f6', line: { width: 0.5, color: '#fff' } },
        hovertemplate: 'p=%{x:.3f}: %{y} MAs<extra></extra>',
    }], {
        margin: { t: 10, b: 40, l: 50, r: 20 },
        xaxis: { title: 'P-value (HKSJ)', range: [0, 1] },
        yaxis: { title: 'Count' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        shapes: [{ type: 'line', x0: 0.05, x1: 0.05, y0: 0, y1: 1, yref: 'paper', line: { color: '#ef4444', width: 2, dash: 'dash' } }],
        annotations: [{ x: 0.05, y: 1, yref: 'paper', text: 'p=0.05', showarrow: false, font: { color: '#ef4444', size: 11 }, yanchor: 'bottom' }],
    }, { responsive: true });

    // Audit fails histogram
    const failVals = VERDICTS.map(v => v.n_audit_fails).filter(f => f !== null);
    Plotly.newPlot('hist-fails', [{
        type: 'histogram',
        x: failVals,
        nbinsx: Math.min(20, Math.max(...failVals) + 1),
        marker: { color: '#3b82f6', line: { width: 0.5, color: '#fff' } },
        hovertemplate: '%{x} fails: %{y} MAs<extra></extra>',
    }], {
        margin: { t: 10, b: 40, l: 50, r: 20 },
        xaxis: { title: 'Number of FAIL/CRITICAL flags', dtick: 1 },
        yaxis: { title: 'Count' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        shapes: [{ type: 'line', x0: 0.5, x1: 0.5, y0: 0, y1: 1, yref: 'paper', line: { color: '#ef4444', width: 2, dash: 'dash' } }],
        annotations: [{ x: 0.5, y: 1, yref: 'paper', text: '0 = pass', showarrow: false, font: { color: '#16a34a', size: 11 }, yanchor: 'bottom' }],
    }, { responsive: true });
}

// ── Sensitivity analysis ──────────────────────────────────────────────
function runSensitivity() {
    const minK = parseInt(document.getElementById('slider-k').value);
    const minN = parseInt(document.getElementById('slider-n').value);
    const alpha = parseFloat(document.getElementById('slider-alpha').value);
    const eggerK = parseInt(document.getElementById('slider-egger-k').value);

    document.getElementById('val-k').textContent = minK;
    document.getElementById('val-n').textContent = minN.toLocaleString();
    document.getElementById('val-alpha').textContent = alpha.toFixed(2);
    document.getElementById('val-egger-k').textContent = eggerK;

    let actionable = 0;
    VERDICTS.forEach(v => {
        const c1 = v.significant && v.p_value !== null && v.p_value < alpha;
        const c2 = !v.pi_crosses_null;
        const c3 = v.robustness === 'Robust' || v.robustness === 'Moderate' || v.robustness === 'not_covered';
        const c4 = v.n_audit_fails !== null && v.n_audit_fails === 0;
        const c5 = v.k >= minK && v.total_n >= minN;
        const c6 = v.k < eggerK ? true : !v.has_pub_bias;
        if (c1 && c2 && c3 && c4 && c5 && c6) actionable++;
    });
    const pct = (100 * actionable / VERDICTS.length).toFixed(1);
    document.getElementById('sensitivity-result').innerHTML =
        'With current thresholds: <span style="color:var(--green);font-size:28px;">' + actionable + '</span> ACTIONABLE (' + pct + '%) out of ' + VERDICTS.length.toLocaleString() + ' MAs';
}

['slider-k', 'slider-n', 'slider-alpha', 'slider-egger-k'].forEach(id => {
    document.getElementById(id).addEventListener('input', runSensitivity);
});

// ── Initialize ────────────────────────────────────────────────────────
buildHeroCards();
buildWaterfall();
buildDonut();
buildFailureBar();
buildComboChart();
renderReviewTable();
buildCriteriaCharts();
runSensitivity();
<""" + """/script>
</body>
</html>"""

    return html


def main():
    summary, verdicts = load_data()
    html = build_html(summary, verdicts)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard written to {OUTPUT_PATH} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
