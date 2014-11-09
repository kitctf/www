---
layout: page
title: First Steps
permalink: /first-steps/
---

TODO


## Glossar
Hier ein paar Begriffe, die am Anfang hilfreich sein können.

### Flag
Sie zu finden ist das ziel. Das Layout ist meist angegeben. Beispiel:

- `flag{das_ist_die_flag}`
- `flag{75c3a63d546d0e7739ff0552c55a3e39e3155d68}` ein Hashwert fester Länge

Man reicht dann entweder nur `das_ist_die_flag` oder `flag{das_ist_die_flag}` ein.

### nc/netcat/telnet/ssh
Meist ist eine Verbindung mit angegeben `nc 1.2.3.4 1337`. Unter Linux kann man das so in die shell eingeben und erhält dann eine meist ASCII basierte Socketverbindung zum Server. Das Selbe gilt für netcat.

Bei telnet wird `telnet` meist nicht explizit mit angegeben sondern nur eine IP und ein Port (Bsp HTTP: `telnet 1.2.3.4 http` oder `telnet 1.2.3.4 80`)

Falls es eine SSH verbindung ist steht das dabei und sieht irgendwie so aus: `ssh nutzer@1.2.3.4`

### Writeup
Sind Lösungen einzelner Aufgaben vergangener CTFs. Diese sind i.d.R. in englisch und mal mehr, mal weniger ausführlich.
