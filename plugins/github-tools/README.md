# GitHub Tools Plugin

Tools for working with GitHub PRs, issues, and code reviews.

## Skills

### pr-reader

Extract and organize GitHub PR review comments into prioritized action plans for systematic fixes.

**What It Does:**
1. **Extracts** PR review comments using `gh` CLI
2. **Parses** comments to identify file locations, severity, and issues
3. **Organizes** feedback by difficulty (quick wins → hard fixes)
4. **Tracks** progress with checkboxes
5. **Executes** fixes systematically from easiest to hardest

**When to Use:**
- "Read PR #X comments"
- "Extract review feedback"
- "Parse PR #X review"
- "Help me fix PR feedback"
- "What did the reviewer say in PR #X?"

**Usage Example:**
```
You: Read PR #1 review from gemini

Claude: [Extracts comments via gh CLI, organizes into prioritized list]
```

## Helper Script

The `parse_comments.py` script is bundled with the pr-reader skill and can also be used standalone from the plugin root:

```bash
# Parse all comments
python3 parse_comments.py /tmp/pr_comments.json

# Filter by reviewer
python3 parse_comments.py /tmp/pr_comments.json gemini
```

## Features

- ✅ Works with any reviewer (human, bot, or tool)
- ✅ Extracts file paths and line numbers
- ✅ Identifies severity levels (critical/high/medium)
- ✅ Sorts by difficulty for momentum building
- ✅ Tracks progress with checkboxes
- ✅ Commits frequently without pushing
- ✅ Provides clear rationale for task order

## Requirements

- `gh` CLI installed and authenticated
- Python 3.6+ (for helper script)
- Git repository with PR access

## License

MIT
