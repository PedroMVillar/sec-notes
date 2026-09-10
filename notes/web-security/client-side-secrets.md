---
topic: web-security
tags: [client-side, source-review, api-key, base64, devtools, info-disclosure]
sources: [mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting, yaworski-web-hacking-101, ball-hacking-apis]
updated: 2026-09-09
---

# Secrets in Client-Side Code

The most reliable easy win in web CTFs and bug bounty: developers leave secrets
in the code the browser downloads. Because the client is fully visible, those
secrets are public the moment the page loads.

## Why the client is public

A web app is client-server. The server sends HTML, CSS, JavaScript and comments;
the browser downloads and runs them **on the user's machine**. That means the
user has complete access to everything delivered — every line, variable and
comment can be read with view-source or DevTools.

The governing rule: **the client side is untrusted and fully visible.** Anything
delivered to the browser is public by definition. An attacker can also read,
modify or replay any request, cookie or header before it reaches the server — so
nothing secret, and no security decision, can live on the client.

## What developers leave behind

- **API keys and tokens** — third-party keys (maps, cloud, payments), OAuth
  client secrets. A leaked private key lets an attacker act with its privileges.
- **Credentials** — basic-auth strings, admin or test passwords in scripts/config.
- **Internal endpoints** — unlinked admin routes, staging URLs, hidden API paths.
- **Comments and config objects** — `TODO`/`FIXME` notes, internal IPs, backend
  config shipped inline "just for the demo".

## How to find them

1. **View source** — `view-source:<url>` shows raw HTML and inline scripts.
2. **DevTools → Sources** (`F12`) — the tree of every downloaded file. Global
   search (`Ctrl+Shift+F`) across all assets for `key`, `secret`, `token`,
   `password`, `api`.
3. **DevTools → Network** — reload and watch requests: endpoints, headers,
   authorization tokens, JSON payloads.
4. **Pretty-print bundles** — minified files (`main.js`, `app.chunk.js`) become
   readable with the `{}` button; then search for `POST`/`GET`, URLs, and the
   keywords above.
5. **From the terminal** — `curl` the page, grep for `src=`, `curl` each script
   and grep it:
   ```bash
   curl -s https://target/ | grep -i "src="
   curl -s https://target/static/js/main.js | grep -niE "key|secret|token|todo"
   ```

## Base64 is not encryption

A common trap: a secret shown as Base64 looks "encoded/safe". It is not.

- **Encoding, not encryption.** Base64 maps bytes to printable ASCII so data
  survives text protocols. It uses **no key**.
- **Reverses instantly.** `echo '...' | base64 -d`, `atob('...')` in the browser
  console, or Burp's Decoder — plaintext in one step.
- **Zero confidentiality.** A Base64 secret (including HTTP Basic-auth
  `Authorization: Basic ...`) offers no protection at all.

Recognise it by its charset (`A–Z a–z 0–9 + /`, sometimes `=` padding) and try
decoding before assuming anything is "hidden".

## Security lesson and fix

- Treat the client as adversary-controlled. Never ship a secret to it, and never
  trust it for authorization.
- Keep secrets server-side — environment variables, a secrets manager, a KMS.
- **Backend proxying:** if the front end needs a third-party API that requires a
  private key, call your own server endpoint; the server adds the key, calls the
  API, and returns only the result. The key never reaches the browser.
- All validation and authorization decisions run on the server.

## Recognising this in a CTF

When the hint mentions "source", "what the browser loads", or "developer",
go straight to the delivered code: view-source, open every JS file, search for
key/secret/token/TODO, and decode anything Base64-looking. It is often the whole
challenge.

## Seen in

- [Secret in the Source](../../course/class-01-intro/secret-in-the-source.md) —
  hardcoded `apiKey` (Base64) left in a shipped JS bundle beside a TODO comment
  admitting it; decoded to the flag.

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **McDonald — *Grokking Web Application Security*** — client-side is untrusted
  and fully visible; where secrets leak.
- **Yaworski — *Real-World Bug Hunting* and *Web Hacking 101*** — finding
  hardcoded keys, endpoints and comments via source review and DevTools.
- **Ball — *Hacking APIs*** — exposed API keys and endpoints in front-end code,
  and why Base64 is not protection.
