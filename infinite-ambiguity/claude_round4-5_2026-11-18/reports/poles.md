# Round 4, agent "poles": attacking Conjecture A (prime pole radii 2^{-1/p} for binary CFLs)

**Claim level: no proof of either resolution. Conjecture A is neither refuted nor proved.**

What this report delivers:
* a "seed lemma": the Lambert/code mechanism can never create prime radii by itself, for any code;
* a general non-CF lemma for the unary-marker mechanism;
* an excess-normalised power set whose complement would have singularities at every radius
  2^{-1/t}. It is not meromorphic, and I could not decide whether that complement is CF;
* a precise statement of the missing step.

Script: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/poles/check.py`. It brute-forces every count and
characterisation below for n ≤ 16, all pass, and it runs in under a minute on one core.

Notation:
* Σ = {a,b}.
* For L ⊆ Σ*, L(z) = Σ|L∩Σ^n| z^n.
* For a series F that is meromorphic in |z| < 1, write
  - Π_1(F) = {p prime : F has a pole of modulus 2^{-1/p}};
  - Π(F) = {p : F has a pole of modulus 2^{-j/p} for some 1 ≤ j < p}.

## 0. Refutation attempts (summary)

| attempt | outcome |
|---|---|
| L_X = X^+ \ {x^k} for a non-regular CF code X | Prime poles of L_X need poles of X or X^+ with prime denominators (§1, PROVED). The construction is seeded and cannot create new primes. |
| radius-1/2 CF codes (Dyck primes, first-passage ballot code) | X(z^k) is branch-singular, so the result is not meromorphic. Also L_X ∩ a⁺b⁺a⁺b⁺ ⊇ {a^i b^i a^j b^j : i≠j}-type slices, so L_X is not CF (IDEA, standard pumping, not written). |
| unary marker a^k b v with "v not a k-th power of a Y-word" (Y full entropy) | Not CF whenever Y contains all powers of one primitive word (§2, PROVED). |
| block count read from the Parikh excess (self-marker) | The excluded set S is exactly computable (§3, PROVED and checked). Its complement T would have singularities at all 2^{-1/t}, but T(z) is **not meromorphic** (branch points), and whether T is CF is unknown (it looks Q-hard). |
| alternating mirror blocks u u^R u u^R … with a k-marker | Escapes the bounded-slice test of §2, but the grammar must locate block boundaries at multiples of n/k (multiplicative). No CF grammar found (IDEA). |

## 1. Seed lemma: Lambert sums over codes only propagate primes already present (PROVED)

**Lemma 1.** Let X ⊆ Σ⁺ be any code (no context-freeness assumed) whose series X(z) is meromorphic
in |z| < 1. Let L_X = X⁺ \ {x^k : x ∈ X, k ≥ 1}. Then L_X(z) is meromorphic in |z| < 1, and

  Π_1(L_X) ⊆ Π(X) ∪ Π_1(X⁺).

*Proof.*
1. **Identity.** Factorisation over a code is unique, and x^k = y^j with x, y ∈ X forces x = y and
   k = j. Hence L_X(z) = X⁺(z) − Σ_{k≥1} X(z^k), where X⁺(z) = X/(1−X) is meromorphic.
2. **Convergence.** The coefficients of X are ≤ 2^n, so |X(w)| ≤ 2|w|/(1−2|w|) ≤ 4|w| for
   |w| ≤ 1/4. On |z| ≤ r < 1, take K with r^K ≤ 1/4. Then Σ_{k≥K} |X(z^k)| ≤ 4Σ r^k uniformly,
   which gives meromorphy. The poles of L_X lie in
   (poles of X⁺) ∪ {z : z^k = σ, σ a pole of X, k ≥ 1}.
3. **McMillan's inequality** (valid for every code) gives X(1/2) ≤ 1. Hence |X(z)| ≤ X(|z|) ≤ 1 on
   |z| ≤ 1/2, so every pole σ of X has |σ| = 2^{-α} with 0 < α < 1.
4. **Matching moduli.** A point with z^k = σ has modulus 2^{-α/k}. If 2^{-α/k} = 2^{-1/p}, then
   α = k/p with k < p, so p ∈ Π(X). ∎

**Consequence.** The repetition-complement construction cannot manufacture prime radii. Any
refutation of A through L_X needs a CF code X (or X⁺) that **already** has poles of modulus
2^{-j/p} for infinitely many primes p. That is a variant of A for codes, so the mechanism is
circular.

The binary-specific obstruction is exactly step 3: the only Lambert sums Σ_k F(z^k) that put poles
at 2^{-1/k} for all k are those where F has a pole at modulus 1/2. Over 3 letters, X = {a,b}*c has
X(z) = z/(1−2z), with a pole at 1/2 (Kraft only bounds X(1/3)). Over 2 letters no code can have
this.

Lemma 1 also extends Theorem 4.3 of analytic.md from regular X to arbitrary codes with meromorphic
series.

## 2. Unary-marker constructions are never CF (PROVED)

**Lemma 2.**
* Let w₀ be a primitive word.
* Let Y ⊆ Σ⁺ contain w₀^s for every s ≥ 1.
* Let M_Y = {a^k b v : k ≥ 1, v ∈ Σ⁺, v ∉ {u^k : u ∈ Y}}.

Then M_Y is not CF.

*Proof.*
1. **Which w₀-powers are excluded.** Suppose w₀^r = u^k. Since w₀ is primitive, k | r and
   u = w₀^{r/k}, and u ∈ Y. Hence a^k b w₀^r ∈ M_Y iff k ∤ r. (COMPUTER-CHECKED for Y = aΣ*,
   w₀ = ab, k < 12, r < 30.)
2. **Transfer to a bounded language.** The factorisation of a word of a*b w₀* is unique: the first
   b ends the a-block, and w₀ is primitive. So a rational transduction maps M_Y ∩ a*b w₀* onto
   {a^k b c^r : k ≥ 1, r ≥ 1, k ∤ r}.
3. **Semilinearity.** If M_Y were CF, this image would be CF, and its Parikh set
   D' = {(k, r) : k ∤ r} would be semilinear. Semilinear sets are Presburger-definable and closed
   under complement, so D = {(k, r) : k | r} would be Presburger-definable.
4. **Contradiction.** Then the set of primes {n ≥ 2 : ∀i (2 ≤ i < n → (i, n) ∉ D)} would be
   Presburger-definable, hence ultimately periodic. It is not. ∎

**Coverage.** This covers:
* Y = Σ⁺ and Y = aΣ* (take w₀ = ab);
* every Y ⊇ xΣ*y with xy primitive (take w₀ = xy, since (xy)^s = x(yx)^{s−1}y);
* hence every full-entropy regular "block set" of that shape.

Lemma 2 generalises the two examples in analytic.md §4. In every case the excluded count would be
Σ_k z^{k+1}·Y(z^k), with poles at z^k = 1/2 for all k when Y = aΣ*. The count formula is
COMPUTER-CHECKED for n ≤ 16. **So M_{aΣ*}, if it were CF, would refute A, and it is not CF.**

## 3. Excess as a self-marker (PROVED characterisation; CF-ness OPEN)

Let exc(v) = |v|_b − |v|_a. Put S = {v : exc(v) ≥ 1 and v is an exc(v)-th power}.

**Lemma 3.** For v with exc(v) ≥ 1: v ∈ S iff the primitive root of v has excess 1. Hence

  S = {u^t : exc(u) = 1, t ≥ 1}  and  S(z) = Σ_{t≥1} E₁(z^t),
  with E₁(z) = Σ_m C(2m+1, m) z^{2m+1}.

*Proof.*
* Write v = w₀^s with w₀ primitive. Then exc(w₀) = exc(v)/s.
* Since w₀ is primitive, v is an e-th power iff e | s.
* With e = exc(v) = s·exc(w₀), this holds iff exc(w₀) = 1, and then v = w₀^e.
* Words of excess 1 are primitive, since u = y^j forces j | 1. So the representation u^t is
  unique, which gives the series. ∎

COMPUTER-CHECKED n ≤ 16.

E₁ has its inverse-square-root branch points at z = ±1/2. So E₁(z^t) is singular, and **not**
polar, at modulus 2^{-1/t}.

The CFL {exc ≥ 1} minus S, call it T, would therefore have singularities at **every** radius
2^{-1/t}, but T(z) is not meromorphic. Here the "number of blocks" is read from the Parikh vector,
so the bounded-slice test of Lemma 2 does not fire: on (b^i a^j)^r, membership depends only on
i − j = 1. However, T ∩ {exc = e} = {exc = e} ∩ coPow_e, which needs a length split at n/e with
e unbounded. I found no CF grammar, and I could not prove T is not CF.

* Status: OPEN (IDEA).
* Even a CF T would only show that A's meromorphy hypothesis is essential. It would not refute A.

## 4. What is missing

The analysis shows that every known CF way to produce radii 2^{-1/k} is a k-fold repetition of
blocks from a block set F. The block boundaries must be located by the grammar, and this fails in
each case:
* boundaries delimited by a code: F has no pole at modulus 1/2 (McMillan, Lemma 1);
* boundaries delimited by a unary length marker: non-semilinear divisibility (Lemma 2);
* boundaries delimited by Parikh/self-marking: either non-meromorphic or Q-like (Lemma 3);
* boundaries delimited by a radius-1/2 nested code: adjacent comparison crosses the nesting.

A proof of A would need a structure theorem making "repetition with grammar-located boundaries" the
**only** source of rational-exponent poles. Precisely:

**Missing Lemma (CONJECTURED).** For every CFG G over Σ with L(G)(z) meromorphic in |z| < 1, there
are
* finitely many series F_1, …, F_r, each the series of a language over Σ that is a code or a
  regular language,
* and a series H with Π_1(H) finite,

such that every pole of L(G) of modulus 2^{-1/p}, for p large, is a pole of some F_i(z^k).

Combined with Lemma 1 (codes) and Pringsheim/Kraft (regular F), this yields A. It is plainly at
least as hard as A. No such structure theory for ambiguous grammars exists.

## Registry entry

1. **Statement aimed at:** refute Conjecture A (a binary CFL, meromorphic in |z| < 1, with poles of
   modulus 2^{-1/p} for infinitely many primes p), or else prove A or a variant of it.
2. **Strongest lemmas proved:**
   * Lemma 1 (seed lemma): for every binary code X with meromorphic series,
     Π_1(L_X) ⊆ Π(X) ∪ Π_1(X⁺), via McMillan.
   * Lemma 2: unary-marker complements M_Y are not CF whenever Y ⊇ w₀⁺, w₀ primitive.
   * Lemma 3: an exact characterisation and series of the excess-normalised power set.
   * All three are PROVED; the counts are COMPUTER-CHECKED n ≤ 16.
3. **Missing step:** the Missing Lemma of §4. Equivalently for this route, Conjecture A itself:
   ∀ CF L ⊆ Σ* with L(z) meromorphic in |z| < 1, Π_1(L) is finite.
4. **Counterexamples found:** none to A. Lemma 3 gives a candidate showing that the meromorphy
   hypothesis would be essential, but its CF-ness is open.
5. **Relative strength:** A and the Missing Lemma are **stronger** than "Q not CF".
6. **What would reopen the route:**
   * a refutation needs a CF mechanism that locates block boundaries of a full-entropy block set
     for unboundedly many block counts, without codes (Lemma 1) and without unary length markers
     (Lemma 2). The test cases are T of §3 and the alternating-mirror language;
   * a proof needs a pole-structure theorem for ambiguous grammars.
