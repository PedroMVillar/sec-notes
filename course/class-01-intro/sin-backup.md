---
platform: course
class: 1
target: sin-backup
category: reversing
difficulty: introductory
tags: [reversing, decompiler, password-check, xor, keygen, ghidra]
technique: reversing-decompiled-password-checks
date: 2026-09-09
---

# Sin Backup

**Class:** 1 (Intro) · **Category:** Reversing · **Level:** Introductory

The lab machine died and there was no backup. All that survived is a text file:
the output someone saved years ago after running the program through a
decompiler. It does not compile, it cannot run, and the names are
tool-generated. It is still enough — the accepted key is in there, just not
written out in one piece. That key is the flag.

This is the step [legado](legado.md) pointed at: when `strings` cannot help
because the key is *built and checked* rather than stored, you read the
decompiler output and reverse the logic.

## Reading the decompiled code

Two functions. The first walks the input until a null byte and returns the
count — it is `strlen`. The second, `check_password(input)`, is the target.
Stripped of the addresses, its logic is:

```c
uint8_t stored[0x15];
memcpy(&stored, "<20 bytes — redacted>", 0x15);   // transformed table, not the key

if (strlen(input) != strlen(stored))              // 1. length gate: must be 20
    return puts("Size don't match"), 0;

for (i = strlen(input); i > 0; i -= 1)            // 2. per-character check
    if (stored[i-1] != (((input[i-1]) - (i-1)) ^ 3))
        break;

if (i != 0) return 0;                             // any mismatch -> fail
return puts("Correct password"), 1;               // all matched -> success
```

The classic shape of a key check: a **length gate**, then a **transform loop**
comparing each processed input byte against a **stored table**. The condition
for position `p` (0-indexed) is:

```
stored[p] == ((input[p] - p) ^ 3)
```

## Reversing it

No guessing — solve for `input[p]`. XOR is its own inverse, and you undo the
steps in reverse order (undo the XOR, then undo the subtraction):

```
stored[p] = (input[p] - p) ^ 3
input[p]  = (stored[p] ^ 3) + p
```

So the accepted key is: for each byte of the stored table, XOR with 3, then add
its index.

## Recovering the key (keygen)

A three-line script turns the table into the password:

```python
stored = "<the 20 bytes from the memcpy>"   # redacted here on purpose
key = "".join(chr((ord(c) ^ 3) + p) for p, c in enumerate(stored))
print(key)
```

**Confirmation without a binary.** The machine is dead, so there is no program
to test against. Instead, re-apply the *forward* transform to the recovered key
and check it reproduces the stored table exactly — it does. That round-trip is
the proof the reversal is correct.

## Flag

```
FaMAF{ ...redacted... }
```

Redacted, and the stored table above with it — publishing both would hand over
the answer. Read in leetspeak the flag says *my first reverse*.

## Technique

Full, source-backed write-up:
[Reversing decompiled password checks](../../notes/reverse-engineering/reversing-decompiled-password-checks.md).

## Lessons learned

- Decompiler output does not run and its names are invented, but the **logic**
  is intact — that is all you need.
- Recognise the key-check shape: length gate → transform loop → table compare.
- To recover the key, invert the transform: reverse the operation order and use
  each operation's inverse (XOR undoes itself; add undoes subtract).
- An encoded key inside a binary is not protected — it is security through
  obscurity. The transform is right there to be inverted.
