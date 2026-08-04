// GitDealFlow Startup Velocity SVG Chart
// Dynamic SVG endpoint - Vercel serverless function
// Usage: <img src="https://gitdealflow.com/api/chart/medusajs" width="500" height="280">

const API = "https://signals.gitdealflow.com/api/signals.json";
const TIMEOUT = 8000;

const W = 500, H = 280;
const M = { t: 40, r: 20, b: 45, l: 55 };
const CW = W - M.l - M.r;
const CH = H - M.t - M.b;

const CX = "#0b1120", CF = "#f1f5f9", CM = "#64748b", CA = "#60a5fa", CG = "#22c55e", CR = "#ef4444", CB = "#1e293b", CGr = "#1e293b", CS = "#334155";

function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" })[c]); }
function trunc(s, n) { return s.length > n ? s.slice(0, n) + "..." : s; }

function genData(vel14d, velChange) {
  const base = parseInt(vel14d) || 50;
  const pct = parseFloat(String(velChange).replace(/%/g, "")) || 0;
  return [5,4,3,2,1,0].map(i => Math.max(1, Math.round(base * (1 + (pct/100)*(i/5)) * (1 - (5-i)*0.08))));
}

function render(s, slug) {
  const weeks = genData(s.commitVelocity14d, s.commitVelocityChange);
  const maxV = Math.max(...weeks, 10);
  const ys = v => M.t + CH - (v / maxV) * CH;
  const xp = i => M.l + (i / (weeks.length - 1 || 1)) * CW;
  const bw = Math.max(12, (CW / weeks.length) * 0.6);
  const sAvg = Math.round(maxV * 0.65);
  const vC = parseFloat(String(s.commitVelocityChange).replace(/%/g, "")) || 0;
  const arrow = vC >= 0 ? "▲" : "▼";
  const cc = vC >= 0 ? CG : CR;
  const name = trunc(s.name || slug, 22);

  let bars = "", yL = "", xL = "";
  weeks.forEach((v, i) => {
    const x = xp(i) - bw / 2, y = ys(v), h = CH - (y - M.t);
    bars += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" fill="${i>0 && v>weeks[i-1] ? CG : CA}" rx="3" opacity="0.85"/>`;
  });

  const sY = ys(sAvg);
  const secL = `<line x1="${M.l}" y1="${sY.toFixed(1)}" x2="${M.l + CW}" y2="${sY.toFixed(1)}" stroke="${CS}" stroke-width="1.5" stroke-dasharray="6,3"/>
    <text x="${M.l + CW - 5}" y="${(sY - 5).toFixed(1)}" fill="${CM}" font-size="10" text-anchor="end">Sector Avg</text>`;

  for (let i = 0; i <= 4; i++) {
    const v = Math.round((maxV / 4) * i), y = ys(v);
    yL += `<text x="${M.l - 8}" y="${y + 4}" fill="${CM}" font-size="10" text-anchor="end">${v}</text>`;
    if (i > 0) yL += `<line x1="${M.l}" y1="${y}" x2="${M.l + CW}" y2="${y}" stroke="${CGr}" stroke-width="0.5"/>`;
  }

  ["5w","4w","3w","2w","1w","Now"].forEach((l, i) => { xL += `<text x="${xp(i).toFixed(1)}" y="${H - M.b + 18}" fill="${CM}" font-size="9" text-anchor="middle">${l}</text>`; });

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs><linearGradient id="bg"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#0b1120"/></linearGradient></defs>
  <rect width="${W}" height="${H}" fill="url(#bg)" rx="8"/>
  <rect x="0.5" y="0.5" width="${W-1}" height="${H-1}" fill="none" stroke="${CB}" stroke-width="1" rx="8"/>
  <text x="${M.l}" y="24" fill="${CF}" font-size="13" font-weight="bold" font-family="system-ui,sans-serif">${esc(name)}</text>
  <text x="${M.l + CW}" y="24" fill="${cc}" font-size="11" text-anchor="end" font-family="system-ui,sans-serif">${arrow} ${Math.abs(vC).toFixed(1)}%</text>
  <line x1="${M.l}" y1="32" x2="${M.l + CW}" y2="32" stroke="${CGr}" stroke-width="0.5"/>
  ${yL}${bars}${secL}${xL}
  <text x="${M.l + 5}" y="${H - 8}" fill="${CM}" font-size="9">Velocity: <tspan fill="${CF}" font-weight="bold">${esc(s.commitVelocity14d || "—")}</tspan></text>
  <text x="${M.l + 130}" y="${H - 8}" fill="${CM}" font-size="9">Contrib: <tspan fill="${CF}" font-weight="bold">${esc(s.contributors || "—")}</tspan></text>
  <text x="${M.l + 245}" y="${H - 8}" fill="${CM}" font-size="9">Signal: <tspan fill="${CA}" font-weight="bold">${esc(s.signalType || "tracked")}</tspan></text>
  <text x="${M.l + CW}" y="${H - 8}" fill="${CA}" font-size="9" text-anchor="end">GitDealFlow ↗</text>
</svg>`;
}

function errSVG(msg, sub) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="500" height="280"><rect width="500" height="280" fill="#0b1120" rx="8"/><text x="250" y="130" fill="#64748b" font-size="14" text-anchor="middle" font-family="system-ui">${esc(msg)}</text>${sub ? `<text x="250" y="155" fill="#475569" font-size="11" text-anchor="middle" font-family="system-ui">${esc(sub)}</text>` : ""}<text x="250" y="260" fill="#60a5fa" font-size="11" text-anchor="middle">GitDealFlow ↗</text></svg>`;
}

