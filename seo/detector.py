"""
detector.py — deterministic SEO issue detection from a Screaming Frog internal_all.csv.

STARTER IMPLEMENTATION. It already detects several issues so the pipeline runs end to
end. Your job in the Sprint is to COMPLETE the rulebook (see rulebook.md): add the
missing detectors, handle edge cases, and improve accuracy against the hidden export.

Standard library only (csv). Detection is plain Python on purpose — the model is for
judgment (rewriting titles, choosing redirect targets), not for counting rows.
"""

from __future__ import annotations
import csv
import os
from collections import defaultdict


def load_rows(export_dir: str) -> list[dict]:
    path = os.path.join(export_dir, "internal_all.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _int(v, default=0):
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default


def _float(v, default=0.0):
    try:
        return float(str(v).strip())
    except Exception:
        return default


def is_html(r):  return "text/html" in (r.get("Content Type", "") or "").lower()
def is_200(r):   return _int(r.get("Status Code")) == 200
def indexable(r): return (r.get("Indexability", "") or "").strip().lower() == "indexable"

def load_issue_csv(export_dir: str, filename: str) -> list[dict]:
    path = os.path.join(
        export_dir,
        "issues_reports",
        filename
    )

    if not os.path.exists(path):
        return []

    with open(
        path,
        encoding="utf-8-sig",
        newline=""
    ) as f:
        return list(csv.DictReader(f))

def detect(
    rows: list[dict],
    export_dir: str | None = None
) -> list[dict]:
    """Return a list of issue dicts: {type, severity, affected_urls, count, explanation}.
    STARTER set — extend to the full rulebook for a high score."""
    issues = []

    def add(t, sev, urls, explanation):
        urls = sorted(set(urls))
        if urls:
            issues.append({"type": t, "severity": sev, "affected_urls": urls,
                           "count": len(urls), "explanation": explanation})

    html = [r for r in rows if is_html(r)]
    idx200 = [r for r in html if is_200(r) and indexable(r)]

    # --- Titles ---
    add("missing_title", "High",
        [r["Address"] for r in idx200 if not (r.get("Title 1", "") or "").strip()],
        "Indexable pages with no title tag.")

    # duplicate titles (indexable only)
    by_title = defaultdict(list)
    for r in idx200:
        t = (r.get("Title 1", "") or "").strip()
        if t:
            by_title[t].append(r["Address"])
    dup_t = [u for urls in by_title.values() if len(urls) > 1 for u in urls]
    add("duplicate_title", "High", dup_t, "Pages sharing an identical title.")

    add("title_too_long", "Medium",
        [r["Address"] for r in idx200
         if _int(r.get("Title 1 Pixel Width")) > 561 or _int(r.get("Title 1 Length")) > 60],
        "Titles likely truncated in search results.")

    # --- Response codes ---
    add("broken_link", "High",
        [r["Address"] for r in rows if 400 <= _int(r.get("Status Code")) <= 499],
        "URLs returning a client error (4xx).")
    add("server_error", "High",
        [r["Address"] for r in rows if 500 <= _int(r.get("Status Code")) <= 599],
        "URLs returning a server error (5xx).")
    add("redirect", "Medium",
        [r["Address"] for r in rows if 300 <= _int(r.get("Status Code")) <= 399],
        "URLs that redirect (3xx).")

    # --- Orphan pages ---
    add("orphan_page", "Medium",
        [r["Address"] for r in idx200 if _int(r.get("Inlinks")) == 0],
        "Indexable pages with zero internal links in.")

    # ----------------------------------------------------------------------- #
    # -----------------------------
    # TITLE ISSUES
    # -----------------------------

    add(
        "title_too_short",
        "Low",
        [
            r["Address"]
            for r in idx200
            if 0 < _int(r.get("Title 1 Length")) < 30
        ],
        "Titles shorter than recommended."
    )

    # -----------------------------
    # META DESCRIPTION ISSUES
    # -----------------------------

    add(
        "missing_meta_description",
        "Medium",
        [
            r["Address"]
            for r in idx200
            if not (r.get("Meta Description 1", "") or "").strip()
        ],
        "Pages missing meta descriptions."
    )

    by_meta = defaultdict(list)

    for r in idx200:
        meta = (r.get("Meta Description 1", "") or "").strip()

        if meta:
            by_meta[meta].append(r["Address"])

    duplicate_meta_urls = [
        url
        for urls in by_meta.values()
        if len(urls) > 1
        for url in urls
    ]

    add(
        "duplicate_meta_description",
        "Medium",
        duplicate_meta_urls,
        "Duplicate meta descriptions."
    )

    add(
        "meta_description_too_long",
        "Low",
        [
            r["Address"]
            for r in idx200
            if _int(r.get("Meta Description 1 Length")) > 155
        ],
        "Meta descriptions exceeding recommended length."
    )

    # -----------------------------
    # H1 ISSUES
    # -----------------------------

    add(
        "missing_h1",
        "Medium",
        [
            r["Address"]
            for r in html
            if is_200(r)
            and not (r.get("H1-1", "") or "").strip()
        ],
        "Pages missing H1."
    )

    by_h1 = defaultdict(list)

    for r in html:
        if not is_200(r):
            continue
        h1 = (r.get("H1-1", "") or "").strip()

        if h1:
            by_h1[h1].append(r["Address"])

    duplicate_h1_urls = [
        url
        for urls in by_h1.values()
        if len(urls) > 1
        for url in urls
    ]

    add(
        "duplicate_h1",
        "Low",
        duplicate_h1_urls,
        "Duplicate H1 headings."
    )

    # -----------------------------
    # CONTENT ISSUES
    # -----------------------------

    add(
        "thin_content",
        "Low",
        [
            r["Address"]
            for r in idx200
            if _int(r.get("Word Count")) < 200
        ],
        "Thin content pages."
    )

    add(
        "non_indexable_but_linked",
        "Medium",
        [
            r["Address"]
            for r in html
            if not indexable(r)
            and _int(r.get("Inlinks")) > 0
        ],
        "Linked pages that are non-indexable."
    )

    add(
        "slow_page",
        "Low",
        [
            r["Address"]
            for r in html
            if _float(r.get("Response Time")) > 1.0
        ],
        "Pages slower than one second."
    )

    # -----------------------------
    # REDIRECT ISSUES
    # -----------------------------

    redirects = {}

    for r in rows:
        status = _int(r.get("Status Code"))

        if 300 <= status <= 399:
            redirects[r["Address"]] = (
                r.get("Redirect URL", "") or ""
            ).strip()

    redirect_chain_urls = []

    for start_url in redirects:

        visited = set()
        current = start_url

        while current in redirects:

            if current in visited:
                redirect_chain_urls.append(start_url)
                break

            visited.add(current)

            next_url = redirects[current]

            if next_url in redirects:
                redirect_chain_urls.append(start_url)
                break

            current = next_url

    add(
        "redirect_chain",
        "High",
        redirect_chain_urls,
        "Redirect chains or loops detected."
    )
    # ----------------------------------------------------------------------- #
    if export_dir:

        missing_alt_rows = load_issue_csv(
            export_dir,
            "images_missing_alt_text.csv"
        )

        add(
            "missing_image_alt",
            "Medium",
            [
                r["Address"]
                for r in missing_alt_rows
            ],
            "Images missing alt text."
        )
    return issues


def summarize(issues: list[dict]) -> dict:
    by_sev = defaultdict(int)
    for i in issues:
        by_sev[i["severity"]] += 1
    return {"total_issues": len(issues),
            "by_severity": {"High": by_sev["High"], "Medium": by_sev["Medium"], "Low": by_sev["Low"]}}


if __name__ == "__main__":
    import sys, json
    d = sys.argv[1] if len(sys.argv) > 1 else "../sample-export"
    rows = load_rows(d)
    iss = detect(rows)
    print(f"Loaded {len(rows)} rows, detected {len(iss)} issue types.")
    print(json.dumps(summarize(iss), indent=2))
    for i in iss:
        print(f"  [{i['severity']:<6}] {i['type']:<24} x{i['count']}")
