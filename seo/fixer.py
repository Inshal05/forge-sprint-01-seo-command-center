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

        content_type = (
            row.get("Content Type", "")
            or ""
        ).lower()

        if "text/html" not in content_type:
            continue

        title = (row.get("Title 1", "") or "").strip()

        if title:
            title_groups[title].append(row)

    duplicate_titles = {
        title
        for title, pages in title_groups.items()
        if len(pages) > 1
    }

    for row in rows:

        content_type = (
            row.get("Content Type", "")
            or ""
        ).lower()

        if "text/html" not in content_type:
            continue

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
def generate_meta_fixes(rows):
    fixes = []

    meta_groups = defaultdict(list)

    for row in rows:

        content_type = (
            row.get("Content Type", "")
            or ""
        ).lower()

        if "text/html" not in content_type:
            continue

        meta = (row.get("Meta Description 1", "") or "").strip()

        if meta:
            meta_groups[meta].append(row)

    duplicate_meta = {
        meta
        for meta, pages in meta_groups.items()
        if len(pages) > 1
    }

    for row in rows:

        content_type = (
            row.get("Content Type", "")
            or ""
        ).lower()

        if "text/html" not in content_type:
            continue

        url = row.get("Address", "")
        h1 = (row.get("H1-1", "") or "").strip()

        meta = (
            row.get("Meta Description 1", "")
            or ""
        ).strip()

        meta_length = _int(
            row.get("Meta Description 1 Length")
        )

        new_meta = None

        # Missing meta description
        if not meta:

            if h1:
                new_meta = (
                    f"{h1} - Learn more about our services and solutions."
                )
            else:
                new_meta = (
                    "Learn more about our services and solutions."
                )

        # Meta description too long
        elif meta and meta_length > 155:

            new_meta = meta[:155]

        # Duplicate meta description
        elif meta and meta in duplicate_meta:

            if h1:
                new_meta = (
                    f"{h1} - Learn more about our services and solutions."
                )

        if new_meta:

            new_meta = new_meta[:155]

            if new_meta != meta:
                fixes.append(
                    {
                        "url": url,
                        "old": meta,
                        "new": new_meta
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