# Bibliography

The reading list behind these notes: 37 books across 11 areas of offensive
security, ordered roughly from foundations to specialisation.

> **The PDFs are not in this repository.** They are copyrighted works and stay
> on local disk only — `.gitignore` excludes every ebook format. What is
> tracked here is the index and the directory layout, so the reading path is
> public even though the material is not. Every title below is commercially
> available; buy the ones you intend to read.

**Level** — `Intro` assumes no prior exposure, `Intermediate` assumes comfort
with a shell and one programming language, `Advanced` assumes working
knowledge of the domain. `Reference` is lookup material, not linear reading.

**Status** — `Queued` · `Reading` · `Read` · `Skimmed`.

---

## 01 · Foundations

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Foundations of Information Security | Jason Andress | 2019 | Intro | Queued |
| How Cybersecurity Really Works | Sam Grubb | 2021 | Intro | Queued |
| Security from Zero | Eric Higgins | 2020 | Intro | Queued |
| The Complete Cyber Security Course, Vol. 1: Hackers Exposed | Nathan House | 2017 | Intro | Queued |
| Linux Basics for Hackers | OccupyTheWeb | 2018 | Intro | Queued |

## 02 · Cryptography

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| The Code Book | Simon Singh | 1999 | Intro | Queued |

> Thin on purpose — crypto is a standing CTF category and this shelf needs
> more than a history of ciphers. *Serious Cryptography* (Aumasson) and the
> *Cryptopals* challenge set are the obvious next additions.

## 03 · Privacy and OPSEC

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| The Art of Invisibility | Kevin Mitnick, Robert Vamosi | 2017 | Intro | Queued |
| Hacklog, Vol. 1: Anonymity | Stefano Novelli, Marco S. Doria | 2019 | Intro | Queued |

## 04 · Web Security

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Grokking Web Application Security | Malcolm McDonald | 2024 | Intermediate | Queued |
| Hacking APIs | Corey J. Ball | 2022 | Intermediate | Queued |
| Real-World Bug Hunting | Peter Yaworski | 2019 | Intermediate | Queued |
| Web Hacking 101 | Peter Yaworski | 2018 | Intro | Queued |
| Bug Bounty Playbook | Ghostlulz | 2020 | Intermediate | Queued |
| XSS Cheat Sheet, 2020 Edition | Rodolfo Assis | 2020 | Reference | Queued |
| Hacklog, Vol. 2: Web Hacking | Stefano Novelli, Marco Silvestri | 2020 | Intermediate | Queued |

## 05 · Binary Exploitation

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Hacking: The Art of Exploitation, 2nd ed. | Jon Erickson | 2008 | Intermediate | Queued |
| Game Hacking | Nick Cano | 2016 | Advanced | Queued |

> The weakest shelf relative to how much `pwn` weighs in CTFs. Erickson
> predates modern mitigations (full ASLR, PIE, CET), so it explains the
> foundations but not the current fight. Worth adding a heap-exploitation and
> a modern-mitigation text.

## 06 · Reverse Engineering

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Reverse Engineering for Beginners | Dennis Yurichev | 2016 | Intro | Queued |
| The Ghidra Book | Chris Eagle, Kara Nance | 2020 | Intermediate | Queued |
| The IDA Pro Book, 2nd ed. | Chris Eagle | 2011 | Intermediate | Queued |
| x86 Software Reverse-Engineering, Cracking, and Counter-Measures | Stephanie Domas, Christopher Domas | 2024 | Advanced | Queued |
| Blue Fox: Arm Assembly Internals & Reverse Engineering | Maria Markstedter | 2023 | Advanced | Queued |

## 07 · Malware Analysis

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Practical Malware Analysis | Michael Sikorski, Andrew Honig | 2012 | Intermediate | Queued |
| Evasive Malware | Kyle Cucci | 2024 | Advanced | Queued |
| Malware Data Science | Joshua Saxe, Hillary Sanders | 2018 | Advanced | Queued |
| Rootkits: Subverting the Windows Kernel | Greg Hoglund, James Butler | 2005 | Advanced | Queued |
| The Android Malware Handbook | Qian Han, Salvador Mandujano et al. | 2023 | Advanced | Queued |

## 08 · OS Internals

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Windows Security Internals | James Forshaw | 2024 | Advanced | Queued |
| Android Security Internals | Nikolay Elenkov | 2014 | Advanced | Queued |

## 09 · Network and Pentesting

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Penetration Testing: A Hands-On Introduction to Hacking | Georgia Weidman | 2014 | Intro | Queued |
| Metasploit: The Penetration Tester's Guide | David Kennedy, Jim O'Gorman, Devon Kearns, Mati Aharoni | 2011 | Intermediate | Queued |

## 10 · Hardware and IoT

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| The Car Hacker's Handbook | Craig Smith | 2016 | Advanced | Queued |

## 11 · Defense and Strategy

| Title | Author | Year | Level | Status |
|---|---|---|---|---|
| Cyberjutsu: Cybersecurity for the Modern Ninja | Ben McCarty | 2021 | Intermediate | Queued |
| Building a Cyber Risk Management Program | Brian Allen, Brandon Bapst, Terry Allan Hicks | 2023 | Intermediate | Queued |
| Building Secure and Reliable Systems | Heather Adkins, Betsy Beyer, Paul Blankinship et al. | 2020 | Intermediate | Queued |
| Software Supply Chain Security | Cassie Crossley | 2024 | Intermediate | Queued |
| Offensive Countermeasures: The Art of Active Defense | John Strand et al. | 2019 | Intermediate | Queued |

---

## Conventions

Files are named `lastname-title-in-kebab-case[-Ned].pdf` — no spaces, commas
or typographic quotes, so paths survive scripts and shells. The full title,
author and year live in this index rather than in the filename.

`Year` is the publication year of the edition on the shelf, not the PDF's
build date.
