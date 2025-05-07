# Elliptic Curve Cryptography (ECC)

---

## Where are we?

- Last time: basics of elliptic curves (EC), group operation
- Now: understand, apply and attack cryptography over EC cyclic group
- Primitives of asymmetric cryptography:
    1. Key exchange (ECDH, last time)
    2. Encryption
    3. Signatures
- Other use cases of EC in cryptography

---

## Recap

- EC $E$ over $\mathbb{Z}_p, p > 3$, Points $(x,y)$ with $y^2 \equiv x^3 + ax + b \mod p$ and $O$
- Discriminant $a,b \in \mathbb{Z}_p$ with $4a^3 + 27b^2 \not\equiv 0 \mod p$ (to avoid singularities)
- Cyclic group with generator $G$
    $x_3 \equiv s^2 -x_1 -x_2 \mod p$
    $y_3 \equiv s (x_1 - x_3) -y_1 \mod p$
    - $s = \frac{y_2-y_1}{x_2-x_1} \mod p$ (addition)
    - $s = \frac{3x_1^2+a}{2y_1} \mod p$ (doubling)

---

## Curve Parameters

- Modulus $p$, usually prime, limits other parameters
- Curve parameters $a,b \in \mathbb{Z}_p$
- Generator $G = (x, y)$
- Group order $n$ for $G$, curve cardinality ($p + 1 - \sqrt{2p} \leq \text{\#}E \leq p + 1 + \sqrt{2p}$), can be prime
- Embedding degree $k$ of $G$, important for some attacks
- Normally, standardized curves are used

---

## Hardness of ECDLP

- ECDLP (EC discreet logarithm problem): given Point $P = (x, y) = mG$, find a
- Attacks: Baby-Step Giant Step, Pollard-Rho, complexity: $\sqrt{p}$
- No sorting or smoothness of elements like in $\mathbb{Z}_p^*$
- Group order can be prime

---

## Encryption: EC-ElGamal

- Elliptic curve $E$ and Generator $G$ for cyclic group
- Function $f: \mathbb{Z}_p \to E, m \mapsto (x,y)$, invertible, e.g., x-coordinate
- Secret key $s \in [1, p-1]$, public key $Q = sG$
- Encrypt: convert message $f(m)=P$, choose nonce $k$, $C = kP, C' = kQ$, ciphertext $(k, C, C'+P)$
- Decrypt: calculate $C'=sC$ and $P = C' + P - C'$, invert $f$
- Some attacks on ElGamal target non-prime group orders, EC order can be prime

---

## Signatures: ECDSA

- Elliptic curve $E$ and Generator $G$ for cyclic group
- Secret key $d \in [2, p-1]$, public key $Q = dG$
- Cryptographic hash function $H$
- nonce **must** be cryptographically secure random

---

## Signatures: ECDSA

- Signing:
    1. Calculate $z = \text{H}_{0..n}(m)$
    2. Choose nonce $k$
    3. Calculate $(x,y) = kG$
    4. If $x \not= 0$: $r = x$, else choose new nonce
    5. Calculate $s = k^{-1}(z+rd)$. Choose new nonce if $s = 0$.
    6. Publish signature $(r, s)$

---

## Signatures: ECDSA

- Verification:
    1. Check $Q \in E, Q \not= O; r, s \in [1..n-1]$
    2. Calculate $z$ like above
    3. Calculate $u_1 = zs^{-1}$, $u_2 = rs^{-1}$
    4. Calculate $P = (x_1, y_1) = u_1G+u_2Q$. Check $P\not= O, x_1=r$.

---

## Signatures: EdDSA

- variant of Schnorr signature based on twisted Edwards curves
- Elliptic curve over $\mathbb{F}_q$, points are $\mathbb{F}_q$-rational, $\#E(\mathbb{F}_q)=2^cl$
- Base point $B \in E(\mathbb{F}_q)$ with order $l$
- Cryptographic hash function $H$ with $2b$ output bits, $2^{b-1}>q$
- Secret key $k, s=H_{0..b-1}(k)$, public key $Q = sB$

---

## Signatures: EdDSA

- Signing:
    1. $r = H(H_{b..2b-1}(k)||m)$, $R = rB$
    2. $S = r + H(R||Q||m)s$
    3. Publish (R,S)
- Verification: check $2^cSB = 2^cR+2^cH(R||Q||m)Q$

---

## Attacks
- Insecure choice of parameters
- Faulty custom implementation, variation from protocols
- How is the point at infinity $O$ handled?
- Reused nonces, insecure nonce generation or leakage
- usage of side channels or faults

---

## Implementation
- Cryptographic libraries in nearly every language
- Group operations are often called `DBLADD` and `MUL`
- Multiplication uses Square-and-Multiply strategy
- Python has libraries for most elliptic curve protocols
- Common attacks are mostly available in Python (some c/cpython)
- Mathematic operations and complex calculations very efficient (and sometimes more readable) in Sagemath

---

## Sagemath
- free open-source mathematics software system
- can be installed via package manager on some distros, available from conda-forge
- Provided by cloud, e.g., [CoCalc](https://cocalc.com/), [SageMathCell](https://sagecell.sagemath.org/) 
- Provides many operations and tutorials for [groups](https://doc.sagemath.org/html/en/thematic_tutorials/group_theory.html), [rings](https://doc.sagemath.org/html/en/tutorial/tour_rings.html) and [Elliptic Curves](https://doc.sagemath.org/html/en/reference/arithmetic_curves/index.html)

---

## Further Topics:
- Other Applications of EC (e.g., for ZK-proofs)
- Pairing based cryptography (often used together, but different concept)

---

## Sources:

- Elliptische-Kurven-Kryptografie (ECC), https://www.youtube.com/watch?v=NeM12tNQ59g
- Kryptographie mit elliptischen Kurven (ECC), https://www.youtube.com/watch?v=N1WBehM9rPk
- ECDSA: Handle with care, https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/
- Wikipedia and cryptography stack exchange are help for basic concepts and specific situations
