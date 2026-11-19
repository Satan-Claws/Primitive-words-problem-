# Analytic investigation: a regular finite-sieve counting model

Status: proposed complete elementary proof, awaiting independent audit. This does not resolve context-freeness. No novelty claim.

## 1. A regular model for finitely many excluded exponents

For an integer d>=1 define D_d=(a^d|b^d)^*. Equivalently, D_d consists of the empty word and all binary words whose maximal constant-letter runs have lengths divisible by d. Consequently

    D_d intersect D_e = D_lcm(d,e).

For a finite set P of primes let M be their product (M=1 if P is empty) and put

    R_P = Sigma^+ minus union_{p in P} D_p.

This is regular, by closure of regular languages under finite union and complement. For n>=1 its number r_P(n) of words of length n is

    r_P(n) = sum_{d | gcd(n,M)} mu(d) 2^(n/d).

Indeed D_d has 2^(n/d) words of length n when d divides n and none otherwise. Inclusion-exclusion and the displayed intersection identity give the formula. This is the same number as words of length n that are not p-th powers for any p in P: intersections of p-th-power sets are d-th-power sets, by the uniqueness of the primitive root. The latter identity can alternatively be proved through the stabilizer of a word under cyclic shifts.

The agreement holds by full letter content, too:

    r_P(i,j) = sum_{d | gcd(i,j,M)} mu(d) binomial((i+j)/d,i/d),

for i+j>=1. The map expanding each letter into d equal letters is a bijection from words with content (i/d,j/d) to D_d with content (i,j).

## 2. Arbitrarily fine exponential counting approximations

Take P to be all primes below a prime r. Primitive words are among words that are not p-th powers for p in P, so

    0 <= r_P(n)-psi(n) <= sum_{r<=d<=n, d|n} 2^(n/d) <= n 2^(n/r).

For the upper bound, every nonprimitive word counted by the finite power sieve has an exponent with no prime factor below r. Choose a prime divisor q>=r of that exponent; then the word is a q-th power. The union bound over such q gives the stronger sum over primes, and the displayed bound follows.

It follows that

    limsup_n (r_P(n)-psi(n))^(1/n) <= 2^(1/r).

Equality holds: choose n=r ell where ell ranges through primes larger than r and not in P. The r-th powers of primitive words of length ell all pass the finite sieve. There are psi(ell)=2^ell-2 of these. Thus the limsup is at least 2^(1/r).

Therefore, for every epsilon>0 there is an explicit regular language whose length-counting function majorizes that of Q and differs by exponential growth rate less than 1+epsilon. For all n with every prime factor in P, r_P(n)=psi(n) exactly.

The counting series of R_P is rational:

    sum_{n>=1} r_P(n) z^n
      = sum_{d|M} mu(d) 2 z^d/(1-2 z^d).

This supplies exact positive-coefficient rational models, rather than merely an arbitrary algebraic majorant.

## 3. Scope and explicit support mismatch

This is a barrier for arguments based only on aggregate counts or finitely many asymptotic exponential scales. It does NOT construct a grammar for Q: the supports differ. For P={2}, the primitive word aabb belongs to D_2 and is excluded by R_P, while the square abab belongs to R_P. Their exchange leaves the total counts consistent.

It also does NOT prove that r_P is the parse-count series of any grammar with support exactly Q. Assigning such multiplicities uniformly by a finite grammar remains an independent, unproved requirement. In particular, a bound on aggregate excess parses must not be confused with a bound on the number of parses of each word.
