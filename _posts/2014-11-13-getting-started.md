---
layout: post
title: "Getting Started with CTF"
categories: learning
author: saelo
permalink: /getting-started/
---

We've created a small guide to get you started with CTF and more or less infosec in general. There are a few selected resources for each of the major CTF disciplines that should help you get up to speed in those. Also feel free to check out our other resource pages.

## Prerequisites

Basic Linux/Unix skills and some knowledge of programming should suffice to begin with.

## CTF in general

Probably the best way to get started with CTF is by reading through the [CTF Field Guide](https://trailofbits.github.io/ctf/), so go there first. Additionally there is also the following [blog post on how to get started with CTF](http://www.endgame.com/blog/how-to-get-started-in-ctf.html).

Other than that you'll usually learn a lot from writeups for CTF challenges (especially for ones you tried but couldn't solve). A writeup is just a guide walking you through the solution for a challenge. There is a [CTF writeup repository on github](https://github.com/ctfs/write-ups) that contains a lot of them. You'll also find writeups for the corresponding CTFs on [ctftime.org](https://ctftime.org/).

If you want to practice a bit (and you definitely should!) you can always take a look at previous CTF challenges [here](http://repo.shell-storm.org/CTF/) or the [overthewire wargames](http://overthewire.org/wargames/), but first check out the following section.

You should also make yourself familiar with [ctftime.org](https://ctftime.org/). The site keeps a global team rating for all CTFs and upcoming events will be announced there. You'll also find some other useful things around the site.

## How to get started in...

### Binary Exploitation

Personally I can strongly recommend the book ["Hacking - The Art of Exploitation"](http://www.nostarch.com/hacking2.htm).
There is also the following extensive tutorial on exploitation: [A Journey into Exploitation](http://myne-us.blogspot.de/2010/08/from-0x90-to-0x4c454554-journey-into.html).

For a nice overview on memory corruption bugs and exploitation see this white paper: [History of Memory Corruption Attacks (pdf)](https://media.blackhat.com/bh-us-10/whitepapers/Meer/BlackHat-USA-2010-Meer-History-of-Memory-Corruption-Attacks-wp.pdf).
That should get you up to speed on memory corruption bugs so you can recognize these vulns in the challenges and then do more research on them if needed.

To develop some more practical skills you can take a look at the [microcorruption](https://microcorruption.com) game. It's a browser based exploitation course guiding you through memory corruption exploitation on an embedded platform. It's designed for beginners but you will need to read up on the topics on your own.\\
Also, you can give the [exploit-excercises](https://exploit-exercises.com/) or the [overthewire wargames](http://overthewire.org/wargames/) mentioned above a try.

### Cryptography

The [cryptopals](http://cryptopals.com/) challenges are a nice set of exercises that guide you through modern cryptography and how to break it. You'll also be doing quite a lot of programming throughout the course.

### Web Security

The [Web Application Hackers Handbook](http://mdsec.net/wahh/) is basically the bible of web security. It will take some time reading through the book but it's definitely worth it.

You can also take a look at the following online challenges/courses for learning some web security:

- [Web Wargames](http://overthewire.org/wargames/natas/)
- [SQLi Challenges](http://www.zixem.altervista.org/SQLi/)
- [XSS Game](https://xss-game.appspot.com/)

Moreover there is the [Open Web Application Security Project](https://www.owasp.org) which also has some nice resources on web security.

### Reversing

To get started with reversing you'll probably want make yourself familiar with some assembly first. There are a lot of guides on that topic out there, just pick one and write a HelloWorld Linux program in assembly.

After that a good idea is to grab a disassembler (see our tools page [here](/tools)) and compile some C code. Afterwards load the binary into your disassembler of choice to see what the compiler generated. This will give you a good feeling for assembly and help you recognize code patterns and functions in disassembled binaries.
You can also take a look at some crackmes (for example from [here](http://www.crackmes.de/)) to get some hands-on experience.

Moreover I can recommend the books ["Reversing - Secrets of Reverse Engineering"](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-0764574817.html) and (if you already have some reversing skills) ["Practical Reverse Engineering"](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-1118787315,subjectCd-CSJ0.html).

### Coding

While not really a core CTF discipline some good coding skills will definitely proof useful (not only for CTF obviously). There are some nice sites to practice on out there, for example [talentbuddy](http://www.talentbuddy.co/) or [hackerrank](https://www.hackerrank.com/).\\
Also, there are some websites organizing regular coding contests like the [Google Code Jam](https://code.google.com/codejam/), [topcoder](https://www.topcoder.com) or [codeforces](http://codeforces.com/).
