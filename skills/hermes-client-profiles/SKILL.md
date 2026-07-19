---
name: hermes-client-profiles
description: "Run and troubleshoot separate Hermes profiles for client/business bots (e.g. plumbing front desk) alongside default. Profile paths, gateway systemd install, Telegram bot-token conflicts, cleanup of stubs/duplicates, beginner mental model. Use when a named profile gateway is stopped, Telegram bot silent, or user asks how many profiles / where profiles live."
---

# Hermes client profiles (multi-bot)

## Mental model (beginner)

- **Default profile** = main Hermes home: `~/.hermes/` (often the owner’s personal chat).
- **Named profiles** = separate mini-Hermes instances under `~/.hermes/profiles/<name>/` (each can have its own Telegram bot, SOUL, memory, sessions).
- A profile is **not working** most often because its **gateway process died** — not because the bot token vanished.

```
~/.hermes/                         ← default
~/.hermes/profiles/
  plumbing/                        ← client bot A
  <other-client>/
```

Inside a full profile: `.env`, `config.yaml`, `SOUL.md`, `sessions/`, `memories/`, `skills/`, `logs/`.

Optional CLI alias: `~/.local/bin/<name>` → `hermes -p <name>`.

## Diagnose “profile not working”

1. `hermes profile list` — note Gateway **running** vs **stopped**.
2. `hermes profile show <name>` — path, model, alias, `.env` present?
3. `cat ~/.hermes/profiles/<name>/gateway_state.json` — last PID / telegram state.
4. `ps -p <pid>` — if dead, process exited and nothing restarted it.
5. Tail `~/.hermes/profiles/<name>/logs/gateway.log` and `gateway-exit-diag.log`.
6. Compare Telegram tokens **by hash** across profiles (never print full tokens):

```bash
# sha of TELEGRAM_BOT_TOKEN per profile — identical hash = same bot = conflict if both gateways run
```

## Fix: keep client gateway alive

Install **profile-scoped** user systemd (not the default unit only):

```bash
hermes -p <name> gateway install --force --start-now --start-on-login
hermes -p <name> gateway status
# Expect: hermes-gateway-<name>.service active, telegram connected
```

Linger should stay enabled so logout doesn’t kill user services.

**Do not** run `hermes gateway restart` from inside a gateway-handled chat for another profile’s unit without `-p`; prefer the profile-scoped commands.

## Telegram bot-token rule

- **One live gateway per bot token.**
- Cloned profiles often **share** the same `TELEGRAM_BOT_TOKEN` → second start fights polling / looks “broken.”
- If two profiles share a hash: keep **one** running; delete or re-token the other.

## Cleanup stubs and duplicates

When user asks to clean extras:

```bash
hermes profile delete <stub-or-duplicate> -y   # requires -y (interactive confirm otherwise cancels)
hermes profile list                            # verify only intended profiles remain
hermes -p <kept> gateway status                # kept client still running
```

Stub smell: profile dir with only `sandboxes/`, no `.env`, 0 skills, no model.

## Explaining locations to beginners

- Prefer a **simple folder map** (text tree + optional diagram image).
- Paths are under the **server** home (`/home/hermes/...`), not the user’s phone.
- “Deleted” = profile directory (+ alias) removed; default and kept profiles untouched.

## User prefs seen in this workspace

- Keep **one** working trade bot profile when duplicates exist (e.g. keep `plumbing`, drop `apex-plumbing` + empty `plumbing-frontdesk`).
- Personal/ops chat stays on **default**; client persona on named profile + its bot.

## Pitfalls

- Assuming `hermes -p X status` “Gateway running” always means X’s process — always confirm unit name / `--profile` in process argv.
- Starting apex + plumbing with the **same** token.
- Leaving client gateway as a one-off manual process (dies → silent bot).
- Editing another profile’s files without explicit user direction (cross-profile guard).
- Confusing empty frontdesk stubs with production profiles.

## Related

- Bundled `hermes-agent` — general CLI (do not patch; read for commands).
- `home-services-ai-agents` — what the plumbing bot is *for* (roles/product).
- `roofer-lead-crm` — owner GTM on default profile, separate from client bots.

## Support files

- `references/profile-layout.md` — paths, unit names, checklist
