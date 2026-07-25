import React, { useState, useEffect, useCallback } from "react";

const JOBS = ["admin.","blue-collar","entrepreneur","housemaid","management","retired","self-employed","services","student","technician","unemployed"];
const MARITALS = ["single","married","divorced"];
const EDUCATIONS = ["basic.4y","basic.6y","basic.9y","high.school","illiterate","professional.course","university.degree"];
const YESNO = ["yes","no"];

const PREDICT_FIELDS = [
  { name: "age", label: "Age", type: "number", value: 34 },
  { name: "job", label: "Job", type: "select", options: JOBS, value: "technician" },
  { name: "marital", label: "Marital status", type: "select", options: MARITALS, value: "married" },
  { name: "education", label: "Education", type: "select", options: EDUCATIONS, value: "university.degree" },
  { name: "housing", label: "Housing loan", type: "select", options: YESNO, value: "yes" },
  { name: "loan", label: "Personal loan", type: "select", options: YESNO, value: "no" },
  { name: "annual_income", label: "Annual income", type: "number", value: 82000 },
  { name: "credit_score", label: "Credit score", type: "number", value: 710 },
  { name: "account_balance", label: "Account balance", type: "number", value: 45000 },
  { name: "digital_banking_score", label: "Digital banking score", type: "number", value: 68 },
  { name: "monthly_transactions", label: "Monthly transactions", type: "number", value: 28 },
  { name: "investment_amount", label: "Investment amount", type: "number", value: 15000 },
  { name: "account_tenure", label: "Account tenure (yrs)", type: "number", value: 6 },
  { name: "number_of_products", label: "Number of products", type: "number", value: 2 },
];

const defaultPredictState = () => {
  const o = {};
  PREDICT_FIELDS.forEach(f => { o[f.name] = f.value; });
  return o;
};

