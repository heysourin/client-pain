# 🎯 Client Pain

> AI-powered agent that discovers client pain points and active buyer intent across 11+ platforms, scores intent 1–10, and generates personalized AI outreach response drafts.

---

## 🎯 What It Does

**Client Pain** searches the web for posts where clients express pain points, immediate help requests, tool searches, or service hiring intent:

1. 🔍 **Searches 11+ platforms** — Reddit, Twitter/X, LinkedIn, Quora, Facebook Groups, IndieHackers, Stack Overflow, GitHub Discussions, Discord, Slack communities, and Telegram groups.
2. 💬 **Reads post content & comments** — Extracts exact client pain points, buyer needs, urgency indicators, and budget signals.
3. 📊 **Scores Buyer Intent (1–10)**:
   - 🔥 **9–10 (Urgent Buyer)** — Explicit budget/deadline + immediate hiring need ("I need someone who can...").
   - 🎯 **7–8 (High Intent)** — Searching for specific software or service providers ("Looking for a tool that...").
   - ⚡ **5–6 (Medium Intent)** — Asking how to automate a process or seeking recommendations ("How do I automate...").
   - 💬 **1–4 (Low Intent)** — Exploratory discussion.
4. 🏷️ **Categorizes Client Pain Leads** — Freelance & Gig Work, SaaS & Tool Need, Automation & Workflow, Agency & Retainer, Consulting & Strategy.
5. ✉️ **Generates AI Outreach Drafts** — Crafts personalized, non-spammy outreach response drafts for every high-intent lead ($\ge 7/10$).
6. 📋 **Outputs Priority Log Report** — Appends structured results to `client_pain_radar.md`.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (for standard library utility scripts — zero third-party dependencies needed)
- **An LLM-powered coding assistant** with web search and browser capabilities (Antigravity, Claude Code, Cursor, etc.)

### Installation Options

**Option 1: CLI via npx (GitHub)**
```bash
npx github:heysourin/client-pain add heysourin/client-pain
```

**Option 2: Manual Clone**
```bash
git clone https://github.com/heysourin/client-pain.git
# Copy the agents/ folder into your workspace .agents/skills/ directory
```

---

## 💡 Usage

Trigger the agent in chat with your target skill, service niche, or keyword:

```text
@client-pain find client leads for "web automation script"
@client-pain search for buyers asking "looking for a tool that automates"
@client-pain discover client pain about "python scraping developer"
```

### Output

After each run, you get:

| File | Description |
|------|-------------|
| `client_pain_radar.md` | Master log containing executive summaries, high-intent lead pipeline tables, intent badges, budget/urgency signals, and ready-to-copy AI outreach response drafts. |

---

## 📂 File Structure

```
<root directory>/
├── agents/
│   ├── client-pain.md              # Core AI Agent Skill file
│   └── utils/
│       ├── append_client_pain.py   # Format & append leads to client_pain_radar.md
│       └── check_duplicates.py     # Deduplication & topic check script
├── client_pain_radar.md            # Master buyer lead log & outreach drafts (auto-created)
├── bin/
│   └── cli.js                      # Skills installer CLI
├── package.json                    # Package manifest
└── README.md                       # Documentation
```

---

## 🐍 Python Utilities

All utility scripts use **Python stdlib only** — zero pip installs required.

### `append_client_pain.py`

Formats JSON lead results into Markdown cards with AI outreach drafts and appends to `client_pain_radar.md`:

```bash
python3 agents/utils/append_client_pain.py --input agents/utils/_temp_client_pain.json --output client_pain_radar.md
```

Features:
- **MD5 Deduplication** — Prevents duplicate lead entries by URL and title hash.
- **Intent Score Sorting** — Sorts leads by buyer intent score (10 to 1).
- **Outreach Draft Generator** — Embeds ready-to-copy personalized AI response drafts for leads $\ge 7/10$.

---

## ⚖️ License

MIT — Free to use, modify, and distribute.
# client-pain
