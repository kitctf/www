---
layout: page
title: Tools
permalink: /tools/
---

In general CTFs aren't about the right tools but about skill. Nontheless you'll usually need a couple of tools to get the job done.
Here we've created a list of useful tools, not only for CTFs but for infosec in general.
You can also find some useful things on our [github page](https://github.com/kitctf) ;)

### Binary Exploitation
Ship with metasploit:

- pattern_create + pattern_offset - generate a pattern to quickly find relevant offsets
- msfpayload - generate payloads for various platforms
- msfencode - encode payloads to avoid special characters (e.g. 0x00, 0x0a, ..)
- metasm_shell - quickly assembly instructions

Standalone: 

- ROPGadget - find ROP gadgets in various binaries
- libformatstr - python lib to simplify format string exploitation

### Reversing
- Hopper
- radare2
- IDA Pro (+ Decompiler)
- metasm
- gdb
- x64dbg
- OllyDbg
- Immunity Debugger

- frida: http://www.frida.re/

- Various python tools: http://pythonarsenal.erpscan.com/

- strace + ltrace - monitor syscalls and library calls
- RegMon - monitor changes to the registry
- FileMon - monitor changes to the file system

### Web
- Burp Suite - multipurpose web security toolkit
- THC Hydra - brute force login credentials for various services
- sqlmap - automated database takeover tool

### Crypto
- HashPump - perform length extension attacks on various hash algorithms
- fastcoll - produce different files with identical md5 hashes
- oclHashcat - probably the fastest hash cracker out there

- tesseract
- cuneiform

### Other
- aircrack-ng - wireless attacking suite
- vagrant - manage virtual machines
- bochs - x86 PC emulator

### Online
- https://anubis.iseclab.org/ - online malware analysis
