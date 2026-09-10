# Course

Challenges from my university course, grouped by class, one write-up per
challenge plus the technique each one taught.

The write-ups document the **method**, never the answer. Flags are redacted:
the challenges live on the course's private platform, and publishing solutions
would break the course rules and spoil the exercise for classmates. What is
public is how to think through a challenge of that kind — the part worth
keeping anyway.

## Layout

One folder per class: `course/class-NN-topic/`. Each write-up links to the
reusable note for its technique in [`notes/`](../notes/README.md), so the
theory is written once and reused across challenges.

## Class 1 — Intro

| Challenge | Category | Technique |
|---|---|---|
| [legado](class-01-intro/legado.md) | Reversing | [Static string analysis](../notes/reverse-engineering/static-string-analysis.md) |
| [Ping-Pong](class-01-intro/ping-pong.md) | Crypto / weak hash | [Weak hashes and preimage attacks](../notes/cryptography/weak-hash-preimage.md) |
| [Sin Backup](class-01-intro/sin-backup.md) | Reversing | [Reversing decompiled password checks](../notes/reverse-engineering/reversing-decompiled-password-checks.md) |
| [Secret in the Source](class-01-intro/secret-in-the-source.md) | Web | [Secrets in client-side code](../notes/web-security/client-side-secrets.md) |
| [InvoiceHub](class-01-intro/invoicehub.md) | Web | [IDOR and broken access control](../notes/web-security/idor-broken-access-control.md) |
| [NorthGate Bank](class-01-intro/northgate-bank.md) | Web | [SQL injection](../notes/web-security/sql-injection.md) |

## Class 2 — Web

| Challenge | Category | Technique |
|---|---|---|
| [Acceso VIP](class-02-web/acceso-vip.md) | Web | [SQL injection](../notes/web-security/sql-injection.md) |
| QuickFind † | Web | [Cross-Site Scripting (XSS)](../notes/web-security/xss.md) |
| NotePad † | Web | [IDOR and broken access control](../notes/web-security/idor-broken-access-control.md) |
| ByteBazaar Leaks † | Web | [UNION-based SQL injection](../notes/web-security/union-based-sql-injection.md) |
| Foro Interno † | Web | [Cross-Site Scripting (XSS)](../notes/web-security/xss.md) |
| InvoiceHub Clone † | Web / API | [Mass assignment & BFLA](../notes/web-security/mass-assignment.md) |
| SecureAuth † | Web | [Blind SQL injection](../notes/web-security/blind-sql-injection.md) |

† Write-up kept local until the course releases the official solution; only the
technique note is published.
