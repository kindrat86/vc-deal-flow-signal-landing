// GitDealFlow PostHog Event Tracking API
// GET  /api/track.js  → returns client-side tracking snippet
// POST /api/track.js  → proxies {event, properties} to PostHog /capture/
//
// Uses NEXT_PUBLIC_POSTHOG_KEY from Vercel environment, or falls back to
// the hardcoded key already used on gitdealflow.com pricing pages.

const POSTHOG_HOST = 'https://eu.i.posthog.com';
const POSTHOG_KEY = process.env.NEXT_PUBLIC_POSTHOG_KEY || 'phc_lyZCgvTpicjLzAO3rY2GhxuX5WUc5jQjP8ZVwwJqauX';

// ─── Client-side tracking snippet ─────────────────────────────────────
function trackingSnippet() {
  return `(function(){
  /* PostHog init — matches existing gitdealflow.com setup */
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement('script')).type='text/javascript',p.async=!0,p.src=s.api_host+'/static/array.js',(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},o='init capture register register_once register_for_session unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group setPersonProperties resetPersonProperties setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags'.split(' '),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  function _init(){
    if(/^https?:$/.test(location.protocol)){
      posthog.init('${POSTHOG_KEY}', {
        api_host: '${POSTHOG_HOST}',
        persistence: 'memory',
        person_profiles: 'identified_only',
        loaded: function(ph) {
          /* Fire pageview on every navigation (SPA-friendly) */
          ph.capture('$pageview');
        }
      });
    }
  }
  if('requestIdleCallback' in window){
    requestIdleCallback(_init,{timeout:2500});
  } else {
    setTimeout(_init,2000);
  }

  /* ── GitDealFlow custom event helpers ───────────────────────────── */
  window.gdfTrack = function gdfTrack(event, properties) {
    properties = properties || {};
    if (typeof window.posthog !== 'undefined' && window.posthog.capture) {
      try { posthog.capture(event, properties); } catch(e) {}
    } else {
      /* Fallback: POST to /api/track.js proxy */
      try {
        var payload = JSON.stringify({event: event, properties: properties});
        if (navigator.sendBeacon) {
          navigator.sendBeacon('/api/track.js', payload);
        } else {
          var xhr = new XMLHttpRequest();
          xhr.open('POST', '/api/track.js', true);
          xhr.setRequestHeader('Content-Type', 'application/json');
          xhr.send(payload);
        }
      } catch(e) {}
    }
  };

  /* ── Auto-wire known interactions ────────────────────────────────── */
  document.addEventListener('click', function(e) {
    var t = e.target.closest('[data-track]');
    if (!t) return;
    var eventName = t.getAttribute('data-track');
    var props = {};
    try { props = JSON.parse(t.getAttribute('data-track-props') || '{}'); } catch(e) {}
    window.gdfTrack(eventName, props);
  });

  /* Benchmark search */
  var benchSearch = document.getElementById('benchmarkSearch') || document.querySelector('.benchmark-search input, .search-box input');
  if (benchSearch) {
    benchSearch.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        window.gdfTrack('benchmark_search', {
          query: (this.value || '').slice(0, 200)
        });
      }
    });
  }

  /* Benchmark share buttons */
  document.addEventListener('click', function(e) {
    var shareBtn = e.target.closest('[data-share]');
    if (shareBtn) window.gdfTrack('benchmark_share', {
      method: shareBtn.getAttribute('data-share') || 'unknown'
    });
  });

  /* Badge copy (startup-badges page) */
  document.addEventListener('click', function(e) {
    var copyBtn = e.target.closest('.copy-badge, [data-action="copy-badge"]');
    if (copyBtn) window.gdfTrack('badge_copy', {
      startup: copyBtn.getAttribute('data-startup') || copyBtn.getAttribute('data-slug') || 'unknown'
    });
  });

  /* Newsletter signup */
  document.addEventListener('submit', function(e) {
    var form = e.target;
    if (form.id === 'newsletter-form' || form.id === 'signup-form' || form.classList.contains('newsletter-form') || form.getAttribute('data-track') === 'newsletter_signup') {
      window.gdfTrack('newsletter_signup', {
        placement: form.getAttribute('data-placement') || document.querySelector('h1') ? document.querySelector('h1').textContent.trim().slice(0, 100) : ''
      });
    }
  });

  /* Velocity check */
  var veloInput = document.getElementById('searchInput') || document.getElementById('velocityInput') || document.querySelector('[data-role="velocity-search"] input');
  if (veloInput) {
    veloInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        window.gdfTrack('velocity_check', {
          query: (this.value || '').slice(0, 200)
        });
      }
    });
  }

  /* Scout check */
  var scoutInput = document.getElementById('username') || document.getElementById('scoutUsername') || document.querySelector('[data-role="scout-search"] input');
  if (scoutInput) {
    scoutInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        window.gdfTrack('scout_check', {
          username: (this.value || '').slice(0, 100)
        });
      }
    });
  }
})();`;
}

// ─── Serverless handler ─────────────────────────────────────────────────
export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  // POST: proxy event to PostHog /capture/
  if (req.method === 'POST') {
    try {
      const body = typeof req.body === 'object' ? req.body : JSON.parse(req.body || '{}');
      const { event, properties } = body;

      if (!event) {
        return res.status(400).json({ ok: false, error: 'Missing event name' });
      }

      const capturePayload = {
        api_key: POSTHOG_KEY,
        event: event,
        properties: {
          ...(properties || {}),
          $host: req.headers.host || '',
          $pathname: (properties && properties.$pathname) || '',
          $ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress || '',
          $user_agent: req.headers['user-agent'] || '',
          source: 'gitdealflow_landing',
        },
        timestamp: new Date().toISOString(),
      };

      // Fire-and-forget to PostHog — don't block response on failure
      const phRes = await fetch(`${POSTHOG_HOST}/capture/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(capturePayload),
      }).catch(() => null);

      return res.status(200).json({ ok: true });
    } catch (err) {
      return res.status(200).json({ ok: false, error: err.message });
    }
  }

  // GET: return tracking snippet
  const snippet = trackingSnippet();
  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400');
  return res.status(200).send(snippet);
}
