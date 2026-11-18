# Round 4, agent "analytic": analytic/algebraic obstructions valid for ambiguous CFLs

**Claim level: no proof of either resolution.** What this report delivers:

* an exact map of which analytic statements survive ambiguity (§1–§2);
* a short answer to "is every CFL counting-equivalent to an unambiguous CFL?" (FALSE), with a
  one-line linear-language witness (§3);
* a sharpened barrier: binary CFLs realize the poles of Q(z) at 2^{-1/m} for every m in dℕ
  (any fixed d ≥ 2) (§4);
* a proof that the standard ambiguous constructions realize the **prime** radii 2^{-1/p} for only
  finitely many p (§4). From this comes a precise analytic conjecture (Conjecture A) that would
  imply "Q not CF". It is stronger than the target.

Tags: PROVED / COMPUTER-CHECKED / LITERATURE / CONJECTURED / IDEA.
Script: `context-free/round4/scripts/analytic/check_counts.py`. It does exact brute-force checks of
every closed form below, and all of them pass.

Notation:
* Σ = {a,b}.
* For L ⊆ Σ\*, L(z) = Σ_n |L ∩ Σ^n| z^n.
* Q(z) = Σ_{d≥1} μ(d)·2z^d/(1−2z^d).
* For a CFG G, N_G(w) is the number of parse trees of w.

---------------------------------------------------------------------------------------------

## 1. Supports of N-algebraic series carry exactly CF information (route (1) collapses)

**L1.1 (LITERATURE; standard: Chomsky–Schützenberger 1963; Salomaa–Soittola, *Automata-theoretic
aspects of formal power series*, 1978, Ch. IV; Kuich–Salomaa, *Semirings, Automata, Languages*, 1986,
the chapter on algebraic series; also quoted e.g. in arXiv:1802.03436 "Thm 5 in [14]").**
A language is context-free iff it is the support of some N-algebraic series in noncommuting
variables. For a (cycle-free) CFG G, S_G = Σ N_G(w) w is N-algebraic with supp S_G = L(G).
Conversely, a proper N-algebraic system is a CFG whose parse counts are the coefficients.

**Consequence (PROVED from L1.1).** "Q = supp S for some N-algebraic S" is *literally* "Q is CF".
Any theorem constraining supports of N-algebraic series is therefore a theorem about CFLs, and it
gives no new leverage. The noncommutative series adds only multiplicities, and the multiplicities
are unconstrained beyond ≥ 1 on the support. Repeating a rule (or adding a useless duplicate
nonterminal) multiplies them freely.

**L1.2 (commutative images carry only Parikh information). PROVED.**
(a) For N-algebraic S in noncommuting variables a,b, the support of its commutative image
c(S) = Σ_w S(w) x^{|w|_a} y^{|w|_b} is Ψ(supp S). There is no cancellation in ℕ, and by Parikh
this support is semilinear.
(b) Every semilinear set M ⊆ ℕ^2 is the support of a commutative N-rational series. Indeed
M = Ψ(R) for a regular R (each linear set c + ℕ{p_1..p_r} is Ψ(w_c (w_{p_1})^\* ⋯ (w_{p_r})^\*)),
and c(char R) is N-rational with support M.
(c) For every regular R, Ψ(Q ∩ R) is semilinear (closure.md, proved there for all rational
transduction images).
Hence for every regular R:
* the commutative image of any N-algebraic series supported on Q ∩ R has the same support as some
  N-rational series;
* its coefficient values are arbitrary ≥ 1 multiplicities on that support.

No theorem about commutative images of N-algebraic series (Pólya–Carlson, Fatou, Skolem–Mahler–Lech,
Pringsheim, …) can separate Q ∩ R from a regular language, because such theorems see either the
support (semilinear, matched by a regular language) or the multiplicities (free). ∎

Remark (LITERATURE / folklore, not needed): supports of **ℤ**-rational series are not always CF.
For example, S(a^i b a^j b) = i − j² is ℤ-rational and its support has non-semilinear Parikh image.
So ℤ-supports are a strictly larger class. The characteristic series of Q is not ℤ-algebraic, since
its commutative image Q(z) is not algebraic (Petersen). I found no theorem that constrains supports
of ℤ-algebraic series in a way that would bear on Q. Skolem–Mahler–Lech (unary ℤ-rational supports
are ultimately periodic) is a statement about unary or bounded objects only, and Q's bounded slices
have rational, Ginsburg-type structure anyway.

## 2. Bounded slices and the multi-block bivariate object

**L2.1 (LITERATURE: Ginsburg 1966, Thm 5.4.2 + Eilenberg–Schützenberger/Ito unambiguous
decomposition of semilinear sets; already used in bounded.md/ambiguity.md).**
If L ⊆ w_1\*⋯w_k\* is CF, then L(z) and its multivariate exponent series are rational.

