#!/usr/bin/env python3
"""Regenerate the writeup index in writeups/README.md from YAML frontmatter.

Walks writeups/ for markdown files carrying a frontmatter block, sorts them
newest first, and rewrites the table between the BEGIN INDEX and END INDEX
markers. Standard library only -- the frontmatter this repo uses is flat
key/value pairs plus inline lists, which does not justify a YAML dependency.

Usage:
    python tools/repo/build_index.py            # rewrite the index
    python tools/repo/build_index.py --check    # exit 1 if it is stale
"""

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WRITEUPS = REPO / "writeups"
INDEX = WRITEUPS / "README.md"

BEGIN = "<!-- BEGIN INDEX -->"
END = "<!-- END INDEX -->"

PLATFORMS = {
    "hackthebox": "Hack The Box",
    "tryhackme": "TryHackMe",
    "picoctf": "picoCTF",
    "competitions": "Competition",
}


def parse_frontmatter(text):
    """Return the frontmatter block of a markdown file as a dict, or None.

    Handles `key: value` and `key: [a, b, c]`. Values keep their original case;
    inline comments after a value are stripped.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None

    data = {}
    for line in lines[1:end]:
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip().strip("'\"") for v in value[1:-1].split(",")]
            data[key.strip()] = [v for v in items if v]
        else:
            # drop trailing "# comment" from template-derived values
            if "#" in value:
                value = value.split("#", 1)[0].strip()
            data[key.strip()] = value.strip("'\"")
    return data


def collect():
    """Gather every writeup with usable frontmatter, newest first."""
    entries = []
    if not WRITEUPS.exists():
        return entries

    for path in sorted(WRITEUPS.rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta:
            print(f"skipped (no frontmatter): {path.relative_to(REPO)}", file=sys.stderr)
            continue
        meta["_path"] = path.relative_to(WRITEUPS).as_posix()
        # fall back to the containing directory when platform is unset
        meta.setdefault("platform", path.parent.name)
        entries.append(meta)

    entries.sort(key=lambda e: (e.get("date", ""), e.get("target", "")), reverse=True)
    return entries


def render(entries):
    if not entries:
        return "_No writeups yet._"

    rows = [
        "| Target | Platform | Difficulty | OS | Tags | Date |",
        "|---|---|---|---|---|---|",
    ]
    for e in entries:
        platform = PLATFORMS.get(e.get("platform", ""), e.get("platform", "-"))
        tags = ", ".join(f"`{t}`" for t in e.get("tags", [])) or "-"
        rows.append(
            "| [{target}]({path}) | {platform} | {difficulty} | {os} | {tags} | {date} |".format(
                target=e.get("target", e["_path"]),
                path=e["_path"],
                platform=platform,
                difficulty=e.get("difficulty", "-"),
                os=e.get("os", "-"),
                tags=tags,
                date=e.get("date", "-"),
            )
        )

    count = len(entries)
    rows.append("")
    rows.append(f"_{count} writeup{'s' if count != 1 else ''}._")
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the index is out of date instead of rewriting it",
    )
    args = parser.parse_args()

    current = INDEX.read_text(encoding="utf-8")
    if BEGIN not in current or END not in current:
        sys.exit(f"error: markers {BEGIN} / {END} not found in {INDEX}")

    head, _, rest = current.partition(BEGIN)
    _, _, tail = rest.partition(END)
    updated = f"{head}{BEGIN}\n{render(collect())}\n{END}{tail}"

    if updated == current:
        print("index is up to date")
        return

    if args.check:
        sys.exit("index is out of date; run: python tools/repo/build_index.py")

    INDEX.write_text(updated, encoding="utf-8")
    print(f"index updated: {INDEX.relative_to(REPO)}")


if __name__ == "__main__":
    main()