function Styles() {
  return (
    <style>{`
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

      html, body, #root{
        margin:0; padding:0; height:100%; background:#14171c;
      }
      body{ font-size:16px; }

      .sc-root{
        --ink:#14171c; --surface:#1b1f27; --line:rgba(233,231,221,0.10); --line-strong:rgba(233,231,221,0.18);
        --paper:#e9e7dd; --paper-dim:#a8a69c; --brass:#c9a24b; --brass-soft:rgba(201,162,75,0.16);
        --slate:#6f8fb3; --good:#7fae86; --bad:#c95b4b; --radius:3px;
        background: radial-gradient(1200px 600px at 100% -10%, rgba(201,162,75,0.06), transparent 60%), var(--ink);
        color: var(--paper);
        font-family:'Inter', sans-serif;
        min-height: 100vh;
        display:grid;
        grid-template-columns: 220px 1fr;
      }
      .sc-root *{ box-sizing:border-box; }
      .sc-rail{ border-right:1px solid var(--line); padding:28px 18px; display:flex; flex-direction:column; gap:28px; position:sticky; top:0; height:100vh; }
      .sc-brand{ font-family:'Fraunces',serif; font-size:20px; font-weight:600; display:flex; align-items:center; gap:10px; }
      .sc-mark{ width:26px;height:26px;border:1px solid var(--brass);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono';font-size:11px;color:var(--brass);flex:none; }
      .sc-brand small{ display:block; font-weight:500; font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--paper-dim); margin-top:2px; }
      .sc-nav{ display:flex; flex-direction:column; gap:2px; }
      .sc-navbtn{ all:unset; cursor:pointer; padding:9px 10px; border-radius:var(--radius); font-size:13.5px; color:var(--paper-dim); display:flex; align-items:center; gap:10px; transition:.15s; }
      .sc-navbtn .n{ font-family:'IBM Plex Mono'; font-size:10.5px; opacity:.6; }
      .sc-navbtn:hover{ background:rgba(233,231,221,0.04); color:var(--paper); }
      .sc-navbtn.active{ background:var(--brass-soft); color:var(--paper); }
      .sc-navbtn.active .n{ color:var(--brass); opacity:1; }
      .sc-foot{ margin-top:auto; }
      .sc-conn{ border:1px solid var(--line); border-radius:var(--radius); padding:12px; font-size:11.5px; }
      .sc-connrow{ display:flex; align-items:center; gap:7px; margin-bottom:9px; }
      .sc-dot{ width:7px;height:7px;border-radius:50%; background:#6b6f78; flex:none; }
      .sc-dot.ok{ background:var(--good); box-shadow:0 0 0 3px rgba(127,174,134,0.18); }
      .sc-dot.bad{ background:var(--bad); box-shadow:0 0 0 3px rgba(201,91,75,0.18); }
      .sc-conn label{ display:block; color:var(--paper-dim); margin-bottom:4px; font-family:'IBM Plex Mono'; }
      .sc-conn input{ width:100%; background:var(--surface); border:1px solid var(--line-strong); color:var(--paper); font-family:'IBM Plex Mono'; font-size:11.5px; padding:6px 7px; border-radius:var(--radius); margin-bottom:8px; }
      .sc-conn input:focus{ outline:1px solid var(--brass); border-color:var(--brass); }
      .sc-conn button{ all:unset; cursor:pointer; width:100%; text-align:center; padding:6px 0; font-size:11.5px; font-weight:600; letter-spacing:.03em; border:1px solid var(--brass); color:var(--brass); border-radius:var(--radius); transition:.15s; }
      .sc-conn button:hover{ background:var(--brass); color:var(--ink); }

      .sc-main{ padding:40px 56px 70px; max-width:1520px; width:100%; margin:0 auto; }
      .sc-eyebrow{ font-family:'IBM Plex Mono'; font-size:12.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--brass); margin-bottom:10px; }
      .sc-h1{ font-family:'Fraunces',serif; font-weight:500; font-size:40px; margin:0 0 10px; }
      .sc-sub{ color:var(--paper-dim); font-size:16px; max-width:65ch; line-height:1.55; }
      .sc-banner{ border:1px solid rgba(201,91,75,0.4); background:rgba(201,91,75,0.08); color:#e8b3a8; padding:12px 14px; border-radius:var(--radius); font-size:13px; margin-bottom:20px; }
      .sc-warn{ border:1px solid rgba(201,122,75,0.4); background:rgba(201,122,75,0.08); border-radius:var(--radius); padding:12px 14px; margin-bottom:18px; font-size:12.5px; color:#e6bc9e; }
      .sc-warn div{ margin-bottom:4px; } .sc-warn div:last-child{ margin-bottom:0; }

      .sc-kpis{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:36px; }
      .sc-kpi{ border:1px solid var(--line); background:var(--surface); border-radius:var(--radius); padding:20px 20px 18px; }
      .sc-kpi .num{ font-family:'IBM Plex Mono'; font-size:32px; font-weight:500; }
      .sc-kpi .label{ font-size:12.5px; color:var(--paper-dim); margin-top:6px; }

      .sc-sectiontitle{ font-family:'Fraunces',serif; font-size:19px; font-weight:500; margin:0 0 16px; padding-bottom:12px; border-bottom:1px solid var(--line); }
      .sc-seggrid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(320px,1fr)); gap:16px; margin-bottom:40px; }
      .sc-card{ border:1px solid var(--line); background:var(--surface); border-radius:var(--radius); padding:22px; position:relative; transition:.15s; }
      .sc-card:hover{ transform:translateY(-2px); border-color:var(--line-strong); }
      .sc-card::before{ content:""; position:absolute; left:0; top:18px; bottom:18px; width:2px; background:var(--brass); opacity:.7; }
      .sc-cardhead{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px; }
      .sc-seal{ width:38px;height:38px;border-radius:50%; border:1px solid var(--brass); display:flex; align-items:center; justify-content:center; font-family:'IBM Plex Mono'; font-size:14px; color:var(--brass); flex:none; }
      .sc-persona{ font-family:'Fraunces',serif; font-size:19px; margin:0 0 4px; }
      .sc-count{ font-family:'IBM Plex Mono'; font-size:12px; color:var(--paper-dim); }
      .sc-stats{ display:grid; grid-template-columns:1fr 1fr; gap:10px 14px; margin:16px 0; padding:14px 0; border-top:1px dashed var(--line); border-bottom:1px dashed var(--line); }
      .sc-statlabel{ font-size:11px; color:var(--paper-dim); text-transform:uppercase; letter-spacing:.06em; }
      .sc-statval{ font-family:'IBM Plex Mono'; font-size:14.5px; margin-top:3px; }
      .sc-chips{ display:flex; flex-wrap:wrap; gap:7px; margin-top:14px; }
      .sc-chip{ font-size:12px; padding:5px 10px; border-radius:20px; border:1px solid var(--line-strong); color:var(--paper-dim); background:rgba(233,231,221,0.03); }

      .sc-barrow{ display:grid; grid-template-columns:170px 1fr 60px; align-items:center; gap:12px; padding:7px 0; }
      .sc-barrow .name{ font-size:12.5px; }
      .sc-track{ height:8px; background:rgba(233,231,221,0.06); border-radius:20px; overflow:hidden; }
      .sc-fill{ height:100%; background:linear-gradient(90deg, var(--brass), var(--slate)); border-radius:20px; }
      .sc-barrow .count{ font-family:'IBM Plex Mono'; font-size:11.5px; color:var(--paper-dim); text-align:right; }

      .sc-panel{ border:1px solid var(--line); background:var(--surface); border-radius:var(--radius); padding:28px; max-width:780px; }
      .sc-searchrow{ display:flex; gap:10px; margin-bottom:26px; max-width:460px; }
      .sc-searchrow input{ flex:1; background:var(--surface); border:1px solid var(--line-strong); color:var(--paper); padding:12px 14px; border-radius:var(--radius); font-family:'IBM Plex Mono'; font-size:14.5px; }
      .sc-searchrow input:focus{ outline:none; border-color:var(--brass); }
      .sc-btn{ all:unset; cursor:pointer; padding:12px 20px; background:var(--brass); color:var(--ink); font-weight:600; font-size:14.5px; border-radius:var(--radius); letter-spacing:.02em; transition:.15s; }
      .sc-btn:hover{ opacity:.88; }
      .sc-btn.ghost{ background:transparent; color:var(--brass); border:1px solid var(--brass); }
      .sc-btn.ghost:hover{ background:var(--brass-soft); }

      .sc-formgrid{ display:grid; grid-template-columns:1fr 1fr; gap:16px 18px; }
      .sc-field{ display:flex; flex-direction:column; gap:7px; }
      .sc-field label{ font-size:12px; color:var(--paper-dim); text-transform:uppercase; letter-spacing:.06em; }
      .sc-field input, .sc-field select{ background:var(--ink); border:1px solid var(--line-strong); color:var(--paper); padding:11px 12px; border-radius:var(--radius); font-family:'Inter'; font-size:14.5px; }
      .sc-field input:focus, .sc-field select:focus{ outline:none; border-color:var(--brass); }
      .sc-formactions{ margin-top:22px; display:flex; gap:10px; }

      .sc-resulthead{ display:flex; align-items:center; gap:14px; margin-bottom:18px; padding-bottom:18px; border-bottom:1px solid var(--line); }
      .sc-resulthead .sc-seal{ width:46px;height:46px; font-size:16px; }
      .sc-resulthead h2{ font-family:'Fraunces',serif; font-weight:500; font-size:20px; margin:0 0 4px; }
      .sc-resulthead .cid{ font-family:'IBM Plex Mono'; font-size:11.5px; color:var(--paper-dim); }
      .sc-profilegrid{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px 18px; margin-bottom:22px; }
      .sc-reclist{ display:flex; flex-direction:column; gap:8px; }
      .sc-rec{ border:1px solid var(--line); border-left:2px solid var(--slate); border-radius:var(--radius); padding:10px 12px; background:rgba(111,143,179,0.05); }
      .sc-rec .rtitle{ font-size:13.5px; font-weight:600; margin-bottom:2px; }
      .sc-rec .rcat{ font-family:'IBM Plex Mono'; font-size:10px; color:var(--slate); text-transform:uppercase; letter-spacing:.05em; margin-bottom:5px; }
      .sc-rec .rreason{ font-size:12px; color:var(--paper-dim); line-height:1.4; }
      .sc-empty{ color:var(--paper-dim); font-size:13px; padding:30px 0; text-align:center; border:1px dashed var(--line); border-radius:var(--radius); }
      .sc-loading{ color:var(--paper-dim); font-size:13px; font-family:'IBM Plex Mono'; }

      @media (max-width: 860px){
        .sc-root{ grid-template-columns:1fr; }
        .sc-rail{ position:relative; height:auto; flex-direction:row; align-items:center; overflow-x:auto; }
        .sc-foot{ margin-top:0; }
        .sc-main{ padding:24px; }
        .sc-kpis, .sc-formgrid, .sc-profilegrid{ grid-template-columns:1fr 1fr; }
      }

      .sc-metricgrid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:16px;
    margin-bottom:30px;
}

.sc-plotgrid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
}

.sc-plot{
    background:var(--surface);
    border:1px solid var(--line);
    border-radius:var(--radius);
    padding:18px;
}

.sc-plot img{
    width:100%;
    border-radius:3px;
}

.sc-plot h3{
    margin:0 0 14px;
    font-family:'Fraunces', serif;
    font-size:18px;
}

.sc-table{
    width:100%;
    border-collapse:collapse;
}

.sc-table th,
.sc-table td{
    padding:12px;
    border-bottom:1px solid var(--line);
    text-align:left;
}

.sc-table th{
    color:var(--paper-dim);
    font-size:12px;
    text-transform:uppercase;
}

    `}</style>
  );
}

