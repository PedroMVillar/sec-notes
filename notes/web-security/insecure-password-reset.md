---
topic: web-security
tags: [authentication, password-reset, account-recovery, predictable-token, host-header-injection, token-leakage, idor, otp, jwt, user-enumeration, business-logic]
sources: [mcdonald-grokking-web-application-security, ball-hacking-apis, yaworski-real-world-bug-hunting, yaworski-web-hacking-101]
updated: 2026-09-15
---

# Attacking Password Reset & Account Recovery

A password reset flow is a **second login** — often a less-audited one. If any
part of it is broken you take over accounts (usually `admin`) without the
password. This note is the full map of what can go wrong and what to test; the
predictable-token case (class 1) is the one from the Corp Portal CTF, but it's
one of many.

## The mindset

A secure reset generates a **random, high-entropy token**, **stores** it bound
to the account, delivers it **out-of-band** (email/SMS), and on return checks it
is *this user's*, *unused*, and *unexpired*. Every attack below is a way that
chain is broken. First recon: register/own two accounts, walk the whole flow in
a proxy, and inspect every request, response, header, and email.

## The vulnerability classes

### 1. Predictable / derived tokens
The token is computed from guessable inputs instead of stored random —
`md5(username + time_block)`, sequential ints, timestamps.
- **Detect:** request several tokens; check length/charset/entropy (Burp
  Sequencer). 32-hex = md5, 40-hex = sha1. An **"expired"** error ⇒ time is in it.
- **Try:** grab the server clock from the `Date` header, compute `epoch//N`
  (N∈{1,30,60,300,900,3600}), and test `md5/sha1(user [+ date/epoch block])`.
  `echo -n "victim1700000000" | md5sum`.

### 2. Host header injection / reset poisoning
The reset link's domain is built from the request `Host` / `X-Forwarded-Host`,
so you point it at your server and the victim's token lands in your logs.
- **Try:** in the `/forgot` request, set `Host: attacker.com` (or add
  `X-Forwarded-Host: attacker.com`); request a reset for a victim; if the email
  link is `https://attacker.com/reset?token=…`, it's vulnerable.

### 3. Token leakage (Referer / response / logs)
Even a strong token leaks through side channels.
- **Response reflection:** the `/forgot` response body/JSON echoes the token or
  `reset_url` — read it directly.
- **Referer:** the reset page loads third-party assets (analytics, fonts, CDNs);
  the full URL with the token goes out in the `Referer` header. Open the reset
  link through a proxy and watch outbound cross-domain requests.
- Also check server logs / URL history.

### 4. Token not bound to the account
Random token, but the server never checks it belongs to the account being reset.
- **Try:** get a valid token for **your** account, then submit the reset for the
  **victim** using *your* token (`{"userid":"victim","token":"<yours>","new_password":"…"}`).
  If it works, there's no `WHERE token=? AND user_id=?`.

### 5. No expiry / no single-use (reuse)
- **Try:** complete a reset, then submit the **same token again** (reuse). And
  hold a token 24h+ (or use an old email link) to test expiry.

### 6. Weak/short OTP + no rate limit
4–6 digit codes are brute-forceable if the verify endpoint doesn't throttle.
- **Try:** request an OTP, then Burp Intruder / Wfuzz `0000–9999` or
  `000000–999999` on `/verify-otp`. Watch for `429`/lockout. If throttled, test
  bypasses: `X-Forwarded-For` rotation, API version swap (`/v2`→`/v3`), junk
  params (`?x=1`), or that the OTP isn't invalidated after N misses.

### 7. User enumeration (and its reversal)
- **Detect:** compare `/forgot` for a real vs fake user — different **body**,
  **status** (`200` vs `404`/`500`), or **timing** (real user sends email = slow;
  fake = fast) leaks who exists. The reverse bug: it says "password updated" even
  for a **non-existent** user (looks like success, but you can't log in as a
  ghost → pivot to a user you know exists, e.g. `admin`).

