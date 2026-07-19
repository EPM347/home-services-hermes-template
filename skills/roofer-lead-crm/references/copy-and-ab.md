# Cold email copy + A/B (roofer GTM)

## Hard preferences (YOUR_NAME)

- Short **title** (subject) and short **body** after baseline Batch 1.
- Vary subjects across batches; score reply rate in `roofer_ab_results.json`.
- No voice / Vapi / “AI phone” in first touch.

## Subject variants

| Key | Pattern |
|-----|---------|
| S1_long_baseline | `Quick idea for {Company} — faster lead response (free setup)` — **Batch 1 only** |
| S2_missed_leads | `{Company} — missed leads?` |
| S3_free_setup | `Free setup for {Company}` |
| S4_15min | `15 min for {Company}?` |
| S5_short_idea | `Idea for your office` |

## Body B2 (default short)

```
Hi {Company} team,

Local roofers lose jobs when leads sit. I set up a free AI office helper
for faster lead reply (forms/after-hours). First few shops free while I
prove it.

15 min this week? WhatsApp +1-555-000-0000 or reply here.

YOUR_NAME
```

## Follow-up body (shorter)

```
Hi {Company} team — quick bump on my note about a free AI office helper
for faster lead reply. Happy to show it in 10 minutes if useful.
WhatsApp +1-555-000-0000 or reply here. — YOUR_NAME
```

## Scoring

Per send: `subject_variant`, `body_variant`, `replied`, `reply_at`.  
Winner = highest reply rate after enough volume per variant.
