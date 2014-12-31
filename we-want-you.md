---
layout: post
title:  "We want you..."
categories: exclude
permalink: /we-want-you/
---

Hi :)

Du bist wahrscheinlich hier gelandet, weil Du Interesse an IT-Sicherheit hast.
Im Folgenden wollen wir Dir näher bringen was wir hier machen und hoffentlich dein Interesse gewinnen.


## Über uns
Wir sind eine Gruppe von KIT Studenten und IT(-Security) Enthusiasten (anders ausgedrückt: Hackern), die CTF als Hobby entdeckt haben.
Momentan treffen wir uns 1x pro Woche, um zu trainieren oder uns generell über Themen aus dem Bereich infosec auszutauschen.

## CTF?
CTFs (Capture the Flag) sind internationale Wettbewerbe im Bereich IT-Sicherheit (ethical hacking).
Sie finden meist online statt (jeopardy style) und dauern normalerweise entweder 24 oder 48 Stunden.
Das bekannteste CTF (sozusagen die Weltmeisterschaft) ist das DEFCON CTF, welches jährlich im Sommer während der DEFCON in Las Vegas stattfindet.
Generell gibt es grob 1-2 mal pro Monat ein CTF, meistens im Rahmen einer IT Security Konferenz.

Bei einem CTF gibt es Aufgaben aus verschiedenen Bereichen der Informatik und IT-Sicherheit (s.u.).
Für das Lösen einer Aufgabe, also konkret das Einreichen der korrekten Flag im Webportal, erhalten die Teams Punkte, deren Höhe sich nach der Schwierigkeit der Aufgabe richtet (meist zwischen 50 und 500 Punkten). Eine Flag ist hier meist einfach eine Zeichenkette, z.B. nach dem Muster `flag{some_secret_string_here}`
Am Ende gewinnt das Team mit den meisten Punkten.


## Aufgabenbereiche
Hier soll einmal skizziert werden, aus welche Bereichen die Aufgaben während eines CTFs kommen (können) und mit was wir uns dementsprechend im Rahmen unserer Studentengruppe beschäftigen.

#### Binary Exploitation
Der Klassiker! Gegeben ist hier meistens eine kompilierte Binary (manchmal mit source code, manchmal mit symbols, oft aber ohne beides). Diese soll nun analysiert werden, um Schwachstellen (meistens memory corruption Bugs) zu finden. Anschließend wird ein Exploit geschrieben und auf den Server der Betreiber losgelassen. Dieser liefert dann meist Shell-Zugriff auf der Box und es findet sich eine Datei, in welcher die Flag steht.

Für die, die sich in dem Bereich schon etwas mehr auskennen: Natürlich kommen hier auch moderne Mitigations wie z.B. NX, ASLR und Stack Canaries zum Einsatz, welche umgangen werden wollen. Je nach Schwierigkeitsgrad der Aufgabe sind mal mehr, mal weniger Mitigations aktiv.

