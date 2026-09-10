---
platform: course
class: 1
target: invoicehub
category: web
difficulty: introductory
access: "https://<course-host>/"
tags: [web, idor, bola, broken-access-control, authorization, owasp-top-10]
technique: idor-broken-access-control
date: 2026-09-09
---

# InvoiceHub

**Class:** 1 (Intro) · **Category:** Web · **Level:** Introductory

InvoiceHub lets each client see their own invoices. Log in with the demo account
shown on the login page and see what else you can reach.

## Recon — log in and watch the URLs

The login page hands you a demo account: `alice` / `alice123`. After signing in
(`POST /login` → `/dashboard`), alice's invoices are listed, and the links tell
the whole story:

```
/invoice/2
/invoice/3
```

Invoices are addressed by a **sequential number**. Alice owns 2 and 3.

## The vulnerability — IDOR

If the objects are numbered and mine are 2 and 3, the obvious question is: who
owns **1**? Request it as alice:

```
https://<course-host>/invoice/1
```

It returns **200** and shows an invoice belonging to a *different* client
(Beacon Corp) — with the flag in it. The app verifies you are logged in
(authentication) but never checks that the invoice is **yours**
(authorization). That gap is an **IDOR / Broken Access Control**.

Invoices 4+ return 404, so the leak is invoice #1.

## Exploitation

Two equivalent ways:

- **Browser:** log in as alice, then edit the number in the address bar from a
  known-yours ID to `1`. The other client's invoice loads.
- **curl:**
  ```bash
  curl -s -c cookies.txt -d "username=alice&password=alice123" \
    https://<course-host>/login -o /dev/null
  curl -s -b cookies.txt https://<course-host>/invoice/1
  ```

No tooling, no payload — just changing an identifier you were never meant to
touch. This is *horizontal* access: same privilege level, someone else's data.

## Flag

```
FaMAF{ ...redacted... }
```

Redacted — see [course notes](../README.md). Decoded intent: *broken access
control — check the owner*.

## Technique

Full, source-backed write-up:
[IDOR and broken access control](../../notes/web-security/idor-broken-access-control.md).

## Lessons learned

- **Authentication is not authorization.** Being logged in does not mean you may
  see a given object; the server must check ownership on every access.
- **Sequential IDs are an invitation.** When a resource is addressed by a
  guessable number (`/invoice/1`), try neighbours you should not own.
- This is OWASP's **#1** risk (Broken Access Control) precisely because it looks
  like a perfectly normal request — scanners miss it, and it is everywhere.
- The fix is one server-side check: `invoice.owner == current_user` before
  returning anything.
