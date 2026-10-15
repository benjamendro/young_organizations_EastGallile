#!/usr/bin/env python3
"""מטמיע את data/organizations.json בתוך index.html.

ה-HTML נשאר קובץ עצמאי (עובד גם בפתיחה ישירה מהדיסק, בלי שרת),
ו-data/organizations.json נשאר מקור האמת היחיד לנתונים.

שימוש:
    python3 scripts/build.py          # מעדכן את index.html
    python3 scripts/build.py --check  # בודק ש-index.html מסונכרן עם ה-JSON
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "organizations.json"
HTML = ROOT / "index.html"

BLOCK = re.compile(r"(const ORGS = ).*?(;\s*/\* DATA:END \*/)", re.S)


def read(path: Path) -> str:
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def render() -> str:
    orgs = json.loads(DATA.read_text(encoding="utf-8"))
    # שומרים על סוף השורה המקורי של הקובץ (CRLF) כדי שה-diff יישאר נקי
    payload = json.dumps(orgs, ensure_ascii=False, indent=2).replace("\n", "\r\n")
    html = read(HTML)
    if not BLOCK.search(html):
        sys.exit("לא נמצא בלוק DATA:START/DATA:END ב-index.html")
    return BLOCK.sub(lambda m: m.group(1) + payload + m.group(2), html, count=1)


def main() -> None:
    new_html = render()
    if "--check" in sys.argv:
        if new_html != read(HTML):
            sys.exit("index.html אינו מסונכרן עם data/organizations.json — הריצו: python3 scripts/build.py")
        print("index.html מסונכרן")
        return
    with open(HTML, "w", encoding="utf-8", newline="") as f:
        f.write(new_html)
    print("index.html עודכן")


if __name__ == "__main__":
    main()
