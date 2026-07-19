# Profile layout & gateway units

## Paths

| What | Path |
|------|------|
| Default Hermes home | `~/.hermes/` |
| Named profile root | `~/.hermes/profiles/<name>/` |
| Profile env/secrets | `~/.hermes/profiles/<name>/.env` |
| Profile config | `~/.hermes/profiles/<name>/config.yaml` |
| Profile persona | `~/.hermes/profiles/<name>/SOUL.md` |
| Profile gateway log | `~/.hermes/profiles/<name>/logs/gateway.log` |
| Profile gateway state | `~/.hermes/profiles/<name>/gateway_state.json` |
| CLI alias (optional) | `~/.local/bin/<name>` → `hermes -p <name>` |

## Systemd user units

| Profile | Typical unit |
|---------|----------------|
| default | `hermes-gateway.service` |
| named | `hermes-gateway-<name>.service` e.g. `hermes-gateway-plumbing.service` |

```bash
systemctl --user status hermes-gateway-plumbing
journalctl --user -u hermes-gateway-plumbing -n 50 --no-pager
```

## Recovery checklist (silent Telegram bot on named profile)

1. `hermes profile list` → Gateway column
2. `ps` / `gateway_state.json` PID alive?
3. Token hash unique among **running** gateways?
4. `hermes -p <name> gateway install --force --start-now --start-on-login`
5. Log: `✓ telegram connected`
6. User messages the **that** bot (not the default bot)

## Delete

```bash
hermes profile delete <name> -y
```

Without `-y`, confirm prompt cancels in non-interactive agents.
