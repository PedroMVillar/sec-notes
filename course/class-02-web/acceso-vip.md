---
platform: course
class: 2
target: acceso-vip
category: web
difficulty: easy
access: "https://<course-host>/"
tags: [web, sql-injection, sqli, auth-bypass, injection]
technique: sql-injection
date: 2026-09-10
---

# Acceso VIP

**Class:** 2 (Web) · **Category:** Web · **Level:** Easy

An internal portal built years ago by an intern who has left; HR never changed
the default config, and the login form looks careless. No account — the task is
to log in as `admin` without knowing the password.

## Solution

Straight authentication bypass via SQL injection — the same technique as
[NorthGate Bank](../class-01-intro/northgate-bank.md). The URL slug
(`web-sqli-easy`) and the "careless login form" hint both point at it.

Username field (any password):

```
admin' --
```

The login concatenates input into its query, so this closes the username string
and comments out the password check:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'x'
```

The effective query is `SELECT * FROM users WHERE username = 'admin'` — password
check gone, logged in as admin, flag on the resulting page. One payload, no
variants needed.

## Flag

```
flag{ ...redacted... }
```

Redacted — see [course notes](../README.md). Decoded intent: *SQLi is easy when
unfiltered*.

## Technique

Same as before — full write-up:
[SQL injection](../../notes/web-security/sql-injection.md).

## Lessons learned

- Second time seeing SQLi auth bypass: recognised from the hint, solved in one
  payload. That is the point of building a technique library.
- `admin' --` remains the first thing to try on any unfiltered login.
- Fix is unchanged: parameterized queries.
