# CRM paths & merge rules

## Files under `~/.hermes/shared/`

| File | Role |
|------|------|
| `roofer_crm_boise.json` | Source of truth for agent scripts |
| `roofer_crm_boise.csv` | Export / Sheet seed |
| `roofer_outreach_log.json` | Per-send message ids + ok flag |
| `roofer_ab_results.json` | Variant counters + per-send rows |
| `roofer_outreach_playbook.md` | Human-readable rules + schedule notes |
| `roofer_crm_README.md` | Workflow overview |
| `roofer_crm_drive_result.json` | Last Drive upload metadata |

## Google Sheet

https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit  
Created via `GOOGLEDRIVE_CREATE_FILE_FROM_TEXT` with spreadsheet mime + CSV text.

## Linear

Team UUID example: `4c85193d-ccf3-4051-ad0a-645ab56f4664` (YOUR_NAME prvs / EMO).  
Issue EMO-5 tracks CRM workflow — not a substitute for the JSON CRM.

## Merge by domain

When scraping, key leads by `urlparse(url).netloc` without `www.`.  
Merge contact-page scrapes into the same company; prefer shorter company name; union emails/phones.

## Rescrape gate

Only bulk Firecrawl when `count(status==new and email)` **&lt; 5**.