**L2.2 (exact bivariate series of Q ∩ (ab\*)^+). PROVED; COMPUTER-CHECKED (n,m ≤ 6).**
Let t mark the a's (blocks) and y mark the b's, and let E_n be the primitive exponent vectors. Then

  F_Q(t,y) = Σ_n t^n Σ_{x∈E_n} y^{|x|} = Σ_{d≥1} μ(d) t^d / (1 − y^d − t^d).

*Proof.* By Möbius over periods (ambiguity.md Lemma 3.1), the t^n-section is
Σ_{d|n} μ(d)(1−y^d)^{−n/d}. Sum the geometric series in u = t^d/(1−y^d). ∎

Here the t^n-section f_n(y) has a simple pole at every primitive n-th root of unity iff μ(n) ≠ 0
(only the term d = n is singular there).

**Barrier 2.3 (PROVED).** Take

  L1′ = (ab\*)^\* {a b^i a b^j : i ≠ j} (ab\*)^\*.

It is CF, in fact a concatenation of regular, linear and regular languages. It has

  E_n(L1′) = {x ∈ ℕ^n : x not constant},

since a word of (ab\*)^+ has a unique block factorization and lies in L1′ iff two adjacent blocks
differ. So its t^n-section is (1−y)^{−n} − (1−y^n)^{−1}, which has a pole at every primitive n-th
root of unity for **every** n ≥ 2. Bivariate:

  F_{L1′} = t/(1−y−t) − Σ_n t^n/(1−y^n).

Therefore the pole data of the sections (root-of-unity orders unbounded in n, pole orders, residues
of Möbius type) is realized by an ambiguous CFL. The bivariate analytic object (t, y) cannot
separate Q. More generally, whatever information an analytic object in finitely many variables
records about L ∩ (ab\*)^+, it is a function of the Parikh-type data of the slices. The only content
there is the slice structure itself, i.e. the Kászonyi–Katsura (KK) question plus uniformity in n.

**IDEA 2.4 (uniform bounded periods; sketch, not fully written).** If Q has a CNF grammar with g
nonterminals, then every pump in the Bar-Hillel product with the DFA of (ab\*)^n is b-only. Its spine
labels are (s,·,t), and its side subtrees are labelled (s,·,s) or (t,·,t). So minimal pumps have
height O(g), and **period vectors of norm ≤ C(g) independent of n**. Presumably, then:

  for every n, E_n is a finite union of stratified linear sets whose period vectors all have
  ℓ1-norm ≤ C, with C uniform in n.

The step I have not written is the label-set-preserving pump removal of the Parikh decomposition with
an n-free height bound. Assessment: this is a valid uniform strengthening of KK in principle, but
every known stratified cover (bounded.md L3, L4, C1; ambiguity.md Thm C) uses periods with entries
in {0,1}. So it is almost certainly **not** an obstruction.

## 3. Is every CFL counting-equivalent to an unambiguous CFL? FALSE

**L3.1 (LITERATURE).**
* Unambiguous CFLs have algebraic counting series (Chomsky–Schützenberger 1963).
* Flajolet, "Analytic models and ambiguity of context-free languages", TCS 49 (1987) 283–309 (INRIA
  RR-0483, 1986), proves inherent ambiguity of several CFLs by showing their counting series are
  transcendental. The best-known example is attributed to Flajolet in the literature: the Goldstine
  language, whose series involves the lacunary Σ z^{n(n+1)/2}. I did not verify that attribution
  against the paper.
* Hence some CFLs have counting sequences that are those of **no** unambiguous CFL.
* The only analytic constraints I know of that hold for **all** CFLs are:
  - the polynomial/exponential growth gap (Incitti, TCS 2001; Bridson–Gilman 2002);
  - rationality of bounded CFLs (L2.1).

Kemp and Baron–Kuich (finite-index and density results) concern restricted classes. I could not
access them and do not rely on them.

**Theorem 3.2 (self-contained witness). PROVED; COMPUTER-CHECKED n ≤ 16.**
L1 = (a\*b)^\*{a^i b a^j b : i ≠ j}(a\*b)^\* is a **linear** CFL with
|L1 ∩ Σ^n| = 2^{n−1} − d(n), where d(n) is the number of divisors of n. So

  L1(z) = z/(1−2z) − Σ_{e≥1} z^e/(1−z^e).

This is transcendental: the Lambert series is unbounded along every radius ending at a root of
unity, so |z| = 1 is a natural boundary, while an algebraic function has finitely many
singularities. Hence L1 is inherently ambiguous, and its counting sequence is that of no
unambiguous CFL.

