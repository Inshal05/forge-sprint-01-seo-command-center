from __future__ import annotations

from collections import defaultdict


def _int(value, default=0):
    try:
        return int(float(str(value).strip()))
    except Exception:
        return default


def generate_title_fixes(rows):
    fixes = []

    # Build duplicate title map
    title_groups = defaultdict(list)

    for row in rows:
        title = (row.get("Title 1", "") or "").strip()

        if title:
            title_groups[title].append(row)

    duplicate_titles = {
        title
        for title, pages in title_groups.items()
        if len(pages) > 1
    }

    for row in rows:

        url = row.get("Address", "")
        title = (row.get("Title 1", "") or "").strip()
        h1 = (row.get("H1-1", "") or "").strip()

        title_length = _int(row.get("Title 1 Length"))
        title_pixels = _int(row.get("Title 1 Pixel Width"))

        new_title = None

        # Missing title
        if not title and h1:
            new_title = h1[:60]

        # Title too short
        elif title and 0 < title_length < 30:

            if h1:
                new_title = h1[:60]
            else:
                new_title = f"{title} | NMG"

        # Title too long
        elif title and (
            title_length > 60
            or title_pixels > 561
        ):
            new_title = title[:60]

        # Duplicate title
        elif title and title in duplicate_titles:

            if h1 and h1.lower() != title.lower():
                new_title = h1[:60]
            else:
                new_title = f"{title[:50]} | Page"

        if new_title and new_title != title:
            fixes.append(
                {
                    "url": url,
                    "old": title,
                    "new": new_title
                }
            )

    return fixes


def generate_redirect_map(rows):
    redirects = []

    homepage = None

    live_urls = [
        row.get("Address")
        for row in rows
        if str(row.get("Status Code", "")).strip() == "200"
    ]

    if live_urls:
        homepage = live_urls[0]

    if not homepage:
        return redirects

    for row in rows:

        try:
            status = int(float(str(row.get("Status Code", "0"))))
        except Exception:
            continue

        if 400 <= status <= 499:

            redirects.append(
                {
                    "from": row.get("Address"),
                    "to": homepage,
                    "reason": "Fallback redirect suggestion"
                }
            )

    return redirects