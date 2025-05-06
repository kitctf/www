
# Introduction to Elliptic Curves

---

## Basics:
- Primitives of asymmetric cryptography:
    1. Key exchange
    2. Encryption
    3. Signatures
- now over a different ring (new algebraic structure)

---

## Motivation:

| Algorithm Family | Cryptosystems | Security <br> short term | Level <br> medium | (bit) <br> long term | <br>  | <br>  |
|--|--|--|--|--|--|--|
| Integer Factorization | RSA | 700 | 1024 | 3072 | 7680 | 15360 |
| Discrete Logarithm ($\mathbb{Z}_{p^*}$) | DH, DSA, Elgamal | 700 | 1024 | 3072 | 7680 | 15360 |
| Elliptic Curves | ECDH, ECDSA | 128 | 160 | 256 | 384 | 512 |
| Symmetric Key | AES, 3DES | 64 | 80 | 128 | 192 | 256 |

---

## Motivation:

Higher security levels for RSA etc. require computations over large numbers, many operations, very slow

Goal: find cyclic group with hard DLP that allows for smaller key sizes and efficient computation

<small>DLP -- Discrete Logarithm Problem</small>

---

## Geometric Interpretation:

Elliptic Curve equation: $y^2 = x^3 + ax + b$

![Elliptic Curve](/imgs/e1e09d8b-db2c-4697-97f2-236190e83051.png)

---

## Geometric Interpretation:

- Group: Generator point $G$, multiplication with natural number
- x-axis symmetry
- Multiplication over EC:
    1. Find intersection with curve
        a. For $2G$: tangent at point $G$
        b. For $aG, a>2$: line through $G$ and $(a-1)G$
    2. Flip y-coordinate

---

## Maths:

- EC group over $\mathbb{Z}_p, p > 3$
- Point $(x, y)$ on curve iff $y^2 \equiv x^3 + ax + b \mod p$, plus (imaginary) point at infinity $O$, $a,b \in \mathbb{Z}_p$ with $4a^3 + 27b^2 \not\equiv 0 \mod p$
- Cyclic group:
    1. set of elements (points on curve)
    2. group operation fulfilling group laws

---

## Maths:

- Group operation:
    - Point addition and point doubling ($(x_1,y_1) + (x_2,y_2)$):
        $x_3 \equiv s^2 -x_1 -x_2 \mod p$
        $y_3 \equiv s (x_1 - x_3) -y_1 \mod p$
        - $s = \frac{y_2-y_1}{x_2-x_1} \mod p$ (addition)
        - $s = \frac{3x_1^2+a}{2y_1} \mod p$ (doubling)
    - neutral element: "artificial" point at infinity $O$
    - inverse: $-P = (x,-y)$ (x-coordinate flipped)

---

## Attributes:

- mathematics necessary for reversing more complicated, less efficient -> smaller keys provide same security
- similar structure to DL-problem, can still be broken with QC

---

## ECDH:

- DL-Problem over EC: given $Q = aG$, finding $a$ is "hard"
- ECDH:
    1. choose curve with generator $G$
    2. Alice and Bob choose and exchange $aG$ and $bG$, $a$ and $b$ are secret
    3. Alice and Bob compute shared secret $(ab)G = a(bG) = b(aG)$

---

## ECDH:

(Search for ECDH and find a nice looking image explanation or draw a CC image and insert it here)

---

## Further Topics:

- ECDSA
- Pairing based cryptography with EC
- EC in `sagemath`

---

## Sources:

- Elliptic Curves, Computerphile: https://www.youtube.com/watch?v=NF1pwjL9-DE
- Einführung in die Elliptische-Kurven-Kryptografie (ECC), Lecture: https://www.youtube.com/watch?v=ikeA6SZ83W8

