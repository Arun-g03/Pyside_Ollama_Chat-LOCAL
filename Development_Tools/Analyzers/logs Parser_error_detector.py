import os
import re
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("Logs")  # Change this to your log folder
OUTPUT_FILE = Path("Development_Tools/Reports/log_report.md")

# Regex patterns
LOG_LEVELS = ["ERROR", "WARNING", "CRITICAL", "EXCEPTION", "TRACEBACK"]
level_pattern = re.compile(r"\b(" + "|".join(LOG_LEVELS) + r")\b", re.IGNORECASE)
timestamp_pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

def parse_log_file(filepath: Path):
    entries = []
    current_traceback = []
    in_traceback = False

    with filepath.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip()

            if "Traceback (most recent call last):" in line:
                in_traceback = True
                current_traceback = [line]
                continue

            if in_traceback:
                current_traceback.append(line)
                if line.strip() == "" or re.match(r"^\s*[\w.]+:", line):  # End of traceback
                    entries.append({
                        "level": "TRACEBACK",
                        "timestamp": extract_timestamp(current_traceback[0]),
                        "message": "\n".join(current_traceback)
                    })
                    in_traceback = False
                    current_traceback = []
                continue

            match = level_pattern.search(line)
            if match:
                level = match.group(1).upper()
                entries.append({
                    "level": level,
                    "timestamp": extract_timestamp(line),
                    "message": line.strip()
                })

    return entries

def extract_timestamp(line: str):
    match = timestamp_pattern.search(line)
    return match.group(0) if match else None

def generate_markdown_report(all_logs: dict):
    lines = ["# 📋 Log Report\n", f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n"]

    # Separate files with and without issues
    logs_with_issues = {k: v for k, v in all_logs.items() if v}
    logs_without_issues = {k: v for k, v in all_logs.items() if not v}

    # Logs with issues (top of report)
    for filename, entries in sorted(logs_with_issues.items()):
        lines.append(f"\n## 📁 `{filename}`")
        entries_by_level = {}
        for entry in entries:
            entries_by_level.setdefault(entry["level"], []).append(entry)

        for level in sorted(entries_by_level.keys()):
            lines.append(f"\n### 🔸 {level}\n")
            for i, entry in enumerate(entries_by_level[level], 1):
                timestamp = f"`[{entry['timestamp']}]` " if entry["timestamp"] else ""
                message = f"```\n{entry['message']}\n```" if "\n" in entry["message"] else f"> {entry['message']}"
                lines.append(f"**{i}.** {timestamp}\n{message}\n")

    # Logs without issues (bottom of report)
    if logs_without_issues:
        lines.append("\n---\n\n# ✅ Log Files with No Issues")
        for filename in sorted(logs_without_issues.keys()):
            lines.append(f"\n### 📁 `{filename}`\n_No issues found._")

    return "\n".join(lines)

def main():
    all_logs = {}
    for path in LOG_DIR.rglob("*"):
        if path.suffix.lower() in [".log", ".txt"] and path.is_file():
            all_logs[path.name] = parse_log_file(path)

    report = generate_markdown_report(all_logs)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"✅ Log report written to: {OUTPUT_FILE.absolute()}")

if __name__ == "__main__":
    main()
