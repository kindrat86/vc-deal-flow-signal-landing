// GitDealFlow Stats SVG Badge
// Serves a dynamic SVG badge at /api/badge/stats
// Usage: <img src="https://gitdealflow.com/api/badge/stats">

const STATS = {
  startups: "400+",
  sectors: "20",
  signals: "1,200+",
  updated: "Weekly",
  source: "SSRN Research",
  ssrnId: "6606558",
  accent: "#60a5fa",
  bg: "#0b1120",
  fg: "#f1f5f9",
  muted: "#94a3b8",
  border: "#1e293b",
  width: 320,
  labelWidth: 160,
  valueX: 290,
};

function renderBadge() {
  const { width, valueX, accent, bg, fg, muted, border } = STATS;
  const rowH = 28;
  const headerH = 44;
  const footerH = 28;
  const rows = [
    { label: "Startups Tracked", value: STATS.startups },
    { label: "Sectors Monitored", value: STATS.sectors },
    { label: "Weekly Signals", value: STATS.signals },
    { label: "Updated", value: STATS.updated },
    { label: "Source", value: STATS.source },
  ];
  const badgeH = headerH + rows.length * rowH + footerH + 2;
  const rowStartY = 50;

  let rowsSvg = "";
  rows.forEach((row, i) => {
    const y = rowStartY + i * rowH;
    const isEven = i % 2 === 0;
    if (isEven) {
      rowsSvg += `<rect x="0" y="${y}" width="${width}" height="${rowH}" fill="rgba(255,255,255,0.02)"/>\n`;
    }
    rowsSvg += `<text x="16" y="${y + 18}" font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace" font-size="12" fill="${muted}">${row.label}</text>\n`;
    rowsSvg += `<text x="${valueX}" y="${y + 18}" font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace" font-size="12" fill="${fg}" text-anchor="end" font-weight="600">${row.value}</text>\n`;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${badgeH}" viewBox="0 0 ${width} ${badgeH}">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${accent}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="${accent}" stop-opacity="0.05"/>
    </linearGradient>
  </defs>

  <!-- Outer border -->
  <rect x="0.5" y="0.5" width="${width - 1}" height="${badgeH - 1}" rx="8" fill="${bg}" stroke="${border}" stroke-width="1"/>

  <!-- Header bar -->
  <rect x="0" y="0" width="${width}" height="${headerH}" rx="8" fill="url(#headerGrad)"/>
  <rect x="0" y="${headerH - 8}" width="${width}" height="8" fill="url(#headerGrad)"/>

  <!-- GitDealFlow logo mark — diamond/arrow -->
  <polygon points="16,12 22,22 16,32 10,22" fill="${accent}" opacity="0.9"/>
  <polygon points="22,14 27,22 22,30 17,22" fill="${accent}" opacity="0.4"/>

  <!-- Title -->
  <text x="36" y="22" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="${fg}">GitDealFlow</text>
  <text x="36" y="36" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="${muted}">Startup Engineering Signals</text>

  <!-- Stats rows -->
${rowsSvg}

  <!-- Footer -->
  <rect x="0" y="${rowStartY + rows.length * rowH}" width="${width}" height="${footerH}" fill="rgba(255,255,255,0.02)"/>
  <text x="16" y="${rowStartY + rows.length * rowH + 18}" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="${muted}">github.com/gitdealflow</text>
  <text x="${width - 16}" y="${rowStartY + rows.length * rowH + 18}" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="${accent}" text-anchor="end">SSRN ${STATS.ssrnId}</text>
</svg>`;
}

export default function handler(req, res) {
  // CORS headers
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  // Handle preflight
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // Serve the SVG badge
  res.setHeader("Content-Type", "image/svg+xml; charset=utf-8");

  // Cache: 1 hour CDN, 5 min browser, stale for 1 day during revalidation
  res.setHeader("Cache-Control", "public, s-maxage=3600, max-age=300, stale-while-revalidate=86400");

  // Security
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Content-Disposition", "inline");

  const svg = renderBadge();
  return res.status(200).send(svg);
}