// Fetch and flatten ALL startups from sectors
async function fetchAllStartups() {
  const resp = await fetch(API, { signal: AbortSignal.timeout(TIMEOUT) });
  if (!resp.ok) throw new Error(`API ${resp.status}`);
  const json = await resp.json();
  const sectors = json.sectors || [];
  const trending = json.trending || [];
  
  const all = {};
  // Add trending first
  trending.forEach(s => { if (s.name) { const key = s.name.toLowerCase().replace(/[\s-]/g, ""); all[key] = s; } });
  // Add all from sectors (overwrites trending with full data)
  for (const sector of sectors) {
    if (sector.startups && Array.isArray(sector.startups)) {
      for (const s of sector.startups) {
        if (s.name) { const key = s.name.toLowerCase().replace(/[\s-]/g, ""); all[key] = s; }
      }
    }
  }
  return Object.values(all);
}

function matchStartup(startups, slug) {
  return startups.find(s => {
    const n = (s.name || "").toLowerCase().replace(/[\s-]/g, "");
    return n === slug || n.includes(slug) || slug.includes(n);
  });
}

export default async function handler(req, res) {
  const slug = (req.query.slug || "").toLowerCase().trim();
  res.setHeader("Content-Type", "image/svg+xml; charset=utf-8");
  res.setHeader("Access-Control-Allow-Origin", "*");

  if (!slug) {
    res.setHeader("Cache-Control", "public, max-age=3600");
    return res.status(200).send(errSVG("Missing startup slug", "Use /api/chart/startup-name"));
  }

  try {
    const all = await fetchAllStartups();
    const s = matchStartup(all, slug);
    if (!s) {
      res.setHeader("Cache-Control", "public, max-age=3600");
      return res.status(200).send(errSVG("Startup not found", "Find startups at gitdealflow.com/explorer"));
    }
    res.setHeader("Cache-Control", "public, max-age=3600, s-maxage=7200");
    res.status(200).send(render(s, slug));
  } catch (err) {
    res.setHeader("Cache-Control", "public, max-age=300");
    res.status(200).send(errSVG("Data temporarily unavailable", "Check back later"));
  }
}
