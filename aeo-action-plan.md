# AEO Action Plan — GitDealFlow

_Prepared 2026-07-18 · AEO plan following the Ahrefs Answer Engine Optimization methodology._

## 0 · Snapshot & scope

- **Brand + URL:** GitDealFlow (also "VC Deal Flow Signal") — `gitdealflow.com` + `signals.gitdealflow.com`
- **Business type:** Product / SaaS (signal tool for investors — **not a fund**) → visibility that matters most:
  **category queries** ("best deal flow tool", "Crunchbase alternative", "startup signal tool") and being named
  inside step-by-step "how do investors find startups early" answers.
- **Branded entity map:**
  - *Main brand:* GitDealFlow / VC Deal Flow Signal (Wikidata Q139376302)
  - *Products:* Signal Digest (free weekly email) · Dashboard Beta (€49/mo) · Insider Circle (€197/mo) ·
    Chrome Extension · Predict (Scout Game) · Receipts / Scout Score tool
  - *Proprietary concepts:* "Velocity Verdict" · "engineering acceleration" · "Scout Score" · "Scout Game"
  - *Personal brand:* The Data Nerd (pseudonymous, ORCID 0009-0002-2222-4112, SSRN preprint 6606558)
- **Competitors benchmarked:** Crunchbase · PitchBook · Tracxn · Grata · Affinity · SourceScrub · Dealroom ·
  CB Insights · AngelList · Private Equity Wire
- **Priority platforms:** **Google AI Overviews + ChatGPT first** (biggest eyeballs); **Perplexity third**
  (aligns with Google rankings — fastest win once you rank). Each gets a distinct tactic below.
- **Tools available:** PostHog (installed), Google Search Console (assumed), Vercel hosting. **No Ahrefs, no
  Cloudflare.** → path taken: **tool-agnostic** (manual prompt sampling + bundled script). No GA4 custom channel
  yet — see §5.

## 1 · Baseline (manual prompt sampling — no Brand Radar)

Run these ~15 prompts in ChatGPT, Perplexity, Google (AIO/AI Mode), Gemini. Repeat each 3× (citations are
probabilistic). Log mention / citation / competitor. This is your Brand Radar proxy until Ahrefs is added.

| Prompt cluster | Sample prompts |
|---|---|
| Category "best" | "best deal flow tools for VCs 2026" · "best tools to find startups before they raise" · "startup signal tools for angel investors" |
| Competitor alt | "Crunchbase alternatives" · "PitchBook alternatives" · "cheaper than Crunchbase" · "Tracxn vs Grata" |
| How-to | "how do VCs find startups early" · "how to spot startups about to raise" · "GitHub signals of startup growth" |
| Branded | "what is GitDealFlow" · "VC Deal Flow Signal" · "Scout Score GitHub" · "engineering acceleration startups" |

> **Expected biggest opportunity:** the gap between *impressions* (AI answering "best deal flow tool" or
> "how do VCs find startups early") and *mentions* (naming GitDealFlow) — closed almost entirely by earning
> third-party web mentions (§3 Influence), because that is the single strongest AI-visibility signal measured.

## 2 · Gap map → priorities

See `aeo-brand-gap-analysis.csv` (filled). Top gaps by dimension:

- **Visibility:** no detectable third-party mentions yet → the #1 blocker. Correlation 0.664 with AIO.
- **Narrative:** "engineering acceleration" risks being read as "accelerator program" (YC/Techstars). llms.txt
  disambiguates; on-site must reinforce.
- **Topic:** weak geo/sector fan-out coverage — city PSEO pages are ~100 words.
- **Format:** **no YouTube** (most-cited AIO domain; 0.737 corr. with ChatGPT visibility); comparison pages
  exist but are too thin to be cited.
- **Web mentions:** absent from every listicle/review/community AI pulls from.
- **Demand:** proprietary concepts (Scout Score, Velocity Verdict) under-distributed — will be flattened into
  generic knowledge unless labeled and pushed widely.

## 3 · The plan (tagged Fix / Build / Influence, sorted by priority)

### 🏗️ Build (create what's missing)

- [ ] **[P1] Expand the 12 `vs/` comparison pages to 600–900 words each.** Today they're 82–200w — below the
      thin-content threshold and too sparse for AI to extract a useful comparison. "X vs Y" is the **#1 format
      AI cites** (43.8% of ChatGPT citations are listicles/comparisons). Apply BLUF (one-sentence verdict up
      front), atomic sections (each H2 stands alone), entity-rich ("GitDealFlow reads commit velocity across
      4,200+ GitHub orgs" not "we track startups"). Dedupe URL variants (`/vs/crunchbase` vs
      `/vs/gitdealflow-vs-crunchbase` — pick one canonical, 301 the other). This is the single highest-leverage
      content build.
