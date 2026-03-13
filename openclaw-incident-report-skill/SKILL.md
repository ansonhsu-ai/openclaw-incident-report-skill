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

## Execution Constraints & Workflow (Strict Mode)

To maintain air-tight privacy and security, OpenClaw **MUST** execute the following steps locally in **Strict mode** before invoking any LLM text generation capabilities:

### 1A. Local Intake & Sanitization Orchestration (Strict Mode)
If the user provides raw incident logs, notes, or tickets:
- **Never ingest this content directly into the context window.**
- Request the user to save the raw notes to a local text file, e.g., `examples/raw-incident.txt`.
- Run the localized strict intake workflow script:
  ```bash
  python3 scripts/intake_workflow.py -i examples/raw-incident.txt -o examples/sanitized-incident.txt
  ```
- This orchestration script will:
  1. Call `scripts/sanitize.py` to deterministically mask values with `[REDACTED_EMAIL]`, `[REDACTED_SECRET_VALUE]`, etc.
  2. Call `scripts/review_sanitized.py` to scan the result for missed heuristics or unredacted tokens.
- **Stop unconditionally** if `intake_workflow.py` fails or warns about leftover sensitive content.
- If it returns "SUCCESS", you may now ingest the `sanitized-incident.txt` file.

### 1B. Local Intake via Direct Paste Mode
If the user pastes raw incident logs directly into the chat prompt:
- **Do not use the raw pasted text for downstream drafting or summarization.** Treat it only as intake material for the local sanitization pipeline.
- Immediately execute the direct paste helper script, feeding it the content:
  ```bash
  python3 scripts/direct_paste_intake.py --text "RAW_PASTED_TEXT_HERE"
  ```
- This script writes the pasted content to a local raw file (`examples/raw-pasted.txt`) and then automatically routes it through the standard Strict Mode sanitization checks.
- If it returns "SUCCESS", continue the workflow using only the generated sanitized file (`examples/sanitized-pasted.txt`) for later drafting and report preparation.
- Do not re-use or re-quote the raw pasted text in later prompt construction when a sanitized version is available.

### 2. Drafting the Configuration JSON
Read the successfully sanitized context. Engage the LLM capability to draft the final report narrative and fill out the structured format required by the report generator. Let OpenClaw write a configuration JSON (e.g., `config.json`).

The final configuration schema requires providing an `appendix` section outlining the event timeline, architecture, procedures, and follow-up measures. (Use the `templates/config-template.json` or `examples/example-config.json` for reference.)

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
