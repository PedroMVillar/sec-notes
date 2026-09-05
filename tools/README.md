# Tools

Scripts I wrote for my own workflow. Nothing here is a wrapper around a tool
that already does the job better — these exist because I hit the gap myself.

## Layout

| Directory | Scope |
|---|---|
| `recon/` | Enumeration, asset discovery, output parsing |
| `web/` | Request tampering, fuzzing helpers, payload generation |
| `crypto/` | Cipher solvers, encoding and hash utilities |
| `repo/` | Maintenance of this repository itself |

Directories appear as tools are written.

## Current tools

| Tool | Purpose |
|---|---|
| [`repo/build_index.py`](repo/build_index.py) | Regenerates the writeup index from YAML frontmatter |

## Conventions

Each tool carries a docstring or header stating what it does, its arguments and
an example invocation. Anything non-trivial gets its own `README.md` next to it.

Python is the default. Standard library only unless a dependency genuinely
earns itself, in which case a `requirements.txt` sits beside the tool.

Code in this directory is MIT licensed — see [`LICENSE`](LICENSE). The rest of
the repository is CC BY 4.0.
