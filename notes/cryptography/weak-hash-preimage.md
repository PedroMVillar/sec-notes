---
topic: cryptography
tags: [hashing, checksum, preimage, collision, integrity, authentication]
sources: [andress-foundations-of-information-security, grubb-how-cybersecurity-really-works, singh-the-code-book]
updated: 2026-09-09
---

# Weak Hashes and Preimage Attacks

Why a homemade "check the hash of the password" scheme falls apart the moment
the hash is not a *cryptographic* one — and how to exploit it. Recognising this
pattern turns a whole class of intro challenges into a two-minute solve.

## What makes a hash cryptographically secure

A cryptographic hash maps arbitrary input to a fixed-size digest and must hold
three properties:

- **Preimage resistance (one-way).** Given a digest `H`, it must be infeasible
  to find *any* input `m` with `hash(m) = H`. You can go message → hash, never
  hash → message.
- **Second-preimage resistance.** Given a specific `m1`, it must be infeasible
  to find a different `m2` with `hash(m2) = hash(m1)`.
- **Collision resistance.** It must be infeasible to find *any* two distinct
  inputs that hash to the same value.

Break any of these and the function is unsafe for security use.

## Why an additive checksum is not a hash

A checksum that sums the byte values of the input — `sum = Σ byteᵢ` — is fine
for catching accidental corruption, but fails every property above:

- **Order independence.** Addition is commutative, so `"CAT"` (67+65+84=216) and
  `"TAC"` (84+65+67=216) collide. Character order carries no weight.
- **Trivial collisions.** Add 1 to one byte and subtract 1 from another and the
  sum is unchanged (`"AZ"` → `"BY"`). You can generate matching inputs by hand.
- **No avalanche effect.** In a real hash, flipping one input bit flips about
  half the output bits. In a checksum, one change moves the result by a small,
  predictable amount — so you can *steer* the output to a target.

## The attack

Authentication checks usually compare hashes, not plaintext:

```
if hash(user_input) == target_hash:  ->  access granted
```

- **Preimage attack.** You know the `target_hash` and construct an input that
  produces it.
- **Collision attack.** You produce two distinct inputs with the same digest.

The key insight: **the program compares bytes, not meaning.** It has no idea
what the "real" password was. Any byte sequence that yields `target_hash`
satisfies the check — even obvious gibberish. Against a weak function, finding
such an input is cheap:

- Additive checksum → pick characters whose values add up to the target. If a
  printable ASCII code `c` divides the target `T`, then `(T / c)` copies of that
  character work. (Example: target 1729, `[` = 91, 1729/91 = 19 → nineteen `[`.)
  Otherwise use one filler character for the remainder.
- Broken cryptographic hashes (MD5, SHA-1) → documented collision techniques.

## Security lessons

- **A weak hash is not authentication.** Non-cryptographic functions (sums,
  CRC32) and broken ones (MD5, SHA-1) let an attacker engineer valid inputs in
  seconds. Real auth uses a strong hash and, for passwords, a slow salted one
  (bcrypt, scrypt, Argon2, PBKDF2).
- **Do not make the secret testable client-side.** A hardcoded expected hash
  hands the attacker a local target to brute-force or reverse.
- **Debug output is an attack surface.** Logging the expected value and the
  received value (`Hash incorrecto 448 != 1729`) gives away the exact target,
  removing all guesswork. Ship with debug off.

## Recognising this in a CTF

Reach for this pattern when a service or binary:

- prints a comparison of two numbers/digests (a leaked target), or
- accepts unlimited attempts and reacts to *how close* you are, or
- calls its check a "hash"/"checksum" but the values are small or change
  predictably with your input.

Then: recover the target, work out the function from a few probes, and forge a
preimage. You are not cracking the key — you are colliding with it.

## Seen in

- [Ping-Pong](../../course/class-01-intro/ping-pong.md) — networked "smart
  padlock" comparing an additive ASCII checksum against 1729; opened with a
  forged 19-byte preimage, target leaked via debug output.

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md); the hash
fundamentals draw on the security-foundations and cryptography titles:

- **Andress — *Foundations of Information Security*** — hashing, integrity, and
  the properties of cryptographic hash functions.
- **Grubb — *How Cybersecurity Really Works*** — hashing basics and why
  non-cryptographic functions are unsuitable for security.
- **Singh — *The Code Book*** — background on why order and diffusion matter in
  sound cryptographic design.