#### Sandboxing
Hier geht es darum, selbst gestrickte Sandboxes zu brechen. Oft werden hier Sandboxes für diverse Skriptsprachen (beliebt ist Python) eingesetzt, es finden sich aber auch Sandboxes auf Basis von [seccomp](http://en.wikipedia.org/wiki/Seccomp).
Generell verhindert die Sandbox mindestens das Ausführen beliebiger Shell Befehle. Der Mechanismus soll dann umgangen und meist wiederum eine Datei (in der die Flag steht) vom Dateisystem gelesen werden.

#### Reverse Engineering
Meistens geht es bei Aufgaben aus dem Bereich Reversing nicht einfach nur darum, eine Binary zu reverse engineeren (das muss schon genug für Binary Exploitation gemacht werden), sondern z.B. mal darum, ein selbst gebautes Kompressionsschema zu analysieren oder das Obfuscation-Schema hinter einer Binary zu verstehen.
Generell ist die Flag hier "nur" gut versteckt in den Daten, die einem bereitgestellt werden.

#### Kryptographie
Ebenfalls beliebt sind Aufgaben aus dem Bereich Kryptographie.
Hier gibt es teilweise Aufgaben, bei denen es darum geht, selbst gebaute Kryptoverfahren zu brechen (z.B. durch Häufigkeitsanalyse). Oft geht es aber auch darum, konkrete Angriffe auf z.B. RSA zu implementieren (beispielsweise [Wiener's Attack](http://en.wikipedia.org/wiki/Wiener%27s_attack) oder [diesen Angriff hier](https://www.cs.unc.edu/~reiter/papers/1996/Eurocrypt.pdf)).

#### Web Security
Eigentlich immer dabei: Web Sicherheit.
Hier sind natürlich die Klassiker SQLi und XSS sowie File Inclusion und Freunde, aber auch ein gutes Verständnis von Web Technologien generell gefragt. Außerdem ist häufig ein gutes Verständnis von Unix und Co (z.B. die Dateien unter /proc/self) und manchmal auch Kryptographie wichtig (z.B. um schwache Signaturschemata für Cookies mithilfe eines [length extension Angriffes](http://en.wikipedia.org/wiki/Length_extension_attack) zu brechen und sich so eine Session als Admin zu verschaffen).
Damit es abwechslungsreich bleibt sind aber oft auch "exotischere" Angriffe gefragt: NoSql- und Object Injection, Dom Clobbering, SSRF usw.

Übrigens muss hier nicht alles serverseitig sein. Da in der Realität clientseitige Angriffe immer wichtiger werden, wird natürlich versucht, dies in den Aufgaben widerzuspiegeln. Meistens wird dabei ein bot (z.B. auf Basis von [phantomjs](http://phantomjs.org/)) eingesetzt, welcher regelmäßig die Seite besucht (oder ihm gesendete Links öffnet) und dabei auch Javascript ausführt.

#### Forensics
Aufgaben aus dem Bereich Computer Forensics. Hier sollen z.B. "post-mortem" Systeme analysiert werden, beispielsweise ein Windows Disk-Image nach einer Vireninfektion oder ein Unix Webserver nach einem Einbruch.
Außerdem beliebt sind Aufgaben bei denen ein packet capture file gegeben ist und aus diesem bestimmte Informationen entnommen werden sollen (z.B. Passwörter).

#### Kernel Exploitation
Kernel exploitation challenges kommen eher selten vor (und dann meist bei on-site Events), da praktisch für jedes Team ein eigener Server eingerichtet werden muss: ein fehlgeschlagener exploit Versuch und die Maschine muss neu gestartet werden.
Hierbei geht es darum, Schwachstellen im Betriebssystemkern (meistens einem selbst geschriebenen Treiber) zu finden und auszunutzen, um sich erweiterte Rechte auf dem System zu verschaffen (unter Linux meist root).

Generell kann man es aber auch in anderen Aufgabenbereichen (z.B. Reversing) mal mit einem (selbst gebauten oder modifizierten) Kernel zu tun haben. ;)

#### Recon
Eher selten und mit weniger Punkten belegt sind Aufgaben im Bereich Recon. Hierbei geht es meist darum, durch geschicktes Suchen im Internet Informationen über Personen herauszufinden.

#### Coding
Nicht unbedingt Security related aber trotzdem ab und zu gesehen.
Hier geht es darum, einen Algorithmus für ein gegebenes Problem zu entwerfen und zu implementieren.
Gegeben wird hier meist eine Beschreibung des Problems sowie die Adresse eines Servers, welcher einem Probleminstanzen liefert (welche meist innerhalb kurzer Zeit gelöst werden müssen). Liefert man dem Server die korrekten Ergebnisse so gibt dieser einem im Ausgleich die Flag.


Das sind die Kategorien, die am häufigsten vorkommen. Oft finden sich aber auch Aufgaben aus ganz anderen Bereichen (nicht mal unbedingt aus dem Bereich Computer Science). CTF Veranstalter sind da häufig kreativ. ;)


## Motivation
Falls Du immer noch nicht überzeugt bist, gibt es hier noch ein paar weitere Gründe, warum sich CTF spielen lohnt:

- es macht Spaß :)
- wird von vielen Firmen (nicht mal unbedingt nur im Bereich IT-Security) sehr gerne gesehen ([proof](http://www.reddit.com/r/netsec/comments/202bsf/hey_guys_we_run_five_infosec_consulting_companies/cfz5pg1), [proof](https://trailofbits.github.io/ctf/)) und z.B. weiß es auch Google sehr zu schätzen ;)
- man lernt sehr viele Technologien kennen (von kernel-level sandboxing über die neusten C++ Features und exotischen Programmiersprachen bis hin zu diversen Web Frameworks und natürlich state-of-the-art exploitation Tricks)
- gute Gelegenheit, um nochmal seine Coding Skills in z.B. Python zu verbessern

Generell sollte sich CTF spielen auch für Deine weitere Informatik Laufbahn (und natürlich die Uni) auszahlen. :)


## Was solltest Du schon können?
Im Prinzip reicht es, wenn Du Interesse am Subjekt hast und ein wenig Zeit aufbringen kannst, um Dich in die entsprechenden Themen einzuarbeiten. Es muss natürlich auch nicht jeder alles können. Oft macht es mehr Sinn sich auf ein Gebiet zu spezialisieren, als in allen ein bisschen was zu können.
Du solltest außerdem über grundlegende Englischkenntnisse verfügen, da die CTFs i.d.R immer auf Englisch sind.

Was außerdem nicht schaden kann:

- Linux/Unix Kenntnisse
- Kenntnisse von C und z.B. Python
- Generelles Verständnis von IT Sicherheit
- evtl. ein gewisses Frustpotential: es kann am Anfang vorkommen, dass man bei einem CTF gar nichts lösen kann (die Aufgaben sind eben auch so gestellt, dass sie selbst für Leute, die in der IT Security Branche tätig sind, noch anspruchsvoll genug sind). Davon sollte man sich jedoch auf keinen Fall demotivieren lassen.


## Interesse geweckt?
Super! Dann melde dich doch bei uns via IRC: #kitctf auf freenode ([one-click-webclient](/irc)) oder auch per Mail an [ctf@samuel-gross.de](mailto:ctf@samuel-gross.de) :)
