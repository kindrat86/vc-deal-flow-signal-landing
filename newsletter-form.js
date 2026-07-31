/*!
 * GitDealFlow Newsletter Signup Form — Embeddable Widget
 * Dark-themed inline email capture, posts to /api/subscribe
 * Usage: <script src="/newsletter-form.js" defer></script>
 *        <div class="gdf-newsletter-form" data-source="my-page"></div>
 */
(function () {
  'use strict';

  var STYLES = [
    '.gdf-newsletter-form { max-width:440px; margin:1.5rem auto; padding:1.5rem; background:#0f172a; border:1px solid #334155; border-radius:12px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }',
    '.gdf-newsletter-form .gdf-nl-title { color:#f1f5f9; font-size:1.05rem; font-weight:700; margin:0 0 .35rem 0; }',
    '.gdf-newsletter-form .gdf-nl-subtitle { color:#94a3b8; font-size:.85rem; margin:0 0 1rem 0; line-height:1.4; }',
    '.gdf-newsletter-form .gdf-nl-row { display:flex; gap:.5rem; }',
    '.gdf-newsletter-form .gdf-nl-input { flex:1; padding:.7rem .85rem; border:1px solid #334155; border-radius:8px; background:#0b1120; color:#e2e8f0; font-size:.9rem; outline:none; transition:border-color .2s; }',
    '.gdf-newsletter-form .gdf-nl-input:focus { border-color:#60a5fa; }',
    '.gdf-newsletter-form .gdf-nl-input::placeholder { color:#475569; }',
    '.gdf-newsletter-form .gdf-nl-btn { padding:.7rem 1.25rem; background:#2563eb; color:#fff; border:none; border-radius:8px; font-weight:600; font-size:.85rem; cursor:pointer; white-space:nowrap; transition:background .2s; }',
    '.gdf-newsletter-form .gdf-nl-btn:hover { background:#1d4ed8; }',
    '.gdf-newsletter-form .gdf-nl-btn:disabled { opacity:.5; cursor:not-allowed; }',
    '.gdf-newsletter-form .gdf-nl-msg { margin-top:.6rem; font-size:.8rem; min-height:1.2em; transition:color .2s; }',
    '.gdf-newsletter-form .gdf-nl-msg.success { color:#34d399; }',
    '.gdf-newsletter-form .gdf-nl-msg.error { color:#f87171; }',
    '.gdf-newsletter-form .gdf-nl-trust { margin-top:.6rem; display:flex; gap:.75rem; flex-wrap:wrap; font-size:.7rem; color:#475569; }',
    '@media(max-width:480px){ .gdf-newsletter-form .gdf-nl-row { flex-direction:column; } .gdf-newsletter-form .gdf-nl-btn { width:100%; } }',
  ];

  var HTML = '\
    <p class="gdf-nl-title">📬 Get Weekly Startup Signals</p>\
    <p class="gdf-nl-subtitle">Five trending startups every Sunday — free email digest from GitDealFlow.</p>\
    <div class="gdf-nl-row">\
      <input type="email" class="gdf-nl-input" placeholder="you@example.com" required aria-label="Email address" inputmode="email" autocomplete="email">\
      <button type="submit" class="gdf-nl-btn">Subscribe</button>\
    </div>\
    <p class="gdf-nl-msg" aria-live="polite"></p>\
    <div class="gdf-nl-trust">\
      <span>📊 324 startups tracked</span>\
      <span>🔬 SSRN research-backed</span>\
      <span>💚 Free forever</span>\
    </div>\
  ';

  // Inject styles once
  function injectStyles() {
    if (document.getElementById('gdf-nl-styles')) return;
    var style = document.createElement('style');
    style.id = 'gdf-nl-styles';
    style.textContent = STYLES.join('\n');
    document.head.appendChild(style);
  }

  function init() {
    injectStyles();
    var containers = document.querySelectorAll('.gdf-newsletter-form');
    if (!containers.length) return;

    containers.forEach(function (el) {
      var source = el.getAttribute('data-source') || 'unknown';
      el.innerHTML = HTML;

      var input = el.querySelector('.gdf-nl-input');
      var btn = el.querySelector('.gdf-nl-btn');
      var msg = el.querySelector('.gdf-nl-msg');

      // Handle enter key
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') submit();
      });

      btn.addEventListener('click', submit);

      function submit() {
        var email = (input.value || '').trim();
        if (!email) {
          msg.textContent = 'Please enter your email address.';
          msg.className = 'gdf-nl-msg error';
          input.focus();
          return;
        }

        // Basic client-side validation
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          msg.textContent = 'Please enter a valid email address.';
          msg.className = 'gdf-nl-msg error';
          input.focus();
          return;
        }

        btn.disabled = true;
        btn.textContent = 'Sending…';
        msg.textContent = '';
        msg.className = 'gdf-nl-msg';

        fetch('/api/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, source: source }),
        })
          .then(function (r) { return r.json(); })
          .then(function (data) {
            if (data.success) {
              msg.textContent = '✅ Confirmed! Check your inbox.';
              msg.className = 'gdf-nl-msg success';
              input.value = '';
              btn.textContent = 'Done ✓';
              setTimeout(function () {
                btn.disabled = false;
                btn.textContent = 'Subscribe';
              }, 3000);
            } else {
              throw new Error(data.error || 'Failed');
            }
          })
          .catch(function () {
            msg.textContent = 'Something went wrong. Try again or email signals@gitdealflow.com.';
            msg.className = 'gdf-nl-msg error';
            btn.disabled = false;
            btn.textContent = 'Subscribe';
          });
      }
    });
  }

  // Run on DOMContentLoaded, or immediately if already loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
