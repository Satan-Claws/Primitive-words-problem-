# Is the language of primitive words context-free?
## A complete record of a three-round research campaign: results, barriers, errors, and open problems

*Last updated: November 2026.*

---

## Read this first

**Bottom line.** The problem is **not resolved**. This document neither constructs a pushdown automaton for the primitive words nor proves that none exists. The question (Dömösi, Horváth, Ito) remains open.

What the campaign *did* produce:

- a set of **barrier theorems** that explain precisely why the standard tools cannot settle the question;
- one **positive structural theorem**: the six-block slice is context-free;
- several **non-context-freeness results for close relatives** of the primitive words. One of them, for the unbordered words, turned out to be already known in the literature;
- a list of **sharply stated open sub-problems**, each of which would advance the main question;
- a **Lean 4 statement** of the problem, so that a machine-checked proof could be accepted unambiguously.

**Provenance and reliability.** The work was carried out by a team of AI research agents (Claude), coordinated in three rounds, with two dedicated adversarial-audit passes.
- **Nothing here is peer-reviewed.**
- The status label on each result tells you how much to trust it.
- I have checked novelty against the literature only for one result: the unbordered words. That one was already known.
- Every other result should be checked against the literature before anyone claims it as new. In particular, check the book by Dömösi and Ito, *Context-Free Languages and Primitive Words* (World Scientific, 2014).

### Status labels used throughout

| Label | Meaning |
|---|---|
| **PROVED (audited)** | A full proof was written and then re-derived line by line by an independent auditor agent. |
| **PROVED (audited, with fixes)** | As above, but the auditor found and repaired a gap or an off-by-one. The repaired statement is the one given here. |
| **PROVED (unaudited)** | A full proof exists in the agent's report, but no independent audit was done. Treat it with caution. |
| **SKETCH** | The argument is plausible but not written out in full. |
| **EVIDENCE** | Finite computation only. It is never a proof of an infinite statement. |
| **CONJECTURE** | Believed true, no proof. |
| **FALSE / FLAWED** | Claimed during the campaign and later refuted by an audit. Recorded here so nobody re-uses it. |
| **KNOWN** | Already in the literature. |

---

## Table of contents

