# openclaw-incident-report-skill

Privacy-first OpenClaw skill for generating Taiwan-format cybersecurity / personal data breach incident reports.

This project adapts the upstream `OEN-Tech/incident-report-skill` concept into an **OpenClaw-compatible skill** and adds a mandatory **local sanitization / de-identification step** before any content is sent to an LLM.

## Goals

- Generate reports in the official Taiwan **個人資料侵害事故通報與紀錄表** style
- Preserve the useful report-generation workflow from the upstream project
- Prevent raw sensitive information from being sent directly to LLMs
- Provide a repeatable local path for sanitization and `.docx` generation

## Key features

### 1. Privacy-first sanitization
The included `scripts/sanitize.py` performs deterministic local masking for sensitive values such as:
- email
- phone
- IPv4
- MAC address
- UUID
- Taiwan ID card number
- bearer token
- API token
- API key
- secret
- password
- credentials
- key/value style token-like secret values

### 2. Local `.docx` generation
The included `scripts/generate.py` generates the final report as a `.docx` file.
It now creates missing parent output directories automatically.

### 3. OpenClaw skill structure
The project contains a valid OpenClaw skill implementation under:

- `openclaw-incident-report-skill/`

## Repository structure

- `openclaw-incident-report-skill/SKILL.md` — main skill instructions
- `openclaw-incident-report-skill/scripts/sanitize.py` — local de-identification script
- `openclaw-incident-report-skill/scripts/generate.py` — report generator
- `openclaw-incident-report-skill/examples/example-config.json` — sample config
- `openclaw-incident-report-skill/examples/raw-incident.txt` — sample raw sensitive input
- `openclaw-incident-report-skill/examples/sanitized-incident.txt` — sample sanitized result
- `dist/openclaw-incident-report-skill.skill` — packaged skill artifact
- `reference-upstream/` — upstream repo as a submodule reference

## Recommended operating flow

1. Save raw incident notes locally
2. Run local sanitization first
3. Use only sanitized content for any LLM-assisted drafting
4. Produce the final JSON/config content
5. Generate the final `.docx` locally

## Example usage

### Step 1: sanitize raw incident notes

```bash
python3 openclaw-incident-report-skill/scripts/sanitize.py \
  -i openclaw-incident-report-skill/examples/raw-incident.txt \
  -o openclaw-incident-report-skill/examples/sanitized-incident.txt
```

### Step 2: generate report

```bash
python3 openclaw-incident-report-skill/scripts/generate.py \
  --config openclaw-incident-report-skill/examples/example-config.json \
  --output output/incident-report.docx
```

## Installation

### Install Python dependency

```bash
python3 -m pip install --user python-docx
```

### Install as an OpenClaw skill

Copy the skill folder into your local OpenClaw skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/incident-report-skill
rsync -a ./openclaw-incident-report-skill/ ~/.openclaw/workspace/skills/incident-report-skill/
```

## Validation status

This project has been validated for:
- skill structure validity
- local sanitization behavior
- packaged `.skill` generation
- successful `.docx` output generation

## Upstream reference

This project is based on:
- <https://github.com/OEN-Tech/incident-report-skill>

The upstream repository is included here as a **git submodule** under `reference-upstream/` for study and comparison.
