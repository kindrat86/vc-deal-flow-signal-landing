# AEO Measurement Setup — GitDealFlow

Ready-to-paste configuration for tracking AI visibility on gitdealflow.com.
Deploy these in the order listed. Each item is standalone — paste it and move on.

## 1. GA4 "AI traffic" channel (ready-to-paste)

**Where:** GA4 Admin → Data display → Channel groups → Copy "Default Channel Group" → create new channel group

**Channel name:** `AI traffic`

**Condition — Source matches regex:**
```
chatgpt\.com|perplexity|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai|deepseek\.com|you\.com|duckduckgo\.com.*chat
```

Save, then go to Reports → Acquisition → Traffic acquisition → select your new channel group.

> **Caveat:** this **undercounts** — many AI platforms strip referrer data and the visit lands in "direct." ChatGPT in-content links on paid accounts use no-referrer. Perplexity desktop app passes no referrer. Grok passes none. Use referral data for the **trend direction**, not the absolute number. Pair it with the survey below for the real number.

## 2. PostHog filter (site already uses PostHog)

**Where:** PostHog dashboard → Data management → Actions or Insights

**Event filter — Referrer matches regex:**
```
chatgpt\.com|perplexity|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai|deepseek\.com|you\.com
```

Name the insight "AI referral traffic" and pin it to a dashboard. This gives you the same data as GA4 but in your existing PostHog setup.

**Bot-activity tracking:** PostHog auto-captures user-agent. Filter by user-agent containing:
```
GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|PerplexityBot|Google-Extended|CCBot
```
Pages these bots hit repeatedly are likely being used as AI sources — keep them fresh.

## 3. "How did you hear about us?" survey (ready-to-paste HTML)

The single most important measurement step. AI visibility that never shows in analytics (someone asks ChatGPT, hears "GitDealFlow," then types gitdealflow.com directly → lands in "direct") is captured here.

**Place on these pages:**
- Signal Digest signup confirmation (`/confirmed.html`)
- Dashboard checkout
- Post-purchase / welcome email

**HTML to paste (dark-theme, matches site):**

```html
<fieldset style="background:#1e293b;border:1px solid #334155;border-radius:.6rem;padding:1.25rem 1.5rem;margin:1.5rem 0">
  <legend style="color:#f1f5f9;font-weight:600;font-size:1.05rem;margin-bottom:.5rem">How did you hear about GitDealFlow?</legend>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.4rem">
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="ai-assistant" style="accent-color:#0ea5e9">AI assistant (ChatGPT, Claude, Gemini)
    </label>
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="perplexity" style="accent-color:#0ea5e9">Perplexity
    </label>
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="google-ai" style="accent-color:#0ea5e9">AI search / Google AI Overviews
    </label>
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="google-search" style="accent-color:#0ea5e9">Google search
    </label>
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="social" style="accent-color:#0ea5e9">Social (Twitter, LinkedIn, Reddit)
    </label>
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="referral" style="accent-color:#0ea5e9">Referral / word of mouth
    </label>
    <label style="display:flex;align-items:center;gap:.4rem;color:#cbd5e1;cursor:pointer">
      <input type="radio" name="source" value="other" style="accent-color:#0ea5e9">Other
    </label>
  </div>
</fieldset>
```

**PostHog event:** Capture this as a custom event `attribution_survey` with property `source`. This lets you cross-reference survey responses with signups and conversions.

**Benchmark:** Ahrefs saw ~3% of conversions come from AI (self-reported), converting far above organic. Vercel saw 10%. Tally reported AI as its largest acquisition channel adding ~$1M ARR. Your number will be invisible without this survey.

## 4. AI bot analytics (no Cloudflare = Vercel middleware approach)

**Since the site is on Vercel (no Cloudflare), you can't use Ahrefs Bot Analytics.** Two alternatives:

**Option A — Vercel log drains (easiest):**
- Vercel Pro includes log drains. Route logs to a tool (Datadog, Logtail, Axiom) and filter for bot user-agents.
- Search for: `GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|PerplexityBot|Google-Extended`
- Pages hit most by citation bots (ChatGPT-User, OAI-SearchBot, PerplexityBot) are your strongest AI-citation candidates — keep them fresh.

