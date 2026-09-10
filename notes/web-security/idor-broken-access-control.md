---
topic: web-security
tags: [idor, bola, broken-access-control, authorization, owasp-top-10, api]
sources: [ball-hacking-apis, yaworski-real-world-bug-hunting, yaworski-web-hacking-101, mcdonald-grokking-web-application-security]
updated: 2026-09-09
---

# IDOR and Broken Access Control

OWASP's #1 risk, and one of the most common real findings in web and API
testing. The app knows *who* you are but forgets to check *what* you are allowed
to touch — so you change an identifier and read someone else's data.

## Authentication vs. authorization

- **Authentication** — proving *who you are* (login, session cookie, token, API
  key).
- **Authorization** — deciding *what you may access or do* once identified.

The classic mistake: implement authentication correctly, then assume any
logged-in request is legitimate. When the code checks *who* the user is but not
whether that user **owns** the requested resource, you get **Broken Access
Control**.

## IDOR / BOLA

An **Insecure Direct Object Reference** (in APIs: **Broken Object Level
Authorization**) happens when the app exposes a direct identifier to an internal
object — a record number, account id, filename, a URL like `/invoice/2` or
`/api/v1/receipt/135` — and does not verify server-side that the logged-in user
is allowed that object. Because the ownership check is missing, User A can read,
change, or delete User B's data just by altering the identifier.

## Finding and exploiting it

**Spot the identifiers.** Look for predictable values in URLs, query strings,
headers, or JSON bodies: `/invoice/2`, `?user_id=15`, `/api/v1/account/2222`.

**Change them.**

- **Numeric fuzzing** — increment/decrement sequential IDs (`id=5501` →
  `5502`), by hand or with Burp Intruder / Wfuzz to sweep a range.
- **A–B testing** — create two accounts. Make an object as User A, note its id,
  then request it while sending User B's session. If B gets A's object, it is
  vulnerable.

**Two directions of access:**

- **Horizontal** — reach data of another user at the *same* privilege level
  (another client's invoice). This is the InvoiceHub case.
- **Vertical** — reach higher-privilege data or functions (`/admin/...`) as a
  low-privileged user (privilege escalation). When it's a *function* rather than
  an object, that's BFLA — see
  [Mass assignment & broken function-level authorization](mass-assignment.md).

## Why it is #1, and the fix

It tops the OWASP list because it is a **business-logic** flaw, not a syntax
bug: the malicious request looks completely normal, so automated scanners miss
it, and when present it lets an attacker enumerate and exfiltrate data across the
whole platform.

The fix is a server-side ownership check on **every** object access:

- Verify `object.owner == current_user` (or the user's role/permission) in the
  backend before returning or modifying anything.
- Never trust client input or client-side checks.
- **Defense in depth:** unguessable IDs (UUIDs) make enumeration harder, but are
  *not* a substitute for the ownership check — they only slow a determined
  attacker.

## Recognising this in a CTF

Hints like "see your own X", "what else can you see", or "log in as demo" point
straight here. Log in, find where an object is addressed by an id, and request
ids you should not own — especially `1`, low numbers, and neighbours of your own.

## Seen in

- [InvoiceHub](../../course/class-01-intro/invoicehub.md) — invoices addressed by
  sequential id; logged in as `alice`, requested `/invoice/1` (another client's)
  and read it without any ownership check.
- NotePad (course, Class 2) — notes addressed by `/notes?id=N`; changed the id to
  read the admin's note (id 1). *(Write-up kept local until the course releases
  it.)*
- DocVault (course, Class 2) — random UUID ids (not enumerable) but leaked via an
  `/activity` feed, and access control was client-side only; calling
  `/api/documents/<uuid>` directly returned the admin's doc. Shows UUIDs and
  client checks are not access control. *(Write-up kept local until release.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **Ball — *Hacking APIs*** — BOLA/IDOR, spotting object ids, numeric fuzzing
  and A–B authorization testing.
- **Yaworski — *Real-World Bug Hunting* and *Web Hacking 101*** — real IDOR
  reports and how they were found.
- **McDonald — *Grokking Web Application Security*** — authentication vs.
  authorization and enforcing access control server-side.
