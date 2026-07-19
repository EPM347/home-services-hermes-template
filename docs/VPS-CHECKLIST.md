# VPS checklist

- [ ] Hermes installed + model auth works (`hermes chat -q "hi"`)
- [ ] Systemd linger: `loginctl enable-linger $USER` (or install does it)
- [ ] Unique Telegram bot per profile
- [ ] `hermes -p <name> gateway install --start-now --start-on-login`
- [ ] `hermes profile list` shows gateway **running**
- [ ] Test DM to client bot
- [ ] Optional: Composio login + Agent Mail / Calendar
- [ ] Optional: `cron.wrap_response: false` for clean scheduled messages
- [ ] Backups: export profile or copy `profiles/<name>` without committing `.env`
