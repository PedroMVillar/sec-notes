---
topic: web-security
tags: [jwt, alg-none, hmac, algorithm-confusion, authentication, api, privilege-escalation]
sources: [ball-hacking-apis, mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting]
updated: 2026-09-11
---

# JWT Attacks

JSON Web Tokens carry auth claims the client holds and sends back. If the server
verifies them wrong, you rewrite your own claims — `role: user` → `role: admin`.
"Mathematically secure" is meaningless if you can turn the maths off from the
header.

## Structure and the core flaw

`header.payload.signature`, each base64url-encoded:

- **Header** — metadata, incl. the signing `alg` (`"alg":"HS256"`).
- **Payload** — claims (`username`, `role`, `exp`).
- **Signature** — header+payload run through `alg` with a secret/key.

**The flaw:** a badly-built server trusts the `alg` value *inside the
user-controlled header* to decide how to verify. You control the header → you
influence verification.

## alg:none

The spec allows `alg: "none"` — an unsigned token. A correct server rejects it;
many don't. Forge:

1. Header `{"alg":"none","typ":"JWT"}`
2. Payload with your claims, e.g. `{"username":"demo","role":"admin","exp":9999999999}`
3. **Empty signature — keep the trailing dot:** `header.payload.`

Two gotchas that decide success:

- **Incomplete blacklists.** Servers often block `"None"`/`"NONE"` but a
  case-sensitive check misses lowercase **`none`** (or `nOnE`). Try the variants.
- **`exp` still checked.** Even with `none` accepted, an expired `exp` is
  rejected — set `exp` to a future timestamp.

```bash
curl -s -H "Authorization: Bearer <hdr>.<payload>." https://target/api/admin/flag
```

## Weak HMAC secret (HS256)

HS256 is symmetric — one secret signs *and* verifies. Since the token is in your
hands, crack the secret **offline** (no requests to the server, no rate limits):

```bash
hashcat -m 16500 jwt.txt rockyou.txt
jwt_tool <token> -C -d rockyou.txt
```

(Or a few lines of Python: HMAC-SHA256 each candidate over `header.payload`,
compare to the signature.) With the secret, forge `role:admin` and sign a valid
token. Weak/common secrets (`secret`, `123456`, an app name) fall instantly.

## Algorithm confusion (RS256 → HS256)

RS256 is asymmetric: **private** key signs, **public** key verifies. If the
server lets the header pick the algorithm:

1. Grab the server's **public** key (often at `/.well-known/jwks.json` or a cert).
2. Craft an admin payload, set `alg` to **HS256**.
3. Sign it with the **public key as the HMAC secret**.

The server, seeing HS256, verifies with that same public key as an HMAC secret —
and it matches. You signed with a "secret" that was never secret.

## The fixes

- **Pin the algorithm server-side** — `jwt.decode(token, key,
  algorithms=["HS256"])`. Never trust the header's `alg`.
- **Reject `none`** and missing signatures outright (allowlist, not blacklist).
- **Strong secret** — ≥256-bit random for HMAC, so offline cracking fails.
- **Always verify the signature** before reading any claim.

## Recognising this in a CTF

An API using `Bearer` JWTs with a `role` claim and an admin-only endpoint.
Decode the token (jwt.io / base64), then in order: try `alg:none` (all case
variants, future `exp`), crack the HS256 secret with rockyou, and check for
RS256→HS256 confusion if a public key is reachable.

## Related

- [Mass assignment & BFLA](mass-assignment.md) — the other API privilege-
  escalation family (trusting client-supplied fields / hidden endpoints).
- [Brute force & missing rate limiting](brute-force-rate-limiting.md) — note that
  JWT secret cracking is *offline*, so rate limits never see it.

## Seen in

- Corp API (course, Class 2) — HS256 token with `role:user`; `alg:none` (lowercase
  only — `None`/`NONE` were blocked) with a future `exp` and empty signature
  forged `role:admin`, and `/api/admin/flag` returned the flag. *(Write-up kept
  local until release.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **Ball — *Hacking APIs*** — JWT structure, alg:none, HS256 cracking,
  RS256→HS256 confusion, and tooling (jwt_tool, hashcat).
- **McDonald — *Grokking Web Application Security*** — signature verification and
  pinning the algorithm server-side.
- **Yaworski — *Real-World Bug Hunting*** — token-handling flaws in real reports.