- [ ] **[P1] Expand homepage FAQ from 3 → 10–12 Q/A in the FAQPage schema** with specific numbers/dates
      (pricing, sector count, lead time "21–47 days", SSRN DOI). AI-hallucination defense: Gemini & Perplexity
      repeat contradicting fiction 37–39% of the time; ChatGPT cites an official FAQ 84% of the time. "When AI
      has to choose between vague truth and specific fiction, it tends to choose the specific fiction."
- [ ] **[P2] Launch a YouTube channel with 5–10 search-hit videos.** Title = the searched keyword
      ("How to find startups before they raise", "Crunchbase vs GitDealFlow", "What is GitHub commit velocity").
      Description = real summary with keyword in line 1. Add timestamps (→ YouTube chapters → Google deep-links).
      Say the keyword in the audio. Match the format that already ranks (tutorials dominate → make tutorials).
      Every video is also training data even if not cited immediately.
- [ ] **[P2] Expand city PSEO pages** (berlin, london, amsterdam, etc.) from ~100w → 400w+ with named local
      startups, active sectors, and a "startups to watch in [city] this quarter" section. Closes the geo fan-out.
- [ ] **[P3] Label and distribute proprietary concepts.** Every time you write "Scout Score" or "Velocity
      Verdict", define it once and attach the brand ("the GitDealFlow Scout Score"). LLMs flatten un-attributed
      originality into generic knowledge. Push definitions to the blog, social, Reddit, the SSRN preprint.

### 🔧 Fix (optimize what exists)

- [ ] **[P1] Refresh the top 5–10 pages for freshness** (homepage, cheatsheet, dashboard, top sector pages).
      AI-cited content is ~25.7% fresher than organic; ChatGPT's top-cited pages are 76% refreshed within 30
      days. **Meaningful** updates only — new stats, current examples, dated sector data. Bumping the publish
      date alone is detected and earns zero credit.
- [ ] **[P2] Reinforce the "not an accelerator" entity on-site.** Add a one-line disambiguation callout on the
      homepage and `/about`: *"GitDealFlow measures engineering acceleration on GitHub — it is not a startup
      accelerator (YC, Techstars, 500 Global)."* llms.txt already says this; mirror it into visible HTML.
- [ ] **[P3] Consolidate duplicate `/vs/` URLs** (see P1 Build) — 301 the `gitdealflow-vs-*` variants into the
      clean `/vs/{competitor}` form so link equity and crawl budget aren't split.

### 📣 Influence (earn off-site mentions)

- [ ] **[P1] Tier-1 outreach — get onto the listicles AI already cites.** These are the pages ChatGPT/AIO pull
      from when answering "best deal flow tools". Targets to pursue (verify each ranks + has referring domains
      before pitching):
      - Saastr, StrictlyVC, Wellfound (AngelList) blog, TechCrunch investor-tools coverage
      - Niche VC/operator blogs that publish "tools we use" round-ups
      - G2 / Capterra / Slashdot listings (review sites AI cites for "X review" queries)
      - Comparison listicles: "best Crunchbase alternatives 2026", "best PitchBook alternatives"
      Pitch the genuinely-different angle: *GitHub engineering signal, 21–47 days pre-round, free digest.* Don't
      wait to be cited first — target pages that already have links and cover the topic.
- [ ] **[P2] Reddit & community — answer the underlying question, don't self-promote.** Find threads in
      r/venturecapital, r/startups, r/SaaS, r/investing, Hacker News "Ask HN: how do you find deal flow" where
      people ask how to spot startups early. Contribute a real answer that mentions the GitHub-signal method;
      link only when relevant. Reddit is a top ChatGPT citation source and a foundational LLM training input.
- [ ] **[P3] Activate owned properties** — the SSRN preprint (already a strong authority signal), Zenodo record,
      the @data_nerd X account, the Telegram channel. Each indexed appearance is an extra citation source +
      training example. Get the preprint linked from a couple of academic/operator write-ups.

## 4 · Technical checklist

- [x] **robots.txt AI-bot access** — `check_ai_bots.py gitdealflow.com` → **ALL bots allowed**
      (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Google-Extended, PerplexityBot, Bingbot, CCBot, …).
      No action.
- [x] **Edge / WAF block check** — `--edge` → **all user-agents HTTP 200**, no Cloudflare/WAF block.
      No action.
