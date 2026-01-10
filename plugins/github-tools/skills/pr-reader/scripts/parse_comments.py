#!/usr/bin/env python3
"""
Helper script to parse GitHub PR review comments from JSON output.
Extracts file paths, line numbers, severity, and comment body.
"""

import json
import sys
from pathlib import Path

def parse_comments(json_file, reviewer_filter=None):
    """
    Parse PR comments from JSON file.

    Args:
        json_file: Path to JSON file from `gh api .../pulls/{n}/comments`
        reviewer_filter: Optional filter by reviewer username

    Returns:
        List of parsed comment dictionaries
    """
    with open(json_file) as f:
        comments = json.load(f)

    parsed = []
    for i, c in enumerate(comments, 1):
        # Skip if not a code comment (no file path)
        if not c.get('path'):
            continue

        # Filter by reviewer if specified
        if reviewer_filter:
            reviewer = c.get('user', {}).get('login', '')
            if reviewer_filter.lower() not in reviewer.lower():
                continue

        # Extract severity from body
        body = c.get('body', '')
        severity = 'Unknown'
        if '![critical]' in body or '🔴' in body:
            severity = '🔴 CRITICAL'
        elif '![high]' in body or '🟠' in body:
            severity = '🟠 HIGH'
        elif '![medium]' in body or '🟡' in body:
            severity = '🟡 MEDIUM'

        # Clean markdown images from body
        lines = body.split('\n')
        clean_body = '\n'.join([
            l for l in lines
            if not l.strip().startswith('![') and not l.strip().startswith('<img')
        ])

        parsed.append({
            'id': i,
            'file': c['path'],
            'line': c.get('line', 'N/A'),
            'severity': severity,
            'reviewer': c.get('user', {}).get('login', 'unknown'),
            'body': clean_body.strip()
        })

    return parsed

def print_summary(comments):
    """Print formatted summary of comments."""
    print(f"\n{'='*80}")
    print(f"Found {len(comments)} review comments")
    print(f"{'='*80}\n")

    for c in comments:
        print(f"{c['severity']} - Comment #{c['id']}")
        print(f"{'─'*80}")
        print(f"File: {c['file']}")
        print(f"Line: {c['line']}")
        print(f"Reviewer: {c['reviewer']}")
        print(f"\n{c['body'][:500]}")
        if len(c['body']) > 500:
            print("...")
        print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse_comments.py <json_file> [reviewer_filter]")
        print("Example: python3 parse_comments.py /tmp/pr_comments.json gemini")
        sys.exit(1)

    json_file = sys.argv[1]
    reviewer = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(json_file).exists():
        print(f"Error: File not found: {json_file}")
        sys.exit(1)

    comments = parse_comments(json_file, reviewer)
    print_summary(comments)
