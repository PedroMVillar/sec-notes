---
topic: web-security
tags: [api, mass-assignment, bfla, broken-function-level-authorization, privilege-escalation, authorization, owasp-api-top-10]
sources: [ball-hacking-apis, mcdonald-grokking-web-application-security, yaworski-real-world-bug-hunting]
updated: 2026-09-10
---

# Mass Assignment & Broken Function-Level Authorization

Two API privilege-escalation bugs that travel together: the server trusts fields
and endpoints the UI never exposes. Where [IDOR/BOLA](idor-broken-access-control.md)
is about reading another user's *object*, these are about changing what you're
*allowed to be* and calling functions you shouldn't.

## Mass assignment

**Mass assignment** (auto-binding, excessive data binding) is when an endpoint
maps the JSON you send straight onto the backend object without an allowlist. A
`PATCH /api/users/me` meant for `bio` also updates `role` if you send it.

```bash
curl -X PATCH https://target/api/users/me \
  -H 'Content-Type: application/json' --data '{"role":"admin"}'
```

If the model has `role` / `is_admin` / `isAdmin` / `account_balance` and the
server binds raw input, you set them. The UI only sending `bio` is a
**client-side** restriction — it stops normal users, not HTTP requests.

Fields worth trying: `role`, `is_admin`, `isAdmin`, `admin`, `permissions`,
`org_id`, `user_id`, `verified`, `account_balance`.

## Broken function-level authorization (BFLA)

**BFLA** is calling a privileged *function* the server fails to gate. Admin
endpoints (`/api/admin`, `POST /api/admin/users`, `DELETE /api/v1/users/42`) are
often left out of the UI on the assumption nobody will find them — but they're
reachable if you guess the path or method and the server doesn't check your role.

- **BOLA** (IDOR) = access another user's **data/object**.
- **BFLA** = perform an unauthorized **action/function**.

## How to find them

1. **Read the front-end JS / API docs.** It reveals real field names, endpoints,
   version prefixes (`/v1/`, `/v2/`), and hidden paths (`/admin/`, `/internal/`).
   (In the InvoiceHub Clone challenge the JS literally commented that the `role`
   restriction "lives only in this JS, not on the server.")
2. **Mass assignment:** on any create/update, add extra fields (`role`,
   `is_admin`) and see if they persist. Fuzz body params with Arjun / Burp
   Intruder.
3. **BFLA:** send requests to admin endpoints from a low-priv session; swap
   methods (`GET`→`POST`/`PUT`/`DELETE`) on the same path. Watch for `200`
   where you expected `401`/`403`.

## The fix

- **Allowlist bindable fields** — bind only approved properties (DTOs / strong
  parameters); never pass raw JSON into an ORM save.
- **Authorize every endpoint, method, and field** server-side (RBAC), deny by
  default.
- **Never rely on the client** — hidden buttons, omitted fields, and
  undocumented endpoints are not security.

## Recognising this in a CTF

An "API" challenge, a hint about "functions the UI doesn't show" or "send
something the interface never offered", or a front-end that only submits a
subset of fields → try adding `role`/`is_admin` (mass assignment) and hitting
`/api/admin`-style endpoints (BFLA).

## Related

- [IDOR and broken access control](idor-broken-access-control.md) — the
  object-level sibling (BOLA); same root idea, missing server-side authorization.
- [Secrets in client-side code](client-side-secrets.md) — why the front-end JS is
  worth reading in the first place.

## Seen in

- InvoiceHub Clone (course, Class 2) — `PATCH /api/users/me {"role":"admin"}`
  (mass assignment) then `GET /api/admin` (a hidden endpoint, BFLA) returned the
  flag. *(Write-up kept local until the course releases it.)*

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **Ball — *Hacking APIs*** — mass assignment, BOLA vs BFLA, finding hidden
  endpoints and fuzzing parameters.
- **McDonald — *Grokking Web Application Security*** — server-side authorization
  and why client restrictions don't count.
- **Yaworski — *Real-World Bug Hunting*** — privilege-escalation reports in the
  wild.
