// GitDealFlow Startup SVG Badge API
// Serves individual SVG badges for each of 324+ tracked startups
// Usage: <img src="https://gitdealflow.com/api/badge/startup/{slug}">
// Viral backlink loop: founders embed their badge in GitHub READMEs

const SIGNALS_URL = 'https://signals.gitdealflow.com/api/signals.json';

// Signal type → badge color
const SIGNAL_COLORS = {
  'Engineering hiring burst': '#22c55e',
  'Deploy frequency spike': '#3b82f6',
  'Infrastructure buildout': '#f59e0b',
  'Framework migration': '#6b7280',
};

const DEFAULT_SIGNAL_COLOR = '#94a3b8';

// Stage → badge color
const STAGE_COLORS = {
  'Pre-seed': '#a78bfa',
  'Seed': '#60a5fa',
  'Series A/B': '#f59e0b',
  'Growth': '#22c55e',
};

// Simple in-memory cache per instance
let cachedData = null;
let cachedAt = 0;
const CACHE_TTL = 10 * 60 * 1000; // 10 min

async function getSignalsData() {
  const now = Date.now();
  if (cachedData && (now - cachedAt) < CACHE_TTL) {
    return cachedData;
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000);

  let res;
  try {
    res = await fetch(SIGNALS_URL, { signal: controller.signal });
  } finally {
    clearTimeout(timeoutId);
  }

  if (!res.ok) {
    throw new Error(`signals.json returned ${res.status} ${res.statusText}`);
  }

  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch (e) {
    throw new Error(`JSON parse failed: ${e.message.slice(0, 100)}`);
  }

  if (!json.sectors || !Array.isArray(json.sectors)) {
    throw new Error(`sectors not found in response, keys: ${Object.keys(json).join(', ')}`);
  }

  // Build a startup-by-slug map that includes sector info
  const startupMap = {};
  const startupList = [];

  for (const sector of json.sectors) {
    if (!sector.startups || !Array.isArray(sector.startups)) continue;
    for (const s of sector.startups) {
      // Derive slug: last segment of profileUrl, or lowercased name
      let slug;
      if (s.profileUrl) {
        slug = s.profileUrl.split('/').pop();
      } else {
        slug = s.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
      }

      const entry = { ...s, sector: sector.name, sectorSlug: sector.slug };
      startupMap[slug] = entry;
      startupMap[s.name.toLowerCase()] = entry;
      startupList.push({ slug, name: s.name, sector: sector.name });
    }
  }

  cachedData = { meta: json.meta, startupMap, startupList };
  cachedAt = Date.now();
  return cachedData;
}

