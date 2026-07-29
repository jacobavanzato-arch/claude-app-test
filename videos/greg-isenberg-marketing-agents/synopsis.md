# "Marketing Agents Are Too Good Now" — Synopsis

**Greg Isenberg (YouTube, @GregIsenberg) with guest Cody Schneider · 37:47 · uploaded Jul 27, 2026 · https://youtu.be/U2hogriGmEw**

The episode is two things: a startup idea (AI for WordPress) and a full end-to-end walkthrough of how to build a real marketing agent — using an autonomous Facebook Ads agent as the worked example.

---

## What a marketing agent actually is (and isn't)

Cody's definition cuts through the hype. A real marketing agent is **not** a linear Zapier automation, and it's not a fully autonomous AGI running your whole marketing stack — anyone claiming that is "full of it." A marketing agent is three things:

1. **Unified data** — the agent sees the whole pipeline (ads → analytics → CRM → revenue) in one place.
2. **An autonomous decision loop** — an LLM thinking on a cadence and acting on live business data, optimizing for revenue.
3. **Cloud hosting** — code deployed to Heroku/Railway/any cloud (not a Mac mini under your desk), reading a live data stream.

The end state is a "virtual employee" that owns one channel completely.

## The worked example: a Facebook Ads agent, end to end

The core walkthrough, step by step:

- **Research:** Agent scrapes Reddit (via Perplexity) for the target customer's pain points, rank-stacks them by frequency of mention — the top pain points become the ad angles.
- **Creative generation:** Bulk statics via Google Nano Banana (through Kai AI), seeded with competitor ads as examples; a vision model QAs every output against brand style guides (fonts, colors, readable text). Video is AI-avatar UGC via HeyGen today, moving to Seedance (limited by short clip length / stitching).
- **Publishing:** Via the Facebook Marketing API — **writes only** (publish, pause, promote). Accounts get banned for spamming the API with massive reads, not for using agents. Reads come from the warehouse instead.
- **Data loop:** Airbyte (open-source data pipeline) pipes Facebook Ads + Google Analytics + PostHog + HubSpot + Stripe into a ClickHouse warehouse. That's how the agent ties a specific ad to actual revenue — and it gives you conversational analytics ("we're having trouble hitting payroll — what's wrong?") from inside Claude Code/Codex.
- **Learning loop:** For one client they ship 2 ad sets/day, 5 ads each. Ads run 2–3 days for signal; losers auto-pause, winners join a "winners pool" competing for budget. A database of every ad's JSON prompt/script is what the agent studies to make better creative.
- **The entropy problem (the part nobody talks about):** Left alone, the agent converges on the same ideas and performance decays day by day. Fixes: inject "new DNA" from the Facebook Ads Library (competitor ads), mine YouTube/podcast transcripts in your niche for fresh insights, and use tools like Viral Loop's API to pull the week's most viral short-form posts per category for trend signals.

## Why Facebook ads, and what Andromeda changed

Facebook's new Andromeda algorithm killed interest-based targeting: the AI reads your creative (image, text, video script) and landing page and decides who sees it. **The creative IS the targeting** — so the game is volume and positioning variety, not audience settings. Cody argues Facebook is now the best B2B ad channel ("it'll find the 10 people in the US with that problem"). Greg's addition: founders quit after a few ads when they should re-position the same ad 10–20 times — the winners are usually angles you'd never have predicted. Paid ads are the only channel where you can test 1,000 creatives, know what the market wants in 48 hours, and feed a $1-in/$5-out machine. And marketing is no longer campaigns (start/stop) — it's a continuous loop reacting to trends that now move ~10x faster, all originating on short-form social.

What used to require a $10k+/mo agency — 100 ads was two weeks of work — a semi-technical founder can now stand up "in the next hour and a half" with Claude Code. The marketer's job becomes "agent jockey": encoding your domain knowledge into these systems.

## The startup idea: AI for WordPress

WordPress powers ~43% of Google-indexed websites and Cody calls it blue ocean — nobody is building AI for it. The pitch: "Lovable for WordPress" — vibe-code your site by chatting with AI, with the usual plugin hodgepodge (forms, CRM, SEO, security) bundled in one package, monetized via token tiers (~$29/mo base). Greg's sharper angle (he ran a WordPress-migration agency that moved time.com and TechCrunch): **find every proven, paid WordPress plugin without an AI component and build the AI-first version** — Yoast that fixes SEO instead of showing red/green dots, WPForms as a conversational lead-qualifying agent, WooCommerce with an AI storekeeper, AI-first Akismet/Wordfence. Validated demand, then 10x it with an agent. Distribution: Facebook/Google ads with pain-point creative ("I paid my agency $1,000/mo… now I chat with AI to change my site").

## The teaser list (comment-to-vote for future episodes)

Google Ads agents; influencer outreach agents (research → cold email → negotiate); cold-email agents that also manage the inbox and book meetings; TikTok reel farms (10 cloud accounts posting product slideshows at scale); SEO agents with on-brand voice; AI-search citation building; LinkedIn/Twitter management agents; podcast-to-newsletter agents with ElevenLabs voices and lead magnets. Cody is at companiesgraph.com.

## Tools named

Perplexity (Reddit pain-point mining) · Kai AI + Google Nano Banana (statics) · HeyGen, Seedance (AI UGC video) · Facebook Marketing API (writes only) · Airbyte → ClickHouse (pipeline + warehouse, open source) · Heroku/Railway (agent hosting) · Claude Code/Codex (build + conversational analytics) · Facebook Ads Library, YouTube/podcast transcripts, Viral Loop API (entropy fixes)

---

## Short synopsis (paste-ready)

Greg Isenberg + Cody Schneider, 38 min: how to build a real marketing agent — cloud-hosted code making decisions off live business data, not a Zapier workflow. Worked example is a Facebook Ads agent that runs the channel end to end: scrapes Reddit for customer pain points, bulk-generates on-brand statics (Nano Banana) and AI-UGC video (HeyGen/Seedance) with a vision model QA-ing brand style, publishes via the Facebook Marketing API (writes only — API read-spam is what gets accounts banned), and learns from an Airbyte→ClickHouse warehouse that ties every ad to Stripe revenue. It ships ~10 ads/day, kills losers after 2–3 days, promotes winners into a budget-competing pool. Key insight nobody talks about: agents decay ("entropy") — you fix it by injecting competitor ads from the FB Ads Library, niche YouTube/podcast transcript insights, and viral short-form trend data. Post-Andromeda, Facebook targeting is dead: the creative IS the targeting, so volume + positioning variety wins, and FB is now arguably the best B2B channel. Also pitched: "Lovable for WordPress" — AI-first versions of every proven WordPress plugin (Yoast, WPForms, WooCommerce), since WordPress runs ~43% of the web and nobody's building AI for it. Bottom line: what took a $10k/mo agency is now a system a semi-technical founder can stand up with Claude Code in an afternoon — marketers become "agent jockeys."