*Proof of the count.* (a\*b)^+ ∩ Σ^n has 2^{n−1} words, namely those ending in b. Each factors
uniquely into blocks a^{m_i}b, and it lies in L1 iff two adjacent blocks differ. The complement in
(a\*b)^+ is {(a^{e−1}b)^{n/e} : e | n}, which has d(n) words. ∎

So the question in the brief has a definite answer: **the counting series of an arbitrary CFL can
be non-algebraic, and even non-D-finite with a natural boundary.**

Still open (PARALLEL_CAMPAIGN_FINDINGS §6, item 9): is (q(n)) itself the counting sequence of some
CFL? "No" would imply Q not CF. That statement is stronger than the target.

## 4. Pole radii: composite radii are cheap, prime radii are not (new)

Q(z) is meromorphic in |z| < 1. For every prime p, it has a simple pole at every ζ with ζ^p = 1/2
(PROVED, scout.md: only the d = p term is singular at ζ). The question is which of these features an
ambiguous CFL over the **same** binary alphabet can reproduce.

**Construction 4.1 (complement of single-codeword repetitions). PROVED.**
Let X ⊆ Σ^+ be a regular prefix code. Put

  L_X = X^\* · D_X · X^\*,  with D_X = {xy : x,y ∈ X, x ≠ y}.

