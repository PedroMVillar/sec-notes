# Notes

Theory distilled into my own words: what I take from the books in
[`books/`](../books/README.md) and from the boxes in
[`writeups/`](../writeups/README.md), rewritten until it holds without the
source open.

A note earns its place here only if it explains *why* something works. Command
sequences without a mechanism behind them belong in
[`cheatsheets/`](../cheatsheets/README.md).

## Layout

One directory per domain. The slugs match `books/`, minus the numeric prefix —
`books/04-web-security` pairs with `notes/web-security`.

| Directory | Scope |
|---|---|
| `foundations/` | Networking, operating systems, the shell, how the pieces fit |
| `cryptography/` | Classical ciphers, modern primitives, common CTF crypto attacks |
| `web-security/` | Injection, auth, SSRF, deserialisation, API abuse |
| `binary-exploitation/` | Memory corruption, ROP, heap, modern mitigations |
| `reverse-engineering/` | Static and dynamic analysis, disassemblers, obfuscation |
| `malware-analysis/` | Triage, sandboxing, unpacking, behavioural analysis |
| `os-internals/` | Windows, Linux and Android security architecture |
| `network-and-pentesting/` | Recon, pivoting, Active Directory, methodology |
| `forensics/` | Disk, memory and network forensics, steganography |

Directories appear as notes are written, not before.

## Conventions

Start from [`.templates/note.md`](../.templates/note.md). Filenames are
kebab-case: `sql-injection.md`, `ret2libc.md`.

Every note cites its sources with book and chapter, and links to the writeups
where the technique actually showed up. A note that connects to nothing is a
note that has not been used yet.
