# Trustpilot Setup Guide for GitDealFlow

## Why Trustpilot Matters

**SEO reality:** Trustpilot pages rank #1-3 for brand queries like `"gitdealflow review"`, `"gitdealflow.com trust"`, `"gitdealflow legit"`. The Russian article is right — if you don't claim your page, someone else can.

**Volume potential:** Branded search queries drive 15-30% of all search traffic for established products. Trustpilot's domain authority (DA 87+) means even unpaid free pages outrank most competitors.

**Risk:** gitdealflow.com currently has **zero Trustpilot presence** — anyone can create a page under your brand and redirect traffic to their site.

---

## Step 1: Claim Your Free Profile

Trustpilot has a **FREE plan** — zero cost. No CC needed.

1. Go to https://business.trustpilot.com/
2. Click **"Start for free"**
3. Create account with `sales@sipiteno.com` or `signals@gitdealflow.com`
4. Enter domain: **`gitdealflow.com`**
5. Choose **Free plan** (100 review invitations/month, 2 widgets, 1 user)
6. Verify domain: Trustpilot sends verification email to your domain email OR you can add a DNS TXT record — I can help with the DNS option below
7. Once verified, you own the profile

**Alternative:** If a page already exists at `trustpilot.com/review/gitdealflow.com` (created by a customer), click "Claim this business" instead.

---

## Step 2: Profile Content (Copy-Paste Ready)

### Company Name
```
GitDealFlow
```

### Tagline / Short Description
```
VC Deal Flow Signal — Engineering Velocity Tracking for Angel Investors & VCs
```

### Full Company Description (Paste into "About")
```
GitDealFlow is a deal-flow signal tool that tracks engineering acceleration across 4,200+ startup GitHub organizations. We analyze commit velocity, contributor growth, and repository expansion to surface breakout startups 21-47 days before fundraise announcements.

Unlike Crunchbase or PitchBook (which report after rounds close), GitDealFlow flags acceleration before the round — from the code side, not the cap table.

Key features:
• 15+ startup sectors tracked weekly
• 20 trending startups updated every Monday
• Individual startup signal pages with metrics
• Public API, MCP server, and A2A endpoint
• Scout Score for GitHub users
• Free Sunday digest — five startups every week
• SSRN-published methodology (DOI: 10.2139/ssrn.6606558)
```

### Business Categories
```
Primary: Market Research
Secondary: Venture Capital Software, Data Analytics
```

### Website
```
https://gitdealflow.com
```

### Business Email
```
signals@gitdealflow.com
```

### Location
```
Kifisia, Greece
```

---

## Step 3: Add TrustBox Widget to Homepage

After claiming your profile, get your **Trustpilot Business Unit ID**:

1. Go to Trustpilot Business Dashboard → Settings → API
2. Find your Business Unit ID (looks like: `5a8f4e9b0000ff0001d2e3f4`)
3. Replace `YOUR_BUSINESS_UNIT_ID` below with the real ID

### TrustBox Widget Code for Index Page

Insert this before `</body>` on index.html:

```html
<!-- TrustBox widget - Micro Star -->
<div class="trustpilot-widget" data-locale="en-US" data-template-id="5419b732fbfb950b0de634e4" 
     data-businessunit-id="YOUR_BUSINESS_UNIT_ID" data-style-height="24px" data-style-width="100%" 
     data-theme="dark">
  <a href="https://www.trustpilot.com/review/gitdealflow.com" target="_blank" rel="noopener">
    Trustpilot
  </a>
</div>

<!-- TrustBox script -->
<script type="text/javascript" src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async></script>
```

**Placement suggestion:** After the nav bar, before main content — or in the footer next to the portfolio network links.

For the signals site (Next.js), it goes in `app/layout.tsx`.

---

## Step 4: Domain Verification DNS Record (Alternative to Email)

If the email verification doesn't work, add this DNS TXT record through your domain registrar (Hover/Cloudflare):

```
Type: TXT
Name: gitdealflow.com
Value: [Trustpilot provides this — will look like "trustpilot-domain-verification=xxxxx"]
TTL: 3600
```

---

## Step 5: Review Invitation Strategy

**Goal:** Get 5-10 organic reviews in the first 30 days. Trustpilot rewards active profiles.

### Who to Ask (In Order)
1. **Current email subscribers** → Send a review invitation to your Sunday list. Frame as "help others find us"
2. **Users who emailed you** → Anyone who's corresponded with signals@gitdealflow.com
3. **GitHub stargazers** → People who starred the MCP server repo — they already trust the product
4. **Telegram subscribers** → Your TG community (if any)

### Invitation Template (Draft)
```
Subject: You've seen the signal — how are we doing?

Hi {first_name},

You subscribed to GitDealFlow's startup signals — you've seen which
startups are accelerating before the round gets crowded.

I'm building this alone. Your honest review helps other investors
find the tool, and it helps me know what to fix.

→ [Leave a 2-minute review on Trustpilot]({invitation_link})

No pressure, no follow-up. If it's not for you, that's valuable too.

— The Data Nerd
```

### Timing
- Send invitations 1-2 days after the Sunday digest (Tuesday morning)
- 5 invitations per week max (Free plan: 50-100/month)
- Space them out — Trustpilot flags mass invitations

---

## Step 6: Respond to Reviews

Respond to EVERY review — positive or negative. Google measures Trustpilot engagement as a trust signal.

**Positive template:**
```
Thanks for the review, {name}! Glad the signal helped you spot {company}.
The data refreshes every Monday — keep watching.
— The Data Nerd
```

**Critical template:**
```
Appreciate the honest feedback, {name}. I'm iterating fast — if there's
something specific I can improve, email me at signals@gitdealflow.com
and I'll respond within 24h.
— The Data Nerd
```

---

## Step 7: Link to Trustpilot from Site

Add this to the homepage footer (next to "Explore Our Network") after Trustpilot is live:

```html
<a href="https://www.trustpilot.com/review/gitdealflow.com" 
   target="_blank" rel="noopener" 
   class="text-gray-500 hover:text-gray-300 transition-colors text-xs">
  Trustpilot
</a>
```

---

## SEO Impact Timeline

| Week | Action | Expected SEO Effect |
|------|--------|-------------------|
| 0 | Claim profile, add widgets | Profile starts crawling |
| 1 | Get 3 reviews | Page indexed in Google |
| 2 | Get 5 reviews, respond to all | "GitDealFlow review" starts ranking |
| 4 | Get 10 reviews | Full brand SERP takeover |
| 8 | 15-20 reviews + widgets on site | Trust signals boost CTR on all brand queries |

**Result:** `trustpilot.com/review/gitdealflow.com` ranks #1-3 for `gitdealflow review`, `gitdealflow legit`, `gitdealflow trust`, `is gitdealflow real`, etc. — protecting your brand SERP from affiliate parasites.
