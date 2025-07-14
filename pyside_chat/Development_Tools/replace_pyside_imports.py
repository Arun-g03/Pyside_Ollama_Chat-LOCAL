#!/usr/bin/env python3
"""
Replace PySide6 Imports with Shared Import

This script scans the codebase and replaces all individual PySide6 imports
with a single import from the shared PySide imports file.

Usage:
    python replace_pyside_imports.py --codebase pyside_chat --dry-run
    python replace_pyside_imports.py --codebase pyside_chat --apply
"""

import os
import re
from pathlib import Path
import argparse

SHARED_IMPORT_LINE = 'from pyside_chat.core.shared_imports.pyside_imports import *'

def find_python_files(codebase_path):
    """Find all Python files in the codebase, excluding shared import files."""
    codebase = Path(codebase_path)
    for file in codebase.rglob('*.py'):
        if 'shared_imports' in str(file) or file.name == 'replace_pyside_imports.py':
            continue
        yield file

# Regex to match PySide6 import lines
PYSIDE_IMPORT_RE = re.compile(r'^(\s*)(from|import)\s+PySide6[.\w\s,()*]+$', re.MULTILINE)

# Regex to match the shared import line
SHARED_IMPORT_RE = re.compile(r'^\s*from\s+pyside_chat\.core\.shared_imports\.pyside_imports\s+import\s+\*', re.MULTILINE)

def process_file(file_path, dry_run=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all PySide6 import lines
    pyside_imports = list(PYSIDE_IMPORT_RE.finditer(content))
    if not pyside_imports:
        return False  # No change needed

    # Remove all PySide6 import lines
    new_content = PYSIDE_IMPORT_RE.sub('', content)

    # Insert the shared import line if not already present
    if not SHARED_IMPORT_RE.search(new_content):
        # Find the first non-comment, non-empty line
        lines = new_content.splitlines()
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'):
                insert_idx = i
                break
        lines.insert(insert_idx, SHARED_IMPORT_LINE)
        new_content = '\n'.join(lines)

    if dry_run:
        print(f"[DRY RUN] Would update: {file_path}")
        for match in pyside_imports:
            print(f"  Remove: {match.group(0).strip()}")
        print(f"  Add: {SHARED_IMPORT_LINE}")
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[APPLIED] Updated: {file_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Replace PySide6 imports with shared import.")
    parser.add_argument('--codebase', default='pyside_chat', help='Path to codebase (default: pyside_chat)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed (default)')
    parser.add_argument('--apply', action='store_true', help='Actually apply the changes')
    args = parser.parse_args()

    dry_run = not args.apply
    changed = 0
    for file_path in find_python_files(args.codebase):
        if process_file(file_path, dry_run=dry_run):
            changed += 1
    print(f"\n{'[DRY RUN]' if dry_run else '[APPLIED]'} {changed} files would be updated.")
    if dry_run:
        print("Run with --apply to make changes.")

if __name__ == '__main__':
    main() 