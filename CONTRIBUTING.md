# Conventions

Rules I hold myself to so this repository stays navigable as it grows. Also
what to follow if you open a pull request.

## Language and format

Everything is written in English, in standard Markdown with relative links.

Notes are drafted in Obsidian and copied in by hand — this repository is not a
vault. That means **no wikilinks**: `[[Lame]]` renders as literal text on
GitHub and cannot be fixed from the reader's side. Use
`[Lame](../writeups/hackthebox/lame.md)` instead.

Filenames are kebab-case: `sql-injection.md`, `ret2libc.md`, `lame.md`.

## The three document types

Keeping these distinct is what stops the repository turning into an
undifferentiated pile of markdown:

| Type | Answers | Test before writing |
|---|---|---|
| Note | *Why* does this work | Can you explain the mechanism without the source open? |
| Writeup | How one target fell, end to end | Did you include the dead ends? |
| Cheatsheet | *How*, for things already understood | Have you actually run this? |

Cross-link them. A writeup points at the note for each technique it used; a
note lists the targets where that technique appeared.

## Frontmatter

Notes and writeups carry YAML frontmatter. In writeups it is not decorative —
it generates the index.

Start from [`.templates/writeup.md`](.templates/writeup.md) or
[`.templates/note.md`](.templates/note.md), which carry the full field list.

Categories live in a writeup's `tags`, never in the directory tree: one machine
usually spans web, privesc and a CVE, and filing it under one loses the rest.

## The writeup index

[`writeups/README.md`](writeups/README.md) contains a generated table between
`<!-- BEGIN INDEX -->` and `<!-- END INDEX -->`. Do not edit it by hand:

```bash
python tools/repo/build_index.py           # regenerate
python tools/repo/build_index.py --check   # exit 1 if stale
```

## What never gets committed

- **Books and ebooks.** Copyrighted works, excluded by `.gitignore`. The
  catalogue in [`books/README.md`](books/README.md) is what ships.
- **Flags**, in prose, command output or screenshots.
- **Writeups for active targets.** Retired only — publishing solutions to live
  Hack The Box machines and equivalents violates their terms.
- **Real infrastructure**: client data, credentials, or IPs outside platform
  lab ranges.

## Tools

Python, standard library by default. Each tool carries a docstring stating what
it does, its arguments and an example invocation. A dependency needs to earn
itself, and brings a `requirements.txt` beside the tool when it does.

## Resource lists

Every link added to the README must be checked before it is committed. A
resource list with dead links is worse than no list.
