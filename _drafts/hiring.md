---
layout: post
title:  "We are hiring"
categories: sticky
---

Hi :)
du bist wahrscheinlich hier gelandet weil du Interesse an IT-Sicherheit hast.
Im Folgenden wollen wir dir näher bringen was wir hier machen und hoffentlich dein Interesse gewinnen.


## Über uns
Wir sind eine Gruppe von KIT Studenten, die CTF als Hobby entdeckt haben.

TODO

Siehe auch ([hier](/about)).

## CTF?
CTFs (Capture the Flag) sind internationale Wettbewerbe im Bereich IT-Sicherheit (ethical hacking).
Sie finden meist online statt (jeopardy style) und dauern normalerweise entweder 24 oder 48 Stunden.
Das bekannteste CTF (sozusagen die Weltmeisteschaft) ist das DEFCON CTF welches Jährlich im Sommer während der DEFCON in Las Vegas stattfindet.

Bei einem CTF gibt es Aufgaben aus verschiedenen Bereichen der Informatik und IT-Sicherheit (s.u.).
Für das Lösen einer Aufgabe (konkret das Einreichen der korrekten flag - einfach eine Zeichenkette - im Web Portal) erhalten die Teams Punkte deren Höhe sich nach der Schwierigkeit der Aufgabe richtet (meist zwischen 50 und 500 Punkten).
Am Ende gewinnt das Team mit den meisten Punkten (doh).


## Aufgabenbereiche
Hier wird einmal skiziert welche Aufgabenbereiche während eines CTFs gefragt werden (können) und dementsprechend mit was wir uns hier beschäftigen.
Generell sind die Aufgaben meist inspieriert von security bugs aus dem real life.

#### Binary Exploitation
Der Klassiker! Gegeben eine kompilierte binary (manchmal mit source code) analysiere sie, finde Schwachstellen (meistens memory corruption bugs) und schreibe einen exploit.
Der Exploit losgelassen auf den Server der Betreiber liefert dann meistens shell Zugriff auf der Box und es findet sich eine Datei in welcher die flag steht.

#### Sandboxing
Hier geht es darum selbstgestrickte sandboxes zu brechen. Oft werden hier sandboxes für diverse Skriptsprachen (python ist beliebt) eingesetzt, es finden sich aber auch sandboxes auf Basis von ([seccomp](http://en.wikipedia.org/wiki/Seccomp)).
Generell verhindert die Sandbox mindestens das Ausführen beliebiger shell Befehle. Der Mechanismus soll dann umgangen werden und meist wiederum eine Datei (in der die flag steht) vom Dateisystem gelesen werden.

#### Reverse Engineering
Meistens geht es hier nicht einfach nur darum eine binary zu reverse engineeren (das muss schon genug für Binary Exploitation gemacht werden) sonder z.B. mal darum ein selbstgebautes Kompressionsschema zu reversen oder eine obfuscatete binary zu verstehen.

#### Cryptographie
Ebenfalls beliebt sind Aufgaben aus dem Bereich Cryptographie.
Hier gibt es teilweise Aufgaben bei denen es darum geht selbstgebaute Cryptoverfahren zu brechen (z.B. mit Häufigkeitsanalyse), oft geht es aber auch darum konkrete Angriffe auf z.B. RSA zu implementieren (Beispielsweise Wiener's Attack oder ([diesen Angriff hier](https://www.cs.unc.edu/~reiter/papers/1996/Eurocrypt.pdf)))

#### Web Security
Eigentlich immer dabei: Web Sicherheit.
Hier gefragt sind natürlich die Klassiker SQLi und XSS sowie File Inclusion und Freunde aber auch ein gutes Verständis von Web Technologien generell. Außerdem wichtig ist häufig ein gutes Verständnis von Unix und CO (z.B. die Dateien unter /proc/self) und manchmal auch Cryptographie (z.B. um schwache Signaturschemata für Cookies mithilfe eines ([length extension Angriffes](http://en.wikipedia.org/wiki/Length_extension_attack)) zu brechen und sich so eine Session als Admin zu verschaffen).
Oft werden auch exotische(re) Angriffe gefragt: NoSql- und Object Injection, Dom Clobbering, ... TODO

#### Misc
TODO

#### Forensics
TODO

#### Recon
TODO


## Motivation
Falls du noch immer nicht überzeugt bist hier ein paar weitere Gründe warum sich CTF spielen lohnt:

- es macht Spaß :)
- wird von vielen Firmen (nicht mal unbedingt nur im Bereich IT-Security) sehr gerne gesehen ([proof](http://www.reddit.com/r/netsec/comments/202bsf/hey_guys_we_run_five_infosec_consulting_companies/cfz5pg1)), und z.B. Google weiß es auch sehr zu schätzen ;)
- man lernt sehr viele Technologien kennen (von kernel-level sandboxing über die neusten C++ features und exotischen Programmiersprachen bis hin zu diversen Web Frameworks und natürlich state-of-the-art exploitation tricks)
- gute Gelegenheit um nochmal seine coding skills in z.B. python zu verbessern

Generell sollte sich CTF spielen auch für die weitere Informatik Laufbahn (und natürlich die Uni) auszahlen.

## Du hast Interesse?
Super! Erreichen kannst du uns z.B. via IRC: #kitctf @ freenode ([one-click-webclient](http://tinyurl.com/kitctf-irc))
oder auch per mail an ctf@samuel-gross.de :)
