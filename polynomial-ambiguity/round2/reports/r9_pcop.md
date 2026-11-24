# R9-A: ¬P_cop via Wich structure: a model-theoretic no-go for every Theorem-U-type extension

Notation as in `R2/pcop.md`. Row N means {w : #a(w) = N}. For w with #a(w) = N ≥ 1, write w = b^s a b^{y_1} a ⋯ a b^{y_{N−1}} a b^t.
Its **cyclic gap sequence** is γ(w) = (y_1, …, y_{N−1}, s+t). It is a complete invariant of the conjugacy class of w.
Script: `round2/scripts/r9_pcop_prime_rows.py`.

## 0. Summary

| item | status |
|---|---|
| **U′ (what Theorem U actually proves).** No unambiguous CFL L has Cop ⊆ L and L ∩ row p ⊆ Q for infinitely many primes p. | [written proof] (it is U's proof verbatim; only those hypotheses are used) |
| **Theorem N (no-go).** There is an explicit CFG G_P with ambiguity ≤ max(1, #a(w) − 1) ≤ \|w\| for every w. Its language L_P satisfies Q ⊆ L_P, and every w ∈ L_P ∖ Q has #a(w) composite. So L_P ∩ row p = Q ∩ row p for **every** prime p. | [written proof] + [computational] (grammar trees counted exactly for all words with \|w\| ≤ 15, 0 failures) |
| Two-letter version: a PCFL L_P2 ⊇ Q such that every w ∈ L_P2 ∖ Q has **both** #a(w) and #b(w) composite. | [written proof] + [computational] (\|w\| ≤ 15) |
| Cor: L_P is inherently ambiguous, with linear ambiguity (U′ applied to L_P). | [written proof] |
| **Consequence for the task.** Any proof of ¬P_cop (counting or not, via Wich markers, pattern splitting, roots-of-unity evaluation, or Möbius/inclusion–exclusion) must use L ⊆ Q on words whose #a and #b are both composite. Every Theorem-U-type row argument is therefore dead for polynomial ambiguity. | [written proof] (model-theoretic: L_P2 is a model of all the other hypotheses) |
| Generalisation L_M (fixed M): the obstruction must come from non-primitive words v^d where #a(v) ∤ M, for every fixed M. So the roots involved must have unboundedly many a's. | [written proof sketch] (§4) |
| Idea (2) (an exact algebraic series vanishing exactly on coprime classes): such a series with nonnegative coefficients cannot exist **for any language** (U*). Signed (Möbius) versions lose Pringsheim. Inclusion–exclusion terms Σ C(amb(w),k) are not algebraic in general. | [written proof] (U*), [assessment] (signed) |
| ¬P_cop | **OPEN**. Exact remaining requirement: §5 |

Verdict: the requested extension of Theorem U does **not** exist in the requested form. This is not a failure of technique: there
is a concrete polynomially (linearly) ambiguous language that satisfies every hypothesis Theorem U consumes.

## 1. What Theorem U consumes (U′)

Read the proof in `R2/pcop.md` §5. For a prime p > max(|S|, m) it uses exactly three things:
1. G = 1/(1−x−y) − F_L is algebraic, which holds because L is unambiguous.
2. e_{pj} = 0 for p ∤ j. This uses only Cop ⊆ L, restricted to row p.
3. e_{p,pk} ≥ 1 for infinitely many k, which gives radius 1. This uses only L ∩ row p ⊆ Q, through (ab^k)^p ∉ L.

So the proof establishes **U′**: no unambiguous CFL L satisfies Cop ⊆ L together with L ∩ row p ⊆ Q for infinitely many primes p.
Nothing about L on composite rows is used.

Abstract form **U\***: no algebraic G = Σ e_{ij} x^i y^j has all of the following:
- e ≥ 0;
- e_{ij} = 0 whenever gcd(i, j) = 1;
- for infinitely many primes p, the row series g_p has infinitely many nonzero coefficients and radius ≥ 1.

The proof is U's proof with "L" deleted.

## 2. Theorem N: a linearly ambiguous model of U′'s hypotheses

Let N_a = {v^n : n ≥ 2, #a(v) = 1}. These are the non-primitive words whose primitive root has exactly one a; a^n is included.
Define
  L_P = Σ⁺ ∖ ({b^m : m ≥ 2} ∪ N_a).

**Lemma 1.** Let #a(w) = N ≥ 2. Then w ∈ N_a ⇔ γ(w) is constant ⇔ [y_i = y_{i+1} for all 1 ≤ i ≤ N−2, and y_{N−1} = s+t].
*Proof.* w = v^N with v = b^s a b^{k−s} iff every cyclic gap equals k. Conjugates of powers are powers. The right-hand condition says
exactly that all entries of γ(w) are equal. ∎

**Lemma 2 (where L_P differs from Q).** Q ⊆ L_P. Moreover, w ∈ L_P ∖ Q ⇔ w = v^d with v primitive, d ≥ 2 and #a(v) ≥ 2. For such w,
#a(w) = d·#a(v) is composite.
*Proof.* The excluded set consists of non-primitive words. Let w be non-primitive with primitive root v and exponent d ≥ 2. If #a(v) = 0 then w = b^d, which is excluded.
If #a(v) = 1 then w ∈ N_a, which is excluded. Otherwise w ∈ L_P and #a(w) = d·#a(v) with both factors ≥ 2. ∎
**Corollary.** For every prime p, L_P ∩ row p = Q ∩ row p. Also Cop ⊆ Q ⊆ L_P.

**Grammar G_P** (the same grammar is in the script). Write Σ* for ST → aST | bST | ε, b* for BS → bBS | ε, and b⁺ for BP → bBS.
```
S   → ONEA | b | W1 | W2
ONEA→ BS a BS                                   (exactly one a)
W1  → ST a K a ST,  K → K1 | K2                 (an internal witness y_i ≠ y_{i+1})
K1  → b K1 b | BP a        (b^{y+d} a b^y)      K2 → b K2 b | a BP   (b^x a b^{x+d})
Z   → a | a ST a                                (from the first a to the penultimate a)
A   → b A b | Z            (b^s Z b^s)
C   → b C b | BP a         (b^{t+d} a b^t)      E → b E b | a BP     (b^e a b^{e+d})
F   → b F b | BP Z         (b^x b^d Z b^x)
W2  → A C | A E | F a BS                        (the wrap witness y_{N−1} ≠ s+t)
```
- *Language.* Let N = #a(w) ≥ 2. W2 generates b^s Z b^x a b^t with x = y_{N−1} ≠ s+t, split into three cases: A·C when x > s+t, A·E when
  s ≤ x < s+t, and F a b* when x < s. W1 generates the words having some i ≤ N−2 with y_i ≠ y_{i+1}. By Lemma 1, W1 ∪ W2 =
  {#a ≥ 2} ∖ N_a. Together with ONEA ∪ {b} this gives exactly L_P.
- *Ambiguity.* ONEA, {b}, W1 and W2 are pairwise disjoint except W1 ∩ W2.
  - Within W2, the three cases are disjoint. Each parse is forced, since s, Z (it ends at the penultimate a), x and t are determined by w.
  - Within W1, a parse is determined by the position of the witness factor a b^x a b^y a.
  - Hence amb(w) = #{i ≤ N−2 : y_i ≠ y_{i+1}} + [y_{N−1} ≠ s+t] ≤ N − 1 for N ≥ 2, and amb(w) = 1 for N ≤ 1.
- *Cycle-free.* Every rule other than a unit rule increases length, and the unit rules (S→ONEA, S→W1, S→W2, K→K1, K→K2, A→Z) are acyclic.
- [computational: `r9_pcop_prime_rows.py 15`. Language equality, Q ⊆ L_P, the composite-row property, and amb ≤ max(1, N−1) all hold, with
  trees counted exactly by DP. 0 failures on all 65 534 words with |w| ≤ 15.]

**Corollary N1.** L_P is inherently ambiguous, by U′, and its ambiguity is linear. This is a new, very simple inherently ambiguous CFL whose
non-unambiguity is certified by the coprime-row singularity argument.

**Two-letter version.** Let L_P2 = Σ⁺ ∖ (N_a ∪ N_b ∪ {a^m, b^m : m ≥ 2}), with N_b obtained from N_a by swapping the letters.
- Words of N_a other than a^n contain no aa, and words of N_b other than b^n contain no bb.
- Split Σ⁺ by the pair [contains aa, contains bb]:
  - both: everything is included (regular);
  - only bb: L_P ∩ (that regular set);
  - only aa: swap(L_P) ∩ (that regular set);
  - neither: the alternating words, minus (ab)^n and (ba)^n for n ≥ 2 (regular).
- So L_P2 is a union of 4 polynomially ambiguous CFLs, hence polynomially ambiguous (ambiguity ≤ |w| + O(1)).
- Every w ∈ L_P2 ∖ Q is a power v^d, d ≥ 2, whose root has ≥ 2 a's and ≥ 2 b's. So #a(w) and #b(w) are both composite.
- [computational: the piece decomposition and the composite property are checked for |w| ≤ 15, 0 failures.]

## 3. Why this kills ideas (1) and (2) (exact logical form)

Let H(L) be the conjunction of these hypotheses:
- L = h(L′) for an unambiguous L′ with Parikh-bounded markers (equivalently, L is a PCFL, by Wich 2001);
- Cop ⊆ L;
- L ∩ {w : #a(w) or #b(w) is prime} ⊆ Q.

L_P2 satisfies H. So **no argument whose hypotheses are only H can reach a contradiction**, whatever machinery it uses:
- marker-pattern decompositions L′ = ⊎_π L′_π;
- evaluation of marker variables at roots of unity;
- position-weighted series B_R(z, t) (the "only residual" of `PA/poly_M.md`);
- singularity analysis of rows;
- inclusion–exclusion over marker subsets.

L_P2's own Wich representation (markers on the witness pair) is a concrete unambiguous L′ on which all of these can be computed, and
they yield no contradiction, because there is none to find.

Specifically:
- **Idea (1).** Every exact series built from L′ (restrictions to regular R′ ⊆ (Σ∪Γ)*, marker substitutions, Hadamard products with rational
  series) satisfies, for L_P2, the same row-p identities that a hypothetical sandwich would satisfy on prime rows. Any contradiction would have to come from
  composite rows. The inclusion–exclusion between patterns π, π′ requires |h(L′_π) ∩ h(L′_π′)|. That is an intersection of PCFLs, with no
  algebraic GF in general (`PA/poly_M.md`, failing step 2). It is also unnecessary, since one pattern suffices for L_P2.
- **Idea (2).** The target object is "an exact algebraic series, ≥ 0, vanishing exactly on coprime classes and with infinite support in infinitely many
  prime rows". By U\* it does not exist for **any** language. So the entire content of idea (2) would be its construction from (L, L ⊆ Q). That construction
  must read L ⊆ Q on composite rows (Theorem N), but its output is only inspected on prime rows. The construction therefore has to transport composite-row
  information into prime rows. No operation in the allowed list (§5 of the prompt) does this: DFA products, CNF, rotations and code pullbacks all
  preserve rows, or map row N to row c·N (h_p). The h_p pullback (Prop H) goes the wrong way: it moves row pq of L to row q of L′ = h_p⁻¹(L).
  That does feed composite-row information into a prime row, but L′ is again only a PCFL sandwich, so we are back at the start.
- **Signed / Möbius variants.** Σ_w [amb(w) ≥ 1] = Σ_{k≥1} (−1)^{k+1} Σ_w C(amb(w), k).
  - The k ≥ 2 terms count k-sets of marked preimages of the same word. That is an intersection of CFLs, and it is not algebraic in general:
    Flajolet-type ambiguity-2 CFLs have a transcendental GF while their multiplicity series is algebraic.
  - A signed series also loses Pringsheim: φ(y^p) with signed coefficients need not be singular at 1.
  - [assessment]

## 4. Generalisation: the obstruction needs roots with unboundedly many a's

Fix M ≥ 1. Let L_M consist of:
- all words with #a ≤ M, and all words with #a = 0;
- the words with #a = N > M whose cyclic gap sequence is not M-periodic, i.e. some i has γ_i ≠ γ_{i+M} (indices mod N).

Properties:
- *PCFL.* A witness is either internal, a factor a b^x (a b*)^{M−1} a b^y a with x ≠ y, or one of finitely many (M) wrap-around comparisons
  between gaps near the two ends, using the outer gap s+t. Each witness type is a linear-ambiguity CFL built like W1/W2. "N > M" is regular.
- *Soundness side.* L_M ⊇ Q. If γ is M-periodic then it is gcd(M, N)-periodic, and gcd(M, N) < N because N > M, so w is not primitive.
- *Difference from Q.* Let w ∈ L_M ∖ Q with #a(w) > M. Then w = v^d where #a(v) ∤ M. Indeed, #a(v) | M would make γ M-periodic.

So any proof of ¬P_cop must use L ⊆ Q on powers v^d with #a(v) ∤ M, for every M. In particular it must use roots whose a-count is
divisible by arbitrarily large prime powers.

Status: [written proof sketch]. The wrap-around witness grammar is not written out. The set-level claims (L_M ⊇ Q, and the extras have #a(root) ∤ M) are
[computational]-checked for M = 2, 3, 4, 6 and |w| ≤ 14, with 0 failures (script part (e)). M = 1 is the fully proved and verified Theorem N.

## 5. What remains: the exact requirement for ¬P_cop

**Requirement R.** A proof of ¬P_cop must exploit the conjunction of Cop ⊆ L with L ∩ X ⊆ Q, where X contains powers v^d (d ≥ 2) with
- #a(v) and #b(v) both ≥ 2 (Theorem N, two-letter version), and
- #a(v) ∤ M, for every fixed M (§4).

On such words, Q's membership is a statement about the **global period of an unboundedly long gap sequence**. This is precisely the
"typical word / varying prime" core (i) of the Round-8 synthesis. So core (ii) is **not independent** of core (i).
- Any analytic or marker argument for ¬P_cop must contain a solution of the structural difficulty in core (i) (negative direction).
- The analytic shell (algebraicity plus Pringsheim on prime rows) contributes only the unambiguous case.
- [assessment, but the logical part — that L_P2 and L_M are models — is proved]

Concrete next lemma (it would revive a row argument): find rows N_1, N_2, … (N_i → ∞) and a property Π(L) of PCFLs such that
1. Cop ⊆ L ⊆ Q ⇒ Π(L), using only L ∩ row N_i;
2. Π(L) forces at least f(N_i) → ∞ singular points of an algebraic row series.

By Theorem N and §4, the rows N_i must be composite, and the deficits used must come from roots v with #a(v) ∤ M for every M.
Natural candidate: N_i = 2q_i (q_i prime). Is there a PCFL L ⊇ Cop with L ∩ row 2q ⊆ Q for all primes q? Here Q ∩ row 2q is
"not a square and γ not 2-periodic". That is an intersection of two linear-ambiguity CFLs whose witnesses can cross. Whether a PCFL can achieve it is **open**
[conjecture: no, which would be a strict step towards ¬P_cop, though not by itself sufficient].

## Files
- `round2/scripts/r9_pcop_prime_rows.py`: G_P, exact tree counts, the L_P / L_P2 checks (`python r9_pcop_prime_rows.py 15`).
