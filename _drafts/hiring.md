---
layout: post
title:  "We are hiring"
permalink: /hiring/
---

Hi :)

du bist wahrscheinlich hier gelandet, weil du Interesse an IT-Sicherheit hast.
Im Folgenden wollen wir dir näher bringen was wir hier machen und hoffentlich dein Interesse gewinnen.


## Über uns
Wir sind eine Gruppe von KIT Studenten und IT(-Security) Enthusiasten, die CTF als Hobby entdeckt haben.
Momentan treffen wir uns 1x pro Woche um zu trainieren oder uns generell über Themen aus dem Bereich IT Security auszutauschen.

Siehe auch ([hier](/about)).

## CTF?
CTFs (Capture the Flag) sind internationale Wettbewerbe im Bereich IT-Sicherheit (ethical hacking).
Sie finden meist online statt (jeopardy style) und dauern normalerweise entweder 24 oder 48 Stunden.
Das bekannteste CTF (sozusagen die Weltmeisterschaft) ist das DEFCON CTF, welches Jährlich im Sommer während der DEFCON in Las Vegas stattfindet.
Generell gibt es grob 1-2 mal pro Monat ein CTF, meistens im Rahmen einer IT Security Konferenz.

Bei einem CTF gibt es Aufgaben aus verschiedenen Bereichen der Informatik und IT-Sicherheit (s.u.).
Für das Lösen einer Aufgabe (konkret das Einreichen der korrekten Flag - einfach eine Zeichenkette - im Web Portal) erhalten die Teams Punkte, deren Höhe sich nach der Schwierigkeit der Aufgabe richtet (meist zwischen 50 und 500 Punkten).
Am Ende gewinnt das Team mit den meisten Punkten.


## Aufgabenbereiche
Hier wird einmal skizziert, welche Aufgabenbereiche während eines CTFs gefragt werden (können) und mit was wir uns dementsprechend im Rahmen unserer Studentegruppe beschäftigen.

#### Binary Exploitation
Der Klassiker! Gegeben sei eine kompilierte binary (manchmal mit source code), die analysiert werden soll, wobei eine Schwachstellen (meistens memory corruption bugs) gefunden  und einen Exploit geschrieben werden soll.
Der Exploit, losgelassen auf den Server der Betreiber, liefert dann meistens shell Zugriff auf der Box und es findet sich eine Datei in welcher die Flag steht.

