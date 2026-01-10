# Claude Skills Marketplace

Collection of custom plugins and skills for Claude Code.

## Plugins

### [github-tools](./plugins/github-tools/)

Tools for working with GitHub PRs, issues, and code reviews.

**Skills:**
- **pr-reader** - Extract and organize GitHub PR review comments into prioritized action plans

**Usage:** "Read PR #1 comments" → Automatically extracts, organizes, and fixes review feedback systematically.

## Installation

### Quick Install

Add the marketplace and install plugins:

```bash
/plugin marketplace add quanhua92/claude-skills
```

```bash
/plugin install github-tools@quanhua92-claude-skills
```

Then restart Claude Code to load the skills.

### Manual Install

1. Clone this repository to your local machine
2. Add to your Claude Code plugins configuration
3. Restart Claude Code

## Structure

```
claude-skills/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── plugins/
│   └── github-tools/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── pr-reader/
│       │       └── SKILL.md
│       ├── parse_comments.py
│       └── README.md
└── README.md
```

## License

MIT
