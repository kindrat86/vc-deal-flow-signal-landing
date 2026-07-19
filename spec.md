# Landing Page Spec for vc-deal-flow-signal

## Above the fold
- **Headline:** Spot Breakout Startups 3 Weeks Before They Hit Your Inbox
- **Subheadline:** GitHub is the largest free dataset of real-time engineering activity. Nobody packages it for investors. Until now.
- **Primary CTA:** "Get the free weekly digest" -> ConvertKit form (email capture)
- **Secondary CTA:** "See pricing" -> scroll to pricing section

## Star Story Solution section
**Star:** An angel investor with 20+ portfolio companies, actively sourcing, proud of their network but quietly frustrated by how often they hear about great rounds after they close.

**Story:** You keep seeing the same decks as everyone else. You hear about the breakout company at demo day, or worse, in the TechCrunch headline. By then, terms are set and your edge is gone. Meanwhile, the smartest quant funds have known for years that public data, read correctly, is the best leading indicator. The problem was never access. It was that nobody built the lens for investors.

**Solution:** VC Deal Flow Signal monitors GitHub engineering activity across thousands of startups and surfaces the ones showing unusual acceleration: commit velocity spikes, contributor growth, new infrastructure repos. You see the momentum weeks before the pitch deck exists.

## How It Works section (3 steps)
1. **We monitor** thousands of startup GitHub orgs for engineering acceleration patterns
2. **We surface** the top movers ranked by commit velocity, contributor growth, and new repo creation
3. **You invest** weeks before the pitch deck lands in everyone else's inbox

## False Beliefs section (objection handling)
- "GitHub data is too noisy" -> We don't show raw commits. We show acceleration patterns: when velocity deviates sharply from a company's own baseline.
- "I already have enough deal flow" -> Your network shows you what others already see. We show you what nobody else is watching.
- "Public data can't give an edge" -> Everyone has access to SEC filings too. The edge is in reading what others ignore.

## Pricing section
- **Free:** Monthly email digest with top 5 trending startups by GitHub momentum. No login required.
  - CTA: "Start free" -> ConvertKit form
- **Pro (EUR 9.97/mo):** Full micro-SaaS dashboard. 60+ startups ranked by engineering acceleration. Filter by sector, stage, geography. Enriched with funding data and team size.
  - CTA: Stripe Payment Link placeholder -> {{STRIPE_LINK_TIER_2}}
- **Premium (EUR 49/mo):** Everything in Pro, plus custom watchlists, API access, Slack alerts, deeper enrichment, portfolio overlap detection, quarterly trend briefings.
  - CTA: Stripe Payment Link placeholder -> {{STRIPE_LINK_TIER_3}}

## About section
**The Data Nerd voice:** I obsess over signals others ignore. I watched a company's commit graph spike and three weeks later they announced a Series A. The signal was right there the whole time, public, free, updating in real time. Nobody was reading it. So I built something that would.

## Manifesto block
We believe the next generation of great investments will be found in data, not networks. The best startups leave footprints in their code long before they leave footprints in the press. Our mission is to make engineering momentum visible to every investor, not just the ones with the right connections.

## Footer
- Mission: We believe the best investments start with seeing what others miss.
- Links: Privacy, Terms, Contact
- ConvertKit form (repeated)

## Tracking
- PostHog snippet: {{POSTHOG_KEY}}
- ConvertKit form ID placeholder: {{CONVERTKIT_FORM}}
- Stripe Payment Link URL placeholders: {{STRIPE_LINK_TIER_2}}, {{STRIPE_LINK_TIER_3}}