function normalizeSlug(str) {
  return String(str).toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function escHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderBadge(startup) {
  const W = 280;
  const H = 120;
  const BG = '#0b1120';
  const BORDER = '#1e293b';
  const FG = '#f1f5f9';
  const MUTED = '#94a3b8';

  const signalColor = SIGNAL_COLORS[startup.signalType] || DEFAULT_SIGNAL_COLOR;
  const stageColor = STAGE_COLORS[startup.stage] || '#94a3b8';

  const title = startup.name.length > 24
    ? startup.name.slice(0, 22) + '…'
    : startup.name;
  const vChange = String(startup.commitVelocityChange || 'N/A');
  const vChangeColor = vChange.startsWith('+') ? '#22c55e'
    : vChange.startsWith('-') ? '#ef4444'
    : '#f1f5f9';

  const sigLabel = startup.signalType && startup.signalType.length > 28
    ? startup.signalType.slice(0, 26) + '…'
    : (startup.signalType || 'Unknown');

  const stageLen = startup.stage ? startup.stage.length : 5;
  const stageBadgeW = Math.max(stageLen * 7 + 16, 60);

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="hdr" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${signalColor}" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="${signalColor}" stop-opacity="0.04"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="8" fill="${BG}" stroke="${BORDER}" stroke-width="1"/>
  <!-- Header accent bar -->
  <rect x="0" y="0" width="${W}" height="30" rx="8" fill="url(#hdr)"/>
  <rect x="0" y="22" width="${W}" height="8" fill="url(#hdr)"/>
  <circle cx="12" cy="15" r="4" fill="${signalColor}"/>
  <text x="24" y="19" font-family="system-ui,-apple-system,sans-serif" font-size="11" font-weight="700" fill="${FG}">${escHtml(title)}</text>
  <text x="${W - 12}" y="19" font-family="system-ui,-apple-system,sans-serif" font-size="7" fill="${signalColor}" text-anchor="end" font-weight="600">${escHtml(sigLabel)}</text>

  <!-- Metric columns -->
  <text x="12" y="50" font-family="ui-monospace,'SF Mono',monospace" font-size="7" fill="${MUTED}">Velocity Δ</text>
  <text x="12" y="68" font-family="system-ui,-apple-system,sans-serif" font-size="17" font-weight="800" fill="${vChangeColor}">${escHtml(vChange)}</text>

  <text x="105" y="50" font-family="ui-monospace,'SF Mono',monospace" font-size="7" fill="${MUTED}">Commits (14d)</text>
  <text x="105" y="68" font-family="system-ui,-apple-system,sans-serif" font-size="17" font-weight="800" fill="${FG}">${startup.commitVelocity14d}</text>

  <text x="198" y="50" font-family="ui-monospace,'SF Mono',monospace" font-size="7" fill="${MUTED}">Contributors</text>
  <text x="198" y="68" font-family="system-ui,-apple-system,sans-serif" font-size="17" font-weight="800" fill="${FG}">${startup.contributors}</text>

  <!-- Stage badge pill -->
  <rect x="12" y="84" width="${stageBadgeW}" height="18" rx="9" fill="${stageColor}18" stroke="${stageColor}40" stroke-width="1"/>
  <text x="${12 + stageBadgeW / 2}" y="96" font-family="system-ui,-apple-system,sans-serif" font-size="8" font-weight="700" fill="${stageColor}" text-anchor="middle">${escHtml(startup.stage || 'N/A')}</text>

  <!-- Sector name -->
  <text x="${12 + stageBadgeW + 10}" y="96" font-family="system-ui,-apple-system,sans-serif" font-size="8" fill="${MUTED}">${escHtml(startup.sector || '')}</text>

  <!-- Footer watermark -->
  <text x="${W - 12}" y="${H - 8}" font-family="system-ui,-apple-system,sans-serif" font-size="6" fill="#1e293b" text-anchor="end" font-weight="600">VC Deal Flow Signal</text>
</svg>`;
}

function renderNotFoundBadge() {
  const W = 280;
  const H = 120;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="ctaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#60a5fa"/>
      <stop offset="100%" stop-color="#a78bfa"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="8" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
  <text x="${W / 2}" y="36" font-family="system-ui,-apple-system,sans-serif" font-size="13" font-weight="700" fill="#f1f5f9" text-anchor="middle">🏷️ Create Your Own Badge</text>
  <text x="${W / 2}" y="56" font-family="system-ui,-apple-system,sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">Not yet tracked? Get your startup's</text>
  <text x="${W / 2}" y="70" font-family="system-ui,-apple-system,sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">engineering velocity checked for free</text>
  <rect x="82" y="84" width="116" height="22" rx="11" fill="url(#ctaGrad)"/>
  <text x="${W / 2}" y="98" font-family="system-ui,-apple-system,sans-serif" font-size="9" font-weight="800" fill="#0b1120" text-anchor="middle">→ Check Velocity</text>
  <text x="268" y="${H - 8}" font-family="system-ui,-apple-system,sans-serif" font-size="6" fill="#1e293b" text-anchor="end">gitdealflow.com/check-velocity</text>
</svg>`;
}

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Debug mode — returns JSON diagnostics
  if (req.query.debug === 'true') {
  try {
    const data = await getSignalsData();
    // Search filter
    const q = (req.query.search || '').toLowerCase();
    let matches = Object.entries(data.startupMap);
    if (q) {
      matches = matches.filter(([k, v]) => k.includes(q) || (v.name || '').toLowerCase().includes(q));
    }
    return res.status(200).json({
      ok: true,
      startupCount: Object.keys(data.startupMap).length,
      uniqueStartups: data.startupList.length,
      sampleSlugs: matches.slice(0, 30).map(([k]) => k),
      matchCount: matches.length,
      searchTerm: q || null,
      meta: data.meta,
    });
  } catch (err) {
    return res.status(500).json({ ok: false, error: err.message });
  }
  }

  const name = (req.query.name || '').trim();
  if (!name) {
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    return res.status(200).send(renderNotFoundBadge());
  }

  try {
    const { startupMap, meta } = await getSignalsData();

    // Try exact match first, then normalized slug
    const slug = normalizeSlug(name);
    let startup = startupMap[name.toLowerCase()] || startupMap[slug];

    // Fuzzy fallback
    if (!startup) {
      const q = name.toLowerCase();
      for (const [key, val] of Object.entries(startupMap)) {
        if (key.includes(q) || q.includes(key)) {
          startup = val;
          break;
        }
      }
    }

    if (startup) {
      const svg = renderBadge(startup);
      res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
      res.setHeader('Cache-Control', 'public, s-maxage=86400, max-age=3600, stale-while-revalidate=86400');
      res.setHeader('X-Content-Type-Options', 'nosniff');
      res.setHeader('Content-Disposition', 'inline');
      return res.status(200).send(svg);
    }

    // Not found
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=300, s-maxage=3600');
    return res.status(200).send(renderNotFoundBadge());

  } catch (err) {
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    return res.status(200).send(
      `<svg xmlns="http://www.w3.org/2000/svg" width="280" height="100" viewBox="0 0 280 100">
        <rect width="280" height="100" rx="8" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
        <text x="140" y="36" font-family="system-ui,sans-serif" font-size="11" fill="#f87171" text-anchor="middle">⚠ Error loading badge</text>
        <text x="140" y="56" font-family="system-ui,sans-serif" font-size="9" fill="#64748b" text-anchor="middle">${escHtml(err.message.slice(0, 60))}</text>
        <text x="140" y="74" font-family="system-ui,sans-serif" font-size="8" fill="#475569" text-anchor="middle">gitdealflow.com/startup-badges</text>
      </svg>`
    );
  }
}
