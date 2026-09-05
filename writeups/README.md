# Writeups

Boxes, rooms and challenges I have solved, written up so the reasoning survives
longer than the flag did.

## Ground rules

These are not negotiable, and they are why this directory can be public:

- **Retired targets only.** Hack The Box and most platforms forbid publishing
  solutions to active machines. Nothing here goes up until the target retires.
- **No flags.** Not in the prose, not in the screenshots, not in the command
  output. Publishing them spoils the exercise for everyone else and breaks the
  terms of service of every platform involved.
- **No real infrastructure.** No credentials, no client data, no IPs outside
  the platform's own lab ranges.

## Layout

| Directory | Source |
|---|---|
| `hackthebox/` | Hack The Box machines and challenges |
| `tryhackme/` | TryHackMe rooms |
| `picoctf/` | picoCTF challenges |
| `competitions/` | Timed CTF events |

Directories appear as writeups are written.

## Conventions

Start from [`.templates/writeup.md`](../.templates/writeup.md). Filenames are
kebab-case after the target: `hackthebox/lame.md`.

Categories live in the `tags` field of the frontmatter, not in the directory
tree — a single machine usually crosses web, privesc and a CVE or two, and
filing it under one of them loses the other two.

## Index

Generated from frontmatter by
[`tools/repo/build_index.py`](../tools/repo/build_index.py). Do not edit the
table by hand; run the script instead.

```bash
python tools/repo/build_index.py
```

<!-- BEGIN INDEX -->
_No writeups yet._
<!-- END INDEX -->
