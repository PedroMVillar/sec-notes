---
platform: course
class: 1
target: legado
category: reversing
difficulty: introductory
os: linux
tags: [reversing, static-analysis, strings, elf, password-check]
technique: static-string-analysis
date: 2026-09-09
---

# legado

**Class:** 1 (Intro) · **Category:** Reversing · **Level:** Introductory

An old lab program that asks for a password and prints "access granted" only if
you get it right. No source code — just the executable. The password is the
flag. A textbook first reversing challenge: it is solved by *reading* the
binary, not by exploiting it.

## Recon — what am I dealing with?

Before opening anything heavy, identify the file:

```bash
file legado
# legado: ELF 64-bit LSB executable, x86-64, ... statically linked,
#         ... not stripped
```

Three things mattered here:

- **ELF x86-64** → a Linux binary. Run it under Linux or WSL, not Windows.
- **statically linked** → it carries its libraries inside; nothing external to
  resolve.
- **not stripped** → the developer's symbol names (function and variable names)
  are still present. This is the "easy target" signal: if `strings` had not
  been enough, a disassembler would have shown readable function names like
  `main` / `check_password`.

## Finding the password

The cheapest move on any password checker is to look for readable text inside
the binary. A hardcoded password is stored verbatim in the file unless the
author encrypted it — most do not. `strings` prints every printable text
sequence in the file; `grep` narrows thousands of lines down to the promising
ones:

```bash
strings -n 6 legado | grep -iE "pass|clave|flag|correct|denied|acceso|\{.*\}"
```

The flag came out on the **first line**. The surrounding strings confirmed the
program's shape — an access-check banner, `Contraseña`, `Acceso denegado.`,
`Acceso concedido.` — so the candidate was clearly the password it compares
against.

## Confirmation

A candidate string is not proof. Feed it to the program and check the verdict —
strings can be decoys, so confirming that *this* one opens the door is part of
the method:

```bash
printf 'THE_CANDIDATE\n' | ./legado
# ========================================
#   Sistema de acceso - Laboratorio 7
# ...
# Contraseña: Acceso concedido.
```

`Acceso concedido.` → confirmed.

## Flag

```
FaMAF{ ...redacted... }
```

Redacted deliberately — see [course notes](../README.md). The flag itself, read in
leetspeak, spelled out the lesson: *strings travel with the binary*.

## Technique

Full, source-backed write-up of the method:
[Static string analysis](../../notes/reverse-engineering/static-string-analysis.md).

The 30-second reflex this challenge drills:

1. `file <binary>` — architecture, static/dynamic, stripped or not.
2. `strings <binary>` — is the answer sitting in plaintext? (it was)
3. Only if not: open **Ghidra** and read the comparison logic.

We reached step 2. Step 3 is for the day the author hides the password
properly — encrypted, packed, or built at runtime — and that is the next note
to write.

## Lessons learned

- A secret that ships to the client is not a secret. Storing a password inside
  a distributed binary is security through obscurity, and `strings` defeats it
  in seconds.
- "not stripped" is a gift — always check it first with `file`.
- Always confirm a candidate against the real program before submitting.
