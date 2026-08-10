#!/usr/bin/env python3
"""
check_duplicates.py — Check if a client pain topic has already been researched.

Scans the master MD file to find previous research runs for a given topic.
Returns whether the topic was searched before, when, and how many leads exist.

Usage:
    python agents/utils/check_duplicates.py --topic "web automation" --results-file client_pain_radar.md
"""

import argparse
import os
import re
import sys


def check_topic(topic: str, results_file: str) -> dict:
    """
    Check if a topic has been researched before.

    Returns a dict with:
        - found: bool
        - searches: list of dicts with date, leads_count
        - total_leads: int
    """
    result = {
        "found": False,
        "searches": [],
        "total_leads": 0,
    }

    if not os.path.exists(results_file):
        return result

    with open(results_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern: ## 📅 2026-06-10 12:30 | Search Query: "web automation"
    pattern = re.compile(
        r'## 📅\s+(.+?)\s+\|\s+(?:Search Query|Topic):\s+"([^"]+)"',
        re.MULTILINE,
    )

    matches = list(pattern.finditer(content))

    for match in matches:
        date_str = match.group(1).strip()
        found_topic = match.group(2).strip()

        if found_topic.lower() == topic.lower():
            section_start = match.end()
            next_section = content.find("\n## 📅", section_start)
            if next_section == -1:
                section = content[section_start:]
            else:
                section = content[section_start:next_section]

            hash_count = section.count("<!-- hash:")

            result["found"] = True
            result["searches"].append({
                "date": date_str,
                "actual_entries": hash_count,
            })
            result["total_leads"] += hash_count

    return result


def main():
    parser = argparse.ArgumentParser(description="Check for duplicate topic research")
    parser.add_argument("--topic", required=True, help="The topic to check")
    parser.add_argument("--results-file", default="client_pain_radar.md", help="Path to the master MD results file")
    args = parser.parse_args()

    result = check_topic(args.topic, args.results_file)

    if not os.path.exists(args.results_file):
        print(f"📄 Results file not found: {args.results_file}")
        print("   This will be created on the first search run.")
        return

    if not result["found"]:
        print(f'✅ Topic "{args.topic}" has NOT been researched before. Proceed with search.')
    else:
        print(f'⚠️ Topic "{args.topic}" has been researched before:')
        for search in result["searches"]:
            print(f"   📅 {search['date']} — {search['actual_entries']} client pain leads recorded")
        print(f"   📊 Total existing leads: {result['total_leads']}")
        print(f"\n   Running again will ADD new findings and skip duplicates (by URL + text hash).")

    if "--json" in sys.argv:
        import json
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
