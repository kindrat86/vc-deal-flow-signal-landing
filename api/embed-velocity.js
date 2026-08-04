// Vercel Serverless Function — serves the embed widget with iframe-friendly headers
// Vercel platform forces X-Frame-Options: DENY on static files but serverless
// functions can override it completely.
export default function handler(req, res) {
  // Read the embed HTML template
  const fs = require('fs');
  const path = require('path');
  
  // Resolve to the embed HTML file
  const embedPath = path.join(process.cwd(), 'embed', 'check-velocity', 'index.html');
  
  let html;
  try {
    html = fs.readFileSync(embedPath, 'utf-8');
  } catch(e) {
    // Try alternate path
    try {
      const altPath = path.join(process.cwd(), 'public', 'embed', 'check-velocity', 'index.html');
      html = fs.readFileSync(altPath, 'utf-8');
    } catch(e2) {
      res.status(500).send('Embed widget not found');
      return;
    }
  }

  // Set iframe-friendly headers — these override Vercel's defaults
  res.setHeader('X-Frame-Options', 'ALLOWALL');
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://signals.gitdealflow.com; frame-ancestors *");
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');
  
  res.status(200).send(html);
}
