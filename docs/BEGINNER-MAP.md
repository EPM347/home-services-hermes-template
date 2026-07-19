# Beginner map: folders

## Default vs profile

| | Default | Profile (e.g. plumbing) |
|--|---------|-------------------------|
| Path | `~/.hermes/` | `~/.hermes/profiles/<name>/` |
| Who | You (owner) | Client AI employee |
| Telegram | Your main bot | Separate BotFather bot |
| Gateway service | `hermes-gateway.service` | `hermes-gateway-<name>.service` |

## Important files

- `.env` — secrets only  
- `config.yaml` — behavior  
- `SOUL.md` — how the agent speaks and decides  
- `logs/gateway.log` — why Telegram is silent  

## Cleanup rule

Delete unfinished stubs and duplicate profiles that share the same bot token.
