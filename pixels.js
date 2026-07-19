/*
 * Centralized retargeting pixels for gitdealflow.com (static landing).
 * Each pixel is gated on its ID below: empty string = no script load, no fire.
 *
 * To activate a pixel:
 *   1. Create the ad account on the platform (see monitoring/retargeting-pixels.md).
 *   2. Drop the pixel ID into the corresponding field in PIXEL_IDS below.
 *   3. Redeploy. The pixel starts collecting visitors immediately.
 *
 * Same env vars are wired in pseo-site/components/PixelManager.tsx for the app.
 * Keep both in sync when you add an ID.
 */
(function () {
  if (!/^https?:$/.test(location.protocol)) return;

  var PIXEL_IDS = {
    meta: "",          // Facebook + Instagram. e.g. "1234567890123456"
    ga4: "",           // GA4 measurement ID. e.g. "G-XXXXXXXXXX"
    googleAds: "",     // Google Ads conversion ID. e.g. "AW-123456789"
    linkedin: "",      // LinkedIn Insight partner ID. e.g. "1234567"
    twitter: "",       // X/Twitter pixel ID. e.g. "abc12"
    tiktok: "",        // TikTok pixel ID. e.g. "C0XXXXXXXXXXXXXXXXXX"
    reddit: "",        // Reddit pixel ID. e.g. "t2_xxxxxxxx"
    quora: "",         // Quora pixel ID. e.g. "abcdef1234567890"
    pinterest: "",     // Pinterest tag ID. e.g. "2612345678901"
    msUet: ""          // Microsoft / Bing UET tag ID. e.g. "12345678"
  };

  // Meta (Facebook + Instagram)
  if (PIXEL_IDS.meta) {
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    fbq("init", PIXEL_IDS.meta);
    fbq("track", "PageView");
  }

  // Google (GA4 + Google Ads share gtag)
  var gtagId = PIXEL_IDS.ga4 || PIXEL_IDS.googleAds;
  if (gtagId) {
    var g = document.createElement("script");
    g.async = true;
    g.src = "https://www.googletagmanager.com/gtag/js?id=" + gtagId;
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments) };
    gtag("js", new Date());
    if (PIXEL_IDS.ga4) gtag("config", PIXEL_IDS.ga4);
    if (PIXEL_IDS.googleAds) gtag("config", PIXEL_IDS.googleAds);
  }

  // LinkedIn Insight Tag
  if (PIXEL_IDS.linkedin) {
    window._linkedin_partner_id = PIXEL_IDS.linkedin;
    window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
    window._linkedin_data_partner_ids.push(PIXEL_IDS.linkedin);
    (function (l) { if (!l) { window.lintrk = function (a, b) { window.lintrk.q.push([a, b]) }; window.lintrk.q = [] } var s = document.getElementsByTagName("script")[0]; var b = document.createElement("script"); b.type = "text/javascript"; b.async = true; b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js"; s.parentNode.insertBefore(b, s) })(window.lintrk);
  }

  // X / Twitter
  if (PIXEL_IDS.twitter) {
    !function (e, t, n, s, u, a) { e.twq || (s = e.twq = function () { s.exe ? s.exe.apply(s, arguments) : s.queue.push(arguments) }, s.version = "1.1", s.queue = [], u = t.createElement(n), u.async = !0, u.src = "https://static.ads-twitter.com/uwt.js", a = t.getElementsByTagName(n)[0], a.parentNode.insertBefore(u, a)) }(window, document, "script");
    twq("config", PIXEL_IDS.twitter);
  }

  // TikTok
  if (PIXEL_IDS.tiktok) {
    !function (w, d, t) { w.TiktokAnalyticsObject = t; var ttq = w[t] = w[t] || []; ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie", "holdConsent", "revokeConsent", "grantConsent"]; ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))) } }; for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]); ttq.instance = function (t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e }; ttq.load = function (e, n) { var r = "https://analytics.tiktok.com/i18n/pixel/events.js", o = n && n.partner; ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = r; ttq._t = ttq._t || {}; ttq._t[e] = +new Date; ttq._o = ttq._o || {}; ttq._o[e] = n || {}; n = document.createElement("script"); n.type = "text/javascript"; n.async = !0; n.src = r + "?sdkid=" + e + "&lib=" + t; e = document.getElementsByTagName("script")[0]; e.parentNode.insertBefore(n, e) }; ttq.load(PIXEL_IDS.tiktok); ttq.page() }(window, document, "ttq");
  }

  // Reddit
  if (PIXEL_IDS.reddit) {
    !function (w, d) { if (!w.rdt) { var p = w.rdt = function () { p.sendEvent ? p.sendEvent.apply(p, arguments) : p.callQueue.push(arguments) }; p.callQueue = []; var t = d.createElement("script"); t.src = "https://www.redditstatic.com/ads/pixel.js", t.async = !0; var s = d.getElementsByTagName("script")[0]; s.parentNode.insertBefore(t, s) } }(window, document);
    rdt("init", PIXEL_IDS.reddit);
    rdt("track", "PageVisit");
  }

  // Quora
  if (PIXEL_IDS.quora) {
    !function (q, e, v, n, t, s) { if (q.qp) return; n = q.qp = function () { n.qp ? n.qp.apply(n, arguments) : n.queue.push(arguments) }; n.queue = []; t = document.createElement(e); t.async = !0; t.src = v; s = document.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, "script", "https://a.quora.com/qevents.js");
    qp("init", PIXEL_IDS.quora);
    qp("track", "ViewContent");
  }

  // Pinterest
  if (PIXEL_IDS.pinterest) {
    !function (e) { if (!window.pintrk) { window.pintrk = function () { window.pintrk.queue.push(Array.prototype.slice.call(arguments)) }; var n = window.pintrk; n.queue = []; n.version = "3.0"; var t = document.createElement("script"); t.async = !0; t.src = e; var r = document.getElementsByTagName("script")[0]; r.parentNode.insertBefore(t, r) } }("https://s.pinimg.com/ct/core.js");
    pintrk("load", PIXEL_IDS.pinterest);
    pintrk("page");
  }

  // Microsoft / Bing UET
  if (PIXEL_IDS.msUet) {
    (function (w, d, t, r, u) { var f, n, i; w[u] = w[u] || [], f = function () { var o = { ti: PIXEL_IDS.msUet, enableAutoSpaTracking: true }; o.q = w[u], w[u] = new UET(o), w[u].push("pageLoad") }, n = d.createElement(t), n.src = r, n.async = 1, n.onload = n.onreadystatechange = function () { var s = this.readyState; s && s !== "loaded" && s !== "complete" || (f(), n.onload = n.onreadystatechange = null) }, i = d.getElementsByTagName(t)[0], i.parentNode.insertBefore(n, i) })(window, document, "script", "//bat.bing.com/bat.js", "uetq");
  }
})();