1. [The problem, stated exactly](#1-the-problem-stated-exactly)
2. [Background that was taken as known](#2-background-that-was-taken-as-known)
3. [How the campaign was run](#3-how-the-campaign-was-run)
4. [Headline findings in one page](#4-headline-findings-in-one-page)
5. [Barrier theorems: why single-length arguments cannot work](#5-barrier-theorems-why-single-length-arguments-cannot-work)
6. [The analytic / generating-function barrier](#6-the-analytic--generating-function-barrier)
7. [Closure-property reductions collapse to one statement, OG(Q)](#7-closure-property-reductions-collapse-to-one-statement-ogq)
8. [The structure of OG(Q): colourings, rigidity, and Gap G](#8-the-structure-of-ogq-colourings-rigidity-and-gap-g)
9. [Bounded slices: the six-block slice is context-free](#9-bounded-slices-the-six-block-slice-is-context-free)
10. [Fixed-run slices satisfy Ogden's lemma](#10-fixed-run-slices-satisfy-ogdens-lemma)
11. [The affirmative side: what a grammar would have to do](#11-the-affirmative-side-what-a-grammar-would-have-to-do)
12. [Related languages that are not context-free](#12-related-languages-that-are-not-context-free)
13. [The MP target: words with minimal period > n/2](#13-the-mp-target-words-with-minimal-period--n2)
14. [Computational data](#14-computational-data)
15. [The common core every route hit](#15-the-common-core-every-route-hit)
16. [Open problems, ranked](#16-open-problems-ranked)
17. [Errors caught by the audits](#17-errors-caught-by-the-audits)
18. [Master status table](#18-master-status-table)
19. [Lean 4 formalization of the problem](#19-lean-4-formalization-of-the-problem)
20. [Recommendations for anyone continuing](#20-recommendations-for-anyone-continuing)
21. [References](#21-references)
22. [Appendix: where the detailed reports live](#22-appendix-where-the-detailed-reports-live)

---

## 1. The problem, stated exactly

**Alphabets and words.**
- Σ is a finite alphabet with |Σ| ≥ 2; the main case is Σ = {a, b}.
- Σ* is the set of all finite words, including the empty word ε, and Σ⁺ = Σ* ∖ {ε}.
- For a word u and an integer k ≥ 0, uᵏ is u concatenated k times.

**Primitive words.** A word w ∈ Σ⁺ is *primitive* if there are no u ∈ Σ⁺ and k ≥ 2 with w = uᵏ.
- ε is **not** primitive.
- Exponent 1 does not count: every word equals w¹.
- Q (or Q_Σ) denotes the set of primitive words.
- Examples over {a,b}: a, b, ab, aab, abba, ababa are primitive; aa, abab, abaaba, aaaa are not.

Equivalent characterisations used throughout:
1. w is primitive iff w is not equal to any non-trivial rotation of itself.
2. With n = |w|: w is primitive iff for every proper divisor d of n there is a position i with w_i ≠ w_{i+d}. It suffices to check d = n/p for the primes p dividing n.
3. Every w ∈ Σ⁺ is uniquely ρ(w)ᵏ with ρ(w) primitive. w is primitive iff k = 1.

**Notation.** ω(n) is the number of distinct primes dividing n, and τ(n) the number of divisors of n. Q_n = Q ∩ Σⁿ.

**The question.** Is there a (nondeterministic, one-stack, one-way) pushdown automaton P with **L(P) = Q exactly**? Equivalently, is there a context-free grammar G with L(G) = Q?
- *Exactly* means both inclusions. A PDA accepting all of Σ⁺ trivially contains Q, which is useless.
- A **negative** answer for Σ = {a,b} implies the negative answer for every |Σ| ≥ 2. The reason: Q_{a,b} = Q_Σ ∩ {a,b}*, and CF languages are closed under intersection with regular sets.
- An **affirmative** answer must give one fixed machine for each alphabet, working for all lengths.

**What does not count** as a resolution:
- restricted-class results (deterministic, unambiguous, finitely ambiguous, linear, …);
- one inclusion only;
- correctness on a subset of lengths;
- families of machines indexed by length;
- results about the complement or about variants;
- finite computation;
- reductions to unproved statements of comparable strength.

---

## 2. Background that was taken as known

These were used as background, with their hypotheses. Citations are from memory; verify them before relying on them.

| Fact | Source |
|---|---|
| Q is deterministic context-sensitive. Primitivity is decidable in linear time. | standard |
| Q is not regular. | pumping lemma |
| Q is not deterministic CF. | complement plus intersection with a regular set gives {aⁱbʲaⁱbʲ} |
| Q is not unambiguous CF. q(n) = Σ_{d\|n} μ(n/d)\|Σ\|^d has a non-algebraic generating function. | H. Petersen, STACS 1994 |
| Q is not linear CF. | S. Horváth, 1995 |
| **Reis–Shyr:** Q² = Σ⁺ ∖ {aⁿ : a ∈ Σ, n ≠ 2}. | Reis and Shyr |
| For each fixed k ≥ 2, the non-k-th-powers form a CF language. Σ* ∖ {ww} is CF. | classical |
| The Abelian primitive words are not CF. Neither are the primitive palindromes. | Domaratzki–Rampersad 2010; known |
| Cyclic shift preserves context-freeness. | Maslov 1973 / Oshiba 1972 |
| Lyndon words are not CF. | Berstel–Boasson |
| **Ginsburg–Spanier:** L ⊆ c₁*⋯c_m* (distinct letters) is CF iff its exponent set is a finite union of *stratified* linear sets. | Ginsburg–Spanier 1964; Ginsburg's 1966 book |

A linear set is *stratified* if two conditions hold:
- every period vector has at most two non-zero coordinates;
- no two period supports cross, i.e. there are no i<j<k<l with one period supported on {i,k} and another on {j,l}.

---

## 3. How the campaign was run

- **Budget.** A bounded campaign with about 6–8 parallel agents per round, three rounds, and an adversarial audit after rounds 1 and 2/3.
- **Round 1: seven independent routes, deliberately diverse.**
  - (A) closure-property reductions;
  - (B) interchange lemma and Bader–Moura;
  - (C) derivation-tree cross-word swaps;
  - (D) analytic / ambiguity;
  - (E) affirmative constructions;
  - (F) computation;
  - (G) grammar-size lower bounds and finite intersections.
- **Round 2.** (H) settle OG(Q); (I) bounded slices; (J) unbordered words; (K) audit of round 1.
- **Round 3.** (L) the MP target; (M) Gap G; (N) audit of round 2 and of M.
- **A registry of approach families** was kept, grouped by mechanism. Routes were marked *blocked* when they reached a lemma of the same strength as the original problem.

Letters A–N below refer to these routes. The per-route reports are listed in the [appendix](#22-appendix-where-the-detailed-reports-live).

---

## 4. Headline findings in one page

1. **Single-length combinatorics is provably dead.** Q_n is an *exact union of O(n) balanced rectangles* contained in Q, and at most 8 when n is odd (§5.2). Q also satisfies the conclusion of the Ogden–Ross–Winklmann interchange lemma with a constant fraction 1/(e(ω(n)+1)), against the 1/(cn²) the lemma asks for (§5.3). Consequences:
   - fooling sets have size O(n), and for 5 ≤ n ≤ 10 the maximum is 1;
   - rectangle and communication-complexity lower bounds on grammar size are vacuous;
   - single cross-word swaps cannot work;
   - **any refutation must relate words of different lengths.**
2. **Counting arguments cannot pass beyond unambiguous grammars.** An explicit binary CFL of ambiguity 2 has a generating function with all the analytic features Petersen's argument uses (§6).
3. **Closure-property reductions add nothing beyond a regular annotation.** Any chain of allowed operations from Q is a single rational transduction of Q. Combined with Ogden's lemma, such a chain can refute Q *iff* Ogden's lemma fails on some π⁻¹(Q) ∩ R (π letter-to-letter, R regular). Call the statement "it never fails" **OG(Q)** (§7).
4. **OG(Q) was reformulated** without π and R: Ogden for Q with pumps restricted to "colour loops" under an arbitrary colouring. A rigidity theory was built: a partner principle and run-skeleton rigidity. The dense-marking core ("Gap G") was **proved**. The sparse-marking case remains open, and all evidence says OG(Q) is *true*. If it is, closure + pumping can never refute Q (§8).
5. **The six-block slice Q ∩ (a⁺b)⁶ is context-free** (proved, audited, with an explicit cover by 464 stratified linear sets). There is computer evidence for every block count m ≤ 24 with two prime factors. Q ∩ (a⁺b)⁺ (unbounded block count) is CF **iff Q is** (§9).
6. **Pumping inside a fixed run structure cannot refute Q.** Q ∩ (a⁺b)^r satisfies Ogden's lemma for p ≥ p₀(r) (§10).
7. **Related languages that are not CF** (§12, §13):
   - the unbordered words (KNOWN: Rampersad–Shallit–Wang 2011);
   - Q ∩ {no border ≤ f(n)} for unbounded f;
   - bounded rotations of the unbordered words;
   - {minimal period > n/c} for 1 < c < 5/4 (unaudited);
   - "no square centred at the middle cut" (unaudited).

   None of these transfers to Q, for a precise geometric reason: Q's complement has no half-spaces.
8. **The affirmative side** is blocked at a precise point. A grammar would have to combine refutations of unboundedly many primes using non-crossing comparisons whose distances cannot be tied to n (§11).
9. **The common core** (§15). Every route ends at the same configuration: a word that one small local edit turns into an exact q-th power, for unboundedly many primes q, with Fine–Wilf failing at near-squares.

---

## 5. Barrier theorems: why single-length arguments cannot work

### 5.1 The two slice lemmas (Route G)

**Lemma 5.1 (slice grammar).** PROVED (audited). Let G = (N, Σ, P, S) be in Chomsky normal form with L(G) = L. For every n there is a CNF grammar G_n with L(G_n) = L ∩ Σⁿ, at most |N|·n nonterminals and at most |P|·n² rules.

*Construction.* Use nonterminals (A, ℓ) for 1 ≤ ℓ ≤ n, with:
- rules (A,ℓ) → (B,ℓ′)(C,ℓ−ℓ′) for each A → BC and 1 ≤ ℓ′ < ℓ;
- rules (A,1) → a for each A → a;
- start symbol (S, n).

By induction on ℓ, (A,ℓ) ⇒* y iff A ⇒* y and |y| = ℓ.

**Consequence.** If Q is CF then, for some constant c and *every* n, Q_n has a CNF grammar with ≤ c·n nonterminals. So a lower bound of ω(n) nonterminals along infinitely many n would refute CF-ness. A superpolynomial bound is far more than needed.

**Lemma 5.2 (balanced rectangles).** PROVED (audited). Fix n ≥ 2. For A ∈ N, offset i and n/3 < ℓ ≤ 2n/3, let
R(A,i,ℓ) = {xyz ∈ Σⁿ : |x| = i, |y| = ℓ, A ⇒* y, S ⇒* xAz}.
Each R(A,i,ℓ) is a combinatorial rectangle (yields × contexts) contained in L, and L ∩ Σⁿ is the union of the ≤ |N|·n² of them.

*Proof.* In any derivation tree, walk from the root into the larger child until the yield is ≤ 2n/3. The node reached has yield > n/3.

### 5.2 Q_n has an O(n) balanced rectangle cover (Route G, fixed by audit K)

Notation:
- D = proper divisors of n, and E = D ∖ {n/2};
- M₁ ≥ M₂ are the two largest elements of E;
- λ = ⌊2n/3⌋;
- s = λ − max(M₁+M₂−1, M₁).

**Lemma 5.3 (period extension).** If X has period d, and a suffix (or prefix) S of X with |S| ≥ d has period g with g | d, then X has period g.

**Lemma 5.4 (chain lemma).** Let E′ ⊆ D be closed under gcd, with two largest elements M₁ ≥ M₂. Take windows of length λ at starting points spaced ≤ s apart, covering the word, where λ − s ≥ max(M₁+M₂−1, M₁). If every window has a period in E′, then w has a global period d ∈ E′, so w is not primitive.

*Proof idea.* Consecutive windows overlap in ≥ M₁ + M₂ − 1 letters. By Fine–Wilf the least E′-periods of consecutive windows must coincide; by Lemma 5.3 they cannot differ. So one period d propagates across the whole word.

**Theorem 5.5 (explicit balanced cover).** PROVED (audited, with fixes). Use *non-wrapping* windows [t, t+λ), with starting points t ∈ T ⊆ [0, n−λ], 0 ∈ T, n−λ ∈ T and gaps ≤ s. Then Q_n is the **exact** union of:
- A_t = {w : the window [t, t+λ) has no period in D}, for t ∈ T;
- (n even only) B_{t,i,a} = {w : the window has no period in E, w_i = a, w_{i±n/2} ≠ a}, with i an endpoint-side position inside the window.

Every piece is a balanced rectangle in the sense of Lemma 5.2. The number of pieces is at most 8 for odd n, and O(|Σ|·n) in general (≤ 12(1+|Σ|⌈n/3⌉)).

*Proof sketch.*
- Soundness: a period in D would be visible inside the window. For the B-pieces, the mismatch at distance n/2 rules out the one remaining period.
- Coverage: if w is primitive, Lemma 5.4 gives a window with no E-period. Either it also has no period n/2 (then w ∈ A_t), or n is even and the non-square w has a mismatch pair {i, i+n/2} with exactly one end inside the window (then w ∈ B).

*Audit fix.* The original version also used windows that wrap around position 0. When 3 | n, such a window's only linear side has length exactly n/3, which is outside the required range (n/3, 2n/3]. The non-wrapping version above is exact, has the right shape for every n, and needs even fewer windows. Exactness was verified exhaustively for binary n ≤ 20 (24 in the original run) and ternary n ≤ 11–12.

**Corollary 5.6 (all one-level methods fail).**
- Every fooling set has size O(|Σ|n).
- Every distribution on Q_n puts mass ≥ 1/O(|Σ|n) on one balanced rectangle inside Q.
- Exhaustive check: for 5 ≤ n ≤ 10 no two distinct primitive words are fooled at every balanced interval, so the maximum fooling set has size 1. (For n = 4 there are 22 such pairs, a small-n artefact.)

**Theorem 5.7 (seam variant).** PROVED (unaudited; verified computationally for binary n ≤ 20, ternary n ≤ 11). If every window contains the "seam" (n−1, 0), the same A/B families still cover Q_n. Now the *yield* side of each rectangle is a free interval of length ⌈n/3⌉, or one with a single fixed letter.

*Consequence:* nested "k-level box" arguments of any depth also give only O(n) boxes. A proof must use the fact that *context* sets are themselves generated recursively by the same grammar.

**Theorem 5.8 (every middle length).** PROVED (unaudited; verified for n = 16…20). For n ≥ 16 and every m, Q_n is a union of ≤ 24(1+|Σ|·3n/8) rectangles whose middle has length ℓ ∈ (m/2, m]. This gives the interchange conclusion with loss 1/O(n), consistent with §5.3.

### 5.3 The interchange barrier (Route B)

**The interchange lemma** (Ogden–Ross–Winklmann, SIAM J. Comput. 14, 1985). For a CFL L there is c_L such that for all n, all R ⊆ L_n and all m ∈ [2, n], there are k ≥ |R|/(c_L n²) words in R with factorizations wᵢxᵢyᵢ such that:
- the |wᵢ| are all equal, the |yᵢ| are all equal, and m/2 < |xᵢ| ≤ m;
- every cross-swap wᵢxⱼyᵢ is in L.

**Lemma 5.9 (≤ ω(n) zeros per line).** PROVED (audited). Fix a window of length ℓ ≤ n/2. Each context has at most ω(n) "bad" middles, i.e. middles completing it to a non-primitive word.

*Proof.* A non-primitive word has period n/p for a prime p | n. The context has cyclic length ≥ n/2 ≥ n/p, so it determines the n/p-periodic completion. The case ℓ > n/2 is symmetric, with middles and contexts swapped.

**Theorem 5.10 (single-window barrier).** PROVED (audited). For every n ≥ 2, every R ⊆ Q_n and *every* window position and length, there is Z ⊆ R with
  |Z| ≥ |R| / (e(ω(n)+1))
such that all cross-swaps between words of Z are primitive.

*Proof.* Put each middle into a random set S independently with probability 1/(ω+1). Keep the contexts none of whose bad middles was chosen. A fixed word of R survives with probability ≥ (1/(ω+1))(1 − 1/(ω+1))^ω ≥ 1/(e(ω+1)). Take a good outcome.

**Corollary 5.11.**
- Q satisfies the interchange lemma's conclusion with c = e and slack ≈ n^{2−o(1)}. No choice of family can work: two halves, near-p-th powers, or lengths with many prime factors. The number of exponents enters only through ω(n)+1 ≤ log₂ n, against an n² budget.
- Because the theorem holds for every window, marked (Ogden-style) interchange variants fail too.
- For any fixed cut, Q_n is covered by ⌈e(ω(n)+1)·n ln|Σ|⌉+1 rectangles inside Q. So the nondeterministic communication complexity of primitivity is ≤ log₂ n + O(log log n) at every cut. **Rectangle lower bounds on CFG size are vacuous for Q, even for ambiguous grammars.**

**Theorem 5.12 (universal box barrier).** PROVED (audited). Cut [0, n) into m pieces and group the pieces into coordinates. For every R ⊆ Q_n some product box of all-primitive reassemblies contains ≥ |R|/(8m)^{ω(n)} elements of R.

*Consequence:* multi-window and nested interchange lemmas of any depth t, which guarantee only (cn²)^{−t}, are also satisfied by Q.

*Computation (EVIDENCE):*
- Across families F0–F3 for n up to 30 (all of Q_n; Hamming-1 near-powers; near-squares; 1–2 flips from words with period d | 30), the minimum fraction over all windows was 0.186–0.556. The proven guarantee is 0.092–0.184.
- Box fractions for n = 30, 42, 60 stayed constant at ≈ 0.010–0.018.

**Bader–Moura** (J. ACM 29, 1982). BLOCKED. Refuting Q with this lemma is *exactly equivalent* to a "pump-rigidity" statement, so there is no weaker sub-lemma.

**Proposition 5.13.** PROVED (unaudited). Let z = ∏ a^{kⱼ} b. Call a block *unsafe* if pumping one or two letters inside it has a bad exponent. At most (3/2)(τ(r)−1) blocks are unsafe.

*Data (EVIDENCE):* exhaustively for n ≤ 13 and |E| ≤ 2, a safe split always exists with Bader–Moura cost ≤ 2. The only cost-2 cases are aᵏbaᵏ^{±1}b with both b's excluded.

### 5.4 Cross-word swaps in derivation trees (Route C)

**Lemma 5.14 (Lemma A).** PROVED (audited). Two distinct non-primitive words of the same length differ in at least 2 positions.

**Lemma 5.15 (Lemma B).** PROVED (audited; the final finite case on ℤ₆/ℤ₁₂ was re-run). If two distinct non-primitive words of length n differ in exactly two positions p, q, then n is even and q ≡ p + n/2.

**Theorem 5.16 (no fooling pair at any scale).** PROVED (audited). Let n ≥ 3 and 2 ≤ m ≤ n/2, and let w ≠ w′ be primitive words of length n. Some interval I with |I| ∈ {m, m+1} makes *both* crossovers (w's context with w′'s filler, and vice versa) primitive.

*Proof idea.* Slide the interval one step at a time. By Lemmas A and B, a bad crossover would have to alternate between the two sides in a way only possible if the two words differ in at most two antipodal positions. Each remaining case has an explicit good interval.

*Consequence:* "design a family so that every pigeonhole collision of (nonterminal, interval) yields a power" is impossible, even for families of size 2.

**Theorem 5.17 (11-label adversary).** PROVED (unaudited). Each node of a tree can be labelled with one of 2·2·|Σ|+|Σ|+1 labels (11 for binary), carrying per-prime "anchor" certificates. Two words that share a label at the same interval then have both crossovers primitive.

**Theorem 5.18.** PROVED (unaudited). For n = p^e (a prime power), every primitive word has a tree in which every node is certified.

**Open Lemma S.** Is the same true for every n? EVIDENCE: all binary n ≤ 22, plus 20,000 samples each at n = 30, 42, 60, with 0 failures. Simple "star" trees fail at n = 12, 18, 20, so adaptive trees are needed. The route's author rated this a finite combinatorial lemma, not of theorem strength.

### 5.5 What survives of the size route

- **Upper bound.** Q_n has an NFA, hence a right-linear CFG, with n^{O(ω(n))} = 2^{O(log²n / log log n)} states: guess one mismatch per prime.
- **Lower bounds.** Only Ω(log n) is unconditional (see §17 for the false c·n claim). A refutation needs ω(n) nonterminals for infinitely many n.
- **What is missing (theorem strength).** A lower-bound technique for *general (ambiguous)* CFGs that uses the recursive, grammar-generated structure of contexts across lengths. None is known.
- **"Nonterminals shared across lengths", used at one level, also fails.**
  - Odd n (proved): one yield set Σ^ℓ per length suffices.
  - Even n (verified for n ≤ 20): 1 + 2|Σ| fixed regular yield languages suffice.

### 5.6 Finite intersections (Route G, part 2)

**Proposition 5.19.** PROVED. Q is an intersection of k CF languages iff (Σ⁺∖Q) ∪ {ε} is a union of k sets whose complements are CF. For k = 1 this is the original question, so proving "Q is not a finite intersection of CFLs" is at least as hard.

**Proposition 5.20.** PROVED. Suppose some CF L ⊇ Q contains only p-th powers among non-primitive words, for p in a finite set F of primes. Then Q = L ∩ ⋂_{p∈F}(non-p-th-powers) is a finite intersection of CFLs.

A sufficient "density lemma" was formulated (it would imply "not a finite intersection"); it is open and at least as strong as non-CF-ness.

---

## 6. The analytic / generating-function barrier

(Route D. Every closed form was verified against brute force.)

**Baseline.** Q(z) = Σ_n q(n)zⁿ = Σ_{k≥1} μ(k)·2z^k/(1−2z^k). It has poles at |z| = 2^{−1/k} for every squarefree k, accumulating on all of |z| = 1, so |z| = 1 is a natural boundary. Hence Q(z) is neither algebraic nor D-finite. By Chomsky–Schützenberger, Q is not unambiguous CF (Petersen).

**The structural reason the argument stops.** For any CFG, the *derivation-count* series is algebraic. The *word-count* series counts only the support. For a k-ambiguous grammar, inclusion–exclusion gives
  c_n = Σ_{j=1}^{k} (−1)^{j+1} N_j(n),
where N_j counts j-sets of distinct derivations of the same word. Only N₁ is known to be algebraic. N₂, which counts pairs of derivations with the same yield, is an intersection-type object with no algebraicity theorem.

**Proposition 6.1.** PROVED. d_n = 2ⁿ is rational and satisfies q(n) ≤ d_n ≤ 2q(n). So "c ≤ d ≤ kc with d algebraic" cannot refute even 2-ambiguity.

**Theorem 6.2 (Petersen's pattern occurs at ambiguity 2).** PROVED (audited). Over {a,b,#}, let:
- L₁ = {u₁#…#u_m : u_{2i} = u_{2i−1}^R};
- L₂ = the same condition, shifted by one segment.

Both are DCFLs with unambiguous grammars, and L₁ ∩ L₂ = {u#u^R#u#u^R#…}. Then
  GF(L₁∪L₂) = rational − Σ_{m≥1} z^{m−1}/(1−2z^m),
which has poles at every z with z^m = 1/2, a natural boundary at |z| = 1, and is non-algebraic and non-D-finite.

The binary code a↦ab, b↦abb, #↦abbb transfers everything to {a,b}, with poles at radii x₀^{1/m} (x₀ ≈ 0.7549, the real root of x²+x³ = 1).

*Consequence:* every analytic feature Petersen's argument uses already appears in an explicit binary CFL of ambiguity 2. A finite-ambiguity proof would need a *structural* lemma controlling N₂, which is of theorem strength. (The auditor notes that "inherent ambiguity exactly 2" is true but not needed.)

**Proposition 6.3 (code slices).** PROVED. Let C be a regular code with C* pure. Then:
- GF(Q ∩ C⁺) = Σ_k μ(k) S(z^k), an infinite Möbius sum (non-algebraic, but this is only Petersen again);
- GF(Q ∩ C^K) = Σ_{e|K} μ(e) c(z^e)^{K/e}, a finite sum, hence rational.

**Proposition 6.4 (dichotomy for regular slices).** SKETCH for the polynomial case.
- A slice of polynomial growth is bounded, and Q ∩ R has a rational generating function.
- A slice of exponential growth ρ has its non-primitive correction at relative size ρ^{−n/2}.
- So no regular slice is "bounded-like but carrying Möbius counting".

**Flajolet's criteria** (1987) prove only inherent ambiguity (non-unambiguity). They rest on Chomsky–Schützenberger, which is about derivation counts, so they can never prove non-context-freeness. The only analytic constraints valid for *all* CFLs are the growth gap and rationality of bounded CFLs. These reduce everything to bounded slices of Q, whose counts are rational.

**Reformulation (open).** (q(n)) is the counting sequence of some CFL iff some co-CF set has exactly 2ⁿ − q(n) words of each length. The natural candidate ⋃_p {u^p} is a union, while co-CF sets are closed only under intersection. This appears as hard as the original problem.

---

## 7. Closure-property reductions collapse to one statement, OG(Q)

(Route A, repaired by audit K.)

**Nivat normal form.** Every rational transduction is τ(L) = g(f⁻¹(L) ∩ R), with f, g alphabetic morphisms and R regular. The following are all rational transductions: inverse morphism, morphism, gsm maps, quotients by regular sets, ∩ regular, and union or concatenation with a regular set.

**Lemma 7.1 (existential projection).** PROVED. y ∈ τ(Q) iff τ⁻¹(y) ∩ Q ≠ ∅. So projections and erasing steps only *weaken* the target, by adding witnesses. Only f⁻¹ and ∩R preserve the conjunctive structure Q_n = ⋂_{p|n} (non-p-th powers).

Example: Q ∩ (a⁺b)⁺ coded by block length mod q, or by any finite letter-to-letter quotient of block lengths, has a **regular** image.

**Definition.** L has property **OG** if for every letter-to-letter π and every regular R, the language π⁻¹(L) ∩ R satisfies Ogden's lemma. Every CFL has OG.

**Theorem 7.2.** PROVED (audited, with a constant fix). OG is preserved by every rational transduction and by reversal. The erasing inverse-morphism case needs window constant (2s+1)p rather than (s+1)p.

**Lemma 7.3 (Q-specific; audit K).** PROVED (audited). Q is closed under rotation and reversal, so every chain of allowed operations starting from Q equals a single rational transduction of Q.

**Corollary 7.4.** PROVED (audited). A chain of allowed operations followed by Ogden's lemma refutes context-freeness of Q **iff** Ogden's lemma already fails for some π⁻¹(Q) ∩ R. Closure reductions add exactly a finite-state annotation, and they do **not** remove the thin-complement obstacle.

*Withdrawn:* the general claim "OG is closed under cyclic shift" had a gap in the mark count and is withdrawn. Lemma 7.3 makes it unnecessary for Q. The remark "the same proofs work for the Bar-Hillel lemma" is also unjustified for erasing images.

**The naive proof of OG(Q) is false.** The natural approach is to Ramsey-select idempotent cut points and then pump only between them. It fails on
  z = aᵏ b a^{k+lcm(1..k)} b
with the cut points in the first run. Every one- or two-sided pump inside the first run eventually becomes a square, at i = 1 + L/T. (Verified for k = 2..6.)

Plain Ogden escapes by pumping an *equal-length partner loop* in the unmarked second run. Any proof of OG(Q) must use such partner loops.

**Large-i lemma.** PROVED (audited). If z = uvw is primitive and uvⁱw is non-primitive for some i ≥ 2, then (i−1)|v| ≤ |z| − 2. So bad exponents are small.

---

## 8. The structure of OG(Q): colourings, rigidity, and Gap G

(Routes H and M, audited by N.)

### 8.1 Annotation-free reformulation

**Definition (CPL_s).** There is p such that every primitive z has a good decomposition under every mark set D with |D| ≥ p and every map χ from cut points to s colours. The decomposition must satisfy:
- vx meets D, and |vwx ∩ D| ≤ p;
- v and x are **colour loops** (equal colours at both ends);
- all uvⁱwxⁱy are primitive.

**Theorem 8.1.** PROVED (audited). OG(Q) ⇔ CPL_s holds for every s. CPL₁ is plain Ogden for Q.

*Proof.* (⇐) Colour each cut point by the DFA state reached there. (⇒) Encode a colouring as a regular local constraint over the alphabet {a,b} × [s] × [s].

*Meaning:* the power of a regular annotation is exactly an *arbitrary* s-colouring of cut points, chosen after p. It need not be periodic or regular.

### 8.2 What colourings can and cannot forbid

**Theorem 8.2.** PROVED (audited).
- (a) Among any s+1 cut points two share a colour, so colour loops are dense.
- (b) In any long π-periodic stretch there are colour loops of length jπ (j ≤ s). Two of them share a start and have different lengths.
- (c) **Synchronized partners survive.** For any fixed ratio μ and offset Δ there are simultaneous colour loops v, x with |x| = μ|v|.
- (d) **Walls are possible.** Loops can be confined between walls, and lengths forced ≡ 0 mod m for m ≤ s. Nothing stronger is possible.

### 8.3 Rigidity tools

**Lemma U (fresh conjugates).** PROVED (audited). If z = uvy is primitive, |v| < |z|, and some conjugate of v is *not* a cyclic factor of z, then uvⁱy is primitive for every i ≥ 1. Only deletion (i = 0) can fail for such loops.

*EVIDENCE:* 0 violations among 69,279 fresh pumps at n = 12. The hypothesis is necessary: 2,608 stale pumps at n = 12 have a bad i.

**Lemma 8.3 (clustering).** PROVED (re-derived by M; not separately audited by N). Fix a loop length ℓ and a small exponent i. All failing one-sided pumps of length ℓ at exponent i, within a window of size ≤ n/6, lie in one ℓ-periodic stretch.

**Theorem 8.4 (labelled-sequence rigidity).** PROVED (audited). Let R ≥ 2 and h : ℤ_R → X. Let S be one site, or two non-antipodal sites (with R ≥ 3). Then at most one relabelling h′ that agrees with h off S has a proper period.

*EVIDENCE:* 4.5M cases exhaustively, plus ≈106k arbitrary-relabelling cases; 0 violations. Only antipodal pairs are degenerate.

**Run skeleton.**
- The skeleton of a cyclic word is its sequence of long runs of small minimal period.
- The word is non-primitive iff its sequence of gap words has a proper period.
- Pumping deep inside a skeleton run changes only that run's gap word.

**Theorem 8.5 (5\*).** PROVED (audited, with a fixed justification). Lengthen or shorten two consecutive long runs of z by m₁π and m₂π′. When the skeleton has R ≥ 3 runs, at most one pair (m₁, m₂) ≠ 0 makes z non-primitive. For a single site, at most one value is bad when R ≥ 2, and none when R = 1.

**Lemma 8.6.** PROVED (audited). With two runs, equal-length pumps of both are always safe.

**Corollary 8.7 (partner principle).** PROVED (audited, with a margin fix: interior margin 2π₀+1, or Λ = 6s²π₀²+4π₀+3). Suppose the marked pumps sit inside a long small-period run, and another such run is reachable within the Ogden window. Then there is a good colour-loop decomposition.

*What it kills:* every counter, wall and block-marker design; the factorial family aᵏba^{k+L}b; every block word with a reachable long partner run.

**Necessary conditions on any counterexample to OG(Q).**
- Marked long runs must be isolated: more than p marks from any partner run.
- Isolated runs *can* be made locally rigid with the factorial trick; this is the only rigid configuration found.
- The marked "buffers" around them must kill every local pump.

### 8.4 Gap G (dense markings): proved

**Theorem 8.8 (Gap G, M1).** PROVED (audited, with fixes). Let s ≥ 1 and λ ≥ 2s. There is p = O(λ² log s) such that the following holds.
- Let z be primitive, χ any s-colouring, and B a factor of z of length p containing no factor with period ≤ s and length ≥ λ.
- Then B contains a colour loop v of length ≤ s whose one-sided pump is good for every i ≥ 0.

*Key new idea.* Apply the rigidity Theorem 8.4 **across different candidate pumps**, not just across the exponents of one candidate.
- A large-exponent pump of a short loop deep in a run-free buffer adds exactly one new skeleton run.
- It thereby splits *the same* gap word into two labels (X, Y), whatever the prime q, the exponent, the target run or the length.
- Theorem 8.4 permits at most one such relabelling to be periodic.

So all large-exponent failures in a buffer share the same new run start (R ≥ 2), lie within λ/2 of each other (R = 1, via the length identity z = N U N⁻ U), or do not exist (R = 0). Small-exponent failures cluster by Lemma 8.3. A pigeonhole count over blocks of s+1 cut points then finds a good colour loop.

*This removes the "unboundedly many primes" obstruction in the dense case.* The auditor supplied one missing justification (|N| ≤ |X| in the R = 1 case).

*Corollary (direction (a) of Route M):* Sturmian, Thue–Morse or random buffers combined with factorially rigid runs cannot produce a counterexample.

### 8.5 What remains open

**Corollary M3 ("π⁻¹(Q) ∩ R satisfies Bar-Hillel for all letter-to-letter π and regular R")** is **FLAWED and unproved**.
- *The flaw:* at the deletion step i = 0, a skeleton run shorter than T′ + |v| drops out of the skeleton. Then the ring shrinks and the rigidity theorems no longer apply. Trivial instance: σ = a¹⁴, T′ = 14, v = a.
- It also inherits a too-small constant.
- A plausible repair route exists (a two-threshold skeleton plus single-site rigidity on the merged ring), but it has not been written out or audited.

**Gap G_sp (sparse markings).** OPEN. This is the case where marks are far apart, so colour loops are long and of unboundedly many lengths. Lemma 8.3 clusters failures only for *equal* (ℓ, i), so a "deletion clustering across lengths" lemma appears to be needed.

**Direction of evidence.**
- Plain Ogden holds with p = 1 for all primitive words up to length 12.
- With 2 colours the needed constant is ≤ 3 (n ≤ 9).
- Prover-side annealing searches found no growth.

Everything points to **OG(Q) being true**. If so, *no* combination of closure operations and Ogden/Bar-Hillel pumping can ever refute context-freeness of Q.

---

## 9. Bounded slices: the six-block slice is context-free

(Route I, audited by N.)

**Reduction.** PROVED (audited).
- The word a^{x₁}b ⋯ a^{x_m}b is non-primitive iff the cyclic tuple x is d-periodic for some proper divisor d of m.
- A gsm (block index kept in the state) and its inverse give: Q ∩ (a\*b)^m is CF ⇔ the letter-bounded language {c₁^{x₁}⋯c_m^{x_m} : x ∈ S_m} is CF ⇔ (Ginsburg–Spanier) S_m is a finite union of stratified linear sets.
- Here S_m = ℕ^m ∖ ⋃_{p | m} A_p, where A_p is the set of (m/p)-periodic vectors.
- The a⁺b variant is the translate (1,…,1) + S_m, so the two questions coincide.
- **If any S_m were not stratifiable, Q would not be CF.**

**Lemma 9.1 (two-sided merge lemma).** PROVED (audited, cosmetic fixes).
- Choose left blocks and right blocks, matched inside-out or outside-in.
- The breakpoints of the partial sums λ_k (left) and ρ_k (right) cut the line into segments, giving a "path".
- For every path, the set of tuples with that path is a single *stratified* linear set.
- These sets partition ℕ^m, and every sign of λ_k − ρ_{k′} is constant on each.

*Consequence:* any predicate on the signs of nested partial-sum comparisons is a finite union of stratified linear sets.

**Theorem 9.2 (F₆ is context-free).** PROVED (audited). For m = 6:
- P₂ = 2-periodic vectors and P₃ = 3-periodic vectors;
- W := P₂ + P₃ = {x₁+x₂ = x₄+x₅, x₂+x₃ = x₅+x₆}, of dimension 4;
- S₆ = ℕ⁶ ∖ (P₂ ∪ P₃).

The cover:

| Piece | Definition | Framework | # stratified linear sets |
|---|---|---|---|
| N1 | x₁+x₂ ≠ x₄+x₅ | inside-out | 40 |
| N2 | x₂+x₃ ≠ x₅+x₆ | inside-out | 40 |
| C0 | x₁+x₂+x₃ ≠ x₄+x₅+x₆ **and** x₂+x₃ ≠ x₄+x₅ | inside-out | 352 |
| C1 | x₁ ≠ x₄ **and** x₁+x₂ ≠ x₃+x₄ | **outside-in** | 32 |

- *Soundness:* each defining functional vanishes on P₂ or on P₃ as needed.
- *Coverage:* outside W, N1 or N2 applies. On W write x = (A+C, B+D, A+E, B+C, A+D, B+E). Then:
  - x ∈ P₃ iff A = B, and x ∈ P₂ iff C = D = E;
  - C0 ∩ W = {A≠B, E≠C} and C1 ∩ W = {A≠B, D≠E};
  - their union is exactly W ∖ (P₂ ∪ P₃).

Hence **Q ∩ (a\*b)⁶ and Q ∩ (a⁺b)⁶ are context-free.** The 464 linear sets are in `campaign/round2/I_bounded_m6_linear_sets.json`.

*Audit checks:*
- the sets were regenerated independently (40/40/352/32, an exact match);
- every period set is stratified;
- a sign certificate proves that every set avoids P₂ ∪ P₃ on *all* of ℕ⁶;
- the union equals S₆ on [0,12]⁶ (4,824,456 points).

*Alternative cover:* the six rotations of C0 alone cover S₆.

*Why this matters:* an earlier lemma of Route A shows that on the hard core, every pair of *single* mismatch witnesses (one per period) crosses or shares an endpoint. So "guess one mismatch per period" cannot even recognise Q ∩ (a⁺b)⁶. Nested **partial-sum** comparisons evade this, and C1's outside-in matching is what makes it work.

**General m.**
- *EVIDENCE.* "Gap frameworks" use nested equal-length arcs about one centre, with one witness per prime. They are always stratified. Their coverage of S_m was checked by exact subspace-arrangement computation:
  - covered for m = 6, 10, 12, 14, 15, 18, 20, 21, 22 (gaps ≤ 1) and m = 24 (gaps ≤ 2);
  - without gaps the scheme fails at m = 12, 18, 20, 24, 30, with explicit witnesses;
  - the ranks were computed modulo large primes, so the auditor rates this coverage "computer evidence, not proof".
- **m = 30 is unsettled.** With gaps ≤ 9, 12,000 sampled hard points were all covered, but the exact check did not finish.
- **CONJECTURE:** F_m is CF for every m. If true, no bounded slice can refute Q.

**Proposition 9.3 (uniformity equals the whole problem).** PROVED (audited).
  Q ∩ (a⁺b)⁺ is CF ⇔ Q ∩ (a\*b)⁺ is CF ⇔ Q is CF.

*Proof:* use the injective morphism a↦a, b↦ab (a suffix code), which preserves and reflects primitivity on words ending in b. Then Q = cyc(Q ∩ Σ\*b) ∪ {a}.

**What breaks when m varies: index matching.** A certificate-model statement, not a theorem about all PDAs.
- Every interval functional that vanishes on A_p compares two arcs with the *same number of blocks*, tied to m/p.
- For fixed m the block index lives in the finite control. Uniformly, the block count and the a-mass would have to share one stack.
- *Nested-matching lemma:* a letter-matching stack then only compares mirror blocks x_{c−i} vs x_{c+1+i}, and mirror comparisons cannot detect periodicity.
- *Semilinearity:* arc lengths tied to m/p can cover only finitely many primes.

**A sound, uniform, CF family U_K.** PROVED (unaudited).
- Weight letters a = 1 and b = K.
- Accept block sequences with a balanced cut whose left and right partial-sum breakpoints never tie.
- U_K is CF and contains no periodic sequence.
- Together with the two-block family, U_K covers *every* primitive class in (a⁺b)⁺ up to length 21 (EVIDENCE).
- It **fails** at abab a⁸b a⁸b (length 22), on scaled words t·x (misses approach 100%), and on some {1,2}-sequences at m = 16 for *every* K ≤ 59.

**Methodological warning.** A uniform candidate can pass every test up to length 21 and still be wildly incomplete. Test on scaled run-length families, long {1,2}-run sequences and near-powers, not just all words up to length 20.

---

## 10. Fixed-run slices satisfy Ogden's lemma

(Route J, completed by audit N.)

**Lemma 10.1 (direction lemma).** PROVED (audited). Let z = ∏ a^{xᵢ}b be primitive with r runs, and let m ≠ j be non-antipodal (j ≢ m ± r/2 mod r). For every proper divisor d of r, the subspace V_d of d-periodic vectors kills at most one pump ratio α:β of the direction αe_m + βe_j.

*Proof:* V_d ∩ span(e_m, e_j) = 0.

**Theorem 10.2.** PROVED (audited, with fixes). For every r ≥ 2 there is p₀(r), e.g. (r+2)(τ(r)+4), such that Q ∩ (a⁺b)^r satisfies the conclusion of Ogden's lemma for p ≥ p₀.

*Proof idea.* Some long run carries a mark. Pump one marked letter of it together with 1..τ(r) letters of a nearby non-antipodal long run, so that some ratio survives. If only one long run exists, a single-run pump survives.

*Audit fix:* the case where the only usable neighbour is antipodal was missing. It is handled by a rotation-by-r/2 argument showing that the ratio 1:1 is never killed when the other antipodal pairs are equal.

*Scope:* this is plain Ogden on the slice itself, not on annotated slices.

**Why this matters.** Every pumping refutation of Q must use pumps that **change the run structure**, or a non-pumping method.

The geometric reason, in contrast with the unbordered words (§12):
- Q's complement in a slice is a union of *subspaces* of codimension ≥ r/2.
- One pump moves along a line in a 2-coordinate plane, and a subspace meeting that plane only at 0 catches at most one ratio.
- A *half-space* would catch a whole cone of ratios, but Q's complement has none.

---

## 11. The affirmative side: what a grammar would have to do

(Route E; obstructions 2, 3 and 5 audited.)

**Lemma 11.1 (transversal reformulation).** PROVED. Q is CF ⇔ there is a CF language P ⊆ Q that meets every primitive conjugacy class. Indeed cyc(P) = Q, and cyclic shift preserves CF. So for any regular R meeting every primitive class, Q is CF ⇔ Q ∩ R is CF.

**Proved obstructions to natural certificate schemes.** These are lemmas about certificate models, not theorems about all PDAs.
1. **Witness positions.** PROVED (unaudited).
   - A mismatch pair refutes at most one prime, so any pair-based certificate needs ≥ ω(n) pairs.
   - There are primitive words whose sets of prime-refuting positions are pairwise disjoint across primes (n = 12, 90, 840 verified).
   - So "one guessed position compared against all primes" fails already at n = 12, e.g. aabaabbaaabb.
2. **Semilinearity.** PROVED (audited). Suppose a CF language exposes, in a finite-state-markable way, a mismatch pair at a distance d with n/gcd(d,n) prime. Then only finitely many primes occur. *So any construction exhibiting a prime-tied refuting chord misses all long words of prime length.*
3. **One quantity against many.** PROVED (audited). {aᵏbaⁱbaʲ : i ≤ k, j ≤ k} and {aᵏbaⁱbaʲ : k ≠ i, k ≠ j} are not CF. This rules out "unique longest run" style transversals.
4. **Binary nested chains.** PROVED (unaudited). A nested chain of mismatch chords covering all distances exists only for words like aⁱbʲ.
5. **Cyclotomic barrier.** PROVED (audited; needs n ≥ 2).
   - Any sound certificate of the form "a fixed linear functional ≠ 0" misses every primitive w with Φ_n | w(x), i.e. every superposition of cosets for two different primes.
   - Example: aabaabbaaabb.
   - For n = 12, 18, 20, 24 these classes coincide exactly with the failures of obstruction 1 (2, 24, 6, 236 classes; EVIDENCE).
6. **Finite counting certificates** miss aᴷbaᴷ′b with K+K′ even. Those words need a genuine comparison K ≠ K′.

**Transversal data (EVIDENCE, n ≤ 20).**
- Lyndon words and unbordered words meet every class but are not CF.
- The cyclic properties "unique longest cyclic a-run" (≈ 74% of classes) and "… or b-run" (≈ 93%) are sound but neither covers everything.
- Genuinely CF sound normal forms cover a vanishing share (13% at n = 20; the counts are exactly Fibonacci numbers for n = 7..20, an observed pattern).
- A union of explicit CF certificate families covers > 99.5% but still misses classes at every tested n ≥ 14, including the prime lengths 17 and 19.

**Missing ingredient (theorem strength).** A *uniform* way to combine non-crossing comparisons that refute unboundedly many primes.

---

## 12. Related languages that are not context-free

| Language | Result | Status | Transfers to Q? |
|---|---|---|---|
| UB = unbordered words | not CF | **KNOWN**: Rampersad, Shallit, Wang, *Inverse star, borders, and palstars*, IPL 2011 (arXiv:1008.2440), Thm 7, also via Ogden. Independently re-proved here (audited). | No |
| Q ∩ {no border of length ≤ f(n)}, f non-decreasing and unbounded | not CF | PROVED (spot-checked by the auditor) | No |
| Q ∩ {no border of length ≤ c}, c constant | CF ⇔ Q is CF | PROVED (unaudited) | equivalent |
| rotations by ≤ c of UB | not CF | PROVED (unaudited; via an inverse morphism back to UB) | No |
| MP_c = {minimal period > n/c}, 1 < c < 5/4 | not CF | PROVED (unaudited) | No |
| L_mid = {no square centred at the middle cut} | not CF | PROVED (unaudited) | No |
| L_mid^{(k)} (any cut within distance k of the middle) | not CF | SKETCH plus simulation | No |
| {k ≥ i, k ≥ j}, {k ≠ i, k ≠ j} on three a-blocks | not CF | PROVED (audited) | No |
| bordered words | not CF | classical pumping | No |

**The UB proof (re-derived).**
- *Slice formula:* w = a^{x₁}ba^{x₂}ba^{x₃}ba^{x₄}b is unbordered iff x₁ > x₄ ∧ (x₂ ≠ x₄ ∨ x₁ > x₃).
- *Witness:* z = a^{p+1}b a^{p+p!}b a^{p+1+p!}b a^p b, with only the first run marked.
- *Every decomposition is killed:*
  - a pump containing b leaves the slice;
  - pumps in run 1, or touching runs 2–3, give x₁ ≤ x₄ at i = 0;
  - for runs 1 and 4: α > β fails at i = 0, α < β at i = 2, and α = β at i = 1 + p!/α, where the pumped word is a square.
- Exhaustively simulated for p ≤ 4 (up to 215,105 decompositions): 0 survivors.

**Why none of these transfers to Q (precise).** In each proof, most decomposition classes are killed by landing in a *primitive* word with a short or long *non-periodic border*. Those words form a **half-space** or a full-dimensional piece of the complement, e.g. {x₁ ≤ x₄}. Only one ratio class needs the factorial trick to land on a square. Q's complement consists of exact powers: subspaces with no half-spaces (§10). So the same proof shape cannot work for Q.

**Dichotomy theorems.** PROVED (unaudited).
- **Borders:** sound transversals forbidding borders of length ≤ f(n) are non-CF when f is unbounded, and equivalent to the main problem when f is bounded.
- **Local witnesses:** pinning the critical-factorization witness to the middle, or to any bounded window, gives a non-CF language. A free cut gives exactly MP (§13).

---

## 13. The MP target: words with minimal period > n/2

MP = {w : per(w) > |w|/2}.
- MP ⊆ Q, since uᵏ with k ≥ 2 has period ≤ n/2.
- MP contains UB, so it meets every primitive class.
- Hence **MP CF ⇒ Q CF**.
- Its complement (words with a period ≤ n/2) is thin, like Q's.

**Structure.** All verified by brute force (Route L, unaudited).
- **Proposition 13.1.** per(w) ≤ n/2 ⇔ w has a period in (n/4, n/2].
- **Proposition 13.2.** MP = {w : some cut c has local period > n/2}, via the critical factorization theorem.
- **Proposition 13.3.** w ∉ MP ⇔ w has a square prefix u² with u primitive and w a prefix of u^ω. By the three-squares lemma there are O(log n) such candidates, and the word itself locates them.
- **Proposition 13.4 (exact slice formula).** On (a⁺b)^r, w ∉ MP iff y = (x₂,…,x_r) is d-periodic for some d ≤ (r−1)/2 with x₁ ≤ y_d, or w is a square.

**Theorem 13.5 (MP_c not CF for 1 < c < 5/4).** PROVED (unaudited).
- *Proof:* Ogden on MP_c ∩ (a⁺b)⁴ with z = a^{X+1}ba^{X+D}ba^{X+1+D}ba^Xb, D = p!, X ≫ D.
- *Check:* an exhaustive string-level check (up to 2.1M decompositions) and a run-model check, with 0 survivors.
- *Sharpness:* the bound 1/5 is sharp for this witness family.
- *Mechanism:* the complement piece {x₁ ≤ x_r, x₁+1 ≥ θn} is full-dimensional for θ < 1/2 and empty at θ = 1/2.

**Theorem 13.6 (L_mid not CF).** PROVED (unaudited).
- L_mid ⊆ MP.
- L_mid meets every primitive class, by the critical factorization theorem applied to w³ (checked to n = 22).
- But L_mid is not CF: Ogden on z = b^{N−1}aᴺ | bᴺa^{N−1}, where any unbalanced pump pushes the middle into a periodic block.

**Why MP is still open.**
- On run slices, MP's complement is Q's geometry plus **one boundary half-space** on the first run.
- An unmarked interior co-pump defeats that half-space.
- Exhaustive run-model Ogden searches (r ≤ 6, p = 2, 3) found no non-degenerate witness.

**Affirmative side.** Nothing survived past n = 16. Abelian-unbordered words miss classes from n = 16, e.g. bbababaabbaabbaa. A real certificate needs "∀ℓ ∈ (n/4, n/2]: no centred repetition at a guessed cut", which requires crossing translation comparisons (theorem strength).

---

## 14. Computational data

(Route F. Everything here is EVIDENCE.)

**Counts.** |Q ∩ {a,b}ⁿ| for n ≤ 30 by Möbius, brute-force verified for n ≤ 22. A few values:

| n | 6 | 10 | 12 | 18 | 20 | 24 | 30 |
|---|---|---|---|---|---|---|---|
| primitive | 54 | 990 | 4020 | 261,576 | 1,047,540 | 16,772,880 | 1,073,708,010 |
| non-primitive | 10 | 34 | 76 | 568 | 1,036 | 4,336 | 33,814 |

**Minimum CNF grammar size of truncations (SAT, CaDiCaL).** Minimum number of nonterminals with L(G) ∩ Σ^{≤n} = T ∩ Σ^{≤n}:

| target \ n | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|
| non-squares | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 |
| non-cubes | 4 | 4 | 6 | 6 | 6 | ≥7 | – | – |
| neither square nor cube | 4 | 5 | 7 | 7 | 7–8 | – | – | – |
| Q | 4 | 4 | 6 | 7 | 7 | 7–8 | – | – |

*Reading:* this cannot distinguish Q from CF comparators. For n ≤ 9, Q differs from "neither square nor cube" only by a⁵, b⁵, a⁷, b⁷. The first non-unary difference, (ab)⁵, is at length 10, exactly where SAT becomes infeasible. Not worth pursuing.

**Shortest cyclically unique factor.** Worst case ⌊n/2⌋ (two-block words); average ≈ 3.2 at n = 20.

**Tester.** `campaign/tools/check_grammar.py` checks any CFG against Q exactly up to a given length, using bitset DP cross-checked against Earley parsing.

---

## 15. The common core every route hit

Independent routes (B, E, H, I, L) stalled at the same configuration:

> a primitive word that, after **one small local edit** per candidate, becomes an exact **q-th power** for unboundedly many different primes q. Fine–Wilf fails exactly at near-squares (two approximate periods ≈ n/2).

How it appears in each route:
- **Negative side (pumping).** Pumps that stay inside fixed lengths or run structures are provably harmless (§5, §10). Dense-marking pumps are provably harmless (§8.4). What remains is sparse marking, where pumped loops are long and of unboundedly many lengths (Gap G_sp).
- **Negative side (size).** Rectangle-type measures are provably vacuous. A lower bound would need a technique using the recursive, cross-length structure of a single grammar. None is known for ambiguous CFGs.
- **Affirmative side.** For each *fixed* block count, nested partial-sum comparisons do refute all primes at once (F₆, evidence to m = 24). But the comparison distances must be tied to m/p, which a uniform PDA cannot do (index matching, semilinearity).

No route found a sub-lemma strictly weaker than the original problem, except Gap G (dense case), which **was then proved**.

---

## 16. Open problems, ranked

| # | Problem | If resolved | Strength (best judgement) |
|---|---|---|---|
| 1 | **Gap G_sp** (Ogden for Q under colourings, with sparse markings), plus a rigorous repair of Corollary M3. Together these give OG(Q). | **Proof:** no closure + Ogden/Bar-Hillel argument can ever refute Q, a real theorem explaining 30 years of failure. **Disproof:** Q is not CF, which resolves the problem. | The most concrete open lemma found. Not judged theorem-strength. |
| 2 | Is MP = {per(w) > n/2} context-free? | CF ⇒ **Q is CF**. | Judged theorem-strength. |
| 3 | MP_c for 5/4 ≤ c < 2 | Any CF one ⇒ Q CF. | Conjectured not CF; needs a cheaper gadget for the 1:1 pump. |
| 4 | Is F_m CF for every m? (m = 30 is the first unsettled case.) | A non-CF F_m ⇒ **Q not CF**. | Evidence says all are CF. |
| 5 | A uniform-in-m nested certificate for Q ∩ (a⁺b)⁺ | Equivalent to **Q CF**. | Blocked by index matching. |
| 6 | "Index-mass rigidity" | Would give a non-CF proof of Q ∩ (a⁺b)⁺. | Theorem-strength. |
| 7 | Lemma S (all-certified trees for every n) | Completes the no-go for the swap game at all lengths. | Finite combinatorics. |
| 8 | A non-rectangle lower bound for general CFG size of Q_n (ω(n) nonterminals suffice) | **Q not CF**. | Theorem-strength. |
| 9 | Is (q(n)) the counting sequence of some CFL? | No ⇒ Q not CF. | As hard as the original problem. |

---

## 17. Errors caught by the audits

Recorded so nobody re-uses them.

1. **"Every grammar for Q_n needs ≥ c·n nonterminals" — FALSE.** For prime n, Q_n is the set of non-constant words. It has a CNF grammar with O(log n) nonterminals, built with an addition chain: 27 nonterminals at n = 13 and 155 at n = 1,000,003, checked exhaustively for n ≤ 17. The only unconditional lower bound is Ω(log n). (The refutation target ω(n) is unaffected.)
2. **"Q_n is a union of O(n) balanced rectangles", original version — off-by-one.** When 3 | n, wrapping windows have a linear side of length exactly n/3, outside (n/3, 2n/3]. Fixed by using non-wrapping windows (§5.2).
3. **"OG is closed under cyclic shift" — proof gap, withdrawn.** The mark count inside the transferred window was not bounded. Replaced by Lemma 7.3 (rotation-closure of Q).
4. **"The same proofs work for Bar-Hillel" — unjustified** for erasing images.
5. **Corollary M3 ("colour Bar-Hillel for Q") — FLAWED** at the i = 0 deletion step (§8.5).
6. **H's Corollary 5.3 — constant too small** for s ≥ 2. Fixed with margin 2π₀+1.
7. **H's Lemma 5.1 — one wrong justification** ("never the whole cycle"; aabaaba is a counterexample to the stated reason). The correct reason was supplied.
8. **J's Theorem 5 — was a sketch.** The antipodal-only case was missing and has been supplied.
9. **Linear "unique longest run" transversals are unsound**: (aba)² has a unique longest linear a-run, and abab has a unique b aᵏ b.
10. **"Testing to length 20 is enough" — false in practice.** U_K passes to length 21 and fails at 22.
11. **Novelty — one rediscovery.** "UB is not CF" is already in the literature (Rampersad–Shallit–Wang 2011).

---

## 18. Master status table

| Result | Section | Status |
|---|---|---|
| Slice-grammar lemma (≤ \|N\|·n nonterminals) | 5.1 | PROVED (audited) |
| Balanced-rectangle lemma | 5.1 | PROVED (audited) |
| Q_n = union of O(n) balanced rectangles (≤ 8 for odd n), non-wrapping version | 5.2 | PROVED (audited, with fixes) |
| Seam variant / every middle length | 5.2 | PROVED (unaudited) + EVIDENCE |
| Interchange barrier 1/(e(ω(n)+1)) | 5.3 | PROVED (audited) |
| Per-cut cover, communication complexity ≤ log₂n + O(log log n) | 5.3 | PROVED (audited) |
| Box barrier (8m)^{ω(n)} | 5.3 | PROVED (audited) |
| Bader–Moura ⇔ pump-rigidity; block-design proposition | 5.3 | PROVED (unaudited) / BLOCKED |
| Lemma A, Lemma B, no fooling pair (Thm 5.16) | 5.4 | PROVED (audited) |
| 11-label adversary; prime-power all-certified trees | 5.4 | PROVED (unaudited) |
| Lemma S for general n | 5.4 | EVIDENCE / open |
| Finite-intersection reformulations | 5.6 | PROVED |
| Ambiguity-2 CFL with Petersen-type GF | 6 | PROVED (audited) |
| Code-slice Möbius sums; slice dichotomy | 6 | PROVED / SKETCH |
| OG preserved by rational transductions and reversal | 7 | PROVED (audited, constant fix) |
| Any allowed chain from Q is one rational transduction | 7 | PROVED (audited) |
| Closure + Ogden refutes Q ⇔ ¬OG(Q) | 7 | PROVED (audited) |
| Ramsey proof of OG(Q) fails (counterexample) | 7 | PROVED |
| OG(Q) ⇔ ∀s CPL_s | 8.1 | PROVED (audited) |
| Power of colourings (walls, partners) | 8.2 | PROVED (audited) |
| Lemma U, large-i lemma | 8.3 | PROVED (audited) |
| Clustering lemma | 8.3 | PROVED (re-derived, not formally audited) |
| Labelled-sequence rigidity; Thm 5\*; Lemma 5.2 | 8.3 | PROVED (audited; one justification fixed) |
| Partner principle | 8.3 | PROVED (audited, constant fix) |
| **Gap G (dense case)** | 8.4 | **PROVED (audited, with fixes)** |
| Colour Bar-Hillel for Q (Cor. M3) | 8.5 | **FLAWED / unproved** |
| Gap G_sp; OG(Q) | 8.5 | OPEN (evidence: true) |
| Ginsburg reduction F_m ⇔ S_m | 9 | PROVED (audited) |
| Merge lemma | 9 | PROVED (audited, cosmetic fixes) |
| **F₆ = Q ∩ (a⁺b)⁶ is CF** | 9 | **PROVED (audited)** |
| Coverage for m ≤ 24 | 9 | EVIDENCE |
| F_m CF for all m | 9 | CONJECTURE |
| Q ∩ (a⁺b)⁺ CF ⇔ Q CF | 9 | PROVED (audited) |
| U_K sound and CF; fails at 22 | 9 | PROVED (unaudited) + EVIDENCE |
| Direction lemma | 10 | PROVED (audited) |
| Q ∩ (a⁺b)^r satisfies Ogden | 10 | PROVED (audited, with fixes) |
| Transversal reformulation | 11 | PROVED |
| Semilinearity, one-vs-many, cyclotomic obstructions | 11 | PROVED (audited) |
| Witness-position, nested-chain obstructions | 11 | PROVED (unaudited) |
| UB not CF | 12 | KNOWN (RSW 2011); re-proved (audited) |
| Q ∩ P_f not CF (f unbounded) | 12 | PROVED (spot-checked) |
| Bounded rotations of UB not CF; border dichotomy | 12 | PROVED (unaudited) |
| MP_c not CF for 1 < c < 5/4 | 13 | PROVED (unaudited) |
| L_mid not CF; meets every class | 13 | PROVED (unaudited) |
| MP CF? | 13 | OPEN |
| Q CF? | — | **OPEN** |

---

## 19. Lean 4 formalization of the problem

A frozen Lean 4 statement is in `lean/PrimitiveWords/Statement.lean`, with acceptance rules in `lean/README.md`. **It has not yet been typechecked against Mathlib**, because Mathlib was not installed on the machine used.

**Definitions** (core of the file):

```lean
def IsPrimitive {α : Type*} (w : List α) : Prop :=
  w ≠ [] ∧ ∀ (u : List α) (n : ℕ), (List.replicate n u).flatten = w → n = 1

def primitiveWords (α : Type*) : Language α := {w | IsPrimitive w}

def Target.negative : Prop :=
  ¬ (primitiveWords Bool).IsContextFree

def Target.affirmative : Prop :=
  ∀ (α : Type) [Fintype α], 2 ≤ Fintype.card α → (primitiveWords α).IsContextFree
```

**How these definitions behave.**
- The case u = [] is vacuous for non-empty w, and so is n = 0, so the definition says exactly "w ≠ ε, and w = uⁿ forces n = 1".
- `Language.IsContextFree` is **Mathlib's own definition**: some `ContextFreeGrammar` with a finite set of rules generates exactly the language.
- The file states context-freeness for grammars, not PDAs. The grammar/PDA equivalence is classical mathematics and is not formalised here.
- The file includes three sanity theorems: abab and ε are not primitive, and a single letter is primitive.

**A machine-checked solution must:**
1. prove a separate `theorem solution : PrimitiveWords.Target.negative` (or `.affirmative`). The targets are definitions, so "no `sorry` in the statement file" proves nothing;
2. leave the statement file byte-identical, with the SHA-256 recorded in the README;
3. build in a fresh checkout at a pinned Mathlib commit;
4. use only the axioms `propext`, `Classical.choice` and `Quot.sound` (`#print axioms`). Reject `sorryAx`, `Lean.ofReduceBool` (`native_decide`) and any user `axiom`;
5. pass an independent kernel replay with `leanchecker`;
6. pass a grep for `axiom`, `sorry`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `set_option debug`, `macro`, `elab` and `#eval`;
7. come with a human audit of the roughly 20 lines of definitions, and of Mathlib's context-free-grammar definitions at the pinned commit.

Mathlib does not appear to contain the pumping lemma or Ogden's lemma for context-free languages, so any negative proof would have to build that infrastructure first. The Langlib project may help. A Lean proof certifies correctness; for acceptance as a solution of the open problem, a human-readable account is still needed.

---

## 20. Recommendations for anyone continuing

1. **Literature first.** Read Dömösi–Ito (2014) and the later papers on context-freeness of primitive words. Establish which of §5–§13 are new before writing anything up. One result here was a rediscovery.
2. **Publishable core, if new.** A note along the lines of "Barriers to proving that the primitive words are not context-free". It would combine:
   - the O(n) rectangle cover and the interchange and box barriers (§5);
   - the reduction of closure-chain arguments to OG(Q) and its colour reformulation (§7–8.1);
   - Gap G (dense case) (§8.4);
   - F₆ CF and the fixed-run Ogden theorem (§9–10).
3. **One focused attack:** Gap G_sp (§8.5), together with a rigorous repair of Corollary M3. Either outcome is meaningful. This needs one careful line of proof with audits, not a swarm of agents.
4. **New tools for the negative direction.** Pumping-type invariants appear to be *satisfied* by Q. A refutation probably needs a necessary condition for context-freeness strictly stronger than Ogden: e.g. exact pumping characterisations (Wise's 1976 "strong pumping lemma" is recalled as a characterisation of CFLs; verify), or rational-cone / generator invariants. These are the only unexplored directions found.
5. **Affirmative direction.** The open question is whether the nested partial-sum mechanism of F₆ can be made uniform in the block count. Any candidate must be tested on scaled words, long {1,2}-run sequences and near-powers, not only all words to length 20.
6. **Settle m = 30** (three primes) exactly, as a sanity check of the bounded-slice conjecture.

---

## 21. References

These are cited from memory unless marked; verify bibliographic details before use.

- P. Dömösi, S. Horváth, M. Ito — origin of the question; P. Dömösi and M. Ito, *Context-Free Languages and Primitive Words*, World Scientific, 2014.
- H. Petersen, "The ambiguity of primitive words", STACS 1994.
- S. Horváth, "Strong interchangeability and nonlinearity of primitive words", 1995.
- H. J. Shyr and C. M. Reis — products of primitive words (Q² result).
- W. Ogden, R. J. Ross, K. Winklmann, "An 'interchange lemma' for context-free languages", SIAM J. Comput. 14 (1985).
- C. Bader, A. Moura, "A generalization of Ogden's lemma", J. ACM 29 (1982).
- W. Ogden, "A helpful result for proving inherent ambiguity", 1968 (Ogden's lemma).
- S. Ginsburg, E. H. Spanier, bounded ALGOL-like languages, 1964; S. Ginsburg, *The Mathematical Theory of Context-Free Languages*, 1966.
- S. Ginsburg, J. Ullian — unambiguity of bounded languages, 1966.
- A. N. Maslov, 1973; T. Oshiba, 1972 — closure of CFLs under cyclic shift.
- J. Berstel, L. Boasson — Lyndon words are not context-free.
- **N. Rampersad, J. Shallit, M.-W. Wang, "Inverse star, borders, and palstars", Information Processing Letters (2011), arXiv:1008.2440** (verified by web search) — unbordered words are not CF.
- M. Domaratzki, N. Rampersad, Abelian primitive words, 2010.
- P. Flajolet, "Analytic models and ambiguity of context-free languages", TCS 1987.
- N. J. Fine, H. S. Wilf, "Uniqueness theorems for periodic functions", 1965.
- Y. Césari, M. Vincent; J.-P. Duval — the critical factorization theorem.
- M. Crochemore, W. Rytter — the three-squares lemma.
- N. G. de Bruijn — vanishing sums of roots of unity.
- N. Chomsky, M.-P. Schützenberger — algebraicity of CF series.
- D. Wise, "A strong pumping lemma for context-free languages", TCS 1976 (recalled; verify).

---

## 22. Appendix: where the detailed reports live

All paths are relative to the project folder.

| File | Contents |
|---|---|
| `campaign/PROBLEM.md` | The problem brief given to every agent |
| `campaign/REGISTRY.md` | Approach registry with every verdict |
| `campaign/FINAL_REPORT.md` | Short end-of-campaign summary |
| `campaign/round1/A_closure.md` | Closure reductions, OG, Ramsey counterexample, F₆ reduction |
| `campaign/round1/B_interchange.md` | Interchange barrier, box barrier, Bader–Moura |
| `campaign/round1/C_structural.md` | Lemmas A/B, swap no-go, labelling scheme |
| `campaign/round1/D_analytic.md` | Analytic barrier, ambiguity-2 example, slice dichotomy |
| `campaign/round1/E_constructive.md` | Transversals, certificate obstructions, cyclotomic barrier |
| `campaign/round1/F_compute.md` | Counts, SAT minimum grammars, transversal coverage |
| `campaign/round1/G_sizebounds.md` (+ `G_sizebounds_code/`) | Slice lemmas, O(n) rectangle cover, finite intersections |
| `campaign/round2/H_og.md` | OG(Q) reformulation, rigidity, partner principle, Gap G |
| `campaign/round2/I_bounded.md` (+ `I_bounded_m6_linear_sets.json`) | Bounded slices, F₆ CF, merge lemma, U_K |
| `campaign/round2/J_unbordered.md` | UB not CF, border dichotomy, fixed-run Ogden theorem |
| `campaign/round2/K_audit.md` | Audit of round 1 |
| `campaign/round3/L_mp.md` | MP, MP_c, L_mid |
| `campaign/round3/M_gapG.md` | Proof of Gap G (dense case), Corollary M3 |
| `campaign/round3/N_audit.md` | Audit of round 2 and of M |
| `campaign/tools/check_grammar.py` | Exact CFG-vs-Q tester |
| `lean/PrimitiveWords/Statement.lean`, `lean/README.md` | Lean statement and acceptance rules |
