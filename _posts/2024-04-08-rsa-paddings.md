---
layout: post
title: "Swampctf coppercrypto and bad paddings in RSA schemes"
categories: learning
author: s1nn105 
mathjax: true
---
A little contribution to revive the KITCTF blog.
## Coppercrypto and bad padding 
One of the two crypto challenges SwampCTF 2024 had was Copper Crypto. It was solved 37 times and gave 328 points. Today we will use this challenge as an opportunity to explore paddings in the RSA scheme.

The challenge is quite simple, here is the source code:
```py
#!/bin/python3

from Crypto.Util.number import *

with open('flag.txt', 'rb') as fin:
	flag = fin.read().rstrip()

pad = lambda x: x + b'\x00' * (500 - len(x))

m = bytes_to_long(pad(flag))

p = getStrongPrime(512)
q = getStrongPrime(512)

n = p * q
e = 3
c = pow(m,e,n)

with open('out.txt', 'w') as fout:
	fout.write(f'n = {n}\n')
	fout.write(f'e = {e}\n')
	fout.write(f'c = {c}\n')
```
The outputs (out.txt) were also given.
There are serveral things wrong with this code. 
First an foremost the fact that it does not use SageMath.
Jokes aside  the weakness lays in the padding.
The script loads the flag, pads it with null bytes and then encrypts it 
with an randomly generated RSA key. for the RSA key we use two 512 bit primes. This 1024 bit modulus is accompanied by 3 as the public exponent.
This small public exponent is dubious at best. While a small public exponent in itself might not be a problem, it is for sure not optimal an will enable multiple attacks on this. 


This challenge essentially calls for the coppersmith  theorem, but we shall not bring guns to a knife fight. [At least not yet.]

Padding with null bytes is unusal, and that for a good reason: 
Consider 0xdeadbeef, padding with a null byte (on the right, if the padding were added on the left it would not impact the number represented by the bytes) is exactly the same as multiplying it with $$ 2^8 $$. You can think of it as multiplying decimal number with 10, but instead we multiply a binary number with two or $$ 2^8 $$ to add an entire null byte on the right end.
What this essentially means is that the pad function can be rewritten in "math" as: 
```py 
pad = lambda x: x * 2^(8*(500 - len(x)))
m = pad(bytes_to_long((flag))
```
This is problematic because now we can remove the padding entirley due to the homomorphic property of RSA.

Lets step back for one second. Assume we know the length of the flag and thus the length of the padding, the padding becomes no more than a constant $$pad$$. Encrypting the padded flag $$ \textit{Enc}_\textit{padded}(pk,pad) = (flag \cdot pad)^3 \textit{ mod } n  = C $$. 

However since we  know the padding $$pad$$ we can (with a little bit of luck) compute $$pad^{-1} \textit{ mod } n$$ using the known public key we can cumpute $$C \cdot (pad^{-1})^3 \textit{ mod } n$$.
Simplifying this results in $$ = flag^3 \textit{ mod } n =: C_f $$.


Hitherto we did not use the low public exponent, but now we can assume (due to the "large" public modulus and the small public exponent) that the ciphertext would not be much larger if it would be calculated in the integers instead of the modular arithmetic. Using this assumption we can simply recover the flag by computing the third root of $$C_f$$. Implementing this is trivial, you can try this your self, but seems a bit cheap if you consider that this "trick" does only work in certain circumstances. A more general approach will be presented in the next chapter.

