(function() {
  'use strict';

  var BASE_URL = 'https://gitdealflow.com';
  var TWITTER_HANDLE = 'gitdealflow';

  function getPageInfo() {
    var path = window.location.pathname.replace(/\/+$/, '') || '/';
    var canonical = document.querySelector('link[rel="canonical"]');
    var url = canonical ? canonical.href : window.location.href;
    var title = document.title.replace(/\s*\|\s*GitDealFlow$/, '').trim();
    var desc = document.querySelector('meta[name="description"]');
    var description = desc ? desc.getAttribute('content') : '';

    // Extract the page slug/name from the path
    var segments = path.split('/').filter(Boolean);
    var lastSegment = segments[segments.length - 1] || '';

    var text = '';
    var tweetText = '';

    // --- Path-based detection ---

    // Geo×Sector pages: /g/{slug} (slug format: {sector}-startups-in-{geo})
    if (segments[0] === 'g' && segments[1]) {
      var gsParts = segments[1].replace(/-startups-in-/i, '|||').split('|||');
      var sector = gsParts[0] ? gsParts[0].replace(/-/g, ' ') : '';
      var geo = gsParts[1] ? gsParts[1].replace(/-/g, ' ') : '';
      if (sector && geo) {
        sector = capitalize(sector);
        geo = capitalize(geo);
        tweetText = sector + ' startups in ' + geo + ' — engineering velocity data \uD83D\uDCC8';
      } else {
        tweetText = 'Geo-sector startup engineering velocity data \uD83D\uDCC8';
      }
    }
    // Competitive set pages: /a/startups-like-{name}
    else if (segments[0] === 'a' && segments[1] && segments[1].indexOf('startups-like-') === 0) {
      var name = segments[1].replace('startups-like-', '').replace(/-/g, ' ');
      name = capitalize(name);
      tweetText = 'Find startups like ' + name + '! Compare engineering velocity on GitDealFlow \uD83D\uDCBB';
    }
    // Signal type pages: /s/{type}-{geo}
    else if (segments[0] === 's' && segments[1]) {
      var signalType = mapSignalType(segments[1]);
      tweetText = signalType + ' — find them on GitDealFlow \uD83C\uDFAF';
    }
    // Sector pages
    else if (segments[0] === 'sector' && segments[1]) {
      var sectorName = segments[1].replace(/-/g, ' ');
      sectorName = capitalize(sectorName);
      tweetText = "Check out " + sectorName + " startups' engineering velocity on GitDealFlow \uD83D\uDE80";
    }
    // City pages: /startups-in-{city}
    else if (path.indexOf('/startups-in-') !== -1) {
      var city = lastSegment.replace(/^startups-in-/, '').replace(/-/g, ' ');
      city = capitalize(city);
      tweetText = "See engineering velocity for startups in " + city + " \uD83C\uDDFA\uD83C\uDDF8";
    }
    // What-is pages
    else if (path.indexOf('/what-is-') !== -1) {
      var term = lastSegment.replace(/^what-is-/, '').replace(/-/g, ' ');
      term = capitalize(term);
      tweetText = "What is " + term + "? Great explainer from @" + TWITTER_HANDLE + " \uD83D\uDCCA";
    }
    // Velocity ranking page
    else if (path === '/high-velocity-startups') {
      tweetText = "Top engineering teams ranked by velocity \uD83C\uDFC6 check the rankings on GitDealFlow";
    }
    // Stage pages: /{stage}-startups (pre-seed, seed, series-a, series-b)
    else if (/-startups$/.test(lastSegment) && segments.length === 1) {
      var stage = lastSegment.replace(/-startups$/, '').replace(/-/g, ' ');
      stage = capitalize(stage);
      // Exclude city pages (startups-in-*) and other non-stage patterns
      if (['pre seed', 'seed', 'series a', 'series b', 'series b+'].indexOf(stage) !== -1) {
        tweetText = "Tracking " + stage + " startups engineering velocity on GitDealFlow \uD83D\uDE80";
      } else {
        tweetText = "Discover startup engineering velocity signals on GitDealFlow \uD83D\uDE80";
      }
    }
    // Tool pages
    else if (path === '/check-velocity' || path === '/benchmark' || path === '/scout' || path === '/tools' || path === '/scout-leaderboard') {
      var toolMap = {
        '/check-velocity': 'check startup engineering velocity',
        '/benchmark': 'benchmark startup engineering velocity',
        '/scout': 'compute your Scout Score',
        '/scout-leaderboard': 'see who has the best Scout Score',
        '/tools': 'free startup engineering tools'
      };
      tweetText = "Free tool: " + (toolMap[path] || 'check startup signals') + " on GitDealFlow \uD83D\uDD0D";
    }
    // BOFU / generic pages
    else if (['/pricing', '/enterprise', '/about', '/documentation', '/api', '/contact', '/apply', '/partners', '/privacy', '/terms', '/compare', '/blog', '/methodology', '/sectors', '/trending', '/startups', '/faq', '/glossary', '/dataset', '/radar', '/sector-radar', '/stats', '/badges-share', '/chrome', '/badge'].indexOf(path) !== -1) {
      tweetText = "Discover startup signals on GitDealFlow";
    }
    else {
      tweetText = "Discover startup engineering velocity signals on GitDealFlow \uD83D\uDE80";
    }

    var fullTweet = tweetText + ' ' + url;
    if (fullTweet.length > 280) {
      fullTweet = tweetText + ' ' + url;
      if (fullTweet.length > 280) {
        tweetText = tweetText.substring(0, 200) + '...';
        fullTweet = tweetText + ' ' + url;
      }
    }

    return {
      url: url,
      title: title,
      description: description,
      tweet: fullTweet,
      tweetText: tweetText
    };
  }

  function capitalize(str) {
    return str.replace(/\b\w/g, function(c) { return c.toUpperCase(); });
  }

  function mapSignalType(slug) {
    var signalMap = {
      'deploy-spike': 'startups with deploy frequency spike signals',
      'framework-migration': 'startups undergoing framework migration',
      'hiring-burst': 'startups with engineering hiring burst signals',
      'infra-buildout': 'startups with infrastructure buildout signals'
    };
    // Try to match the type prefix
    for (var key in signalMap) {
      if (slug.indexOf(key) === 0) {
        // Try to extract geo/count
        var rest = slug.replace(key, '').replace(/^-/, '');
        if (rest) {
          return signalMap[key] + ' in ' + rest.replace(/-/g, ' ').toUpperCase();
        }
        return signalMap[key];
      }
    }
    return 'Startup engineering signals tracked on GitDealFlow \uD83C\uDFAF';
  }

  function buildUI(info) {
    // Create container
    var container = document.createElement('div');
    container.id = 'gdf-share-bar';
    container.setAttribute('aria-label', 'Share this page');
    container.style.cssText =
      'position:fixed;bottom:0;left:0;right:0;z-index:999999;' +
      'display:flex;justify-content:center;align-items:center;padding:10px 16px;' +
      'background:rgba(11,17,32,0.92);' +
      'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);' +
      'border-top:1px solid rgba(96,165,250,0.2);' +
      'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;' +
      'transition:transform 0.3s ease,opacity 0.3s ease;';

    // Label
    var label = document.createElement('span');
    label.textContent = 'Share';
    label.style.cssText =
      'color:#94a3b8;font-size:13px;font-weight:600;margin-right:12px;' +
      'text-transform:uppercase;letter-spacing:0.5px;';

    // Twitter button
    var twitterBtn = makeButton('\uD83D\uDC26', 'Share on Twitter', function() {
      var w = 600, h = 450;
      var left = (screen.width/2)-(w/2), top = (screen.height/2)-(h/2);
      window.open(
        'https://twitter.com/intent/tweet?text=' + encodeURIComponent(info.tweet),
        'share-twitter',
        'toolbar=0,status=0,width='+w+',height='+h+',top='+top+',left='+left
      );
    });

    // LinkedIn button
    var linkedinBtn = makeButton('\uD83D\uDCBC', 'Share on LinkedIn', function() {
      var w = 600, h = 500;
      var left = (screen.width/2)-(w/2), top = (screen.height/2)-(h/2);
      window.open(
        'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(info.url),
        'share-linkedin',
        'toolbar=0,status=0,width='+w+',height='+h+',top='+top+',left='+left
      );
    });

    // Copy link button
    var copyBtn = makeButton('\uD83D\uDD17', 'Copy link', function() {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(info.url).then(function() {
          showToast('Link copied!');
        }).catch(function() {
          fallbackCopy(info.url);
        });
      } else {
        fallbackCopy(info.url);
      }
    });

    container.appendChild(label);
    container.appendChild(twitterBtn);
    container.appendChild(linkedinBtn);
    container.appendChild(copyBtn);

    document.body.appendChild(container);

    // Add a small spacer to prevent content from being hidden behind the bar
    var spacer = document.createElement('div');
    spacer.id = 'gdf-share-spacer';
    spacer.style.cssText = 'height:56px;';
    document.body.appendChild(spacer);
  }

  function makeButton(icon, label, onClick) {
    var btn = document.createElement('button');
    btn.innerHTML = '<span style="font-size:18px;line-height:1">' + icon + '</span> ' +
      '<span style="font-size:13px">' + label + '</span>';
    btn.style.cssText =
      'display:inline-flex;align-items:center;gap:6px;' +
      'padding:8px 16px;margin:0 4px;border:1px solid rgba(96,165,250,0.25);' +
      'border-radius:8px;background:rgba(30,41,59,0.8);color:#e2e8f0;' +
      'font-size:13px;font-family:inherit;cursor:pointer;' +
      'transition:all 0.15s ease;white-space:nowrap;';
    btn.onmouseenter = function() {
      btn.style.background = 'rgba(96,165,250,0.15)';
      btn.style.borderColor = 'rgba(96,165,250,0.5)';
    };
    btn.onmouseleave = function() {
      btn.style.background = 'rgba(30,41,59,0.8)';
      btn.style.borderColor = 'rgba(96,165,250,0.25)';
    };
    btn.onclick = function(e) {
      e.preventDefault();
      onClick();
    };
    return btn;
  }

  function showToast(msg) {
    var existing = document.getElementById('gdf-toast');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.id = 'gdf-toast';
    toast.textContent = msg;
    toast.style.cssText =
      'position:fixed;bottom:70px;left:50%;transform:translateX(-50%);' +
      'background:#1e293b;color:#e2e8f0;padding:8px 20px;border-radius:8px;' +
      'font-size:14px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;' +
      'z-index:1000000;box-shadow:0 4px 12px rgba(0,0,0,0.3);' +
      'border:1px solid rgba(96,165,250,0.3);' +
      'animation:gdfFadeIn 0.2s ease;';
    document.body.appendChild(toast);
    setTimeout(function() { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.3s'; }, 2000);
    setTimeout(function() { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 2500);
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); showToast('Link copied!'); } catch(e) { showToast('Copy failed — select and copy manually'); }
    document.body.removeChild(ta);
  }

  // Inject CSS animation keyframes
  var style = document.createElement('style');
  style.textContent = '@keyframes gdfFadeIn{from{opacity:0;transform:translateX(-50%) translateY(8px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}';
  document.head.appendChild(style);

  // Initialise on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      var info = getPageInfo();
      buildUI(info);
    });
  } else {
    var info = getPageInfo();
    buildUI(info);
  }
})();
