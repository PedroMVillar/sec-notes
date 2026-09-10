---
topic: web-security
tags: [sql-injection, sqli, union-based, data-extraction, enumeration, sqlite, information-schema, owasp-top-10]
sources: [mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting, ball-hacking-apis]
updated: 2026-09-10
---

# UNION-based SQL Injection

The data-extraction side of SQLi. Where [auth-bypass SQLi](sql-injection.md)
skips a check, UNION-based SQLi **reads other tables** through an injectable
search or listing that displays its results. Same root cause (input concatenated
into a query), different goal.

## What UNION does

`UNION` glues a second `SELECT`'s rows onto the first query's results. If a page
shows the rows of `SELECT name, price FROM products WHERE name LIKE '%q%'`, you
append `UNION SELECT something, something FROM other_table` and the page renders
*that* table's data too.

Two hard requirements:

- **Same number of columns** as the original query.
- **Compatible types** per column (text where text is shown).

## The workflow

**1. Find the column count.** Two ways:

- `ORDER BY n --` — increment `n` (`ORDER BY 1`, `2`, `3`…) until it errors; the
  last non-erroring number is the count.
- `UNION SELECT NULL --`, `UNION SELECT NULL,NULL --`, … — `NULL` fits any type,
  so it stops erroring when the count matches.

**2. Use a non-matching base term.** Search for something that returns zero rows
(`zzz'`, `-1'`) so the page shows **only your injected rows**, not real results.
Close the string with `'` and comment the tail with `--` (keep the trailing
space).

**3. Fingerprint the DB and enumerate the schema** via its metadata catalog:

- **MySQL / PostgreSQL** — `information_schema`:
  ```
  ' UNION SELECT table_name, NULL FROM information_schema.tables-- 
  ' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users'-- 
  ```
- **SQLite** — `sqlite_master` (holds each table's `CREATE` statement, so you get
  tables *and* columns at once):
  ```
  ' UNION SELECT name, sql FROM sqlite_master WHERE type='table'-- 
  ```

Whichever catalog works also tells you which engine you're on.

**4. Extract.** With the table and columns known:

```
' UNION SELECT username, password_hash FROM users-- 
```

## Column count / type tips

- If the displayed columns are fewer than the query's real count, pad with
  `NULL`s and put your data in a column you can see.
- To place text into a numeric column position, wrap or cast; usually easier to
  find a text column that's rendered.
- Concatenate multiple values into one visible column when needed
  (`col1||':'||col2` in SQLite/PostgreSQL, `CONCAT()` in MySQL).

## The fix

- **Parameterized queries** — the one real fix, same as every SQLi.
- **Least privilege** — the web DB user should only touch its own tables, so a
  UNION can't reach `information_schema`-visible secrets or other databases.
- **Database hygiene** — remove leftover test/backup tables (`users_backup`,
  staging dumps) from production; they are exactly what UNION enumeration finds.

## Recognising this in a CTF

A search, product listing, or any feature that **displays rows from the
database** and reacts to a `'`. Hints about "returns more than it should",
"leftover table", or "old data never deleted" point straight at UNION
extraction. Slug `sqli-medium` and up usually means this rather than auth bypass.

## Related

- [SQL injection](sql-injection.md) — auth bypass and the shared fundamentals
  (why a quote breaks out, parameterized queries).

## Seen in

- ByteBazaar Leaks (course, Class 2) — SQLite product search; counted 2 columns,
  enumerated `sqlite_master`, found a leftover `secrets(flag, note)` table and
  dumped it with `UNION SELECT flag, note FROM secrets`. *(Write-up kept local
  until the course releases it.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **McDonald — *Grokking Web Application Security*** — how UNION injection works
  and the parameterized-query fix.
- **Yaworski — *Real-World Bug Hunting*** — SQLi data extraction in real reports.
- **Ball — *Hacking APIs*** — column counting, schema enumeration, and extraction
  methodology.
