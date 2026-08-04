// GitDealFlow Scout Score API
// Serves dynamic SVG badges or JSON data for a GitHub user's Scout Score.
//
// Usage:
//   /api/scout-score?user=USERNAME             → SVG badge
//   /api/scout-score?user=USERNAME&format=json  → JSON

async function fetchScoutScore(username) {
  const url = 'https://signals.gitdealflow.com/api/mcp/rpc';
  const body = JSON.stringify({
    jsonrpc: '2.0',
    method: 'tools/call',
    params: {
      name: 'get_scout_receipts',
      arguments: { github_username: username }
    },
    id: 1
  });

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body
  });

  if (!res.ok) throw new Error(`MCP API responded with ${res.status}`);

  const data = await res.json();
  const text = data?.result?.content?.[0]?.text || '';

  try {
    return JSON.parse(text);
  } catch {
    const match = text.match(/\b(\d{1,3})\b/);
    return {
      scout_score: match ? parseInt(match[1]) : 0,
      summary: text.slice(0, 300)
    };
  }
}

function getLevel(score) {
  if (score >= 85) return 'Maven';
  if (score >= 65) return 'Elite';
  if (score >= 40) return 'Scout';
  if (score >= 20) return 'Tracker';
  return 'Novice';
}

function renderSvgBadge(username, score, level) {
  const width = 320;
  const height = 160;
  const accent = '#60a5fa';
  const bg = '#0b1120';
  const fg = '#f1f5f9';
  const muted = '#94a3b8';
  const border = '#1e293b';

  const levelColors = {
    'Novice': '#94a3b8',
    'Tracker': '#fbbf24',
    'Scout': '#60a5fa',
    'Elite': '#a78bfa',
    'Maven': '#22c55e'
  };
  const levelColor = levelColors[level] || accent;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#60a5fa"/>
      <stop offset="100%" stop-color="#a78bfa"/>
    </linearGradient>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="${bg}"/>
      <stop offset="100%" stop-color="#0d1426"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="${width - 1}" height="${height - 1}" rx="12" fill="url(#bg)" stroke="${border}" stroke-width="1"/>
  <!-- Top accent bar -->
  <rect x="0" y="0" width="${width}" height="3" fill="url(#g)" rx="1.5"/>
  <!-- Score -->
  <text x="160" y="58" font-family="system-ui, -apple-system, sans-serif" font-size="44" font-weight="800" fill="url(#g)" text-anchor="middle">${score}</text>
  <text x="160" y="76" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="${muted}" text-anchor="middle" letter-spacing="1">SCOUT SCORE / 100</text>
  <!-- Level badge -->
  <rect x="${160 - (level.length * 5 + 16)}" y="84" width="${level.length * 10 + 32}" height="22" rx="11" fill="${levelColor}20" stroke="${levelColor}40" stroke-width="1"/>
  <text x="160" y="98" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="${levelColor}" text-anchor="middle" letter-spacing="1">${level.toUpperCase()}</text>
  <!-- Username -->
  <text x="160" y="130" font-family="ui-monospace, 'SF Mono', monospace" font-size="11" fill="${fg}" text-anchor="middle">@${username}</text>
  <!-- Footer -->
  <text x="${width - 12}" y="${height - 8}" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="${muted}" text-anchor="end">gitdealflow.com/scout</text>
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

  const username = req.query.user;
  if (!username) {
    if (req.query.format === 'json') {
      return res.status(400).json({ error: 'Missing user parameter' });
    }
    // Return an error SVG
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    return res.status(200).send(
      `<svg xmlns="http://www.w3.org/2000/svg" width="320" height="80" viewBox="0 0 320 80">
        <rect width="320" height="80" rx="8" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
        <text x="160" y="42" font-family="system-ui, sans-serif" font-size="12" fill="#f87171" text-anchor="middle">Missing ?user= parameter</text>
        <text x="160" y="62" font-family="system-ui, sans-serif" font-size="9" fill="#64748b" text-anchor="middle">Usage: /api/scout-score?user=GITHUB_USERNAME</text>
      </svg>`
    );
  }

  // Sanitize username
  const sanitized = username.replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 39);
  if (!sanitized) {
    return res.status(400).json({ error: 'Invalid GitHub username' });
  }

  try {
    const data = await fetchScoutScore(sanitized);
    const score = data.scout_score !== undefined ? data.scout_score : (data.score || 0);
    const level = getLevel(score);

    // JSON response
    if (req.query.format === 'json') {
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.setHeader('Cache-Control', 'public, s-maxage=300, max-age=60, stale-while-revalidate=3600');
      return res.status(200).json({
        user: sanitized,
        scout_score: score,
        level,
        summary: data.summary || data.description || '',
        percentile: data.percentile || null,
        startups: data.startups || data.matches || []
      });
    }

    // SVG badge response
    const svg = renderSvgBadge(sanitized, score, level);
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=300, max-age=60, stale-while-revalidate=3600');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Content-Disposition', 'inline');
    return res.status(200).send(svg);

  } catch (err) {
    if (req.query.format === 'json') {
      return res.status(502).json({ error: 'Failed to fetch scout score', detail: err.message });
    }
    // Error SVG
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    return res.status(200).send(
      `<svg xmlns="http://www.w3.org/2000/svg" width="320" height="80" viewBox="0 0 320 80">
        <rect width="320" height="80" rx="8" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
        <text x="160" y="36" font-family="system-ui, sans-serif" font-size="11" fill="#f87171" text-anchor="middle">Error fetching score</text>
        <text x="160" y="56" font-family="system-ui, sans-serif" font-size="9" fill="#64748b" text-anchor="middle">${err.message.slice(0, 50)}</text>
        <text x="160" y="70" font-family="system-ui, sans-serif" font-size="8" fill="#475569" text-anchor="middle">Visit gitdealflow.com/scout to check</text>
      </svg>`
    );
  }
}
