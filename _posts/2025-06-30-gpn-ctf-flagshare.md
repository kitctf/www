---
layout: post
title: "Report: Flag Sharing Incidents during GPN CTF 2025"
categories: gpnctf-23
excerpt: >
  <p>We implemented <i>dynamic flags</i> for GPN CTF 2025, and got more than we wanted.</p>

---

![](/imgs/gpnctf23-flagshare-meme.png)

## Background

Last year we organized GPN CTF 2024. During the event we received multiple reports from participants via Discord stating they had been approached by others asking for flags. In most cases, we responded by handing out an invalid but realistic fake flag. We later used these flags to identify teams engaging in flag-sharing.

Given the frequency of these incidents, we decided to implement **dynamic, team-specific flags** for GPN CTF 2025.

## Dynamic Flags in 2025

For the 2025 event, most challenges featured **team-specific dynamic flags**, generated to appear similar at first glance, with differences in casing and typical leet-speak substitutions.

A team was assigned a flag when they either spawned their first instance of the challenge or downloaded its handout.

Throughout the event, we were contacted twice by teams who had been asked for a flag and handed out a wrong one – both of which allowed us to identify the submitting team.

To aid detection, we **logged every flag submission** in our CTF system’s database, including timestamps, submitting teams, and users.

After the event, we queried the database for all cases where a team submitted a **valid flag of another team for a challenge they had not yet solved**. This yielded **53 incidents**, excluding submissions of known fake flags.
In analyzing these incidents, we also reviewed instances where shared flags were submitted after the team's correct submission.

## Investigation Summary

In total, we reviewed **53 incidents**, plus an additional **9 cases** involving known fake flags.

For each incident, we analyzed team activities, submission timings, and flag ownership:

- **7 incidents** had plausible non-malicious explanations. While still technically detected correctly, these were not pursued further.
- **3 teams** were directly linked to fake flag submissions, providing **conclusive evidence of flag-sharing**.
- **2 teams** were observed swapping flags shortly before the competition ended.

In many cases, the submitting team had **never spawned an instance for the challenge or downloaded the handout**, making it clear that they obtained the flag externally.

Typically, **only individual players within teams** were involved in these incidents.

---

## Involved Teams and Incidents

### 0bug
- Submitted a flag for `nasa` originating from **NOVA** at `2025-06-21 09:53:25`.

### 0day@freddy
- Their flags for `hinting`, `mini-dsp`, `the-old-way`, `free-parking-network`, and `intro-web-2` were later submitted by **FPTU Ethical Hacker Club** during the final 6 hours of the competition.

### 0xfun
- Submitted a flag for `the-old-way` belonging to **NOVA** at `2025-06-21 09:47:11`.

### 4O4NULLERS
- Submitted a **previously-known fake flag** for `real-christmas` at `2025-06-20 20:22:18`, as well as one for `intro-web-1` between `2025-06-20 13:27:52` and `2025-06-20 13:57:28` 4 times.
- Their flags for `intro-web-1`, `intro-web-2`, and `the-old-way` were later submitted by **ACSS Override**.

### ACSS Override
- Submitted flags for `intro-web-1`, `intro-web-2`, and `the-old-way` that belonged to **4O4NULLERS**.

### Band 0xF Br3ach3rs
- Submitted flags for `check-this-out` and `image-contest` belonging to **Nc{Cat}**.

### BigBoys
- Their flag for `broccoli` was submitted by **seagull** at `2025-06-20 18:29:02`.

### FPTU Ethical Hacker Club
- Submitted flags for `hinting`, `mini-dsp`, `the-old-way`, `free-parking-network`, and `intro-web-2` belonging to **0day@freddy** during the competition’s final 6 hours.

### Ganesh
- Submitted flags from **xupa curintia** for `the-old-way` and `hinting`.

### HoleInBottle
- Their flags for `intro-web-3` and `intro-web-4` were submitted by **ncodeks**.
- Submitted a flag for `hinting` that belonged to **ncodeks**.

### Ialone
- Their flag for `mini-dsp` was submitted by **omtose phellack**.

### MindCrafters
- Their flag for `mini-dsp` was submitted by **NOVA** at `2025-06-20 14:04:23`.

### NOVA
- Solved `nasa` at `2025-06-21 09:41:17`; their flag later appeared with **0bug** at `2025-06-21 09:53:25`.
- Submitted **fake flags** for `real-christmas` at `2025-06-20 20:17:05` and `20:24:35`, with an intermediate attempt by **4O4NULLERS**.
- Submitted **MindCrafters'** flag for `mini-dsp`.
- Their flag for `the-old-way` was later submitted by **0xfun**.

### Nc{Cat}
- Their flags for `check-this-out` and `image-contest` were submitted by **Band 0xF Br3ach3rs**.
- Submitted flags for `restricted-oracle` and `free-parking-network` belonging to **SNI**.

### PuuPuu
- Submitted flags for `no-nc` and `note-editor` belonging to **RaptX**.

### RaptX
- Their flags for `no-nc` and `note-editor` were submitted by **PuuPuu**.
- Their `restricted-oracle` flag was submitted by **momo** and **capablanca**.
- Submitted a flag for `intro-web-1` belonging to **PuuPuu**.

### SNI
- Their flags for `restricted-oracle` and `free-parking-network` were submitted by **Nc{Cat}**.

