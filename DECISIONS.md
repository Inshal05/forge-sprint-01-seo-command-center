# Decisions & Learnings Log

## 2026-06-06: Hook Repair
- **Decision:** Added `"type": "shell"` to all hook definitions in `.claude/settings.json`.
- **Why:** The Claude Code harness requires the `type` field to correctly dispatch shell commands; without it, the `audit.sh` script was not executing, causing `/doctor` to report invalid inputs.

## 2026-06-06: Readiness Analysis
- **Decision:** Prioritized the creation of the output contract (`report.schema.json`) over adding new detectors.
- **Why:** Schema validation is a hard requirement gate. Accuracy (detectors) is a scoring dimension, but missing required files can lead to total point loss for that category.

## 2026-06-06: Fixer Architecture Audit
- **Finding:** Discovered that `seo/fixer.py` was using deterministic logic instead of the required Ollama `ask()` calls.
- **Decision:** Marked as a P0 critical fix. LLM-generated rewrites are essential for the "Fix Champion" tier and overall human-scored quality.
