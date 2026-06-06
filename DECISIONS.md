# DECISIONS.md — decision & learnings log

A short running note of the real choices you made: what you tried, what failed and why, what
you changed. This is your engineering judgement on the record — it is what separates a builder
from a button-presser, and it is graded (challenge brief section 08).

Append a 1–2 line entry whenever you make a real decision or hit/fix a wall. Add a timestamp.

Format:
`[HH:MM] <decision or problem> → <what you did and why>`

---

## Example (replace with your own)
- `[10:20]` Chose plain-csv parsing over pandas → fewer deps, fast enough for 5k rows, model
  quota saved for the fixer.
- `[11:05]` Title detector over-counted duplicates → realized non-indexable pages were
  included; added an indexable+200 filter (per rulebook).
- `[12:40]` Dashboard wasn't updating live → MCP tool wasn't emitting the SSE event; added
  `_emit("issue", row)` in extract.

---

## My log

  - [12:15] Compared `seo/detector.py` against the SEO rulebook → identified multiple missing detectors affecting audit coverage and hidden-export accuracy.

  - [12:15] Implemented additional rulebook detectors → added title_too_short, missing_meta_description, duplicate_meta_description, meta_description_too_long, missing_h1, duplicate_h1, thin_content, non_indexable_but_linked, slow_page, and redirect_chain.

  - [12:16] Re-ran the sample export after detector updates → issue coverage increased from 4 detected issue types to 12 issue types while maintaining successful report generation.

  - [12:17] Added repository cleanup improvements → updated .gitignore and removed cache files before continuing implementation.

  - [12:18] Reviewed outputs/report.json after detector changes → verified output structure remained compatible with the required report contract.

  - [12:19] Inspected server.py reporting pipeline → identified seo_set_fixes() as the intended integration point for title fixes and redirect map generation.

  - [12:20] Updated CLAUDE.md project memory → documented architecture, detector strategy, validation workflow, and Ollama usage guidelines.

  - [12:21] Decided to keep issue detection fully deterministic → reserve Ollama exclusively for title generation, meta generation, redirect recommendations, and report enhancements.
  - [12:53] Added fix generation pipeline → integrated seo/fixer.py and populated redirect_map in report.json.
  - [13:01] Expanded title fix generation beyond missing titles → added handling for duplicate, too-short and too-long titles so the fixer produces actionable recommendations on real exports.
  - [13:07] Added CSV fix exports → generated title_fixes.csv and redirect_map.csv from report fixes to create client-ready deliverables.
