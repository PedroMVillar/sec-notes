# sec-notes

Notes, writeups and resources from my journey into CTFs and offensive security.

This is a working repository, not a finished course. It grows as I read, break
things and understand why they broke — so expect gaps, and expect earlier
material to get rewritten once I know better.

## Layout

| Directory | What lives there |
|---|---|
| [`books/`](books/README.md) | Annotated bibliography — 37 titles across 11 areas, with reading status |
| [`notes/`](notes/README.md) | Theory in my own words, by domain: web, pwn, rev, crypto, forensics |
| [`writeups/`](writeups/README.md) | Retired boxes, rooms and challenges, tagged by technique |
| [`cheatsheets/`](cheatsheets/README.md) | Syntax and payloads I have already understood and want to recall fast |
| [`tools/`](tools/README.md) | Scripts I wrote for my own workflow |
| [`.templates/`](.templates/) | Starting points for a new note or writeup |

Directories fill in as material is written, so a missing subfolder means "not
written yet", not "lost".

## The three kinds of document

The split between notes, writeups and cheatsheets is what keeps this usable:

- A **note** explains *why* something works. If it does not describe a
  mechanism, it is not a note.
- A **writeup** is one target, end to end, including the dead ends. The failed
  attempts are the part worth rereading.
- A **cheatsheet** recalls *how*, for things already understood. Nothing goes in
  one until I have run it for real.

They cross-link: a writeup points at the note for the technique it used, the
note points back at every target where that technique showed up.

## Conventions

Everything is written in English, in standard Markdown with relative links.
Notes are drafted in Obsidian but the repository is not a vault — no wikilinks,
since GitHub cannot render them.

Filenames are kebab-case. Writeups and notes carry YAML frontmatter; in
writeups it drives the generated index:

```bash
python tools/repo/build_index.py     # regenerate writeups/README.md
```

Books are catalogued in [`books/README.md`](books/README.md) but the PDFs
themselves are never committed — they are copyrighted works and `.gitignore`
excludes every ebook format.

## Scope and ethics

Everything here comes from legal practice: CTF platforms, deliberately
vulnerable labs and my own machines. Nothing in this repository was learned
against a system I was not authorised to touch.

Consequently:

- **Retired targets only.** Active Hack The Box machines and equivalent are
  never published here.
- **No flags**, in prose, output or screenshots.
- **No real infrastructure** — no client data, credentials or IPs outside
  platform lab ranges.

The techniques documented here are offensive by nature. They are published for
learning and defence. Using them against systems you do not own or have written
permission to test is illegal in most jurisdictions, and is on you.

## License

Written content is [CC BY 4.0](LICENSE); code under `tools/` is
[MIT](tools/LICENSE). Attribution is appreciated — corrections more so.
