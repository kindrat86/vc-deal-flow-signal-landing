// GitDealFlow Comparison SVG Chart — Side by side
// https://gitdealflow.com/api/chart/compare?startups=medusajs,fleetbase

const API = "https://signals.gitdealflow.com/api/signals.json";
const TIMEOUT = 8000;
const CM = "#64748b", CF = "#f1f5f9";
const CA1 = "#60a5fa", CA2 = "#22c55e", CB = "#1e293b", CGr = "#1e293b", CY = "#eab308";

function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[c]); }
function trunc(s, n) { return s.length > n ? s.slice(0, n) + "..." : s; }
function genData(v, c) {
  const b = parseInt(v) || 50;
  const p = parseFloat(String(c).replace(/%/g, "")) || 0;
  return [5,4,3,2,1,0].map(i => Math.max(1, Math.round(b * (1 + (p/100)*(i/5)) * (1 - (5-i)*0.08))));
}

async function fetchAll() {
  const r = await fetch(API, { signal: AbortSignal.timeout(TIMEOUT) });
  const j = await r.json();
  const all = {};
  (j.trending || []).forEach(s => { if (s.name) all[s.name.toLowerCase().replace(/[\s-]/g,"")] = s; });
  for (const sec of (j.sectors || [])) {
    if (sec.startups) sec.startups.forEach(s => { if (s.name) all[s.name.toLowerCase().replace(/[\s-]/g,"")] = s; });
  }
  return Object.values(all);
}
function match(all, slug) { return all.find(s => { const n = (s.name||"").toLowerCase().replace(/[\s-]/g,""); return n === slug || n.includes(slug) || slug.includes(n); }); }

function render(startups) {
  const W = 800, H = 360, M = { t: 50, r: 15, b: 45, l: 50 };
  const hW = (W - M.l - M.r) / 2, CH = H - M.t - M.b;
  const sets = startups.slice(0,2).map((s,i) => ({...s, data: genData(s.commitVelocity14d, s.commitVelocityChange), color: i===0? CA1 : CA2 }));
  const mV = Math.max(...sets.flatMap(d=>d.data), 10);
  const ys = v => M.t + CH - (v/mV)*CH;
  let e = "";

  sets.forEach((ds, idx) => {
    const ox = M.l + idx*hW, bw = Math.max(8, (hW/ds.data.length)*0.5);
    if (idx === 0) for (let i=0;i<=4;i++) { const v=Math.round((mV/4)*i), y=ys(v); e += `<text x="${M.l-8}" y="${y+4}" fill="${CM}" font-size="9" text-anchor="end">${v}</text>`; if(i>0) e += `<line x1="${M.l}" y1="${y}" x2="${W-M.r}" y2="${y}" stroke="${CGr}" stroke-width="0.5"/>`; }
    ds.data.forEach((v,i) => { const x=ox+(i/(ds.data.length-1))*hW-bw/2,y=ys(v),h=CH-(y-M.t); e += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" fill="${ds.color}" rx="2" opacity="0.85"/>`; });
    const vC = parseFloat(String(ds.commitVelocityChange).replace(/%/g, ""))||0, arrow = vC>=0 ? "▲":"▼", cc = vC>=0 ? "#22c55e":"#ef4444";
    e += `<text x="${ox+hW/2}" y="22" fill="${CF}" font-size="14" font-weight="bold" text-anchor="middle" font-family="system-ui,sans-serif">${esc(trunc(ds.name,18))}</text>`;
    e += `<text x="${ox+hW/2}" y="${H-M.b+16}" fill="${cc}" font-size="10" text-anchor="middle">${arrow} ${Math.abs(vC).toFixed(1)}%</text>`;
    e += `<text x="${ox+10}" y="${H-8}" fill="${CM}" font-size="9">Vel: <tspan fill="${CF}" font-weight="bold">${esc(ds.commitVelocity14d||"—")}</tspan></text>`;
  });

  const v0=parseInt(sets[0]?.commitVelocity14d)||0, v1=parseInt(sets[1]?.commitVelocity14d)||0;
  if (sets.length===2 && v0!==v1) { const wi=v0>v1?0:1; e += `<circle cx="${M.l+wi*hW+hW/2+45}" cy="14" r="10" fill="${CY}"/><text x="${M.l+wi*hW+hW/2+45}" y="18" fill="#0b1120" font-size="10" font-weight="bold" text-anchor="middle">#1</text>`; }

  e += `<line x1="${M.l+hW}" y1="45" x2="${M.l+hW}" y2="${H-M.b}" stroke="${CGr}" stroke-width="0.5" stroke-dasharray="4,4"/>`;
  e += `<text x="${W-10}" y="${H-8}" fill="${CM}" font-size="8" text-anchor="end">GitDealFlow.com</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><linearGradient id="bg"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#0b1120"/></linearGradient></defs><rect width="${W}" height="${H}" fill="url(#bg)" rx="8"/><rect x="0.5" y="0.5" width="${W-1}" height="${H-1}" fill="none" stroke="${CB}" stroke-width="1" rx="8"/>${e}</svg>`;
}

export default async function handler(req, res) {
  const raw = (req.query.startups || "").trim();
  const slugs = raw.split(",").map(s => s.trim().toLowerCase()).filter(Boolean);
  res.setHeader("Content-Type", "image/svg+xml; charset=utf-8");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "public, max-age=3600, s-maxage=7200");

  if (slugs.length < 2) return res.status(200).send(`<svg xmlns="http://www.w3.org/2000/svg" width="600" height="280"><rect width="600" height="280" fill="#0b1120" rx="8"/><text x="300" y="130" fill="#64748b" font-size="14" text-anchor="middle">Compare two startups</text><text x="300" y="152" fill="#475569" font-size="11" text-anchor="middle">?startups=medusajs,fleetbase</text><text x="300" y="260" fill="#60a5fa" font-size="11" text-anchor="middle">GitDealFlow ↗</text></svg>`);
  try {
    const all = await fetchAll();
    const found = slugs.map(slug => match(all, slug)).filter(Boolean);
    if (found.length < 2) return res.status(200).send(`<svg xmlns="http://www.w3.org/2000/svg" width="600" height="280"><rect width="600" height="280" fill="#0b1120" rx="8"/><text x="300" y="130" fill="#64748b" font-size="14" text-anchor="middle">Could not find both startups</text><text x="300" y="155" fill="#475569" font-size="11" text-anchor="middle">Check names at gitdealflow.com/explorer</text><text x="300" y="260" fill="#60a5fa" font-size="11" text-anchor="middle">GitDealFlow ↗</text></svg>`);
    res.status(200).send(render(found));
  } catch(e) {
    res.status(200).send(`<svg xmlns="http://www.w3.org/2000/svg" width="600" height="280"><rect width="600" height="280" fill="#0b1120" rx="8"/><text x="300" y="130" fill="#64748b" font-size="14" text-anchor="middle">Data temporarily unavailable</text><text x="300" y="260" fill="#60a5fa" font-size="11" text-anchor="middle">GitDealFlow ↗</text></svg>`);
  }
}