**Option B — simple middleware (free, DIY):**
- Add a lightweight `_middleware.ts` at the edge that counts bot user-agent hits and stores them in a simple KV store or logs them to a PostHog event.

**What to watch for:**
- A citation bot hitting one page repeatedly → likely being used as a source
- Important pages bots never visit → discovery problem (revisit internal linking)
- Training bots (GPTBot, Google-Extended, CCBot) → feeding model training; volume is a proxy for inclusion odds

## 5. Monthly monitoring checklist

Run these checks on the **first Monday of every month**:

| Check | Tool | What to look for |
|---|---|---|
| AI referral traffic trend | GA4 / PostHog | Growing? Which platforms? Any new platforms appearing? |
| "How did you hear about us?" AI % | Survey results | Directional trend — is AI attribution growing? |
| AI bot crawl activity | Vercel logs / middleware | New pages being crawled? Old pages being dropped? |
| Brand Radar proxy: prompt sampling | Manual (10 prompts × 3 tries each) | Are we mentioned for "best deal flow tool"? "Crunchbase alternative"? Any new competitors appearing? |
| Compare page freshness | Manual | Any new listicles/roundups we should be on? Any stale ones that dropped us? |
| Top 5 traffic pages | GA4 / PostHog | Which pages get the most traffic? Are they the comparison pages (AI-cited format) or something else? Refresh the top 5. |

**Prompt-sampling template (the Brand Radar proxy):** Run these 10 queries in ChatGPT, Perplexity, and Google AI Overviews. Repeat each 3×. Log: mentioned (✓), cited with link (🔗), competitor mentioned instead (✗ + which competitor).

1. "best deal flow tools for VCs 2026"
2. "best startup signal tools"
3. "Crunchbase alternatives"
4. "PitchBook alternatives"
5. "how to find startups before they raise"
6. "GitHub signals for startup investing"
7. "alternative data for angel investors"
8. "deal sourcing tools for seed funds"
9. "what is GitDealFlow"
10. "Scout Score GitHub"

Track changes month-over-month. An increase in "✓" across queries is progress. The presence of any competitor that wasn't there before is a signal to check their strategy.

## 6. Quarterly competitive audit

Run this **once per quarter** (90 days). Add to cron or calendar.

| Check | What to do |
|---|---|
| Competitor content audit | Check Crunchbase, PitchBook, Tracxn's comparison/blog pages. Any new formats or topics they're covering that we're not? |
| Mention gap re-check | Run the 10 prompt-sampling queries again. Has any competitor gained ground? Any new listicles we should be on? |
| Sleeper-page refresh | In GA4, find pages with declining AI-referral traffic but still getting bot crawls — they need a content refresh (the freshness signal that gets AEO citations back). |
| New AEO surfaces | Any new AI-search platforms launched? (Grok search, Meta AI, etc.) Should we be optimizing for them? |
| Schema audit | Run `scripts/check_ai_bots.py gitdealflow.com` to confirm no new bot blocks. Check that all new pages have proper JSON-LD. |

## 7. ROI framing (when someone asks "is AEO worth it?")

Use these data points from the Ahrefs methodology:

- AI referral traffic averages **~0.25%** of total site traffic currently — small raw volume, but:
- AI visitors convert at **23×** the rate of organic (Ahrefs data)
- AI traffic grew **~9.7×** in a year; ChatGPT **+85%** since January
- **~45%** of AI Overview citations change on refresh (~every 2 days) — so consistency beats intensity
- Branded web mentions had the **strongest correlation** with AI Overview visibility (0.664) — this is why tier-1 outreach is the #1 remaining lever

**The deeper value:** AI visibility isn't just direct clicks — it's brand awareness *inside the AI conversation*. Someone asks ChatGPT "how do I find startups," hears GitDealFlow named, and then Googles you or types your URL directly. That attribution is invisible without the survey. Early movers in AEO gain a lasting advantage because they become the answer AI defaults to for the category.

---

**Do this week:** (1) Paste the GA4 regex, (2) paste the survey HTML on signup confirmation page, (3) run the 10-prompt baseline, (4) save results as the month-0 snapshot.