### Seagull
- Submitted a flag for `broccoli` belonging to **BigBoys** at `2025-06-20 18:29:02`.

### TroJeun
- Submitted a flag for `free-parking-network` belonging to **Vuln3ra** at `2025-06-20 23:39:18`.

### Vuln3ra
- Their `free-parking-network` flag was submitted by **TroJeun**.

### Zerolight
- One player was active and submitted flags on both **Zerolight** and **kBxAc**.
- A known **fake flag** was also submitted for `intro-web-2` at `2025-06-20 13:28:51`

### capablanca
- Submitted a flag for `restricted-oracle` belonging to **RaptX** at `2025-06-21 23:59:02`.

### kBxAc
- One player participated and submitted flags on both **Zerolight** and **kBxAc**.

### momo
- Submitted a flag for `restricted-oracle` belonging to **RaptX** at `2025-06-21 23:54:58`.

### ncodeks
- Submitted **HoleInBottle's** flags for `intro-web-3` and `intro-web-4`.
- Their flag for `hinting` was submitted by **HoleInBottle**.

### omtose phellack
- Submitted a flag for `mini-dsp` belonging to **Ialone** at `2025-06-21 12:01:53`.

### xupa curintia
- Their flags for `the-old-way` and `hinting` were submitted by **Ganesh**.

## Graph of Shared Flags
![](/imgs/gpnctf23-flagshare-graph.svg)


## Statements

We asked all involved teams to open a ticket in order to investigate the incidents and clear up misconceptions. Additionally, we allowed them to provide a statement in text form to provide their perspective on the situation. We publish those statements below.

### capablanca

> During the competition, we opened three support tickets requesting the removal of a newly joined member after observing that he was asking for solutions and appeared to be seeking them on behalf of another team. This behavior is unethical, violates competition rules, and is not tolerated by our team. Although the member was not removed from the CTF platform, we promptly removed him from our Team server. He submitted a flag for a challenge we had already solved while continuing to request additional solutions on private messages, requests we explicitly denied.
> 
> A second member, also participating with our team for the first time, submitted a flag for a different challenge. He provided a plausible explanation of how he obtained it, and based on the information available at the time, the Captain chose to trust him. At no point did he demonstrate any intention to share or request flags. However, after the announcement of the flag sharing, when we followed up for further clarification, he gave an explanation we were unable to verify. 
> Both of these individuals were removed and banned from the team.
> 
> We acted in good faith throughout the competition and took proactive steps to maintain its integrity. As well as collaborated to the investigation when we were told about the irregularities.

### kBxAC
> Not much to report Just we were not aware our team mate was playing from another team we got to only when you told us just as I failed as Captain and a good teammate and We team kBxAc promised that this will not happen again in any of the ctf and once again we are sorry this happened

### Nc{Cat}

> Its regrettable that flag sharing did happen under our team, but we were not at all aware about this. One member was actively part of both SNI and Nc{Cat}, and another member was identified to be leading his own personal team for ctftime points. The guilty members were banned from the team as soon as we got to know about this. We will be doing a more careful background check of current and future members to prevent this from happening again.

### NOVA

> **Official Statement from Team NOVA Regarding Flag Sharing Incident**
> 
> We, **Team NOVA**, would like to formally present our position regarding the recent flag sharing incident during GPNCTF:
> 
> - **Pre-existing Suspicions**:Prior to the event, we had ongoing concerns about a specific individual, dev_fire, being associated with multiple teams and potentially compromising our internal communications.
> 
> - **Controlled Integrity Test (Poisoned Flags)**:To validate these concerns, we strategically shared fake, invalid flags within our private team space during the competition. These flags were intentionally crafted to detect potential leaks and were never intended for legitimate submission.
> 
> - **Immediate and Transparent Reporting**:**We opened an official ticket during the CTF itself** to transparently report this situation and provide full context for any unusual flag activity that might originate from our team. This was done to demonstrate good faith and maintain the competition's integrity.
> 
> - **Acknowledgement of Process Oversight**:In hindsight, we recognize that conducting such an internal test without prior coordination with event organizers was not ideal. Our intention was solely to safeguard competition integrity, but we acknowledge that our method conflicted with established rules.
> 
> - **Respect for the Organizers' Decision**:While we regret the disqualification outcome, we fully respect the organizers' commitment to ensuring fairness across all teams. We appreciate the opportunity to share our perspective and clarify that at no point were valid, legitimate flags shared or compromised by our actions.
> 
> **Commitment to Future Integrity**:Moving forward, Team NOVA will:
> 
> Coordinate directly with organizers before competitions if internal leak concerns arise.
> 
> Implement stricter internal controls, including verified-only flag channels and comprehensive membership audits.
> 
> We appreciate the organizers' recognition of our cooperation and respectfully request that our proactive approach, including the fact that we opened a ticket during the CTF itself, be noted in the final report to help preserve the integrity and reputation of Team NOVA.
> 
> Thank you for your time and understanding.
> 
> **Team NOVA**

### RaptX
RaptX provided their statement as a PDF:
[statement.pdf](/files/gpnctf-23/statement-raptx.pdf)

### TroJeun
> one of our players played the CTF for another team and submitted a flag from another team without our knowledge, the player who did it is now kicked out of the team, and it was decided that the credentials of the CTF being played should never be shared in a public channel but in a private channel for the specific CTF
