---
name: github-pr-reader
description: Extract and organize GitHub PR review comments into prioritized action plans. Use when user asks to "read PR comments", "extract review feedback", "organize PR review", "parse PR #X", or mentions fixing code review comments from a specific pull request. Works with reviews from Gemini Code Assist, human reviewers, or any GitHub review comments.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - TodoWrite
---

# GitHub PR Reader

Extract and organize GitHub PR review comments into prioritized action plans for systematic fixes.

## When to Activate

Activate this skill when the user says:
- "read PR #X comments"
- "extract review feedback from PR #X"
- "organize review comments"
- "help me fix PR review feedback"
- "what did [reviewer] say in PR #X"
- "parse PR #X review"
- Provides any GitHub PR URL format:
  - `https://github.com/{owner}/{repo}/pull/{number}` - Full PR URL
  - `https://github.com/{owner}/{repo}/pull/{number}#pullrequestreview-{id}` - PR URL with review ID
  - `#pullrequestreview-{id}` or just `{id}` - Review ID only (with PR context)

## Workflow

### Step 0: Parse URL (if provided)

When user provides a URL, parse it to extract owner, repo, PR number, and optionally review ID:

**Supported URL formats:**
- `https://github.com/{owner}/{repo}/pull/{number}` - Full PR URL
- `https://github.com/{owner}/{repo}/pull/{number}#pullrequestreview-{id}` - PR URL with review ID
- `#pullrequestreview-{id}` or just `{id}` - Review ID only (requires PR context)

Extract using regex or string parsing:
```bash
# Example: https://github.com/quanhua92/buildscale-ai/pull/1#pullrequestreview-3646706772
# Owner: quanhoa92
# Repo: buildscale-ai
# PR: 1
# Review ID: 3646706772
```

### Step 1: Extract Comments

Use the gh CLI to fetch PR review comments. If a specific review ID is provided, fetch only that review's comments:

```bash
# Option A: Get ALL review comments from a PR
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments > /tmp/pr_comments.json

# Option B: Get a SPECIFIC review's comments (when review ID is provided)
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews/{review_id}/comments > /tmp/pr_comments.json

# Option C: Get review summary first
gh pr view {pr_number} --json title,body,reviews

# Option D: Get review details
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews/{review_id}
```

### Step 2: Parse Comments

Parse the JSON to extract:
- File paths and line numbers
- Severity indicators (e.g., `![critical]`, `![high]`, `![medium]`)
- Comment body/description
- Reviewer name/handle

Use the Python helper script to format the output:

```bash
python3 {baseDir}/scripts/parse_comments.py /tmp/pr_comments.json
```

### Step 3: Prioritize by Difficulty

Sort issues into tiers based on complexity:

**Quick Wins (5-15 minutes)**
- Remove redundant exports/imports
- Fix type assertions
- Clean up unused code
- Simple search/replace fixes

**Medium Complexity (30-45 minutes)**
- Remove code duplication
- Add memoization (useMemo, useCallback)
- Update error handling
- Refactor helper functions

**Complex (1+ hours)**
- Multi-file changes
- Update validation logic
- Improve form handling
- State management changes

**Hardest (1-2+ hours)**
- Backend + frontend changes
- Architecture refactoring
- Database migrations
- Breaking API changes

### Step 4: Create Action Plan

Generate a structured plan with:
- Checkbox tracking for progress
- Estimated time per task
- Risk level (Low/Medium/High)
- Specific file locations with line numbers
- Clear "Why this order" rationale

### Step 5: Execute and Track

Work through items easiest-to-hardest:
1. Build momentum with quick wins
2. Progress to medium complexity
3. Tackle complex problems
4. Save hardest for last

Use TodoWrite to track progress:
```
- [ ] Fix #6: Redundant exports (5 min)
- [x] Fix #5: Type assertions (10 min) - DONE
```

## Example Output Format

