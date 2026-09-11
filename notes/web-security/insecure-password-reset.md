---
topic: web-security
tags: [authentication, password-reset, predictable-token, md5, user-enumeration, csprng, business-logic]
sources: [mcdonald-grokking-web-application-security, ball-hacking-apis, yaworski-real-world-bug-hunting]
updated: 2026-09-11
---

# Insecure Password Reset & Predictable Tokens

A password reset flow is a second login. If its token can be predicted or
forged, an attacker resets anyone's password — usually `admin`'s — without ever
seeing the email. The classic flaw: **deriving the token from public data
instead of storing a random one.**

## What a secure reset looks like

Four properties, all required:

- **Cryptographically random, high-entropy token** — from a CSPRNG (`secrets`,
  `SecureRandom`, `/dev/urandom`), ≥128 bits (e.g. 32-byte hex or UUIDv4).
  Guessing it is infeasible.
- **Stored server-side, bound to the account** — the token (or its hash) sits in
  the DB tied to the user id, with a created-at and a `used` flag.
- **Single-use** — invalidated the moment it's accepted.
- **Time-limited** — short expiry (10–15 min).

The security is in *storing a random value*. You cannot guess random.

## The vulnerability: derived / predictable tokens

A "stateless" shortcut computes the token from user data + time instead of
storing a random one:

```
token = md5(username + time_block)
```

Every input is public or discoverable, so the attacker recomputes it offline:

- **The username is public** (or found via enumeration). Note: if the reset form
  asks for a **username, not email**, the formula is built from the username.
- **The server leaks its clock** in the HTTP `Date:` header on *every* response —
  so you know the exact server time the formula uses.

### Time blocks and the "expired" tell

A per-second token would change before you could use it, so apps round time into
blocks: `epoch // 60` (1-minute window), `epoch // 900` (15-min), etc. The token
is stable across the block and "expires" after it.

So an error like **"Token inválido o expirado"** is a gift: *expired* means time
is in the token. Read the server's `Date` header, compute the block, and test a
handful of candidates (the current block ±1) — a few hashes, not a brute force.

### The workflow

1. Reset form asks for **username** → formula uses the username.
2. Send a junk token → "inválido o **expirado**" → time-based.
3. Grab the server time from the `Date` header.
4. Brute-force the *scheme* (not passwords): `md5(user)`, `md5(user+date)`,
   `md5(user + epoch//N)` for N in {30,60,300,900,3600}, md5/sha1, until one
   stops returning "inválido".
5. Forge the target's token, reset, log in.

## Related logic flaws

- **User enumeration** — different responses for existing vs non-existing
  accounts leak who exists.
- **The reverse** — saying "Contraseña actualizada" (or `200`) even for a
  **non-existent** user. Looks like success but you can't log in as a ghost, so
  pivot to an account you know exists: **`admin`**.
- **Pivot to high-value accounts** — a predictable scheme lets you target
  `admin`/`root` directly and escalate.

## The fixes

- **Never derive a secret from predictable inputs** — no usernames, timestamps,
  PIDs, or counters in a token.
- **Random + stored** — CSPRNG token, store it (or its hash) bound to the user,
  invalidate on first use.
- **Expiry, single-use, and rate limiting** per IP and per account.
- **Uniform responses** — one generic message regardless of whether the account
  exists.

## Recognising this in a CTF

An `auth`/recovery challenge with a `/forgot` + `/reset` pair, a token you never
receive (no mailbox), and an "expired" error. Check whether the form keys on
username, read the `Date` header, and try `md5(user + epoch//block)`.

## Related

- [Brute force & missing rate limiting](brute-force-rate-limiting.md) — the other
  way to abuse an auth flow with no throttling.
- [Secrets in client-side code](client-side-secrets.md) — same theme: a "secret"
  that isn't secret.

## Seen in

- Corp Portal — Recuperación (course, Class 2) — `/reset` recomputed the token as
  `md5(username + epoch//60)` instead of storing a random one; the `Date` header
  gave the time, so the admin token was forged and its password reset. Reset also
  reported success for non-existent users. *(Write-up kept local until release.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **McDonald — *Grokking Web Application Security*** — secure reset design,
  CSPRNG tokens, storage, expiry, uniform responses.
- **Ball — *Hacking APIs*** — predictable-token derivation, the `Date`-header
  clock leak, and pivoting to admin.
- **Yaworski — *Real-World Bug Hunting*** — password-reset and user-enumeration
  reports in the wild.
