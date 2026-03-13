## Implementation Plan

## Proposed workspace
- `reference-upstream/` — cloned upstream repo for study only
- `openclaw-incident-report-skill/` — new OpenClaw skill implementation (DONE)

## Proposed deliverables
1. OpenClaw skill folder with:
   - `SKILL.md` (Created)
   - `examples/` (Created, with example config and testing resources)
   - `scripts/` (Created)
2. Local sanitization utility for de-identification (Created `sanitize.py`)
3. Example sanitized config / usage flow (Created `raw-incident.txt` -> `sanitized-incident.txt`)
4. Packaged `.skill` artifact if validation succeeds (Tested successfully via local python execution)

## Architecture direction
- Reuse the upstream report-generation concept (Done, copied `generate.py`)
- Do not rely on raw incident details being sent directly to an LLM (Enforced in SKILL.md)
- Add a local preprocessing stage:
  1. raw incident input
  2. local sanitization / masking (Done deterministic masking)
  3. sanitized summary for LLM-assisted drafting if needed
  4. final deterministic document generation

## Key design decisions to make
- Whether to reuse the upstream generator directly or adapt it (Reused, copied as `scripts/generate.py`)
- Which fields are always masked vs optionally masked (Pattern matching covers general emails, IPs, MACs, UUIDs, generic tokens)
- Whether the LLM is used only for drafting narrative sections (Yes, LLM writes config payload, local code builds Docx)

## Validation plan
- Validate skill structure (Confirmed)
- Validate sanitization on sample sensitive inputs (Passed: `raw-incident.txt` tested)
- Validate that report generation still works after sanitization-aware workflow is introduced (Confirmed)
