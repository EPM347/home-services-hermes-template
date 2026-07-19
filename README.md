# Home-Services Hermes Template

Reusable starter kit to run **AI “employee” agents** for plumbing / HVAC / roofing on a VPS with [Hermes Agent](https://hermes-agent.nousresearch.com/).

Built from a real setup (multi-profile Telegram bots, front-desk SOUL, lead CRM + outreach patterns, Composio tools).

## What you get

| Piece | Purpose |
|-------|---------|
| `profiles/plumbing/` | Ready SOUL + profile metadata for a **plumbing front desk** bot |
| `profiles/trade-frontdesk/` | Same pattern, rename for HVAC/roofing |
| `skills/` | Ops playbooks (home-services product, roofer CRM GTM, multi-profile gateway) |
| `crm/templates/` | Empty CRM schema + short cold-email playbook |
| `scripts/` | Create profile, install gateway service, CRM helpers |
| `config/config.snippet.yaml` | Safe Hermes config snippets (e.g. clean cron delivery) |
| `docs/` | Beginner maps + VPS checklist |

**Not included (on purpose):** API keys, bot tokens, OAuth files, real customer data.

## Requirements

- Ubuntu/Debian VPS (2–4 GB RAM minimum; 4 GB comfortable)
- [Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation) installed
- A **separate Telegram bot** per client profile (BotFather)
- Model access (Nous Portal / xAI / OpenRouter / etc.)

Optional: [Composio](https://composio.dev) CLI for Gmail/Agent Mail/Calendar/Firecrawl.

## Quick start (new VPS)

```bash
# 1) Install Hermes (official installer)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2) Login / model
hermes setup
# or: hermes auth / hermes model

# 3) Clone this template
git clone https://github.com/EPM347/home-services-hermes-template.git
cd home-services-hermes-template

# 4) Create a client profile from the plumbing template
./scripts/create_client_profile.sh plumbing

# 5) Put secrets in the profile .env (never commit)
nano ~/.hermes/profiles/plumbing/.env
# TELEGRAM_BOT_TOKEN=...
# TELEGRAM_ALLOWED_USERS=your_id

# 6) Install profile gateway as a service (survives reboot/logout)
hermes -p plumbing gateway install --force --start-now --start-on-login

# 7) Verify
hermes profile list
hermes -p plumbing gateway status
```

Message the **plumbing bot** on Telegram (not your personal main Hermes bot).

## Mental model (beginner)

```
~/.hermes/                      ← YOUR main agent (default)
~/.hermes/profiles/
   plumbing/                    ← client “employee” bot
      .env                      ← secrets
      config.yaml
      SOUL.md                   ← personality + rules
      sessions/ memories/ logs/
```

- **One Telegram bot token → one running gateway**
- Don’t run two profiles that share the same bot token
- Always `gateway install` for client profiles or the bot goes silent when the process dies

## GTM / lead bank (optional)

See `skills/roofer-lead-crm/` and `crm/templates/`.

Pattern:

1. Bulk scrape a city once → CRM JSON/CSV  
2. Send 5–10 short emails/day (Agent Mail)  
3. Update status in CRM (don’t rescrape every batch)  
4. Day-3 follow-up only for no-replies  

## Composio MCP note

Hosted `connect.composio.dev/mcp` may return 401. Prefer:

- Composio CLI (`composio execute …`), and/or  
- Local stdio bridge: copy `scripts/composio-mcp-bridge.py` → `~/.hermes/bin/` and wire `mcp_servers` as in `config/config.snippet.yaml`

## Safety

- Never invent prices, licenses, or calendar slots  
- Escalate gas leaks / flooding / sewage — see SOUL emergency section  
- Keep humans for quotes and licensed judgment  

## License

MIT — use and adapt for your clients.
