# Cheatsheets

Lookup material — syntax, flags and payloads I have already understood and no
longer want to re-derive under time pressure.

The distinction from [`notes/`](../notes/README.md) is deliberate: notes
explain *why*, cheatsheets recall *how*. Everything here is something I have
used at least once; copied-in reference tables I have never run do not belong.

## Planned sheets

| File | Contents |
|---|---|
| `nmap.md` | Scan types, timing, NSE scripts worth remembering |
| `reverse-shells.md` | One-liners per language, upgrading to a full TTY |
| `gdb-pwntools.md` | Debugging and exploit-scripting syntax |
| `linux-privesc.md` | SUID, capabilities, cron, sudo misconfigurations |
| `windows-privesc.md` | Tokens, services, unquoted paths, AD misconfigurations |
| `burp.md` | Workflow, useful extensions, match-and-replace rules |
| `sqli.md` | Payloads per DBMS, WAF bypasses, blind techniques |

Files appear as they are written.

## Conventions

Every entry pairs a command with what it does and when to reach for it. A
payload with no context is a payload you will paste blindly and misread the
output of.

Where a sheet has a matching note, link to it — the cheatsheet is the index,
the note is the explanation.
