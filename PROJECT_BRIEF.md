# Project Brief

## Goal
Create an OpenClaw-compatible skill based on `OEN-Tech/incident-report-skill`.

## Core requirements
1. Reproduce equivalent skill capability for OpenClaw.
2. Preserve the useful reporting workflow and document-generation behavior.
3. Add a mandatory **de-identification / sanitization step** before any sensitive incident content is sent to an LLM.
4. The de-identification mechanism must remove or mask sensitive fields such as:
   - names
   - phone numbers
   - email addresses
   - addresses
   - customer identifiers
   - account identifiers
   - API keys / tokens / secrets
   - IPs / domains if they are considered sensitive in context
   - any directly identifying incident details the user marks as sensitive
5. The resulting skill should be usable by OpenClaw.

## Desired output
- A new skill package in this workspace
- Clear instructions for usage in OpenClaw
- Sanitization-first workflow documentation
- Supporting scripts/templates as needed

## Constraints
- Do not send raw sensitive incident details to the LLM.
- Prefer deterministic local sanitization before any model step.
- Keep the skill practical and reusable.
- Keep references to Taiwan incident report format where relevant.

## Acceptance criteria
- There is a valid OpenClaw skill structure.
- The skill documentation clearly states when to use it.
- There is a documented sanitization/de-identification workflow.
- Sensitive inputs can be transformed locally before LLM processing.
- There is a repeatable generation path for the final report.
