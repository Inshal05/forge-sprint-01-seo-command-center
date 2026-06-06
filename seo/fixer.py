from __future__ import annotations


def generate_title_fixes(rows):
    fixes = []

    for row in rows:
        title = (row.get("Title 1", "") or "").strip()

        if title:
            continue

        url = row.get("Address", "")
        h1 = (row.get("H1-1", "") or "").strip()

        if not h1:
            continue

        fixes.append(
            {
                "url": url,
                "old": "",
                "new": h1[:60]
            }
        )

    return fixes


def generate_redirect_map(rows):
    redirects = []

    homepage = None

    for row in rows:
        if str(row.get("Status Code", "")).strip() == "200":
            homepage = row.get("Address")
            break

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
