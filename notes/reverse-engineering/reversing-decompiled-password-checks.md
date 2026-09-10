---
topic: reverse-engineering
tags: [decompiler, ghidra, ida, password-check, xor, keygen, static-analysis]
sources: [eagle-the-ghidra-book, yurichev-reverse-engineering-for-beginners, sikorski-practical-malware-analysis]
updated: 2026-09-09
---

# Reversing Decompiled Password Checks

The step after [static string analysis](static-string-analysis.md): when the
key is not stored as plaintext but *transformed and compared* at runtime,
`strings` gives you nothing. You read the decompiler's pseudo-C, recognise the
check, and invert the transform to recover the accepted key.

## What decompiler output is

A decompiler (Ghidra, IDA) turns machine code back into C-like pseudocode. It:

- **Does not compile.** Binaries drop macros, exact types, and struct layouts,
  so the tool emits best-guess casts, raw pointer arithmetic, and assembly
  artifacts a real compiler rejects.
- **Has invented names.** With symbols stripped, the tool labels by stack offset
  (`var_28`, `local_28`), argument position (`param_1`), or address
  (`FUN_00401200`). The names carry no meaning — you assign it.
- **Is still useful.** It hides register juggling and stack setup and shows the
  real control flow: `if`/`else`, loops, calls. That is enough to follow logic.

`strlen` often shows up as a small helper that walks a buffer to the null byte
and returns the count — recognise it by behaviour, not name.

## Recognising a key check

Password / serial validators share a shape in decompiled listings:

1. **Length gate.** `strlen(input)` compared to a fixed number; wrong length
   branches straight to failure. This also tells you the key's length for free.
2. **Transform loop.** Iterates the input; each byte is modified with `+`, `-`,
   `^` (XOR), or bit rotations, often folding in the index `i`.
3. **Table comparison.** Transformed bytes are checked against a hardcoded table
   (`.rodata`/`.data`) — via `memcmp`/`strcmp` or a byte-by-byte loop that
   `break`s on the first mismatch.
4. **Branch.** Success path prints "Correct"/sets a flag; failure path prints an
   error.

## Inverting the transform

If each position transforms as `stored = f(input, i)`, recover `input` by
undoing `f` — **reverse the operation order and apply each inverse**:

- **XOR is its own inverse:** `a ^ k ^ k == a`. Undo an XOR by XORing the same
  constant again.
- **Add/subtract undo each other.** If the code subtracted the index, add it
  back.

Worked example — the code computes `stored[i] = (input[i] - i) ^ 3`. Reverse it:

```
undo XOR:  t = stored[i] ^ 3
undo sub:  input[i] = t + i
```

So `input[i] = (stored[i] ^ 3) + i`.

## Writing a keygen

Turn the inversion into a few lines over the stored table:

```python
stored = "...bytes from the binary's table..."
key = "".join(chr((ord(c) ^ 3) + i) for i, c in enumerate(stored))
print(key)
```

**Confirming without the binary.** If the program cannot be run (dead disk,
server-only), re-apply the *forward* transform to your recovered key and check
it reproduces the stored table byte-for-byte. A clean round-trip is proof.

## Security lesson

- An encoded/obfuscated key inside a binary is **security through obscurity**.
  The transform that hides it also tells you exactly how to invert it.
- Local code runs on the attacker's hardware: it can be decompiled, scripted,
  emulated, or debugged to dump values in memory — and the conditional jump can
  simply be patched (`JNZ` → `NOP`) to skip the check entirely.
- Real authentication runs on a server and returns short-lived tokens; the
  client never holds the master key or the check.

## Related

- [Static string analysis](static-string-analysis.md) — the first thing to try;
  this note is what you do when it fails.

## Seen in

- [Sin Backup](../../course/class-01-intro/sin-backup.md) — decompiler output of
  a dead binary; recovered a 20-byte key by inverting a per-character
  `(input - index) ^ 3` transform.

## Sources

Grounded via NotebookLM in the [bibliography](../../books/README.md):

- **Eagle & Nance — *The Ghidra Book*** — reading decompiler pseudocode,
  auto-generated names, and navigating control flow.
- **Yurichev — *Reverse Engineering for Beginners*** — per-character check
  loops and inverting arithmetic/XOR transforms.
- **Sikorski & Honig — *Practical Malware Analysis*** — recognising encoding
  routines and scripting their inverse to recover values.
