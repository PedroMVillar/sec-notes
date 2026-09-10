---
platform: course
class: 1
target: secret-in-the-source
category: web
difficulty: introductory
access: "https://<course-host>/"
tags: [web, client-side, source-review, api-key, base64, devtools, info-disclosure]
technique: client-side-secrets
date: 2026-09-09
---

# Secret in the Source

**Class:** 1 (Intro) · **Category:** Web · **Level:** Introductory

Beacon Corp's internal-tools portal is online. Somewhere in what the browser
downloads there is something that should never have left a developer's machine.
The task: find it.

## Recon — read what the browser downloads

A browser does not just render a page; it **downloads files** — the HTML and
everything it links (JS, CSS). All of it is yours to read. First, see what the
page pulls in:

```bash
curl -s https://<course-host>/ | grep -i "src="
# src="/static/js/main.js"
```

One linked script. In the browser the same view is **F12 → Sources** (the tree
of every downloaded file) or `view-source:` on the URL.

## Finding the secret

Read the JS bundle to the end:

```bash
curl -s https://<course-host>/static/js/main.js
```

Two things stand out — and they belong together:

- A developer comment admitting the mistake:
  ```js
  // TODO(dev): pull this from the secrets manager before prod deploy, not
  // hardcoded here. Leaving inline for now so the demo works offline. -M
  ```
- An internal config object shipped straight to every visitor, holding a
  hardcoded credential:
  ```js
  const INTERNAL_CFG = {
    env: "staging",
    featureFlags: { newDashboard: false, betaSearch: true },
    apiKey: "<base64 string — redacted>"
  };
  ```

That `apiKey` is the thing that should never have left the dev's machine.

## Decoding it — Base64 is not encryption

The `apiKey` value is not a random key: it is a run of letters and digits, which
is the tell for **Base64**. Base64 is *encoding*, not encryption — it has **no
key** and reverses instantly. Recognising it is half the work:

```bash
echo '<the apiKey value>' | base64 -d
# or in the browser console:  atob('<the apiKey value>')
```

Out comes the flag. Encoding a secret protects nothing.

## Flag

```
FaMAF{ ...redacted... }
```

Redacted, and the `apiKey` value with it — publishing the Base64 string is
publishing the flag. Decoded, it reads *client-side secrets aren't secret*.

## Technique

Full, source-backed write-up:
[Secrets in client-side code](../../notes/web-security/client-side-secrets.md).

## Lessons learned

- Everything sent to the browser is public. Nothing secret can live in
  client-side code — HTML, JS, comments, config objects included.
- Look where developers slip: `TODO`/`FIXME` comments, and variables named
  `key` / `token` / `secret` / `apiKey`. In DevTools, global-search the bundle
  for those words.
- Base64 is encoding, not encryption. A "hidden" secret in Base64 is one
  command away from plaintext.
- The fix is server-side: keep secrets on the backend and proxy third-party
  calls so the key never reaches the browser.
