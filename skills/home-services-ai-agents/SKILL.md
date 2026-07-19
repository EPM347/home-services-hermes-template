---
name: home-services-ai-agents
description: "Design and implement AI agent 'employees' for field-service businesses (HVAC, plumbing, roofing, electrical), and GTM to sell free/pilot setups to those shops. Covers roles, phased rollout, custom Python stack, dispatcher architecture, and roofer outreach. Use when building receptionists, lead intake, reviews, tech assistants, or prospecting trade businesses."
---

# Home-Services AI Agent Employees

For shops where revenue is lost to missed calls, slow lead response, no-shows, and paperwork—not to lack of technicians.

## Core roles (priority order)

1. **24/7 receptionist / dispatcher** — answer, qualify, book, emergency escalate  
2. **Lead qualifier + CRM logger** — speed-to-lead from web/ads  
3. **Reminders / no-show reducer** — SMS confirm + easy reschedule  
4. **Review & referral bot** — post-job Google review push  
5. **Collections / memberships** — invoices, tune-up plans  
6. **On-site tech assistant** — manuals, parts, job notes  
7. **Marketing writer** — seasonal content (lower urgency)

## Phased rollout

1. After-hours phone answering (immediate revenue)  
2. Reminders + reviews  
3. Lead intake / speed-to-lead  
4. Tech assistant + collections  

Do not build all roles at once.

## Stack choice: no-code vs custom

| Approach | Glue | When |
|----------|------|------|
| **No-code** | Vapi/Synthflow/Retell + n8n/Make/Zapier + Jobber/ServiceTitan/Housecall Pro | Fast pilot, non-dev owner |
| **Custom** | Twilio/Vapi → Python FastAPI + LLM tool-calling → Calendar/SMS/CRM APIs | Full control, lower per-step SaaS, complex multi-step judgment |

**User preference signal (this workspace):** prefer **custom Python orchestration** over n8n when building “the same system without n8n.” Still use telephony SaaS (Twilio/Vapi) for the phone pipe.

### Custom architecture (replace n8n)

```
Phone/SMS → Twilio/Vapi webhook
         → FastAPI agent (LLM + tools)
         → book_appointment / lookup / sms / CRM / on-call alert
         → SQLite/Postgres for jobs + customers
         → cron for reminders/reviews
```

LLM routes to **real functions** (book, lookup_tech, send_review)—not rigid node boxes. Same capabilities as n8n; agent owns branching in natural language.

### Cost sketch

- Voice: ~$0.01–0.05/min + LLM pennies per call  
- Hosting: small VPS  
- vs n8n: similar infra + n8n subscription if cloud

## CRM options

Jobber, ServiceTitan, Housecall Pro, or Google Sheets for MVP.

## Example dispatcher contract

> Greet → problem + address → emergency? → next calendar slot → book → confirmation SMS → if after-hours emergency, text on-call tech.

## Implementation checklist

- [ ] Telephony (Twilio or Vapi) + number  
- [ ] Calendar source of truth  
- [ ] SMS path  
- [ ] CRM or sheet log  
- [ ] Emergency routing rules + on-call contact  
- [ ] After-hours vs business-hours policy  
- [ ] Phase-1 live test with real missed-call scenario  

## Parallel track: office agent v0 (no phone yet)

While telephony is pending, ship a **desk-side agent** on Hermes + Composio (this workspace preference: custom orchestration, not n8n):

1. Mail/tools linked via Hermes (skill `composio-with-hermes` — CLI bridge if Connect MCP 401s)  
2. Google Calendar linked for booking truth  
3. Job/lead log in Notion, Linear, or Sheets  
4. Optional owner-facing cron **only if requested** (do not invent morning digests)  
5. Only then: Twilio/Vapi receptionist (Phase 1 above)

Do not block all progress on phone setup. Email+calendar automation is real revenue (speed-to-lead) and validates tool wiring.

## Client Hermes profile (trade bot)

When the “AI employee” runs as a **separate Telegram bot**, use a **named Hermes profile**
(e.g. `plumbing`) — not the owner’s `default` chat:

- Install **profile gateway** systemd or the bot goes silent after process death.
- **One bot token → one running gateway** (duplicates break polling).
- Ops skill: **`hermes-client-profiles`** (+ `hermes-messaging-gateway`).

Owner GTM (roofer outreach) stays on **default** + Agent Mail; client front desk stays on the named profile.

## GTM: selling AI employees to roofers (and similar trades)

This workspace also **prospects** local roofing companies to offer free pilot setups (learn-by-doing), then optional monthly maintenance.

### Offer shape (user defaults)

- **Hook:** free implementation (VPS, automation, messaging gateway, working AI office employee)  
- **Paid later:** monthly maintain — price decided per engagement  
- **Channels in cold email:** faster lead response / missed-inquiry follow-up — **not** a voice-agent pitch unless the prospect asks  
- **Voice vs SMS:** decide **per client** after interest  
- **Volume:** 5–10 personalized emails/day  
- **Owner contact:** keep phone/WhatsApp internally for handoff, but cold emails should use **reply here / reply to this email** only; BCC owner outbound; CC owner when replying to threads  
- **Outbound mailbox:** **Agent Mail** (`composio-with-hermes`), not personal Gmail when available  

### Geo

Prefer **smaller US metros** first (less agency noise than Miami/Phoenix). Valid starting markets: **Boise/Nampa ID**, **Spokane WA**. One geo per batch.

### Pre-flight before any send

Collect: sender identity (Agent Mail inbox), owner BCC/CC email, offer one-liner, free scope, daily cap, geo.  
Do **not** mass-blast. Test-send to owner → batch.

### Lead pipeline

1. Bulk directory/search + Firecrawl **once per geo** → CRM bank (skill `roofer-lead-crm`)  
2. Daily: pull `new`+email from CRM (do **not** rescrape every batch)  
3. **Short** plain-text email + A/B subject; Agent Mail; BCC owner; log message ids  
4. Optional day-3 **follow-up** cron for non-replies only (not “re-batch” the same list)  
5. On reply: draft response, **CC** owner, book assessment  

### Cold email pitfalls

- Pitching **voice** in first touch when outreach is lead-response only  
- Using personal Gmail when Agent Mail is ACTIVE  
- Inventing emails not found on site  
- Long subjects/bodies after user asked for short  
- Confusing “batch 2” with follow-up to the same companies  
- Creating “helpful” digests/crons the user did not ask for  
- Sending before test-to-owner  
- Firecrawl on every 5 sends while CRM still has queue  

## Pitfalls

- Building marketing bots before after-hours phone (wrong ROI order **for the contractor product**)  
- For **GTM**, blocking all sales until voice works — office/lead-response pilot is enough to start  
- Treating LLM chat as enough without **write tools** (book/SMS)  
- Skipping confirmation SMS → higher no-shows  
- Over-automating licensed judgment; keep humans for quotes/diagnostics  
- Waiting on broken hosted Composio Connect MCP instead of **CLI + local MCP bridge**  

## References

- `references/custom-dispatcher-shape.md` — Python-shaped flow and tool stubs outline  
- `references/roofer-gtm-outreach.md` — short copy + batch vs follow-up checklist  
- Skill `roofer-lead-crm` — CRM bank, A/B, Agent Mail batches, follow-up crons  
- Skill `composio-with-hermes` — Agent Mail, Firecrawl, MCP bridge, optional digests  
- Skill `hermes-client-profiles` — multi-profile paths, gateway install, cleanup  
