---
topic: web-security
tags: [sql-injection, sqli, auth-bypass, injection, parameterized-queries, owasp-top-10]
sources: [mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting, yaworski-web-hacking-101, ball-hacking-apis]
updated: 2026-09-10
---

# SQL Injection

Injecting SQL through user input that the app concatenates into a query. The
oldest trick in web security and still everywhere. The clearest first form to
learn is **authentication bypass**: log in without a password.

## Why a quote breaks everything

In SQL the single quote `'` is a **metacharacter** — it marks the start and end
of a string literal. When an app builds a query by pasting input into a template:

```sql
SELECT * FROM users WHERE username = 'INPUT' AND password = 'INPUT'
```

it assumes you will type `alice`. But if your input contains a `'`, the database
reads that quote as the *end of the string* — and everything after it as **SQL
code**: keywords, operators, comments. Your data has escaped its slot and become
instructions.

## Auth-bypass payloads

**`admin' --`** in the username:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'x'
```

- `admin'` closes the username string.
- `--` is a single-line comment; the rest of the line is ignored.
- The `AND password = ...` check is now inside the comment — deleted.

Effective query: `SELECT * FROM users WHERE username = 'admin'`. You are in as
admin, no password.

**`' OR '1'='1' --`** in the username:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = 'x'
```

`'1'='1'` is always true, so the WHERE matches every row; the database returns
the first (often the admin), and you log in as whoever that is.

Payloads vary by how the app builds the query — trying variants (`'`, `--`,
`#`, `" `, `' OR 1=1-- `) is part of the job.

## Why it works

Concatenation hands the parser **code and data in one stream**. The database has
no memory of which characters the developer wrote and which came from the user —
once pasted, your input carries the same authority as native SQL keywords. That
is the entire vulnerability.

## Beyond auth bypass

The single quote is also how you *detect* SQLi: submit `'` and watch for a
database error or changed behaviour. From there SQLi extends to:

- **UNION-based** — append `UNION SELECT ...` to pull data from other tables.
  Full workflow in [UNION-based SQL injection](union-based-sql-injection.md).
- **Blind (boolean/time-based)** — no visible output, so you ask true/false
  questions (`AND 1=1` vs `AND 1=2`) or use delays (`SLEEP(5)`) and read the
  answer from the response.
- Automated with `sqlmap` once you have confirmed an injectable parameter.

## The fix

**Parameterized queries (prepared statements).** Send the query and the values
separately:

```python
cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password))
```

The database compiles the query structure *before* the input arrives, then binds
the input strictly as data. Submit `' OR 1=1--` and it looks for a user literally
named `' OR 1=1--` — attack neutralised. Parameterisation is not a nice-to-have;
it is the only thing that makes the problem not exist. (Then also: least-
privilege DB accounts, and hashing passwords so a dumped table is not plaintext.)

## The broader class: code vs. data

SQLi is one case of a universal bug — **untrusted input mixed into a code
context**:

- **XSS** — input concatenated into HTML runs as JavaScript.
- **Command injection** — input concatenated into a shell runs OS commands.
- **Template / NoSQL injection** — input evaluated by a template or query engine.

Core rule: keep a trust boundary — never concatenate untrusted input into a
query, command, or markup. Pass it as data.

## Recognising this in a CTF

A login (or any input that hits a database) where the hint points at "admin" or
"what does the server do with your input". Try `'` to break it, then `admin' --`
or `' OR '1'='1' --` to bypass auth.

## Seen in

- [NorthGate Bank](../../course/class-01-intro/northgate-bank.md) — login built
  by string concatenation; `admin' --` commented out the password check and
  logged in as admin.
- [Acceso VIP](../../course/class-02-web/acceso-vip.md) — same auth bypass on an
  unfiltered internal portal; solved in one payload.

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **McDonald — *Grokking Web Application Security*** — how injection works,
  the code/data boundary, and parameterized queries as the fix.
- **Yaworski — *Real-World Bug Hunting* and *Web Hacking 101*** — SQLi in
  practice and real reports.
- **Ball — *Hacking APIs*** — injection against API-backed queries and testing
  approach.