### 8. IDOR / parameter manipulation in the reset
The final step trusts a client-supplied `user_id`/`email` to pick the account,
overriding the token's identity.
- **Try:** with your valid token, change the body: `{"token":"<yours>","email":"victim@x","userid":"5502","new_password":"…"}`.
  Also **array/HPP**: `{"email":["you@x","victim@x"],"token":"…"}`.

### 9. Multi-step bypass / response tampering
- **Step skipping:** POST the final `/set-new-password` directly, skipping the
  email/question steps — the server may not check they were completed.
- **Response tampering:** if the front-end gates the last step on
  `{"success":false}`/`400`, intercept and flip it to `200`/`{"verified":true}`
  so the UI shows the new-password form. Client-side checks aren't security.

### 10. Weak security questions
Low-entropy, OSINT-able answers ("mother's maiden name", high school), often
with no rate limit.
- **Try:** brute-force common answers (dictionary of pets/cities/schools); test
  case-sensitivity and SQL/NoSQL injection in the answer field.

### 11. JWT / signed reset tokens
If the reset token is a JWT (`eyJ…`, `header.payload.signature`), it inherits all
[JWT flaws](jwt-attacks.md): `alg:none`, weak HMAC secret (crack offline),
RS256→HS256 confusion. Decode it, change `sub`/`email` to the victim, and re-sign
or strip the signature.

## Fast triage checklist

1. Read the `/forgot` **response** and the **email**: token reflected? link
   domain from the `Host` header? third-party assets on the reset page?
2. Does the form key on **username** or **email**? (tells you the token formula)
3. Send a junk token → note the wording (**"expired"** ⇒ time-based → class 1).
4. Is the token a **JWT**? → class 11. Short **numeric OTP**? → class 6.
5. Own two accounts: is the token **bound** to the user (class 4) / can you swap
   the `user_id` in the final step (class 8)?
6. **Reuse** an old token / wait for expiry (class 5).
7. Different response for real vs fake user (class 7).

## The fixes (all classes)

- **Random, stored, single-use, expiring** tokens (CSPRNG ≥128 bits; store the
  token or its hash bound to the user id; invalidate on first use; short TTL).
- **Never derive a secret from public data** (username, time, counters).
- **Hardcode** the reset URL domain; never build it from request headers.
- **Never return** tokens/URLs in responses; set `Referrer-Policy: no-referrer`
  on reset pages.
- Derive the target account **from the token record**, not from client params.
- **Rate-limit** requests and verification (per IP and per account); uniform,
  generic responses to prevent enumeration.
- For JWT tokens: pin algorithms, reject `none`, strong secret.

## Recognising this in a CTF

Any `/forgot` + `/reset` pair. Walk the checklist above. Course example was a
predictable token; real targets more often fall to host-header poisoning, an
unbound token, or a client-controlled `user_id` in the final step.

## Related

- [JWT attacks](jwt-attacks.md) — when the reset token is a JWT.
- [Brute force & missing rate limiting](brute-force-rate-limiting.md) — OTP
  brute forcing (class 6).
- [IDOR and broken access control](idor-broken-access-control.md) — class 8.

## Seen in

- Corp Portal — Recuperación (course, Class 2) — **class 1**: `/reset` recomputed
  `md5(username + epoch//60)` instead of storing a random token; the `Date`
  header gave the time, so the admin token was forged. Reset also reported
  success for non-existent users (**class 7** reversal). *(Write-up kept local
  until release.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **Ball — *Hacking APIs*** — token binding, IDOR/HPP in reset, OTP brute force,
  JWT reset tokens, host-header and multi-step bypasses.
- **McDonald — *Grokking Web Application Security*** — secure reset design,
  CSPRNG tokens, uniform responses, `Referrer-Policy`.
- **Yaworski — *Real-World Bug Hunting* & *Web Hacking 101*** — host-header
  poisoning, token leakage, and enumeration reports in the wild.