export default function SegmentationConsole() {
  const [apiBase, setApiBase] = useState("http://localhost:8000");
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [overviewError, setOverviewError] = useState(false);
  const [view, setView] = useState("overview");

  const [clusters, setClusters] = useState([]);
  const [personas, setPersonas] = useState([]);
  const [recs, setRecs] = useState([]);

  const [customerId, setCustomerId] = useState("");
  const [lookupResult, setLookupResult] = useState(null);
  const [lookupError, setLookupError] = useState(false);

  const [predictData, setPredictData] = useState(defaultPredictState());
  const [predictResult, setPredictResult] = useState(null);
  const [predictError, setPredictError] = useState(false);

  const [evaluation, setEvaluation] = useState({
  silhouette: 0.472,
  davies: 0.813,
  calinski: 14284,
  optimal_k: 4,

  plots: {
    elbow: "/customer-segmentation-agent/plots/elbow.png",
    silhouette: "/customer-segmentation-agent/plots/silhouette.png",
    credit: "/customer-segmentation-agent/plots/credit_score_distribution.png",
    heatmap: "/customer-segmentation-agent/plots/correlation_heatmap.png",
  }
});

  const loadOverview = useCallback(async (base) => {
    try {
      const [c, p, r] = await Promise.all([
        fetch(base + "/clusters").then(res => res.json()),
        fetch(base + "/personas").then(res => res.json()),
        fetch(base + "/recommendations").then(res => res.json()),
      ]);
      setClusters(c);
      setPersonas(p);
      setRecs(r);
      setOverviewError(false);
    } catch (e) {
      setOverviewError(true);
      setClusters([]); setPersonas([]); setRecs([]);
    }
  }, []);

  const connect = useCallback(async () => {
    setConnecting(true);
    const base = apiBase.replace(/\/$/, "");
    try {
      const res = await fetch(base + "/");
      if (!res.ok) throw new Error("bad status");
      setConnected(true);
      setOverviewError(false);
      await loadOverview(base);
    } catch (e) {
      setConnected(false);
      setOverviewError(true);
    } finally {
      setConnecting(false);
    }
  }, [apiBase, loadOverview]);

  useEffect(() => { connect(); /* eslint-disable-next-line */ }, []);

  const personaMap = {};
  personas.forEach(p => { personaMap[p.cluster] = p.persona; });
  const recMap = {};
  recs.forEach(r => { recMap[r.cluster] = r.recommended_products; });

  const totalCustomers = clusters.reduce((s, c) => s + Number(c.customers || 0), 0);
  const avgCredit = totalCustomers ? clusters.reduce((s, c) => s + Number(c.average_credit_score || 0) * Number(c.customers || 0), 0) / totalCustomers : 0;
  const avgIncome = totalCustomers ? clusters.reduce((s, c) => s + Number(c.average_income || 0) * Number(c.customers || 0), 0) / totalCustomers : 0;
  const maxCount = Math.max(...clusters.map(c => Number(c.customers || 0)), 1);

  async function doLookup() {
    setLookupError(false);
    setLookupResult(null);
    if (!customerId.trim()) return;
    const base = apiBase.replace(/\/$/, "");
    try {
      const res = await fetch(base + "/customers/" + encodeURIComponent(customerId.trim()));
      if (!res.ok) throw new Error("not found");
      const data = await res.json();
      setLookupResult(data);
    } catch (e) {
      setLookupError(true);
    }
  }

  function updatePredictField(name, value) {
    setPredictData(prev => ({ ...prev, [name]: value }));
  }

  function fillSample() {
    setPredictData(defaultPredictState());
  }

  async function submitPredict(e) {
    e.preventDefault();
    setPredictError(false);
    setPredictResult(null);
    const base = apiBase.replace(/\/$/, "");
    const payload = {};
    PREDICT_FIELDS.forEach(f => {
      payload[f.name] = f.type === "select" ? predictData[f.name] : Number(predictData[f.name]);
    });
    try {
      const res = await fetch(base + "/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("predict failed");
      const data = await res.json();
      setPredictResult(data);
    } catch (e) {
      setPredictError(true);
    }
  }

  const navItems = [
    { key: "overview", num: "01", label: "Overview" },
    { key: "lookup", num: "02", label: "Find Customer" },
    { key: "predict", num: "03", label: "New Customer" },
    { key: "evaluation", num: "04", label: "Model Evaluation" },
  ];

  return (
    <div className="sc-root">
      <Styles />

      <aside className="sc-rail">
        <div className="sc-brand">
          <span className="sc-mark">§</span>
          <div><small>Segmentation Console</small></div>
        </div>

        <nav className="sc-nav">
          {navItems.map(item => (
            <button
              key={item.key}
              className={"sc-navbtn" + (view === item.key ? " active" : "")}
              onClick={() => setView(item.key)}
            >
              <span className="n">{item.num}</span> {item.label}
            </button>
          ))}
        </nav>

        <div className="sc-foot">
          <div className="sc-conn">
            <div className="sc-connrow">
              <span className={"sc-dot" + (connecting ? "" : connected ? " ok" : " bad")} />
              <span>{connecting ? "Connecting…" : connected ? "Connected" : "Not connected"}</span>
            </div>
            <label>API base URL</label>
            <input
              value={apiBase}
              onChange={e => setApiBase(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter") connect(); }}
              spellCheck={false}
            />
            <button onClick={connect}>Connect</button>
          </div>
        </div>
      </aside>

      <main className="sc-main">
        {view === "evaluation" && (

<section>

<div className="sc-eyebrow">
Model Diagnostics
</div>

<h1 className="sc-h1">
Model Evaluation
</h1>

<p className="sc-sub">
Performance metrics and visual evaluation of the clustering model.
</p>

<div className="sc-metricgrid">

<div className="sc-kpi">
<div className="num">
{evaluation.silhouette.toFixed(3)}
</div>
<div className="label">
Silhouette Score
</div>
</div>

<div className="sc-kpi">
<div className="num">
{evaluation.davies.toFixed(3)}
</div>
<div className="label">
Davies-Bouldin
</div>
</div>

<div className="sc-kpi">
<div className="num">
{evaluation.calinski.toLocaleString()}
</div>
<div className="label">
Calinski-Harabasz
</div>
</div>

<div className="sc-kpi">
<div className="num">
{evaluation.optimal_k}
</div>
<div className="label">
Optimal K
</div>
</div>

</div>


<div className="sc-sectiontitle">
Evaluation Plots
</div>

<div className="sc-plotgrid">

<div className="sc-plot">
<h3>Elbow Curve</h3>
<img src={evaluation.plots.elbow} alt="" />
</div>

<div className="sc-plot">
<h3>Silhouette Analysis</h3>
<img src={evaluation.plots.silhouette} alt="" />
</div>

<div className="sc-plot">
<h3>Credit Score Distribution</h3>
<img src={evaluation.plots.credit} alt="" />
</div>

<div className="sc-plot">
<h3>Correlation Heatmap</h3>
<img src={evaluation.plots.heatmap} alt="" />
</div>

</div>


<div
className="sc-sectiontitle"
style={{marginTop:40}}
>
Cluster Statistics
</div>

<table className="sc-table">

<thead>

<tr>

<th>Cluster</th>

<th>Customers</th>

<th>Income</th>

<th>Balance</th>

<th>Credit Score</th>

</tr>

</thead>

<tbody>

{clusters.map(c=>(

<tr key={c.cluster}>

<td>{c.cluster}</td>

<td>{c.customers}</td>

<td>${Math.round(c.average_income).toLocaleString()}</td>

<td>${Math.round(c.average_balance).toLocaleString()}</td>

<td>{Math.round(c.average_credit_score)}</td>

</tr>

))}

</tbody>

</table>

</section>

)}

        {view === "overview" && (
          <section>
            <div className="sc-eyebrow">Portfolio Summary</div>
            <h1 className="sc-h1">Customer segments, at a glance</h1>
            <p className="sc-sub">Clusters derived from behavioural and financial attributes, profiled and mapped to personas and product recommendations.</p>
            {overviewError && <div className="sc-banner" style={{ marginTop: 16 }}>Could not reach the API. Check the base URL and that the server is running.</div>}

            <div className="sc-kpis" style={{ marginTop: 24 }}>
              <div className="sc-kpi"><div className="num">{totalCustomers.toLocaleString()}</div><div className="label">Total customers</div></div>
              <div className="sc-kpi"><div className="num">{clusters.length}</div><div className="label">Segments</div></div>
              <div className="sc-kpi"><div className="num">{Math.round(avgCredit)}</div><div className="label">Avg. credit score</div></div>
              <div className="sc-kpi"><div className="num">${Math.round(avgIncome).toLocaleString()}</div><div className="label">Avg. income</div></div>
            </div>

            <div className="sc-sectiontitle">Segment distribution</div>
            <div style={{ marginBottom: 36 }}>
              {clusters.length === 0
                ? <div className="sc-loading">No data loaded.</div>
                : [...clusters].sort((a, b) => b.customers - a.customers).map(c => (
                  <div className="sc-barrow" key={c.cluster}>
                    <div className="name">{personaMap[c.cluster] || `Cluster ${c.cluster}`}</div>
                    <div className="sc-track"><div className="sc-fill" style={{ width: `${(Number(c.customers) / maxCount * 100).toFixed(1)}%` }} /></div>
                    <div className="count">{Number(c.customers).toLocaleString()}</div>
                  </div>
                ))}
            </div>

            <div className="sc-sectiontitle">Persona ledger</div>
            <div className="sc-seggrid">
              {clusters.map(c => {
                const persona = personaMap[c.cluster] || `Cluster ${c.cluster}`;
                const products = (recMap[c.cluster] || "").split(",").map(s => s.trim()).filter(Boolean).slice(0, 4);
                return (
                  <div className="sc-card" key={c.cluster}>
                    <div className="sc-cardhead">
                      <div>
                        <div className="sc-persona">{persona}</div>
                        <div className="sc-count">Segment {c.cluster} · {Number(c.customers).toLocaleString()} customers</div>
                      </div>
                      <div className="sc-seal">{c.cluster}</div>
                    </div>
                    <div className="sc-stats">
                      <div><div className="sc-statlabel">Avg. income</div><div className="sc-statval">${Math.round(c.average_income).toLocaleString()}</div></div>
                      <div><div className="sc-statlabel">Avg. balance</div><div className="sc-statval">${Math.round(c.average_balance).toLocaleString()}</div></div>
                      <div><div className="sc-statlabel">Credit score</div><div className="sc-statval">{Math.round(c.average_credit_score)}</div></div>
                      <div><div className="sc-statlabel">Digital score</div><div className="sc-statval">{Math.round(c.average_digital_score)}</div></div>
                    </div>
                    <div className="sc-chips">{products.map(p => <span className="sc-chip" key={p}>{p}</span>)}</div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {view === "lookup" && (
          <section>
            <div className="sc-eyebrow">Directory Lookup</div>
            <h1 className="sc-h1">Find a customer</h1>
            <p className="sc-sub">Look up an existing customer by ID to see their segment, persona, and recommended products.</p>

            <div className="sc-searchrow" style={{ marginTop: 24 }}>
              <input
                placeholder="Customer ID, e.g. 1"
                value={customerId}
                onChange={e => setCustomerId(e.target.value)}
                onKeyDown={e => { if (e.key === "Enter") doLookup(); }}
              />
              <button className="sc-btn" onClick={doLookup}>Search</button>
            </div>

            {lookupError && <div className="sc-banner">Customer not found, or the API could not be reached.</div>}

            {lookupResult && (
              <div>
                <div className="sc-resulthead">
                  <div className="sc-seal">{lookupResult.customer.cluster}</div>
                  <div>
                    <h2>{lookupResult.persona}</h2>
                    <div className="cid">Customer #{lookupResult.customer.customer_id} · Segment {lookupResult.customer.cluster}</div>
                  </div>
                </div>
                <div className="sc-profilegrid">
                  <div><div className="sc-statlabel">Age</div><div className="sc-statval">{lookupResult.customer.age}</div></div>
                  <div><div className="sc-statlabel">Job</div><div className="sc-statval">{lookupResult.customer.job || "—"}</div></div>
                  <div><div className="sc-statlabel">Annual income</div><div className="sc-statval">${Math.round(lookupResult.customer.annual_income).toLocaleString()}</div></div>
                  <div><div className="sc-statlabel">Credit score</div><div className="sc-statval">{Math.round(lookupResult.customer.credit_score)}</div></div>
                  <div><div className="sc-statlabel">Account balance</div><div className="sc-statval">${Math.round(lookupResult.customer.account_balance).toLocaleString()}</div></div>
                  <div><div className="sc-statlabel">Digital banking score</div><div className="sc-statval">{Math.round(lookupResult.customer.digital_banking_score)}</div></div>
                  <div><div className="sc-statlabel">Monthly transactions</div><div className="sc-statval">{lookupResult.customer.monthly_transactions}</div></div>
                  <div><div className="sc-statlabel">Account tenure</div><div className="sc-statval">{lookupResult.customer.account_tenure} yrs</div></div>
                  <div><div className="sc-statlabel">Products held</div><div className="sc-statval">{lookupResult.customer.number_of_products}</div></div>
                </div>
                <div className="sc-sectiontitle" style={{ fontSize: 13 }}>Recommended products</div>
                <div className="sc-chips">
                  {(lookupResult.recommendations || "").split(",").map(s => s.trim()).filter(Boolean).map(p => (
                    <span className="sc-chip" key={p}>{p}</span>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {view === "predict" && (
          <section>
            <div className="sc-eyebrow">Live Scoring</div>
            <h1 className="sc-h1">Score a new customer</h1>
            <p className="sc-sub">Enter a customer profile to predict their segment and generate personalized product recommendations.</p>

            <div className="sc-panel" style={{ marginTop: 24 }}>
              <form onSubmit={submitPredict}>
                <div className="sc-formgrid">
                  {PREDICT_FIELDS.map(f => (
                    <div className="sc-field" key={f.name}>
                      <label>{f.label}</label>
                      {f.type === "select" ? (
                        <select value={predictData[f.name]} onChange={e => updatePredictField(f.name, e.target.value)}>
                          {f.options.map(o => <option value={o} key={o}>{o}</option>)}
                        </select>
                      ) : (
                        <input type="number" step="any" value={predictData[f.name]} onChange={e => updatePredictField(f.name, e.target.value)} />
                      )}
                    </div>
                  ))}
                </div>
                <div className="sc-formactions">
                  <button className="sc-btn" type="submit">Predict segment</button>
                  <button className="sc-btn ghost" type="button" onClick={fillSample}>Fill sample</button>
                </div>
              </form>
            </div>

            {predictError && <div className="sc-banner" style={{ marginTop: 20 }}>Prediction failed. Check the API connection and that all fields are filled.</div>}

            {predictResult && (
              <div style={{ marginTop: 26 }}>
                <div className="sc-resulthead">
                  <div className="sc-seal">{predictResult.predicted_cluster}</div>
                  <div>
                    <h2>{predictResult.persona}</h2>
                    <div className="cid">Predicted segment {predictResult.predicted_cluster}</div>
                  </div>
                </div>
                {predictResult.warnings && predictResult.warnings.length > 0 && (
                  <div className="sc-warn">
                    {predictResult.warnings.map((w, i) => <div key={i}>⚠ {w}</div>)}
                  </div>
                )}
                <div className="sc-sectiontitle" style={{ fontSize: 13 }}>Recommendations</div>
                <div className="sc-reclist">
                  {(predictResult.recommendations || []).length === 0
                    ? <div className="sc-empty">No recommendations generated.</div>
                    : predictResult.recommendations.map((r, i) => (
                      <div className="sc-rec" key={i}>
                        <div className="rtitle">{r.title}</div>
                        <div className="rcat">{r.category}</div>
                        <div className="rreason">{r.reason}</div>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
