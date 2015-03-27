---
layout: post
title: "Boston Key Party 2015 'Wood Island' writeup"
categories: writeups bkp2015
tags: crypto
author: OOTS
---

Originally, I wanted to write up the write-up for the [airport challenge](/writeups/bkp2015/airport/), but since Niklas has already done that, I'm doing the *Wood Island* challenge instead. It was worth 150 points on the [Boston Key Party 2015](http://bostonkey.party/).

The goal was to break [ElGamal Signatures](https://en.wikipedia.org/wiki/ElGamal_signature_scheme). In short, the solution is based on exploiting "random" values that occur multiple times.

We are given access to a network server, and a [tar archive with the server source code and a couple of signatures](https://github.com/kitctf/writeups/blob/master/bkp2015/wood_island/wood-island.tar.gz.3cd7b18f7ae8205b0a71097733e0c4bb).
From the server source code, we can see that the server will happily dump our flag if we manage to forge a signature for the message "There is no need to be upset":

{% highlight python %}
if not elgamal_verify(r, s, m):
    self.request.close()
elif is_duplicate(sig):
    self.request.close()
elif m != "There is no need to be upset":
    self.request.close()
else:
    self.request.sendall(FLAG)
    self.request.close()
{% endhighlight %}

When viewing the signature file, we notice that we already have a signature for that message, but the server will not hand over the flag when we give it the exact same signature. So we need to somehow create a new signature for the message.
This is a good time to have a look at the ElGamal signature scheme if you did not know it before:

## The ElGamal Signature Scheme

The ElGamal scheme works in the multiplicative group of integers modulo a prime number *P* with generator *g*.
(In the task at hand, *P* even is a [safe prime](https://en.wikipedia.org/wiki/Safe_prime), i.e. a number of the form *P = 2p + 1* where *p* is also prime.)
The signing key is a secret, random exponent *x*.
The corresponding verification key is *y = g<sup>x</sup>*.

To sign a message, firstly choose a random integer *k* between *1* and *P - 1* (excluding both) with *gcd(k, P - 1) = 1*, and set *r = g<sup>k</sup>*.
Then compute *s = (H(m) - xr)k<sup>-1</sup> (mod P - 1)*, where *H* is a cryptographic hash function and *m* is the message being signed.
The final signature consists of *r* and *s*.

To verify such a signature, check that
*g<sup>H(m)</sup> = r<sup>s</sup> y<sup>r</sup> (mod P)*.
This equation can be rewritten as
*g<sup>H(m)</sup> = (g<sup>k</sup>)<sup>s</sup> (g<sup>x</sup>)<sup>r</sup> (mod P)* by filling in *y* and *r*.
If we look purely at the exponent, this equation implicitly checks whether *H(m) = ks + xr (mod P - 1)*.

The ElGamal scheme is similar to the [DSA](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm) and the [Schnorr signature scheme](https://en.wikipedia.org/wiki/Schnorr_signature), and (like these two) breaks when the same random value is used for different signatures.

## The Attack

If we have two signatures *(r, s<sub>1</sub>)*, *(r, s<sub>2</sub>)* with the same *r* value, which are valid for two message *m<sub>1</sub>, m<sub>2</sub>*, respectively, we know that the *k* values used for signing must also be equal.
We can then subtract the *s* values to eliminate the unknown secret key *x* from the above equation:

*s<sub>1</sub> - s<sub>2</sub> = (H(m<sub>1</sub>) - xr)k<sup>-1</sup> - (H(m<sub>2</sub>) - xr)k<sup>-1</sup> = (H(m<sub>1</sub>) - H(m<sub>2</sub>))k<sup>-1</sup> (mod P - 1)*

We can thus compute *k<sup>-1</sup> = (s<sub>1</sub> - s<sub>2</sub>)/(H(m<sub>1</sub>) - H(m<sub>2</sub>)) (mod P - 1)*.
(Doing this modular division is actually a little tricky, see below.)
Once we have the correct *k<sup>-1</sup>*, we can create a forgery for any message *m* we like, by letting

*s' = s<sub>1</sub> + (H(m) - H(m<sub>1</sub>))k<sup>-1</sup> (mod P - 1)*

This *s'* together with *r* will be a valid signature for *m*, because

*ks' = k(s<sub>1</sub> + (H(m) - H(m<sub>1</sub>))k<sup>-1</sup>) = ks<sub>1</sub> + (H(m) - H(m<sub>1</sub>)) = H(m<sub>1</sub>) - xr + H(m) - H(m<sub>1</sub>) = H(m) - xr (mod P - 1)*

and thus *ks' + xr = H(m) (mod P - 1)*, which is implicitly checked during verification.

My python code for this attack is:
{% highlight python %}
def forgeSignature(message, sig1, sig2):
	
	# definitions
	r = sig1['r']
	s1 = sig1['s']
	s2 = sig2['s']
	m1 = sig1['m']
	m2 = sig2['m']
	h1 = int(hashlib.sha384(m1.encode('ASCII')).hexdigest(), 16)
	h2 = int(hashlib.sha384(m2.encode('ASCII')).hexdigest(), 16)
	hNew = int(hashlib.sha384(message.encode('ASCII')).hexdigest(), 16)
	
	# sanity checks
	assert(sig1['r'] == sig2['r'])
	assert(elgamal_verify(r, s1, m1))
	assert(elgamal_verify(r, s2, m2))
	
	# get k^(-1)
	kInvCandidates = moddiv( \
		(s1 - s2) % (SAFEPRIME - 1), \
		(h1 - h2) % (SAFEPRIME - 1),
		SAFEPRIME - 1 \
	)
	kInvCandidates = filter( \
		lambda c: pow(r, c, SAFEPRIME) == GENERATOR, \
		kInvCandidates \
	)
	kInv = next(kInvCandidates)

	# compute the new s value
	s = (s1 + (hNew - h1) * kInv) % (SAFEPRIME - 1)
	
	return {'r': r, 's' : s}
{% endhighlight %}
Here, *H* was instantiated with the [SHA-384](https://en.wikipedia.org/wiki/SHA-384) hash function.

When seeing the code above, you notice that I have multiple candidates for *k<sup>-1</sup>*.
This is because the aforementioned difficulty dividing *s<sub>1</sub> - s<sub>2</sub>* by *H(m<sub>1</sub>) - H(m<sub>2</sub>)*.
Namely, both *H(m<sub>1</sub>) - H(m<sub>2</sub>)* and *s<sub>1</sub> - s<sub>2</sub>* are even and thus have a common factor with *P - 1 = 2p*. Thus, *H(m<sub>1</sub>) - H(m<sub>2</sub>)* is not invertible modulo *2p*.
Nonetheless, the division has **two** solutions, which are returned by the *moddiv* function.

I then filter for the correct one by checking that *r<sup>(k<sup>-1</sup>)</sup> = (g<sup>k</sup>)<sup>k<sup>-1</sup></sup> = g<sup>kk<sup>-1</sup></sup> = g<sup>1</sup> = g*.

## Dividing modulo *2p*

Now it is time to dive into the details of modular division.
Our main tool is the [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem).
It allows us to do calculations modulo *2* and *p* distinctly, instead of doing calculations modulo *2p* directly.

More precisely, if we have an integer *h* between *0* and *2p-1* (including both), we can represent *h* as the pair *(h mod 2, h mod p)*.
This representation is equivalent to the number *h*, i.e. we can recover *h* given just *h mod 2* and *h mod p*.
Moreover, this even is an isomorphism: If we are to multiply two numbers *h*, *i* modulo *2p*, we can represent both as *(h mod 2, h mod p)* and *(i mod 2, i mod p)*, and multiply componentwise.
The result is *(hi mod 2, hi mod p)*, which can be transformed back to *hi mod 2p*.

We can now use this knowledge to our advantage when doing modular division.
Suppose we want to compute the modular division of *s = s<sub>1</sub>-s<sub>2</sub>* by *h = H(m<sub>1</sub>) - H(m<sub>2</sub>)*.
Then, if *s* is even (as is the case in our scenario), then *s mod 2 = 0*, so *s* is equivalent to *(0, s mod p)*.
Likewise, *h* is even, so *h* can be represented as *(0, h mod p)*.

As said before, multiplication is done componentwise. Suppose we know the modular inverse *e* of *h* modulo *p*.
(This can be computed easily using the extended euclidean algorithm.)
Then there are two possible numbers *r<sub>1</sub>, r<sub>2</sub>* that map *h* to *(0, s mod p)* upon multiplication: *(0, se mod p)* and *(1, se mod p)*.
(Of course, *(2, se mod p)* would also work. But since we are computing modulo *2* in the first component, this is equivalent to *(0, se mod p)*.)

These are the possible solutions to the division of *s* by *h*.
We now only need to transform them back. There is a general method for this, but I decided to take a shortcut.

Basically, we are looking for two numbers *r<sub>1</sub>, r<sub>2</sub>* that satisfy *(r<sub>1</sub> mod 2, r<sub>1</sub> mod p) = (0, se mod p)* and *(r<sub>2</sub> mod 2, r<sub>2</sub> mod p) = (1, se mod p)*.
In words, these numbers must be congruent to *se* when reduced modulo *p*, and one of them must be even, while the other must be uneven.
It is easy to see that *se mod p* is one of them and *(se mod p) + p* is the other.

My code for this division is given below. It also implements a few other cases that I needed while toying around.
{% highlight python %}
def moddiv(a, b, modulus):
	
	# only implemented for modulus = 2p where p is prime and a,b % p != 0
	assert(modulus % 2 == 0)
	p = modulus // 2
	assert(is_probable_prime(p))
	assert(p > 2)
	assert(a % p != 0)
	assert(b % p != 0)
	
	# if neither a nor b have a common divisor with 2p, the solution
	# is straightforward: r = a * b^(-1) mod 2p
	if isUnit(a, modulus) and isUnit(b, modulus):
		r = (a * modinv(b, modulus)) % modulus
		assert(r * b % modulus == a % modulus)
		return {r}
	
	# if a and b are even, invert b mod p, then use the chinese
	# remainder theorem to find the two solutions.
	elif (a % 2 == 0) and (b % 2 == 0):
		e = modinv(b % p, p)
		r1 = (a * e) % p
		r2 = r1 + p
		assert((r1 * b) % modulus == (a % modulus))
		assert((r2 * b) % modulus == (a % modulus))
		return {r1, r2}
	
	# if a is uneven but b is even, there is no solution.
	elif a % 2 == 1 and b % 2 == 0:
		raise ValueError(
			"division of " + str(int(a)) + " by " + str(int(b)) + \
			" modulo " + str(int(modulus)) + " has no solution" \
		)
	
	# if a is even but b is uneven, there is only one solution.
	else:
		e = modinv(b % p, p)
		r = (a * e) % p
		if r % 2 != 0:
			r = r + p
		assert((r * b) % modulus == a % modulus)
		return {r}
{% endhighlight %}

The code uses a few helper functions (like *modinv*, *isUnit* and *is_probable_prime*) I partially copied from websites, and partially wrote myself.
You can find their implementation in the [full source code](https://github.com/kitctf/writeups/blob/master/bkp2015/wood_island/exploit.py) in our [github repository](https://github.com/kitctf/writeups).
(Note that my code is written for Python 3 and apparently not compatible with Python 2.)

## Putting the Pieces together

Above, I have covered the main concepts behind the solution. But the full solution must also accomplish some other stuff that is less exciting:
For example, actually finding the signatures with repeated *r* values.
This is done by the following code:
{% highlight python %}
# import signatures from file
import json
f = open("sigs.txt")
sigs = [ json.loads(line) for line in f ]
f.close()

# get signatures with identical r values
sigpairs = findDoubles(sigs)
{% endhighlight %}

The *findDoubles* function mentioned here simply sorts the list of signatures by their *r* values and then does a linear scan over the result.
This search returns 3 pairs of signatures. However, only one of these pairs is actually built from **valid** signatures. The other pairs contain at least one invalid signature.
We therefore need to filter for the signature pairs:
{% highlight python %}
# eleminate tuples that are no valid signatures
verify = lambda sig: elgamal_verify(sig['r'], sig['s'], sig['m'])
sigpairs = filter(lambda p: verify(p[0]) and verify(p[1]), sigpairs)
{% endhighlight %}

For each of the remaining pairs (which is just one in our case), we can then attempt to forge a signature.
{% highlight python %}
message = "There is no need to be upset"
for sigpair in sigpairs:
	try:
		forgedSig = forgeSignature(message, sigpair[0], sigpair[1])
		print(submitSolution(message, forgedSig))
	except ValueError as e:
		print(e)
{% endhighlight %}

The *submitSolution* function takes care of the network communication with the server and solves the "captcha" that the server sends.
It returns the answer received from the server, which is the flag
{% highlight python %}
FLAG{nonces_are_fucking_rad_amirite}
{% endhighlight %}
(Whatever that means.)