- [x] **JS rendering** — content is **server-side rendered** (131 KB HTML, ~4,071 visible words on the
      homepage in the raw response). ChatGPT's non-rendering crawler sees full content. ✅ No action.
- [x] **Clean HTML / heading hierarchy** — H1 + structured H2s present; sections are reasonably atomic.
      Keep reinforcing one-idea-per-heading as you expand pages.
- [x] **Schema markup** — already rich: Organization, Person (founder), WebSite, SoftwareApplication, Offer×4,
      FAQPage (3 Q/A), BreadcrumbList, SiteNavigationElement. **Action:** expand the FAQPage schema to match
      the new 10–12 Q/A (§3 Build P1). Consider adding `Article`/`Dataset` schema on the SSRN methodology page.
- [x] **Agent surfaces** — excellent and rare: `llms.txt`, `agents.md`, OpenAPI 3.1, MCP server (stdio + HTTP),
      A2A, NLWeb, function-calling API, RSS feed. This is best-in-class for agent/answer-engine retrieval.
- [ ] **Page speed / Core Web Vitals** — not measured here; run PageSpeed Insights. Vercel + static HTML +
      `max-age=3600, s-maxage=86400` caching is a strong base. PostHog is the only third-party script — keep it
      that way.
- [ ] **Hallucinated-URL 404s** — once AI traffic is tracked (§5), watch GA4/PostHog for AI-referrer hits to
      404s. AI sends visitors to 404s 2.87× more than Google; ChatGPT is the worst offender (~1% of clicked
      URLs). Redirect consistent hallucinations to the nearest real page. (You already have a custom `404.html`
      — good safety net.)

## 5 · Measurement setup

> **Full ready-to-paste setup delivered in `aeo-measurement-setup.md`** (GA4 regex, PostHog filter, survey HTML, monthly checklist, quarterly audit).

- [x] **AI referral tracking.** GA4 regex + PostHog filter ready-to-paste in `aeo-measurement-setup.md`.
- [x] **AI bot activity.** Vercel log drain approach documented (no Cloudflare for Bot Analytics).
- [x] **"How did you hear about us?" survey** — ready-to-paste dark-theme HTML with AI options.
- [x] **Baseline saved.** Prompt-sampling template (10 prompts × 3 tries) for month-0 snapshot.
- [x] **Monthly monitoring checklist** — 6 checks, first-Monday cadence.
- [x] **Quarterly competitive audit template** — 5 checks, every 90 days.

## 6 · Per-platform strategy (each genuinely distinct)

Only ~14% of the top-50 cited domains appear on all of Google AIO, ChatGPT, and Perplexity — "optimize for AI
search" is not a strategy. Distinct tactics:

- **Google AI Overviews / AI Mode** → own Google top-10 for the comparison + "best" queries (AIO still draws
  its largest citation pool from top-10 organic results), and **launch YouTube** — YouTube is ~5.6% of AIO
  citations and the most-cited domain overall. Googlebot (not Google-Extended) crawls for AIO — already allowed.
- **ChatGPT** → earn mentions on **high-DR editorial listicles and Reddit** (its most-cited sources). Training-
  data presence matters: the SSRN preprint + wide distribution of "Scout Score"/"Velocity Verdict" definitions
  bakes you into the model. Keep the official FAQ rich — ChatGPT cites official FAQs 84% of the time.
- **Perplexity** → leans hardest on existing Google rankings (~28.6% of its citations come from Google's top
  10). Fastest win once your `vs/` and "best" pages rank organically — so the comparison-page build (§3 P1)
  pays off here first.

## 7 · Cadence

- **This week:** (1) confirm AI-bot access ✅ done; (2) stand up PostHog AI-traffic channel + "How did you hear
  about us?" survey; (3) run the §1 prompt-sampling baseline; (4) start expanding the top-3 `vs/` pages; (5)
  list 10 tier-1 outreach targets.
- **Monthly:** re-run prompt sampling; check AI Share of Voice trend vs Crunchbase/PitchBook/Tracxn; note new
  citing domains; refresh the 5 highest-traffic pages with current stats. (>45% of AIO citations change on
  refresh ≈ every 2 days — so consistency beats intensity.)
- **Quarterly:** deeper competitive audit — re-check competitor vs/ pages, new listicles that appeared, Reddit
  threads that now rank.

---

**Do first:** the **`vs/` comparison-page expansion (§3 Build P1)** + the **tier-1 listicle outreach (§3
Influence P1)**. Together they attack the two biggest gaps — the format AI cites most (comparisons) and the
strongest AI-visibility signal (third-party web mentions). Technical AEO is already in excellent shape, so the
leverage is now 100% on content depth + off-site mentions, not on fixes.