```markdown
## PR #1 Review Analysis - 6 issues found

Reviewer: gemini-code-assist[bot]

### Phase 1: Quick Wins (0/2) - 15 minutes
- [ ] Fix #6: Remove redundant exports (5 min)
  File: frontend/sdk/src/index.ts:17
  Severity: 🟡 Medium
  Action: Delete hooks/useAuth.ts, update exports

- [ ] Fix #5: Fix unsafe type assertion (10 min)
  File: AuthRegister.tsx:21
  Severity: 🟡 Medium
  Action: Build typed object explicitly

### Phase 2: Medium (0/2) - 45 minutes
- [ ] Fix #3: Memoize instances (15 min)
  File: AuthContext.tsx:40
  Severity: 🟠 High
  Action: Wrap storage/apiClient in useMemo

- [ ] Fix #4: Remove code duplication (30 min)
  File: api/client.ts:80
  Severity: 🟡 Medium
  Action: Extract fetchWithAuth helper

### Phase 3: Complex (0/1) - 45 minutes
- [ ] Fix #2: Complete form validation (45 min)
  File: AuthForm.tsx:60
  Severity: 🟠 High
  Action: Update AuthInput to use useFormErrors

### Phase 4: Hard (0/1) - 1-2 hours
- [ ] Fix #1: Add session persistence (1-2 hrs)
  Files: AuthContext.tsx:34 + backend
  Severity: 🔴 Critical
  Action: Add useEffect + GET /auth/me endpoint

**Strategy:** Quick wins first → Build confidence → Tackle harder problems
```

## Tools Required

- `gh` CLI - Must be authenticated
- Python/JSON parsing - For extracting structured data
- TodoWrite - For progress tracking
- Edit/Write tools - For implementing fixes

## Commands Used

```bash
# Extract ALL comments from a PR
gh api repos/{owner}/{repo}/pulls/{number}/comments > /tmp/comments.json

# Extract comments from a SPECIFIC review
gh api repos/{owner}/{repo}/pulls/{number}/reviews/{review_id}/comments > /tmp/comments.json

# View PR summary
gh pr view {number}

# Get specific review details
gh api repos/{owner}/{repo}/pulls/{number}/reviews/{review_id}

# Check commit history
git log --oneline -10
```

## Limitations

- Only works with accessible PRs (requires proper gh authentication)
- Requires reviewer comments to have file paths for precise locations
- Cannot process review comments without code context (general PR comments only)
- Severity badges are optional - may not exist in all reviews
- Does NOT automatically push commits (user must confirm)

## Best Practices

1. **Sort by difficulty** - Quick wins build momentum
2. **Test frequently** - Build after each phase
3. **Commit often** - One commit per fix with clear messages
4. **Update progress** - Check off items as you complete them
5. **Stay focused** - Complete one phase before moving to next
6. **Communicate** - Tell user what you're doing and why

## Sample Interaction

**Example 1: User provides PR URL with review ID**

**User:** "We have the comment id https://github.com/quanhua92/buildscale-ai/pull/1#pullrequestreview-3646706772"

**Claude:**
1. Parses URL: owner=`quanhua92`, repo=`buildscale-ai`, PR=`1`, review_id=`3646706772`
2. Fetches specific review: `gh api repos/quanhua92/buildscale-ai/pulls/1/reviews/3646706772`
3. Fetches review comments: `gh api repos/quanhua92/buildscale-ai/pulls/1/reviews/3646706772/comments`
4. Parses comments (e.g., 5 issues with severity levels)
5. Creates prioritized TODO list by difficulty
6. Starts with easiest fix (quick wins)
7. Updates progress checkboxes
8. Commits each fix separately
9. Reports completion: "5/5 issues fixed (100%)"

**Example 2: User provides PR URL only**

**User:** "Read PR #1 from quanhoa92/buildscale-ai"

**Claude:**
1. Extracts comments: `gh api repos/quanhua92/buildscale-ai/pulls/1/comments`
2. Parses 6 issues with file locations
3. Creates prioritized TODO list
4. Starts with easiest fix (5-minute cleanup)
5. Updates progress checkboxes
6. Commits each fix separately
7. Reports completion: "6/6 issues fixed (100%)"

## After Completion

- All items checked off
- All commits made (but NOT pushed without user confirmation)
- Summary provided
- Ready for user to review and push
