#!/usr/bin/env python3
"""
append_client_pain.py — Format and append client pain points and buyer intent leads to client_pain_radar.md.

Reads JSON lead data and appends formatted Markdown sections to client_pain_radar.md.
Handles deduplication, timestamping, intent score sorting, and outreach draft rendering.

Usage:
    python agents/utils/append_client_pain.py --input agents/utils/_temp_client_pain.json --output client_pain_radar.md
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime


def load_json(filepath: str) -> dict:
    """Load and validate the JSON lead results file."""
    if not os.path.exists(filepath):
        print(f"❌ Error: Input file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {filepath}: {e}", file=sys.stderr)
            sys.exit(1)

    required = ["keyword", "leads", "summary", "metadata"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"❌ Error: Missing required fields in JSON: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return data


def generate_lead_hash(lead: dict) -> str:
    """Generate MD5 hash for lead deduplication."""
    key = f"{lead.get('source_url', '')}|{lead.get('lead_title', '')}"
    return hashlib.md5(key.encode()).hexdigest()[:12]


def load_existing_hashes(output_file: str) -> set:
    """Extract existing lead hashes from the master file."""
    hashes = set()
    if not os.path.exists(output_file):
        return hashes

    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            if "<!-- hash:" in line:
                start = line.index("<!-- hash:") + len("<!-- hash:")
                end = line.index(" -->", start)
                hashes.add(line[start:end].strip())

    return hashes


def intent_badge(score: int) -> str:
    """Return badge emoji for intent score."""
    if score >= 9:
        return f"🔥 **{score}/10 (Urgent Buyer)**"
    elif score >= 7:
        return f"🎯 **{score}/10 (High Intent)**"
    elif score >= 5:
        return f"⚡ **{score}/10 (Medium Intent)**"
    else:
        return f"💬 **{score}/10 (Exploratory)**"


def category_emoji(cat: str) -> str:
    """Return category emoji."""
    cat_lower = cat.lower()
    if "freelance" in cat_lower or "gig" in cat_lower:
        return "🛠️"
    elif "automation" in cat_lower or "workflow" in cat_lower:
        return "⚡"
    elif "saas" in cat_lower or "product" in cat_lower or "tool" in cat_lower:
        return "🧰"
    elif "agency" in cat_lower or "retainer" in cat_lower:
        return "🏢"
    elif "consulting" in cat_lower or "strategy" in cat_lower:
        return "💡"
    return "📌"


def format_section(data: dict, existing_hashes: set) -> tuple[str, int, int]:
    """Format JSON leads into Markdown section. Returns (markdown, new_count, dup_count)."""
    keyword = data["keyword"]
    summary = data["summary"]
    metadata = data["metadata"]
    leads = data["leads"]
    timestamp = data.get("timestamp", datetime.now().isoformat())

    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Sort leads by intent_score descending
    sorted_leads = sorted(leads, key=lambda x: x.get("intent_score", 0), reverse=True)

    new_leads = []
    dup_count = 0

    for lead in sorted_leads:
        h = generate_lead_hash(lead)
        if h in existing_hashes:
            dup_count += 1
        else:
            new_leads.append((lead, h))
            existing_hashes.add(h)

    if not new_leads:
        return "", 0, dup_count

    lines = []
    lines.append(f'\n## 📅 {date_str} | Search Query: "{keyword}"\n')
    lines.append(
        f"**Platforms searched**: {metadata.get('platforms_searched', '?')} | "
        f"**Pages visited**: {metadata.get('pages_visited', '?')} | "
        f"**Total leads found**: {len(leads)} | "
        f"**High-Intent Leads (≥7/10)**: {sum(1 for l in leads if l.get('intent_score', 0) >= 7)}\n"
    )

    lines.append("### 📝 Executive Summary\n")
    lines.append(f"{summary}\n")

    # High-Intent Pipeline Summary Table
    lines.append("### 🏆 Client Pain Pipeline\n")
    lines.append("| # | Intent | Category | Client Pain Summary | Platform | Action Link |")
    lines.append("|---|--------|----------|---------------------|----------|-------------|")

    for i, (lead, h) in enumerate(new_leads, 1):
        score = lead.get("intent_score", 0)
        badge = intent_badge(score)
        cat = lead.get("category", "General")
        cat_e = category_emoji(cat)
        title = lead.get("lead_title", "N/A")
        platform = lead.get("platform", "Web")
        url = lead.get("source_url", "#")
        lines.append(f"| {i} | {badge} | {cat_e} {cat} | {title} | {platform} | [Open Post]({url}) | <!-- hash:{h} -->")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed Lead Cards & Outreach Drafts
    lines.append("### 🎯 Detailed Client Pain Cards & AI Outreach Drafts\n")

    for i, (lead, h) in enumerate(new_leads, 1):
        score = lead.get("intent_score", 0)
        badge = intent_badge(score)
        cat = lead.get("category", "General")
        cat_e = category_emoji(cat)
        title = lead.get("lead_title", "N/A")
        platform = lead.get("platform", "Web")
        url = lead.get("source_url", "#")
        author = lead.get("author", "Anonymous")
        urgency = lead.get("urgency", "Flexible")
        budget = lead.get("budget_signal", "Not specified")
        buying_signals = lead.get("buying_signals", [])
        draft = lead.get("outreach_draft", "")
        raw_quote = lead.get("raw_quote", "")

        lines.append(f"#### Lead #{i}: {title}\n")
        lines.append(f"- **Platform**: [{platform}]({url}) | **Author**: `{author}`")
        lines.append(f"- **Intent Score**: {badge} | **Category**: {cat_e} {cat}")
        lines.append(f"- **Urgency**: `{urgency}` | **Budget Indicator**: `{budget}`")

        if buying_signals:
            lines.append("- **Key Client Pain Signals**:")
            for sig in buying_signals:
                lines.append(f"  - *\"{sig}\"*")

        if raw_quote:
            lines.append(f"\n> **Original Post Snippet**: *\"{raw_quote}\"*\n")

        if draft and score >= 7:
            lines.append("##### ✉️ AI Personalized Outreach Draft\n")
            lines.append("```markdown")
            lines.append(draft)
            lines.append("```\n")

        lines.append("---\n")

    return "\n".join(lines), len(new_leads), dup_count


def main():
    parser = argparse.ArgumentParser(description="Append client pain leads to master MD file")
    parser.add_argument("--input", required=True, help="Path to JSON results file")
    parser.add_argument("--output", required=True, help="Path to master MD output file")
    args = parser.parse_args()

    data = load_json(args.input)
    existing_hashes = load_existing_hashes(args.output)
    section, new_count, dup_count = format_section(data, existing_hashes)

    if new_count == 0:
        print(f"⚠️ No new leads to append (skipped {dup_count} duplicates).")
        return

    header = "# 🎯 Client Pain — Buyer Intent & Lead Log\n\n"

    if os.path.exists(args.output):
        with open(args.output, "r", encoding="utf-8") as f:
            existing_content = f.read()

        if existing_content.startswith(header):
            existing_content = existing_content[len(header):]

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(section)
            f.write(existing_content)
    else:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(section)

    print(f"✅ Added {new_count} new client pain leads to {args.output}")
    if dup_count > 0:
        print(f"ℹ️ Skipped {dup_count} duplicate leads")
    print(f"📄 Master log path: {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
