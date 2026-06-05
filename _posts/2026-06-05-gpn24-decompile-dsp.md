---
layout: post
title: "Talk: How to decompile a DSP architecture"
categories: learning
authors:
  - Alkalem
---

This talk was held at [GPN24](https://entropia.de/GPN24), running from June 04, 2026 to June 07, 2026 at ZKM and HfG in Karlsruhe.

- The slides are here: [Slides](/talks/2026-06-05-gpn24-decompile-dsp/decompiler-slides.pdf)
- The link to the recording will be added here once available

## Introduction

About a year ago, a friend gave me a binary to reverse engineer to playtest for a CTF. As the architecture lacked the necessary tooling, I started developing a decompiler plugin. What started as a small side project for learning, has been a part of my life over the last year. The project grew as my understanding of the architecture deepened, and it took several API updates to finally work. Join me on a journey into the rabbit hole of architecture features and how the decompiler works.

This talk will discuss the TMS320C6x Digital Signal Processor (DSP) family and use Binary Ninja as the decompiler.

## Description

Decompilers take a compiled executable and aim to recover higher-level structures close to the original source code. As the name implies, they try to reverse the work of a compiler. This process is structured into many analysis steps of which most are independent of the architecture. However, a decompiler needs to support an architecture to get the required information for its analysis. Using a decompilers API, an architecture plugin can extend this support to any architecture (in theory).

In this talk, I will share my experiences from building such a plugin, and talk about occurring problems and solutions. You will learn the core tasks of an architecture plugin and how to fulfill them. The talk will discuss the TMS320C6x architecture family from high-level overview to opcode details. Both parts are combined to arrive at a plugin that can handle DSP architecture features. Along the way, we will discover limitations of APIs, compiler quirks and specification errors.

The talk uses Binary Ninja and its API. Some parts are specific to this tool, many concepts (and sadly problems) apply to other decompilers as well.
