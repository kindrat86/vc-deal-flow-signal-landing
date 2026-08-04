// Vercel Serverless Function — serves the Scout Score embed widget with iframe-friendly headers.
// Vercel platform forces X-Frame-Options: DENY on static files but serverless
// functions can override it completely.

const EMBED_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VC Scout Score Widget</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:transparent;color:#e8eaed;line-height:1.5}
.widget{background:#0b1120;border:1px solid #1e293b;border-radius:16px;padding:1.25rem;max-width:100%}
.widget-header{display:flex;align-items:center;gap:.5rem;margin-bottom:.75rem}
.widget-header .logo{width:20px;height:20px;background:linear-gradient(135deg,#60a5fa,#a78bfa);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;font-weight:700}
.widget-header h3{font-size:.85rem;font-weight:600;color:#f1f5f9}
.input-row{display:flex;gap:.4rem;margin-bottom:.75rem}
.input-row input{flex:1;padding:.5rem .6rem;background:#0f172a;border:1px solid #1e293b;border-radius:8px;color:#f1f5f9;font-size:.8rem;outline:none;min-width:0}
.input-row input:focus{border-color:#60a5fa}
.input-row button{padding:.5rem .75rem;background:linear-gradient(135deg,#60a5fa,#a78bfa);border:none;border-radius:8px;color:#fff;font-size:.75rem;font-weight:600;cursor:pointer;white-space:nowrap}
.input-row button:hover{opacity:.9}
#widgetResult{display:none}
.score-display{text-align:center;padding:.75rem;background:#0f172a;border-radius:10px;margin-bottom:.5rem}
.score-value{font-size:2rem;font-weight:800;background:linear-gradient(135deg,#60a5fa,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1}
.score-label{color:#64748b;font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;margin-top:.25rem}
.score-level{display:inline-block;margin-top:.4rem;padding:.15rem .6rem;border-radius:999px;font-size:.65rem;font-weight:600}
.level-novice{background:rgba(100,116,139,0.15);color:#94a3b8;border:1px solid rgba(100,116,139,0.2)}
.level-tracker{background:rgba(251,191,36,0.1);color:#fbbf24;border:1px solid rgba(251,191,36,0.2)}
.level-scout{background:rgba(96,165,250,0.1);color:#60a5fa;border:1px solid rgba(96,165,250,0.2)}
.level-elite{background:rgba(167,139,250,0.1);color:#a78bfa;border:1px solid rgba(167,139,250,0.2)}
.level-maven{background:rgba(34,197,94,0.1);color:#22c55e;border:1px solid rgba(34,197,94,0.2)}
#widgetError{color:#f87171;font-size:.75rem;display:none;text-align:center;padding:.5rem;background:rgba(248,113,113,0.08);border-radius:8px;margin-bottom:.5rem}
#widgetLoading{display:none;text-align:center;color:#64748b;font-size:.75rem;padding:.5rem}
.powered{text-align:center;margin-top:.5rem;padding-top:.5rem;border-top:1px solid #1e293b}
.powered a{color:#475569;font-size:.65rem;text-decoration:none}
.powered a:hover{color:#60a5fa}
</style>
</head>
<body>
<div class="widget">
  <div class="widget-header">
    <div class="logo">G</div>
    <h3>VC Scout Score</h3>
  </div>
  <div class="input-row">
    <input type="text" id="wu" placeholder="GitHub username..." onkeydown="if(event.key==='Enter')wCheck()">
    <button onclick="wCheck()">Score</button>
  </div>
  <div id="widgetLoading">Analyzing...</div>
  <div id="widgetError"></div>
  <div id="widgetResult">
    <div class="score-display">
      <div class="score-value" id="ws">--</div>
      <div class="score-label">Scout Score</div>
      <div class="score-level" id="wl"></div>
    </div>
  </div>
  <div class="powered">
    <a href="https://gitdealflow.com/scout" target="_blank">Powered by GitDealFlow</a>
  </div>
</div>
<script>
(function(){var p=new URLSearchParams(window.location.search);var u=p.get('user');if(u){document.getElementById('wu').value=u;wCheck();}})();
async function wCheck(){var u=document.getElementById('wu').value.trim();var e=document.getElementById('widgetError');var r=document.getElementById('widgetResult');var l=document.getElementById('widgetLoading');e.style.display='none';r.style.display='none';l.style.display='block';if(!u){e.textContent='Enter a username';e.style.display='block';l.style.display='none';return;}
try{var res=await fetch('https://signals.gitdealflow.com/api/mcp/rpc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',method:'tools/call',params:{name:'get_scout_receipts',arguments:{github_username:u}},id:1})});var d=await res.json();var t=d.result?.content?.[0]?.text||'';var p;try{p=JSON.parse(t);}catch{p={scout_score:0,summary:''};}
var sc=p.scout_score!==undefined?p.scout_score:(p.score||0);var lv=sc>=85?'Maven':sc>=65?'Elite':sc>=40?'Scout':sc>=20?'Tracker':'Novice';document.getElementById('ws').textContent=sc;var le=document.getElementById('wl');le.className='score-level level-'+lv.toLowerCase();le.textContent=lv;r.style.display='block';}catch(e){e.textContent='Error: '+e.message;e.style.display='block';}
l.style.display='none';}
</script>
</body>
</html>`;

export default function handler(req, res) {
  let html = EMBED_HTML;

  // Pass through query params (e.g. ?user=)
  const query = req.url.includes('?') ? req.url.split('?')[1] : '';
  if (query) {
    const scriptInject = `<script>
(function() {
  const params = new URLSearchParams('${query.replace(/'/g, "\\'")}');
  const u = params.get('user');
  if (u && document.getElementById('wu')) {
    document.getElementById('wu').value = u;
    if (typeof wCheck === 'function') setTimeout(wCheck, 100);
  }
})();
</script>`;
    html = html.replace('</head>', scriptInject + '</head>');
  }

  // Set iframe-friendly headers — these override Vercel's defaults
  res.setHeader('X-Frame-Options', 'ALLOWALL');
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://signals.gitdealflow.com; frame-ancestors *");
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');

  res.status(200).send(html);
}
