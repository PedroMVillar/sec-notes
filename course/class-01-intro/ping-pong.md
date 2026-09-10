---
platform: course
class: 1
target: ping-pong
category: cryptography
difficulty: introductory
access: "nc <course-host> 1338"
tags: [crypto, weak-hash, checksum, preimage, collision, network, debug-leak]
technique: weak-hash-preimage
date: 2026-09-09
---

# Ping-Pong

**Class:** 1 (Intro) · **Category:** Crypto / weak hash · **Level:** Introductory

A homemade "smart padlock" (built on a microcontroller over a weekend) guarding
a store room. Nobody has the original key, but the lock answers over the network
as many times as you like — and it was shipped with its debug output still on.
You reach it with `nc <course-host> 1338`.

## Recon — talk to the service

First move on any network service: connect and read what it says. Don't guess,
observe.

```bash
nc <course-host> 1338
```

The banner and a probe input revealed the whole mechanism:

```
   candado v0.3  ---  build de prueba
Depósito 4. Estado: CERRADO.
[debug] salida de diagnóstico activada
clave> test
[debug] Hash incorrecto 448 != 1729
ACCESO DENEGADO
```

That `[debug]` line is the entire challenge. A finished product would say only
"denied"; this one leaks two numbers: **the hash of my input** and **the target
hash it wants (1729)**.

## Analysis — what is the hash?

Probing a few inputs (one connection each) exposed the function:

| Input | Reported hash | Sum of ASCII bytes |
|---|---|---|
| `test` | 448 | 116+101+115+116 = 448 |
| `AAAA` | 260 | 65×4 = 260 |
| `AB` | 131 | 65+66 = 131 |
| `BA` | 131 | 66+65 = 131 |

Two conclusions:

- The "hash" is just the **sum of the ASCII byte values** of the input.
- `AB` and `BA` give the same result → **order does not matter**. Addition is
  commutative, so the function is riddled with collisions.

This is a checksum, not a cryptographic hash. See the technique note for *why*
that distinction is the whole vulnerability.

## Exploitation — forge a preimage

We don't need the original key. We need **any** input whose bytes sum to 1729
(a *preimage*). Because collisions are trivial, one is easy to build.

1729 = 7 × 13 × 19. Of those factors, **91** is a printable ASCII code
(`chr(91)` = `[`), and 1729 ÷ 91 = 19 exactly. So **19 `[` characters sum to
1729**:

```bash
python3 -c "print('['*19)" | nc <course-host> 1338
```

Result:

```
clave> [debug] Hash correcto 1729 == 1729
ACCESO CONCEDIDO
```

## Flag

```
FaMAF{ ...redacted... }
```

Redacted deliberately — see [course notes](../README.md). Read in leetspeak the
flag stated the lesson outright: *a checksum is not a password*.

## Technique

Full, source-backed write-up:
[Weak hashes and preimage attacks](../../notes/cryptography/weak-hash-preimage.md).

## Lessons learned

- **Comparing a weak hash is not authentication.** A sum (or CRC, or MD5) is
  built for speed and error-detection, not to resist an adversary.
- **Collisions = you never need the real secret.** Any input reaching the
  target hash opens the door; the program only compares bytes, not intent.
- **Debug output is an attack surface.** Leaking the target value and your
  input's value handed us everything needed to forge a preimage in one shot.
- On a network service, the first step is always to *connect and observe*
  before sending anything clever.
