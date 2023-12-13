---
layout: post
title: "Talk: Frida Game Hacking"
categories: learning
author: mawalu
---

CTF challenges are usually well-behaved programs. But what do you do in more complex cases such as games, messenger applications (e.g. e2e encryption) or mobile applications (e.g. certificate pinning)?
Frida to the rescue!

The talk covers:
* how the frida architecture works.
* how to ignore certificate errors in mobile applications.
* a live demo on how to use frida to solve a game hacking challenge from an internal CTF.

The slides can be found [here](/talks/2023-12-14-frida-game-hacking/_game__hacking_with_frida.re.pdf) and the code of the live demo [here](/talks/2023-12-14-frida-game-hacking/index.ts).

The demo project has been set up like this:
```shell
sudo sysctl kernel.yama.ptrace_scope=0
pip install frida-tools
frida-create -t agent
npm i
npm run watch
frida -l _agent.js craft # game has to already run
```
The workshop was held on 2023-12-07.
