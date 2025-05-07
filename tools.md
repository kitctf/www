---
layout: page
title: The Tools We Built
permalink: /tools/
---

Here we want to present some of the tools that KITCTF members have developed
to help us solve CTF challenges more efficiently.

## [dbgtools](https://github.com/two-heart/dbgtools)

dbgtools is a GDB and pwndbg extension. It aims to remove friction and repetition from binary exploitation and reverse engineering.

Main use cases include:

* Scripting gdb from pwntools
* Flexible tracing of a whole binary execution with gdb
* Various commands that make common exploitation steps quicker


## [libc-database](https://github.com/niklasb/libc-database)

Often in binary exploitation scenarios on Linux, we do not have enough information
about the target system to figure out the precise version of the *glibc* standard
C library that it uses. However, we want to be able to call arbitrary functions
from that library, say the function `system()`.

Let's say we can leak a function address from the libc, for example by dumping a
[GOT](http://bottomupcs.sourceforge.net/csbu/x3824.htm) entry. We're in luck now,
because randomization under Linux works on a page level, so the least
significant 12 bits of the function address are not randomized. The
[*libc-database*](https://github.com/niklasb/libc-database) allows us to look
up the different *glibc* versions that have the given function at an address
that shares the given 12 least significant bits.

### Example

Say we were able by using some bug in the target binary that the `printf`
function has address `0x7fcc67a16400`. Let's run *libc-database*'s `find`
utility:

    $ ./find printf 0x7fcc67a16400
    ubuntu-trusty-amd64-libc6 (id libc6_2.19-0ubuntu6.6_amd64)
    archive-eglibc (id libc6-i386_2.11.1-0ubuntu7_amd64)

The output tells us that there are at least two common *glibc* versions
(from Ubuntu) with the `printf` function at address `?????????400`. In this case it is
clear that the former is the correct one, because the latter is 32-bit. In
other cases it might be necessary to dump more entries and cross-reference or
just try all the possible options.

Please note that at this time *libc-database* only indexes the Ubuntu versions
of *glibc*, because those are predominant in CTFs. Pull requests for other
distributions are more than welcome :)

The `find` utility outputs an identifier, in this case the string
`libc6_2.19-0ubuntu6.6_amd64`, that can be used to reference the libc version.
We can now use this to dump the offsets of important functions and strings in
the binary:

    $ ./dump libc6_2.19-0ubuntu6.6_amd64
    offset___libc_start_main_ret = 0x21ec5
    offset_system = 0x0000000000046640
    offset_dup2 = 0x00000000000ebfe0
    offset_read = 0x00000000000eb800
    offset_write = 0x00000000000eb860
    offset_str_bin_sh = 0x17ccdb

Those can be pasted and used in your exploit script. `offset_str_bin_sh` is the
offset of the string `"/bin/sh"` in the libc binary.
`offset___libc_start_main_ret` is the offset of the instruction after the
`call` to `main`, which can be rather useful if you can leak stack memory
including that address. There's commands to update the database yourself and to
add custom libc binaries, which you can read about in the
[README](https://github.com/niklasb/libc-database/blob/master/README.md) file.

## [dump-seccomp](https://github.com/niklasb/dump-seccomp)

From [Wikipedia](https://en.wikipedia.org/wiki/Seccomp):

> seccomp (short for secure computing mode) is a computer security facility
> that provides an application sandboxing mechanism in the Linux kernel [...]

Usually the [*seccomp-bpf*](https://en.wikipedia.org/wiki/Seccomp#seccomp-bpf)
extension is used to define seccomp rules (i.e. rules to determine which
syscalls the program is allowed to perform). Basically the [Berkeley Packet
Filter](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter) is a virtual
machine with a rather restricted instruction set that can be used to inspect
memory (such as network packets), extract information and make a decision based
on the content of the memory. For *seccomp-bpf*, a BPF program is registered
that will inspect a `struct seccomp_data`:

    struct seccomp_data {
        int nr;                    // syscall number
        __u32 arch;                // system architecture
        __u64 instruction_pointer; // location of the syscall instruction
        __u64 args[6];             // syscall arguments
    };

and returns either `SECCOMP_RET_ALLOW`, `SECCOMP_RET_KILL` or
`SECCOMP_RET_TRAP`, resulting in the syscall being allowed, the process being
killed immediately or a `SIGSYS` being sent to the process, respectively.

The filter is registered via a call to `prctl(PR_SET_SECCOMP,
SECCOMP_MODE_FILTER, bpf_program)`. The Chromium project includes
[a small example of a program that restricts itself in this manner](https://github.com/niklasb/dump-seccomp/blob/master/example/example.c).

For more information about seccomp internals and how the BPF bytecode can be dumped see [this writeup](https://kitctf.de/writeups/32c3ctf/ranger/).

[*dump-seccomp*](https://github.com/niklasb/dump-seccomp) is a simple GDB
plugin that hooks calls to `prctl`, inspects the arguments and for each
registered seccomp filter, dumps a rudimentary disassembly of the BPF program
associated with it.

### Example

After getting the plugin, we will have to build the `bpf_dbg` program via
a call to `make`. Then we can compile the example and use the plugin to dump
the filter:

    $ git clone https://github.com/niklasb/dump-seccomp/
    $ cd dump-seccomp
    $ make
    $ cd example
    $ make
    $ cd ..
    $ gdb example/example64 -ex 'source gdbinit.py' -ex run

You might need to interrupt GDB using Ctrl+C after you think all the relevant
`prctl` calls have happened.

The plugin will output all the information, but interleaved with the
normal GDB output. You can see the pure plugin output by inspecting the file
`seccomp.log` afterwards:

    Using architecture elf64-x86-64
    prctl(PR_SET_NO_NEW_PRIVS)
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, ...)
      fprog @ 00007fffffffdab0
      15 blocks @ 00007fffffffdac0
      Disassembly:
         l0:	ld [4]
         l1:	jeq #0xc000003e, l3, l2
         l2:	ret #0
         l3:	ld [0]
         l4:	jeq #0xf, l5, l6
         l5:	ret #0x7fff0000
         l6:	jeq #0xe7, l7, l8
         l7:	ret #0x7fff0000
         l8:	jeq #0x3c, l9, l10
         l9:	ret #0x7fff0000
         l10:	jeq #0, l11, l12
         l11:	ret #0x7fff0000
         l12:	jeq #0x1, l13, l14
         l13:	ret #0x7fff0000
         l14:	ret #0

In order to understand the assembly syntax, you can consult the
[documentation for the *bpfc* compiler](http://man7.org/linux/man-pages/man8/bpfc.8.htm).

## Other tools and libraries

#### [sqli.py](https://github.com/niklasb/ctf-tools/blob/master/pwnlib/sqli.py)

A small library to perform blind SQL injection. If you wonder why you might not
always want to use [*sqlmap*](http://sqlmap.org/) for that, [just look at the amount of parameters
needed](https://github.com/niklasb/ctf-tools/blob/master/tools.md) to make it
work even for a very simple case. *sqli.py* is a simple Python module that does
the work too, but with a very simple design. You just provide a function that
evaluates a boolean SQL expression (possibly on the remote end via some
injection vulnerability), and it allows you to "upgrade" that to
a function that can evaluate numbers and strings. It also works in parallel for
maximum performance.

#### [rsa.sage](https://github.com/niklasb/ctf-tools/blob/master/rsa.sage)

Implementations of various attacks on RSA in
[SAGE](https://github.com/niklasb/ctf-tools/blob/master/rsa.sage).

#### [saelo's boxes](https://github.com/saelo/boxes)

A collection of [Vagrantfiles](https://www.vagrantup.com/) for quickly creating new virtual machines.
In particular, the [ctfbox](https://github.com/saelo/boxes/tree/master/ctfbox) is a box that is equipped
with many tools you might need during a CTF, such as GDB with the pwndbg plugin, strace, checksec, angr,
ROPgadget, PIN, ... Use `vagrant up` to start the VM and then `vagrant ssh` to log into the machine and start the pwnage.

#### [saelo's ctfcode collection](https://github.com/saelo/ctfcode)

Contains a great [exploit template](https://github.com/saelo/ctfcode/blob/master/pwn.py) with very nice
debugging features and various Python modules for specific CTF-related tasks.

There's also a [mini-libc](https://github.com/saelo/ctfcode/tree/master/LibC) which might come in handy for some kernel exploitation.

Gramarye has a [modified version](https://github.com/Gram21/ctfcode) for Python 2 based on [pwntools](https://github.com/Gallopsled/pwntools/).

#### [niklasb's tools.py](https://github.com/niklasb/ctf-tools/blob/master/tools.py)

A wild collection of useful utilities wrapped into a Python module. Wraps
assemblers for x86 and x86_64 and defines a lot of shellcode, including
a mini-server that can run inside a target binary and run read/write/execute
commands provided by the client. The latter can be useful for sandbox escapes.

There's also the classical [De Bruijn pattern
generator](https://github.com/niklasb/ctf-tools/blob/master/pattern.py).
