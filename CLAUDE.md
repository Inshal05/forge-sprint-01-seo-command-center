# CLAUDE.md — SEO Command Center Project Memory

## Project Goal

Build a Claude Code plugin that ingests a Screaming Frog export, detects SEO issues using deterministic rules, prioritizes findings, generates fixes, serves a live dashboard on localhost:7700, and outputs:

- outputs/report.json
- outputs/report.html

Target stack:

- Claude Code
- MCP Server
- Ollama (qwen3.5:9b)
- Local dashboard
- Fully offline audit logic

---

## Competition Constraints

- Detection logic must be deterministic Python.
- Never use LLMs for issue detection.
- Use Ollama only for:
  - title generation
  - meta description generation
  - redirect recommendations
  - recommendation writing
- report.json must match report.schema.json.
- Must work on hidden exports.
- Dashboard must update while audit runs.
- Keep process logs, commits, prompts, and decisions updated.

---

## Current Architecture

### Pipeline

run.py

load → detect → recommend → report → export

### Detection Engine

seo/detector.py

Implemented detectors:

- missing_title
- duplicate_title
- title_too_long
- title_too_short
- missing_meta_description
- duplicate_meta_description
- meta_description_too_long
- missing_h1
- duplicate_h1
- broken_link
- server_error
- redirect
- redirect_chain
- orphan_page
- thin_content
- non_indexable_but_linked
- slow_page

### Reporting

mcp/server.py

Outputs:

- report.json
- report.html

Dashboard:

- localhost:7700

---

## Development Decisions

### Detector Strategy

Only evaluate title and meta issues on:

- text/html pages
- status code 200
- indexable pages

### Redirect Analysis

Redirect chains detected through redirect graph traversal.

Future improvement:

- separate loops from chains
- generate redirect suggestions

### Duplicate Detection

Use grouped URL collections to identify:

- duplicate titles
- duplicate meta descriptions
- duplicate H1s

---

## Ollama Strategy

Model:

qwen3.5:9b

Use only for:

- title fixes
- meta fixes
- redirect recommendations

Never use Ollama for:

- issue detection
- counting issues
- severity assignment
- crawl analysis

---

## Validation Checklist

Before every commit:

- Run python run.py ../sample-export
- Verify report.json exists
- Verify report.html exists
- Verify dashboard loads
- Verify issue counts are reasonable

Before submission:

- Validate report.json against schema
- Verify audit.jsonl exists
- Verify agent-log.md exported
- Verify CLAUDE.md updated
- Verify PROMPTS.md updated
- Verify DECISIONS.md updated
- Verify 10+ commits exist

---

## Build Learnings

- Starter bundle only implemented a subset of the SEO rulebook.
- Issue detection accuracy is the most valuable scoring category.
- Deterministic rules are more reliable than LLM analysis for crawl data.
- report generation already exists in server.py.
- seo_set_fixes() is the intended hook for title fixes and redirect maps.
- Hidden export compatibility is more important than optimizing for the sample export.