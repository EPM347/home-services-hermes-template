# Custom dispatcher (no n8n)

## Components

1. **Telephony** — Twilio voice/SMS or Vapi/Retell for the LLM voice loop  
2. **Backend** — FastAPI/Flask webhook receiver  
3. **Agent loop** — LLM with tool schemas  
4. **Tools** — pure functions with side effects (calendar, SMS, CRM, on-call)  
5. **Store** — SQLite → Postgres when multi-tech  
6. **Scheduler** — cron/APScheduler for reminders + review texts  

## Call flow

```
POST /incoming-call (or media stream)
  → transcript / speech events
  → agent.decide(user_text, history)
  → optional tool_calls: book_appointment, check_emergency, page_on_call
  → TTS / TwiML reply
```

## Tool stubs (conceptual)

```python
def book_appointment(address: str, problem: str, when: str) -> str: ...
def send_sms(to: str, body: str) -> str: ...
def page_on_call(summary: str) -> str: ...
def log_job(customer: dict, notes: str) -> str: ...
```

## vs n8n

n8n = visual if/HTTP nodes. Custom = LLM chooses tools; host owns code and hosting. Capabilities match; custom wins on complex multi-step judgment and avoiding per-node SaaS limits.

## Phase-1 MVP scope

- After-hours only  
- Capture address + issue  
- Book next morning slot OR page on-call if emergency keywords  
- SMS confirmation  
- Log row to sheet/CRM  
