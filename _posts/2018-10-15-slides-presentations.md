---
layout: post
title: "Folien der Vorträge im Sommersemester '18"
categories: meetings
excludeRSS: true
author: itaton
---

## Binary Exploitation (07. Mai)
Hier sind die [Folien]({{ "/files/BinaryExploitation.pdf" | absolute_url }}) des Einführungsvortrags zum Thema Binary Exploitation am 07.05.2018.

Das erste Beispielprogramm ([simpleStackOverflow]({{ "/files/introduction_binary/simpleStackOverflow.c" | absolute_url }})) wurde wiefolgt kompiliert:

{% highlight bash %}
$ gcc -fno-stack-protector -o simpleStackOverflow simpleStackOverflow.c
{% endhighlight %}

Für das zweite Beispielprogramm ([shellcode]({{ "/files/introduction_binary/shellcode.c" | absolute_url }})) wurde zunächst systemweit ASLR deaktiviert mit: 

{% highlight bash %}
$ echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
{% endhighlight %}

und anschließend das Programm kompiliert mit:

{% highlight bash %}
$ gcc -m32 -fno-stack-protector -z  execstack -o shellcode shellcode.c
{% endhighlight %}

Ausgeführt wurde das Programm wiefolgt:

{% highlight bash %}
$ (cat shellcode_input.txt; cat -) | ./shellcode
{% endhighlight %}

Das letzte Beispielprogramm ([formatString]({{ "/files/introduction_binary/formatString.c" | absolute_url }})) wurde ohne Zusatzoptionen kompiliert:
{% highlight bash %}
$ gcc -o formatString formatString.c
{% endhighlight %}


## Web (14. Mai)
Die Folien zum Überblick über Web Exploitation finden sich [hier]({{ "/files/Vortrag_Web.pdf" | absolute_url }}).


## 1. Crypto Vortrag
Die Folien vom ersten Vortrag über Crypto finden sich [hier]({{ "/files/Crypto.pdf" | absolute_url }}).

## 2. Crypto Vortrag
Die Folien vom zweiten Vortrag über Crypto finden sich [hier]({{ "/files/Crypto2.pdf" | absolute_url }}).
