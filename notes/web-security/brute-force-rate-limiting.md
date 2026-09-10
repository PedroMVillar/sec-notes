---
topic: web-security
tags: [authentication, brute-force, password-spraying, credential-stuffing, rate-limiting, account-lockout, mfa]
sources: [mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting, ball-hacking-apis]
updated: 2026-09-10
---

# Brute Force & Missing Rate Limiting

An authentication attack, not an injection one: if a login accepts unlimited
attempts, a weak password is only a matter of time. Parameterized queries and
server-side validation do nothing here — **missing rate limiting is itself the
vulnerability.**

## Why it's a bug even with "secure" code

A perfectly injection-proof login still fails if it lets an attacker submit
thousands of guesses per minute with no lockout, delay, or CAPTCHA. The SQL is
safe; the *business logic* permits automated guessing until something matches.

## The variants

- **Password guessing (targeted):** one known user (`admin`), a wordlist of
  common passwords. This challenge.
- **Password spraying:** many users, a *few* high-probability passwords
  (`Winter2026!`, `Password1!`), 1–2 tries each — stays under per-account
  lockout thresholds.
- **Credential stuffing:** breached `user:pass` pairs replayed against the app,
  exploiting password reuse.

## Running it, and reading success

A shell loop is enough for a single user; Hydra, Burp Intruder (Sniper /
Cluster Bomb / Pitchfork), or Wfuzz scale it.

```bash
while read -r p; do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST https://target/login \
    --data-urlencode "username=admin" --data-urlencode "password=$p")
  [ "$code" != "401" ] && { echo "FOUND: $p"; break; }
done < passwords.txt
```

**Tell success from failure** by an anomaly across responses:

- **Status code** — `401`/`400` on failure vs `200`/`302` (redirect to
  dashboard) on success.
- **Response length** — failures are a fixed byte size; success differs (session
  token, dashboard).
- **Error string** — presence/absence of "Invalid credentials".

*Use the provided/known wordlist when there is one* — don't burn requests
improvising your own.

## The fixes

- **Rate limiting + exponential backoff** per IP and per account.
- **Account lockout** after N failures (track per IP too, so it can't be abused
  to lock out real users = DoS).
- **CAPTCHA** on repeated failures.
- **MFA** — a guessed password alone isn't enough.
- **Strong-password policy** (block common passwords, e.g. zxcvbn).
- **Monitoring** — alert on failed-login spikes and one-IP-many-users patterns.

## Recognising this in a CTF

A login that hints "no limit on attempts", "we gave you a password list", or a
recovery/OTP flow with a short code and no throttling. Slug `auth-easy` often
means straight password guessing. Confirm the failure response, then loop the
list and watch for the odd-one-out.

## Related

- [SQL injection](sql-injection.md) — the *other* way into a login; fixing it
  doesn't fix guessing.

## Seen in

- Corp Portal v2 (course, Class 2) — login rewritten with parameterized queries
  but no rate limit; looped the provided 20-password list against `admin`, the
  correct one returned `302` instead of `401`. *(Write-up kept local until
  release.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **McDonald — *Grokking Web Application Security*** — auth abuse, rate limiting,
  lockout, MFA, strong-password policy.
- **Yaworski — *Real-World Bug Hunting*** — credential attacks in practice.
- **Ball — *Hacking APIs*** — spraying/stuffing, Hydra/Intruder/Wfuzz, reading
  success by status/length.
