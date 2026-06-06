# PROMPTS.md — my key prompts log

Keep the handful of prompts that actually moved the build. Not every message — the ones that
mattered: the system/sub-agent prompts, the ones you iterated on, the "this finally worked"
moment. This shows how you direct an AI, which is graded (challenge brief section 08).

Format per entry:
- **Prompt** (paste it)
- **For:** what you were trying to do
- **Revised?** did you have to change it, and why

---

## Example (replace with your own)

- **Prompt:** "Extend seo/detector.py to detect redirect chains: build a map of {Address ->
  Redirect URL} for all 3xx rows, then a chain exists when a Redirect URL is itself a key in
  that map. Add a redirect_chain issue (High). Run python seo/detector.py and show counts."
- **For:** adding the redirect-chain detector
- **Revised?** Yes — first version flagged single redirects as chains; added the "target is
  also a redirecting URL" condition.

---

## My prompts

### 1

- **Prompt:** "Review seo/detector.py against the SEO rulebook and identify all missing detectors required for scoring."

- **For:** Finding gaps between the starter implementation and the required SEO rulebook.

- **Revised?** No.

---

### 2

- **Prompt:** "Implement the missing rulebook detectors while preserving the existing detector architecture and report output format."

- **For:** Improving issue-detection accuracy without breaking the reporting pipeline.

- **Revised?** Yes. The implementation was reorganized into title, meta, H1, content and redirect sections for maintainability.

---

### 3

- **Prompt:** "Validate detector output by running the sample export and compare issue coverage before and after implementation."

- **For:** Verifying that new detectors increased audit coverage and did not break the audit workflow.

- **Revised?** No.

---

### 4

- **Prompt:** "Review server.py and identify where fix generation should integrate into the existing architecture."

- **For:** Planning title fixes, redirect maps and Ollama integration.

- **Revised?** No.
### 5

- **Prompt:** "Review the fixer architecture and implement fix generation without breaking the reporting pipeline."

- **For:** Adding title fixes and redirect map generation.

- **Revised?** Yes. Started with deterministic fixes before introducing Ollama.
