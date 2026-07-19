---
name: roofer-lead-crm
description: "Boise/Treasure Valley (and similar) roofer lead CRM + cold outreach ops. CRM-first batches, Agent Mail sends, short A/B subjects, day-N follow-ups for no-replies, status updates. Use for roofing lead gen, batch 2+, follow-ups, or CRM maintenance — not product architecture (see home-services-ai-agents)."
---

# Roofer Lead CRM & Outreach Ops

## User preferences (hard rules)

- **Short subject + short body** every cold email after Batch 1 baseline. Vary subjects; track which reply.
- **No voice pitch** in cold email (lead-response / free office helper only).
- **Batch N** = **new companies**, not a follow-up to yesterday's list.
- **Follow-up** = separate day-N bump to **non-replies only** (default ~day 3 after first touch).
- Cap **5–10** personalized emails/day.
- From **Agent Mail** (`your-inbox@agentmail.to` when that inbox is the active one); **BCC** `YOUR_EMAIL@example.com` on outbound; **CC** owner when replying to a live thread.
- **No WhatsApp CTA in cold emails**. CTA should be **reply here** / **reply to this email** only. Keep owner email BCC/CC rules.
- **CRM first** — do not Firecrawl/Apify for every 5-lead send.
- Chat deliveries: keep reports **content-only** (`cron.wrap_response: false`). Explain settings in plain language if the user asks "what changed."

## Status check style

When user asks “how’s it going,” answer with a **short table**: sent counts, replies, next cron times, queue of `new`+email — not a long narrative. Prefer a diagram/image when they ask where something lives or how folders fit together.

## Stores

| Store | Location |
|-------|----------|
| Primary JSON | `~/.hermes/shared/roofer_crm_boise.json` |
| CSV | `~/.hermes/shared/roofer_crm_boise.csv` |
| Google Sheet | https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit |
| Linear | https://linear.app/YOUR_WORKSPACE/issue/XXX |
| A/B | `~/.hermes/shared/roofer_ab_results.json` |
| Playbook | `~/.hermes/shared/roofer_outreach_playbook.md` |
| Send log | `~/.hermes/shared/roofer_outreach_log.json` |
| README | `~/.hermes/shared/roofer_crm_README.md` |

## Status lifecycle

`new` → `contacted` → `replied` → `qualified` | `won_pilot` | `lost`  
Also: `invalid_or_unverified` for dead/placeholder sites.

## New-lead batch algorithm

1. Load CRM JSON → filter `status=="new"` and `email!=""`.
2. Check Agent Mail inbox for replies; mark `replied` and **never** cold/follow those again until owner says.
3. If `new`+email count **&lt; 5** → bulk Firecrawl contact pages, merge **by domain**, rewrite JSON+CSV (+ Sheet when easy).
4. Take 5–10 leads. Prefer company-domain email over gmail. Drop scrape artifacts (`nroofs@` if `roofs@` exists).
5. Send short variants via Agent Mail + BCC owner (`export PATH="$HOME/.composio:$PATH"`).
6. Patch rows: `contacted`, `last_contacted`, `subject_variant`, `body_variant=B2_short`.
7. Append send log + A/B counts; refresh CSV.

## Follow-up algorithm (no-replies)

1. Load contacted leads from target batch + Agent Mail messages.
2. Any reply from prospect domain/email → `replied`, skip.
3. Else one short bump only if notes lack `followup1`.
4. Subjects like `{Company} — still open?` / `Re: faster lead response for {Company}`.
5. Notes append `followup1 YYYY-MM-DD`; log `type=followup`.

## Subject / body variants

See `references/copy-and-ab.md` and playbook.  
**Default after Batch 1:** short subjects S2–S5 + body B2 — **not** the long baseline subject.

## Scheduling pattern

When user says "wait until tomorrow" / "follow up no replies":

- One-shot cron for **new batch** next day.
- Separate one-shot for **follow-up** ~+3 days after first touch.
- Load skill `roofer-lead-crm`; `deliver: origin`; `attach_to_session: true` if owner may reply in Telegram.
- Prompts must be **self-contained** (paths, inbox, BCC, short-copy rules).

## Clean cron delivery

```yaml
# ~/.hermes/config.yaml
cron:
  wrap_response: false
```

Re-read on each delivery via `load_config()` — restart usually not required.  
When explaining: "Before = Cronjob Response header + footer; after = only the useful message."

## Notion

Composio Notion needs a **page shared** with the integration before `NOTION_CREATE_DATABASE`. Until then Sheet + JSON + Linear is enough.

## Pitfalls

- Calling Batch 2 a "next-day email" to the **same** 5 — wrong; Batch 2 = **new** names.
- Same-day follow-up spam.
- Long Batch-1 subjects as default forever.
- Re-scraping while CRM still has `new`+email queue.
- Inventing emails; pitching voice cold; personal Gmail when Agent Mail ACTIVE.
- Creating unsolicited digests/crons.
- Gateway `hermes gateway restart` **from inside** gateway session is blocked — use `/restart` in chat.

## Related

- `home-services-ai-agents` — product roles + GTM offer shape  
- `composio-with-hermes` — Agent Mail / Firecrawl / MCP bridge  
- `hermes-client-profiles` — client trade bots (separate from this owner GTM track)  

## Support files

- `references/copy-and-ab.md` — short templates + A/B keys  
- `references/crm-paths.md` — paths, statuses, merge rules  
