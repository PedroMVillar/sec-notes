---
platform: hackthebox        # hackthebox | tryhackme | picoctf | competitions
target: Target Name
difficulty: easy            # easy | medium | hard | insane
os: linux                   # linux | windows | other
tags: [web, sqli, privesc]  # techniques, CVEs, protocols
date: 2026-01-01
---

# Target Name

**Platform:** Hack The Box · **Difficulty:** Easy · **OS:** Linux

One paragraph: what this box is about and what makes it interesting. Write it
last, once you know what the box actually taught you.

## Recon

Scope, initial scans, what the surface looks like. Commands with their output
trimmed to what mattered.

```bash
nmap -sC -sV -oA scans/target 10.10.10.10
```

## Enumeration

Following the threads recon opened. Which services, which versions, what they
expose.

## Foothold

How initial access happened. Include the exploit or payload, and explain *why*
it works — a command you cannot explain is a command you have not learned.

## Privilege Escalation

The path from low-privilege user to root/SYSTEM.

## Dead Ends

What you tried that did not work, and why it failed. This is the section you
will thank yourself for in six months, and the one everyone else skips.

## Lessons Learned

Two or three things worth carrying to the next target. Link to the relevant
topic note — for example, [SQL injection](../../notes/web-security/sql-injection.md).

## References

- Advisory, writeup or documentation that helped.
