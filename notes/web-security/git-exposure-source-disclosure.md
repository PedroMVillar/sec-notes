---
topic: web-security
tags: [misconfiguration, git-exposure, source-disclosure, information-disclosure, secrets, recon]
sources: [yaworski-real-world-bug-hunting, mcdonald-grokking-web-application-security, ghostlulz-bug-bounty-playbook]
updated: 2026-09-16
---

# Exposed .git & Source Code Disclosure

A deploy misconfiguration: the site's `.git/` directory is served to the web, so
the whole source **and its history** are downloadable. "We cleaned the secrets
before publishing" doesn't help — git history keeps every version, including the
files and commits where the secret lived. *dot git never forgets.*

## Detect it

Even with directory listing **off** (`/.git/` → 404), the internal files are
still served:

```bash
curl -s https://target/.git/HEAD        # "ref: refs/heads/master"  -> exposed
curl -s https://target/.git/config      # remote URL, sometimes creds
curl -s https://target/.git/logs/HEAD   # commit hashes + messages (the timeline)
```

Any `200` on these means the repo is dumpable. `logs/HEAD` is gold: it lists
every commit hash and message (e.g. "initial import", "remove secrets") — the map
of what to reconstruct.

## Dump it

- **Directory listing ON** → `wget -r https://target/.git/` (or any recursive
  mirror), then `git checkout .`
- **Listing OFF** → **git-dumper** (`git-dumper https://target/.git/ out/`): it
  enumerates the known git paths (HEAD, refs, index, objects by hash) without
  needing a listing. The standard tool.
- **By hand** (no tools): the object of each hash is at
  `/.git/objects/<first2>/<rest38>`, zlib-compressed. Fetch, inflate, and walk
  `commit → tree → blob`; get the commit hashes from `logs/HEAD` / `refs`.

Once dumped, read *everything*, including deleted/edited files:

```bash
git log --oneline --all
git log -p --all          # full diffs -> secrets removed in later commits
git show <commit>:<path>  # a file as it was in any commit
```

## What to look for

- **Config files not linked from the site** (`config.py`, `settings.py`,
  `.env`, `wp-config.php`) — the web only serves `index.html`, but the repo has
  everything tracked.
- Hardcoded **credentials, API keys, DB DSNs** (`postgres://user:pass@host/db`),
  tokens, private keys.
- Secrets **removed in a later commit** but alive in history (`git log -p`).

## Related misconfiguration exposures

Same idea, other artifacts — always worth a quick check:

- `.env`, `.svn/`, `.hg/`, `.bzr/` (other VCS metadata)
- Backup / editor leftovers: `index.php.bak`, `config.py~`, `*.old`, `*.save`,
  `.swp` (vim swap)
- **Directory listing** enabled (browse the tree directly)
- `.DS_Store` (macOS — leaks filenames to enumerate)
- Source shown instead of executed (`.phps`, wrong handler)

## Fixes

- **Never deploy the `.git/` directory** — deploy build artifacts, not the repo;
  or block dotfiles at the web server (`location ~ /\.git { deny all; }`).
- **Secrets in environment variables**, never committed to code.
- **Rotate anything ever committed** — removing it from the latest commit is not
  enough; assume history is public.

## Recognising this in a CTF

Tags like `#misconfiguration` / `#git-exposure`, a "legacy/old portal", or
"we cleaned the code before publishing". First move: `curl /.git/HEAD`. If it's
`200`, dump and read the history.

## Related

- [Secrets in client-side code](client-side-secrets.md) — the other
  "secret that shouldn't have shipped" bug (this one is server-side source).

## Seen in

- Corp Portal — Legacy (course, Class 3) — `.git/` exposed (listing off, files
  reachable); dumped the objects by hash and found `FaMAF{...}` and a DB DSN in a
  `config.py` never linked from the site. The "cleanup" commit only added a
  footer — nothing was actually removed. *(Write-up kept local until release.)*

## Sources

Relevant reading in the [bibliography](../../books/README.md) (this note was
written from established technique; NotebookLM grounding pending re-auth):

- **Yaworski — *Real-World Bug Hunting*** — information disclosure and exposed
  source/metadata reports.
- **McDonald — *Grokking Web Application Security*** — security misconfiguration
  and keeping secrets out of code.
- **Ghostlulz — *Bug Bounty Playbook*** — recon for exposed `.git`/backup files.
