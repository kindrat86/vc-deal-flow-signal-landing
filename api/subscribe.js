// GitDealFlow Newsletter Subscription API
// Accepts POST with {email, source} — stores in /tmp/subscribers.json
// Vercel serverless: /tmp is writable per-instance

const FS = require('fs');
const PATH = require('path');

const DATA_FILE = '/tmp/subscribers.json';

// Simple email regex
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function json(res, code, data) {
  const body = JSON.stringify(data) + '\n';
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  });
  res.end(body);
}

function loadSubscribers() {
  try {
    if (FS.existsSync(DATA_FILE)) {
      const raw = FS.readFileSync(DATA_FILE, 'utf-8');
      return JSON.parse(raw);
    }
  } catch (_) {}
  return { subscribers: [] };
}

function saveSubscribers(data) {
  FS.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

module.exports = (req, res) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    });
    res.end();
    return;
  }

  // Only accept POST
  if (req.method !== 'POST') {
    json(res, 405, { error: 'Method not allowed' });
    return;
  }

  // Parse body
  let body = '';
  req.on('data', chunk => { body += chunk; });
  req.on('end', () => {
    let payload;
    try {
      payload = JSON.parse(body);
    } catch (_) {
      json(res, 400, { error: 'Invalid JSON' });
      return;
    }

    const email = (payload.email || '').trim().toLowerCase();
    const source = (payload.source || '').trim() || 'unknown';

    // Validate email
    if (!email || !EMAIL_RE.test(email)) {
      json(res, 400, { error: 'Invalid email' });
      return;
    }

    // Load, append, save
    const db = loadSubscribers();
    const exists = db.subscribers.some(s => s.email === email);

    if (!exists) {
      db.subscribers.push({
        email,
        source,
        subscribed_at: new Date().toISOString(),
      });
      saveSubscribers(db);
    }

    // Always return success — don't reveal whether email existed
    json(res, 200, { success: true, message: 'Confirmed!' });
  });
};