#### Sandboxing
Hier geht es darum, selbstgestrickte Sandboxes zu brechen. Oft werden hier Sandboxes für diverse Skriptsprachen (beliebt ist Python) eingesetzt, es finden sich aber auch Sandboxes auf Basis von ([seccomp](http://en.wikipedia.org/wiki/Seccomp)).
Generell verhindert die Sandbox mindestens das Ausführen beliebiger shell Befehle. Der Mechanismus soll dann umgangen und meist wiederum eine Datei (in der die Flag steht) vom Dateisystem gelesen werden.

#### Reverse Engineering
Meistens geht es hier nicht einfach nur darum, eine Binary reverse zu engineeren (das muss schon genug für Binary Exploitation gemacht werden), sondern z.B. darum, ein selbstgebautes Kompressionsschema zu reversen oder eine obfuscatete binary zu verstehen.

#### Kryptographie
Ebenfalls beliebt sind Aufgaben aus dem Bereich Kryptographie.
Hier gibt es teilweise Aufgaben, bei denen es darum geht, selbstgebaute Cryptoverfahren zu brechen (z.B. mit Häufigkeitsanalyse). Oft geht es aber auch darum, konkrete Angriffe auf z.B. RSA zu implementieren (beispielsweise Wiener's Attack oder ([diesen Angriff hier](https://www.cs.unc.edu/~reiter/papers/1996/Eurocrypt.pdf)))

#### Web Security
Eigentlich immer dabei: Web Sicherheit.
Hier sind natürlich die Klassiker SQLi und XSS sowie File Inclusion und Freunde, aber auch ein gutes Verständnis von Web Technologien generell gefragt. Außerdem ist häufig ein gutes Verständnis von Unix und CO (z.B. die Dateien unter /proc/self) und manchmal auch Kryptographie wichtig (z.B. um schwache Signaturschemata für Cookies mithilfe eines ([length extension Angriffes](http://en.wikipedia.org/wiki/Length_extension_attack)) zu brechen und sich so eine Session als Admin zu verschaffen).
Oft werden auch exotischere Angriffe gefragt: NoSql- und Object Injection, Dom Clobbering, ... TODO

#### Forensics
Aufgaben aus dem Bereich Computer Forensics. Hier sollen z.B. "post-mortem" Systeme analysiert werden, beispielsweise ein Windows Disk-Image nach einer Vireninfektion oder ein Unix Web Server Image nach einem Einbruch.
Außerdem beliebt sind Aufgaben bei denen ein packet capture file gegeben ist und aus diesem bestimmte Informationen entnommen werden sollen (z.B. Passwörter).

#### Recon
Eher selten und mit weniger Punkten belegt sind Aufgaben im Bereich Recon. Hierbei geht es meist darum durch geschicktes Suchen im Internet Informationen über Personen herauszufinden.

#### Coding
Hier bekommt man eine Aufgabe gestellt und soll diese Programmieren. I.d.R. erhält man einen Netzwerkzugang und soll in einem kurzen Zeitraum (1-3s) eine oder mehrere Aufgabe lösen. Der Zeitraum ist normalerweise für einen Menschen zu kurz. Klassisches Beispiel wäre eine Art Captcha maschinell zu lösen.


TODO Message: das ist das Zeug was im realen leben relevant ist.

Das sind die Häufigsten Kategorien. Oft finden sich aber auch Aufgaben aus ganz anderen Bereichen (nicht mal unbedingt aus dem Bereich Computer Science). CTF Veranstalter sind da häufig kreativ. ;)


## Motivation
Falls du immer noch nicht überzeugt bist, gibt es hier noch ein paar weitere Gründe, warum sich CTF spielen lohnt:

- es macht Spaß :)
- wird von vielen Firmen (nicht mal unbedingt nur im Bereich IT-Security) sehr gerne gesehen ([proof](http://www.reddit.com/r/netsec/comments/202bsf/hey_guys_we_run_five_infosec_consulting_companies/cfz5pg1)) und z.B. weiß es auch Google sehr zu schätzen ;)
- man lernt sehr viele Technologien kennen (von kernel-level sandboxing, über die neusten C++ features und exotischen Programmiersprachen, bis hin zu diversen Web Frameworks und natürlich state-of-the-art exploitation tricks)
- gute Gelegenheit, um nochmal seine Coding Skills in z.B. Python zu verbessern

Generell sollte sich CTF spielen auch für die weitere Informatik Laufbahn (und natürlich die Uni) auszahlen. :)


## Was solltest du schon können?
Generell reicht es wenn du Interesse am Subjekt hast und ein wenig Zeit aufbringen kannst um dich in die ensprechenden Themen einzuarbeiten. Es muss natürlich auch nicht jeder alles können. Lieber in einem Feld gut sein als in allen ein bisschen was können.
Du solltest außerdem über grundlegende Englischkenntnisse verfügen da die CTFs i.d.R immer auf Englisch sind.
Was außerdem nicht schaden kann:
- Linux/Unix Kentnisse
- Kentnisse von C und z.B. Python
- Generelles Verständnis von IT Sicherheit
- evtl. ein gewisses Frustpotential: es kann am Anfang vorkommen, dass man bei einem CTF gar nichts lösen kann (die Aufgaben sind eben auch so gestellt dass sie selbst für Leute die in der IT Security Branche tätig sind noch anspruchsvoll genug sind). Davon sollte man sich jedoch auf keine Fall demotivieren lassen.


## Interesse geweckt?
Super! Erreichen kannst du uns z.B. via IRC: #kitctf @ freenode ([one-click-webclient](http://tinyurl.com/kitctf-irc))
oder auch per Mail an ctf@samuel-gross.de :)
Außerdem könnten dich folgende Seiten noch interessieren:
- resources
- tools
- first-steps
