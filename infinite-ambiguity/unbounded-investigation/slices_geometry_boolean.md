# Boolean points in the sum of periodic subspaces

Status: complete elementary proofs below; independently proposed during this investigation. No claim of novelty, and no resolution of context-freeness. Awaiting adversarial audit.

For n>=2 and each prime p dividing n, write

V_p = {x in R^n : x_i=x_(i+n/p) for all i modulo n},
W_n = sum_(p|n) V_p.

A binary vector is identified with a binary word of length n. It is primitive precisely when it belongs to none of the V_p: any proper power has prime exponent after possibly enlarging its root.

## Theorem 1: complete classification of existence

There is a primitive Boolean vector in W_n if and only if n has at least two distinct prime factors and is not the product of two distinct primes.

Equivalently, none exist for prime powers or n=pq with p!=q; examples exist for p^a q^b with a+b>=3 and for every n having at least three distinct prime factors.

### Fiber description

Let r be the product of the distinct primes dividing n and h=n/r. Every index has a unique form c+h t, where 0<=c<h and t in Z/rZ. Translation by n/p sends t to t+r/p, without changing c. By the Chinese remainder theorem, identify t with coordinates (t_p)_(p|n), t_p in Z/pZ. Translation by r/p changes only coordinate t_p, and cycles through all its values. Thus V_p is precisely the space of functions which, on every fixed fiber c, are independent of coordinate t_p. Different fibers impose no constraints on one another.

Consequently W_n consists exactly of functions whose restriction to each fiber is a sum of functions each missing at least one prime coordinate.

### One prime

If n is a prime power, W_n=V_p, which contains no primitive vector.

### Two primes, one fiber

Let n=pq. Then every f in W_n has the form f(i,j)=u(i)+v(j). If f is Boolean, either u or v is constant. Indeed, if u(i1)<u(i2), then for each j the two Boolean values u(i1)+v(j),u(i2)+v(j) must be 0,1 respectively; this fixes v(j)=-u(i1) for every j. Therefore f depends on at most one coordinate, belongs to V_p or V_q, and is not primitive.

### Two primes, multiple fibers

Let n=p^a q^b and h=n/(pq)>=2. Set the Boolean function on fiber c=0 equal to [t_p=0], on fiber c=1 equal to [t_q=0], and on all other fibers equal to 0. Each fiber function omits one prime coordinate, so f belongs to W_n. It is not in V_p, witnessed in fiber 0, and not in V_q, witnessed in fiber 1. It is therefore primitive.

### At least three primes

List distinct prime coordinates as t1,...,tk with k>=3. On one fiber put

A=[t1=0], B=[t2=0], H=product_(j=3..k)[tj=0],
f=AH+B(1-H).

This is Boolean because it chooses A when H=1 and B otherwise. Its first summand omits coordinate t2 and its second omits coordinate t1. Hence f belongs to W_n, setting the other fibers to 0 if needed.

It depends on t1 by taking H=1, on t2 by taking H=0, and on any tj with j>=3 by taking A=1, B=0 and all remaining coordinates in H equal to 0. Thus it is in none of the V_p, and is primitive. This completes the classification. QED.

## Theorem 2: exact count for two prime factors

Let n=p^a q^b, p!=q primes, a,b>=1, h=n/(pq). The number of primitive Boolean vectors in W_n is exactly

(2^p+2^q-2)^h - 2^(ph) - 2^(qh) + 2^h.

Proof. On each fiber every Boolean additive matrix depends on one coordinate, by the argument above. There are 2^p functions of the p-coordinate and 2^q of the q-coordinate; their intersection consists of the two constant functions. Hence |W_n intersect {0,1}^n|=(2^p+2^q-2)^h. Within this set the nonprimitive vectors are exactly the union of the Boolean points in V_p and V_q. These have sizes 2^(qh), 2^(ph), and intersection size 2^h respectively. Inclusion-exclusion proves the formula. QED.

Examples: n=6 gives 0; n=12 gives 24; n=18 gives 432; n=20 gives 120; n=24 gives 5664. These values explain earlier finite computations in context-free/reports/devil.md, rather than relying on them as proof.

## Consequence for linear certificates

Any linear form annihilating every periodic subspace annihilates W_n. Therefore a scheme certifying primitivity by the nonzero value of one of these forms necessarily misses all the vectors counted or constructed above. The exceptions occur for arbitrarily large n, including squarefree n with three prime factors. This refutes any extrapolation from the squarefree two-prime case that Boolean primitive words always lie outside W_n.

This is a barrier for that certificate scheme, not a proof about arbitrary CFGs or PDAs. The bounded primitive-word language outside W_n is known locally to be context-free, but restricting to W_n is not a regular-language intersection in the original word encoding; no context-free closure conclusion for the residual part follows automatically.
