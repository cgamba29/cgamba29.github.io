"""Fetch citation metrics from Chiara's Google Scholar profile into data/scholar.json.

If Google Scholar blocks the request, the script leaves the previous numbers
untouched and exits without error, so the website keeps showing the last values.
"""
import json
import sys
from datetime import date
from pathlib import Path

SCHOLAR_ID = "0toJwMkAAAAJ"
OUT = Path(__file__).resolve().parent.parent / "data" / "scholar.json"


def main():
    try:
        from scholarly import scholarly
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author, sections=["basics", "indices", "counts"])
    except Exception as err:  # blocked, timeout, page changed...
        print(f"Could not read Google Scholar this time, keeping old numbers: {err}")
        return 0

    data = {
        "citations": author.get("citedby"),
        "h_index": author.get("hindex"),
        "i10_index": author.get("i10index"),
        "citations_per_year": {str(k): v for k, v in sorted(author.get("cites_per_year", {}).items())},
        "updated": date.today().isoformat(),
        "source": f"https://scholar.google.com/citations?user={SCHOLAR_ID}",
    }
    if data["citations"] is None:
        print("Scholar answered without numbers, keeping old file.")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print("Saved:", data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