(i) L_X is CF. D_X is the image of ({u#v : u ≠ v} ∩ X#X) under erasing #, which is CF ∩ regular
followed by a morphism.
(ii) L_X = X^+ \ {x^k : x ∈ X, k ≥ 1}, because factorizations over a code are unique.
(iii) Since x^k = y^j with x,y ∈ X forces x = y and k = j,

  L_X(z) = X/(1−X) − Σ_{k≥1} X(z^k).

**Theorem 4.2 (binary CFLs with poles at 2^{-1/m} for all m ∈ dℕ). PROVED; COMPUTER-CHECKED (d=2, n ≤ 18).**
Fix d ≥ 2 and let X_d = (aΣ^{d−1})^\* b. This is a complete prefix code with
X_d(z) = z/(1−2^{d−1}z^d). Then L_{X_d}(z) has:
* a simple pole at z = 1/2 (growth 2, as for Q);
* for all but finitely many j ≥ 1, a simple pole at **every** z with z^{dj} = 1/2.

So these poles have modulus 2^{-1/(dj)}, and they accumulate on |z| = 1, which is a natural
boundary.

*Proof.*
* Kraft gives X_d(1/2) = 1, so 1 − X_d vanishes at 1/2. The derivative of 1 − X_d is negative
  there (positive coefficients), so the zero is simple.
* Put k = (d−1)j. The term X_d(z^k) has simple poles where z^{kd} = 2^{−(d−1)}. That set contains
  all z with z^{dj} = 1/2.
* Another term X_d(z^{k′}) is singular there only if |z|^{k′d} = 2^{−(d−1)}, i.e. k′ = k.
* The tail Σ_{k′>K} X_d(z^{k′}) converges uniformly on |z| ≤ r < 1.
* X/(1−X) has finitely many poles.

For d = 2 the counts are 0,0,0,4,6,18,34,84,152,336,…, matching brute force. ∎

**Theorem 4.3 (prime radii are rare for these constructions). PROVED.**
Let X be any regular code over Σ (|Σ| = 2). Then the set of primes p such that L_X(z) has a
singularity of modulus 2^{-1/p} is finite. The same holds for any function in the ring generated
by rational functions and finitely many such L_X(z). This ring includes finite unions of the L_X
with disjoint regular "tags" and products with regular languages.

*Proof.*
* By McMillan, X(1/2) ≤ 1. X is rational with nonnegative coefficients, so by Pringsheim its radius
  ρ_X is a pole. That forces ρ_X > 1/2, since X(r) ↑ ∞ as r ↑ ρ_X.
* So every pole σ of X has |σ| = 2^{−α} with α < 1, and there are finitely many such σ.
* The singularities of L_X(z) in |z| < 1 lie among the finitely many poles of X/(1−X) and the
  points with z^k = σ, which have modulus 2^{−α/k}.
* 2^{−α/k} = 2^{−1/p} means α = k/p < 1, so k < p, gcd(k,p) = 1, and α has reduced denominator
  exactly p.
* Hence each pole modulus of X yields at most one prime. The ring statement follows because
  singular sets of sums and products lie in the union of the factors' singular sets. ∎

The same argument covers the marker construction of PARALLEL_CAMPAIGN_FINDINGS Thm 6.2 after its
binary coding: radii x_0^{1/m}, with x_0 a fixed algebraic number, give at most one prime. It covers
any alphabet size s ≥ 2 with 2 replaced by s (Kraft: X(1/s) ≤ 1).

**Why prime radii are hard (IDEA, with two proved observations).**
* A pole of modulus 2^{-1/p} needs a family of about 2^{n/p} words of length n that are "a free
  binary word of length n/p plus deterministic redundancy" at full entropy.
* Over 3 letters this is easy. X = {a,b}^\*c gives L_X(z) = z/(1−3z) − Σ_k z^k/(1−2z^k), with poles
  at z^k = 1/2 for **all** k (PROVED by 4.1). So any obstruction must use that the alphabet size
  matches the base of the radius.
* The obvious binary attempts to get unboundedly many primes fail through non-semilinearity
  (PROVED for these specific languages). Examples:
  - the prefix code {a^j b (aΣ^{j−1})^m b} meets a^+ba^\*b in {a^j b a^{jm} b};
  - the marker language {a^p b v : v ≠ u^p} meets a^+bb^\* in {a^p b^{m+1} : p ∤ m}.
  Both Parikh images are non-semilinear, so these languages are not CF. Entropy-free unary markers
  of p are visible to Parikh. Markers invisible to Parikh bring back the Q problem itself.

**Conjecture A (CONJECTURED; sufficient for the target, and stronger than it).** If L ⊆ {a,b}^\*
is CF and L(z) continues meromorphically to |z| < 1, then L(z) has poles of modulus 2^{-1/p} for
only finitely many primes p.
* A ⇒ Q not CF, by the scout/Petersen pole computation.
* Theorems 4.2 and 4.3 show that A is sharp in two ways:
  - "prime" cannot be weakened to "infinitely many m" (4.2);
  - "binary" cannot be weakened to "radius 2^{-1/p} over a larger alphabet" (the ternary L_X).
* Status: A is a statement about all CFLs, and its proof would need a structure theory for word
  counts of ambiguous grammars (the N_2-type terms of PARALLEL_CAMPAIGN_FINDINGS §6) that does not
  exist. I do not expect it to be easier than the target. Its value is as a precise test: anyone
  who believes Q is CF must produce a binary CFL with infinitely many prime radii. No such CFL is
  known, and none arises from §3–§4 constructions.

---------------------------------------------------------------------------------------------

## Registry entry

1. **Statement aimed at:** an analytic or algebraic invariant of arbitrary (ambiguous) CFLs that Q
   (or Q ∩ R for regular R) violates.
2. **Strongest proved:**
   * (L1.1–1.2) Noncommutative N-algebraic supports are exactly the CFLs. Commutative images carry
     exactly the semilinear support, which every Q ∩ R satisfies. So routes via supports or
     commutative images are tautological or dead.
   * (2.3) The bivariate block/length series and its section pole data are matched by the linear
     CFL L1′.
   * (3.2) "Every CFL is counting-equivalent to an unambiguous CFL" is FALSE. Witness: the linear
     L1 with count 2^{n−1} − d(n).
   * (4.2) Binary CFLs have poles at 2^{-1/m} for all m ∈ dℕ.
   * (4.3) Code-complement constructions, and the ring they generate with rational functions, hit
     only finitely many prime radii 2^{-1/p}.
3. **Missing step:** Conjecture A. For every binary CFL L with L(z) meromorphic in |z| < 1,
   #{p prime : L(z) has a pole of modulus 2^{-1/p}} < ∞.
   A weaker variant would also suffice: the same for every L with L(z) = Q(z), i.e. "(q(n)) is not
   the counting sequence of a CFL".
4. **Counterexamples found:**
   * to "CFL counting series are algebraic/D-finite/finitely singular" (L1, L_{X_d});
   * to "the bivariate sections have bounded pole orders or bounded root-of-unity orders" (L1′);
   * to "infinitely many radii 2^{-1/m} ⇒ not CF" (Thm 4.2).
5. **Relative strength:** Conjecture A is **stronger** than "Q not CF", since it implies it and
   speaks about all CFLs. The variant "(q(n)) is not a CFL counting sequence" is also stronger
   (sufficient, not necessary). IDEA 2.4 is a necessary condition for Q CF, i.e. a weaker target,
   but it is almost certainly satisfied.
6. **What would reopen the route:** either of
   * a structure theorem for word-count series of ambiguous grammars, e.g. that L(z) lies in a
     ring generated by algebraic series and finitely many "Lambert-type" sums Σ_k A(z^k) with A
     algebraic of radius > 1/2;
   * an explicit binary CFL with poles at 2^{-1/p} for infinitely many primes p, which would refute
     A and show counting cannot help even in principle.

The first would make Theorem 4.3's argument apply to all CFLs and prove Q not CF. Such a theorem
is not known.
