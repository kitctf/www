---
layout: post
title: "Talk: Attacking and Defending GitHub Actions - Is it safe now?"
categories: learning
authors:
  - intrigus
---

You know GitHub Actions, these small building blocks that make your dev life easier… But they can also get you pwned in no time, if you are not careful.

The talk covers:
* the basic structure of a GitHub Actions workflow.
* the permission model of GitHub Actions.
* insecure templating and executing user-controlled code in privileged workflows.
* safer checkout defaults in `actions/checkout@v7`.
* cache poisoning in workflows, including a case study on tempo/tempo-xyz.
* new defenses: workflow execution protections and planned cache hardening.

The slides can be found [here](/talks/2026-07-02-attacking-and-defending-github-actions-is-it-safe-now/attacking-and-defending-github-actions-is-it-safe-now.pdf). The talk was held on 2026-07-02.
