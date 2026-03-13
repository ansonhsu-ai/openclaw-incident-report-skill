---
name: incident-report-skill
description: A privacy-first skill for OpenClaw to generate cybersecurity incident reports in the official Taiwan government format with a mandatory local sanitization step.
---

# OpenClaw Incident Report Skill — 資安事件通報報告產生器 (Privacy-First)

Generate cybersecurity incident reports in the official Taiwan government format (個人資料侵害事故通報與紀錄表) as `.docx` files.

This OpenClaw skill follows the notification format required by Taiwan's Ministry of Digital Affairs (數位發展部) under the Personal Data Protection Act (個人資料保護法). **Crucially, it implements a mandatory local sanitization and de-identification step** to ensure no sensitive PII, credentials, or internal tokens are sent to any LLM during the drafting process.

## When to Use

Use this skill when the user asks to:
- Create a cybersecurity incident report (資安事件報告)
- Generate a government notification form (通報表)
- Write an incident report for a Taiwan regulatory body
- Respond to a data breach notification requirement
- Create a 個人資料侵害事故通報 document

## Execution Constraints & Workflow

To maintain air-tight privacy and security, OpenClaw **MUST** execute the following steps locally on the user's machine before doing any LLM-powered content generation:

### 1. Mandatory Local Sanitization
If the user provides raw incident logs, notes, or tickets that contain sensitive information (emails, phone numbers, IP addresses, credentials, UUIDs):
- **Do not send this content directly to the LLM context.**
- Request the user to save the raw notes to a local text file, e.g., `examples/raw-incident.txt`.
- Run the local Python sanitization script:
  ```bash
  python3 scripts/sanitize.py -i examples/raw-incident.txt -o examples/sanitized-incident.txt
  ```
- This script uses deterministic regular expressions to replace identifiers with tags like `[REDACTED_EMAIL]`, `[REDACTED_IP]`, etc.
- Only ingest and summarize the *sanitized* content file (`sanitized-incident.txt`) into context for subsequent drafting.

### 2. Drafting the Configuration JSON
Read the strictly-sanitized context. Engage the LLM capability to draft the final report narrative and fill out the structured format required by the report generator. Let OpenClaw write a configuration JSON (e.g., `config.json`).

The final configuration schema requires providing an `appendix` section outlining the event timeline, architecture, procedures, and follow-up measures. (See `examples/example-config.json` for reference.)

### 3. Generate Report Locally
Once the JSON configuration is fully drafted and approved by the user, invoke the document generator:
```bash
python3 scripts/generate.py --config config.json --output incident-report.docx
```
The generator now creates missing parent output directories automatically, so nested output paths are allowed.
Provide the `.docx` to the user for final review and editing.

### 4. Privacy-first operating note
Use the LLM only after the raw incident material has been sanitized locally.
Do not paste raw notes containing personal data, credentials, API keys, tokens, secrets, passwords, or internal identifiers into model context.
If the user provides raw notes directly, first save them locally, sanitize them with `scripts/sanitize.py`, and only then use the sanitized result for drafting.

## Report Format & Contents
Generated documents follow the standard **個人資料侵害事故通報與紀錄表**:
1. **Part 1**: The form including company name, reporter info, incident details, possible consequences.
2. **Part 2**: The appendix outlining incident summary, relation to company, timeline, technical architecture analysis, audit results, and conclusions.

## Directory Structure
- `scripts/sanitize.py`: Local deterministic de-identifier for PII and sensitive values such as API tokens, API keys, bearer tokens, secrets, passwords, credentials, UUIDs, emails, phone numbers, IPs, MAC addresses, and Taiwan ID card numbers.
- `scripts/generate.py`: The `.docx` generation script.
- `examples/example-config.json`: Sample configuration for `generate.py`.
- `examples/raw-incident.txt`: Example raw input containing sensitive data.
- `examples/sanitized-incident.txt`: Example sanitized result for safe LLM drafting.

Use the combination of these scripts and OpenClaw agentic oversight to produce compliant, safe incident reports.
