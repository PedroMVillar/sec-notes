---
topic: reverse-engineering
tags: [static-analysis, strings, elf, pe, triage, reversing]
sources: [sikorski-practical-malware-analysis, yurichev-reverse-engineering-for-beginners, eagle-the-ghidra-book, domas-x86-software-reverse-engineering]
updated: 2026-09-09
---

# Static String Analysis

Reading the human-readable text embedded in a compiled program **without
running it**, to understand what it does and often to recover secrets outright.
It is the fastest, cheapest first move in reverse engineering, and a
surprising number of introductory challenges fall to it alone.

## Why the strings are in there

When source code contains a literal — `"Enter password:"`, a URL, an API key —
the compiler must store those bytes inside the binary so the code can reference
their address at runtime. In C/C++ they are raw character bytes (1 byte per
ASCII char, 2 for UTF-16), terminated by a null byte `0x00`. The compiler files
them by role:

| Section | Holds | Example |
|---|---|---|
| `.rodata` (ELF) / `.rdata` (PE) | Read-only constants | A hardcoded password |
| `.data` | Initialised globals that can change | A mutable config default |
| `.rsrc` (PE) | UI strings, icons, dialogs | Windows resource strings |

A constant password lives in `.rodata` — read-only, so the program cannot
overwrite it, and plainly readable to anyone with the file.

## How `strings` works, and why it is step one

`strings` scans the raw bytes of a file — no execution, no parsing — and prints
every run of printable characters at least N long (default 3–4; use `-n 6` to
cut noise). In seconds it surfaces high-value indicators: URLs, IP addresses,
file paths, registry keys, compiler tags (`GCC: (Ubuntu ...)`), and library
function names.

```bash
strings -n 6 target | grep -iE "pass|key|flag|http|token|denied|\{.*\}"
```

Beyond recovering secrets, a located string is a **navigation handle**: in
Ghidra or IDA you jump to the string and follow its cross-references (XREFs)
straight to the function that uses it — e.g. find `"Enter Password"`, follow the
XREF, and you are standing in the check routine.

## Stripped vs. not stripped

`file target` tells you which, and it changes everything:

- **Not stripped** — the symbol table survives: original function names
  (`main`, `check_password`), globals, sometimes line numbers. Tools show
  readable labels; logic is easy to follow.
- **Stripped** (`strip`, or `gcc -s`) — those names are gone; the disassembler
  invents placeholders like `FUN_00101241`, `DAT_00301018`, and you deduce each
  function's purpose by hand. Same behaviour, smaller file, harder to read.
- Either way, **imported library functions stay visible** (`puts`, `strcmp`,
  `LoadLibraryA`) — the OS loader needs their names to resolve at startup. So
  even a stripped binary gives you anchors.

## When it fails, and what to reach for

`strings` is fast but blind to context. It breaks down when:

1. **Junk / false positives** — random opcode bytes that happen to be
   printable, and strings that exist but are never executed.
2. **Encrypted / obfuscated strings** — decrypted by a routine in memory right
   before use, so nothing readable sits on disk.
3. **Packed binaries** (UPX, tElock…) — whole `.text`/`.data` compressed; you
   see only a small unpacking stub and a few loader APIs.
4. **Runtime-constructed strings** — built on the stack byte by byte
   (`mov byte ptr, 'e'`) or via `sprintf`, so the characters are scattered
   through instructions, not stored in sequence.

The common thread: the secret must still become plaintext **in RAM** for the
CPU to use it. So when static analysis fails, move to dynamic:

- **Debuggers** (GDB, x64dbg) — breakpoint right after the decrypt/unpack
  routine and read the plaintext straight from memory.
- **Disassemblers / decompilers** (Ghidra, IDA) — read the decryption loop,
  or script/emulate it to decode the strings.
- **Unpackers** — restore a packed binary before static analysis.

## Security lesson

Storing a secret in a client-side binary is fundamentally unsafe:

- Once distributed, the attacker has full control to inspect, disassemble,
  debug and dump memory.
- Hiding a credential in an executable is security through obscurity — `strings`
  extracts it in seconds.
- Encryption or packing only raises the cost: the value is decrypted into RAM
  eventually, where a debugger captures it.
- The fix is architectural: keep secrets and auth logic on a **server**. The
  client sends credentials and receives short-lived tokens; it never holds the
  master secret.

## Seen in

- [legado](../../course/class-01-intro/legado.md) — introductory course challenge; hardcoded
  password recovered from `.rodata` with `strings`.

## Sources

Grounded in these titles from the [bibliography](../../books/README.md):

- **Sikorski & Honig — *Practical Malware Analysis*** — `strings` as a primary
  triage step; string encryption, packing, and stack-constructed strings; using
  a debugger to recover decrypted strings from memory.
- **Yurichev — *Reverse Engineering for Beginners*** — how string literals are
  laid out in binary sections; stripped vs. unstripped symbols.
- **Eagle & Nance — *The Ghidra Book*** — navigating from a string to its code
  via cross-references; placeholder naming in stripped binaries.
- **Domas — *x86 Software Reverse-Engineering*** — byte-level layout of strings
  and instructions on x86.
