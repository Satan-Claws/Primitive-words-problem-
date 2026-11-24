# Task G: ambiguity growth of the R4 test grammars (walk.md, builder3.md)

**Summary.** Neither test grammar generates Q, so neither bears on the main problem.

- **walk.md.** The grammar printed in walk.md §1 is **exponentially ambiguous**.
  - There is an explicit C_exp witness [written proof], and A_G grows by a factor of about 4 per 4 letters [computational].
  - A same-language repair is polynomially ambiguous, with amb ≤ n^{k+1} for T^k [written proof]. This is harmless, because L ⊊ Q: L has density → 0, and the first miss is `ab`.
- **builder3.md.** builder3 gives **no grammar**: 𝒰 is defined only by membership tests.
  - L(𝒰) ≠ Q. The first discrepancy is at n = 26, re-verified [computational].
  - A witness-count proxy for the natural guess-and-verify grammar grows about n³ [computational, proxy only].

Scripts are in `polynomial-ambiguity/round2/scripts/`:
- `testgram_cfg.py`: the CFG toolkit and a big-int CYK counting DP;
- `testgram_walk.py`;
- `testgram_builder3.py`.

## 1. walk.md: G_k for T^k(E′), k = 1, 2, 3

### 1.1 Grammar and language

- **E′ grammar.** The base grammar is copied verbatim from walk.md §1:
  - S → K X K | K Y K
  - K → ε | X K Y K | Y K X K
  - The pieces are X → a, Y → Z a, Z → b W a W, W → ε | b W a W.
- **The operator T.** T(M) = Cyc(σ(M)) ∪ swap(Cyc(σ(M))). The cyclic closure is the exact construction of `PA/poly_S4C.md` Theorem C, with amb_Cyc(w) = Σ_{j<n} amb(rot_j w).
- **Construction.** G_1 = T(E′) and G_{k+1} = T(G_k). These are built literally in code.
- **Tree-count-preserving transforms only:**
  - ε-removal, used only where each nullable nonterminal has exactly one ε-tree (asserted);
  - acyclic unit-rule removal;
  - binarisation.
- **Sizes.** The CNF sizes (nonterminals / rules) are 101/342, 433/2112 and 1745/12824 for k = 1, 2, 3.

**Language claim in walk.md.** L(G_k) ⊆ Q is claimed exactly. Equality with Q is not claimed: the density is ≍ n^{−2^{−(k+1)}}.

**Language check [computational].** Literal CYK was run on all words of length |w| ≤ 12, 10 and 8 for k = 1, 2, 3.
- No non-primitive word is accepted.
- The first primitive word that is missed is `ab` (n = 2): Δ = 0, so the walk tower cannot start.
- Every even length is missed entirely.

### 1.2 C_exp witness (Wich Def 2.7): [written proof] that the walk.md grammar is exponentially ambiguous

Use the ε-reduced rules of K: K → Y K X K | Y X K | X Y | …. Two distinct pumping trees at K have the same interface (α, β) = (YXYX, ε):
- T1: K → Y K X K, then the first K → X Y. The frontier is Y·XY·X·K.
- T2: K → Y X K, then K → Y X K. The frontier is YX·YX·K.

K is useful in G_k for every k, since its sibling rules are copied into the Cyc grammar. So C_exp holds, and G_k is exponentially ambiguous for k = 1, 2, 3.

The cause: K is meant to be "balanced words", but its inner K is not restricted to Dyck words. Explicitly, K((ab)^m) satisfies the Catalan recursion.

**Explicit family.** w_m = (a·baa)^m·a has |w_m| = 4m + 1 and Φ(w_m) = (XY)^m X. Its counts are amb_{G_1}(w_m) = 4, 13, 42, 138, 462, 1573, 5434, 19006 for m = 1..8. This is ≥ C_{m+1} ≈ 4^m, so the growth rate is √2 per letter.

### 1.3 Exact reduction formula (cross-checked against literal CYK: 0 mismatches)

Notation:
- swap w so that D = Δ(w) > 0;
- Φ(w) ∈ {a,b}^D is its first-passage type word.

Then:
- amb_{G_1}(w) = Σ_{t<D} amb_{E′}(rot_t Φ(w));
- amb_{G_k}(w) = D · amb_{G_{k−1}}(Φ(w)) for k ≥ 2.

Proof: Theorem C, plus three facts:
- the canonical rotations of w are exactly D of them (cycle lemma), and their type words are the D rotations of Φ(w);
- the piece decomposition is unique and the pieces are unambiguous;
- amb_{G_{k−1}} is invariant under rotation and swap.

**Literal CYK checks.** Comparing the literal CYK count with the formula over all words of length |w| ≤ 12, 10 and 8 for k = 1, 2, 3 gave 0 mismatches for both variants.

**Computing A_G(n) from the formula.** A_G(n) is obtained by enumerating type words v with #a + 3#b ≤ n. This is exhaustive, because the shortest w with Φ(w) = v is v[a→a, b→baa].

### 1.4 Repaired grammar G′_k (same language)

The repair replaces K by the first-return grammar K → ε | X P Y K | Y M X K, where P and M are Dyck-word grammars (`EFIX`).

Bounds [written proof, from §1.3]:
- amb_{E′}(v) ≤ |v|;
- amb_{G′_1}(w) ≤ D² ≤ n²;
- amb_{G′_k}(w) ≤ n^{k+1}.

Since these bounds are polynomial, Wich's dichotomy implies that G′_k has no C_exp.

### 1.5 A_G(n) tables [computational; exact for n ≤ 33, all words]

Values change only at odd n.

| n | lit k=1 | fix k=1 | lit k=2 | fix k=2 | lit k=3 | fix k=3 |
|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 3 | 3 | 3 | 3 |
| 9 | 13 | 9 | 20 | 20 | 140 | 140 |
| 13 | 42 | 16 | 117 | 81 | 180 | 180 |
| 17 | 138 | 25 | 143 | 99 | 1521 | 1053 |
| 21 | 462 | 36 | 546 | 208 | 1755 | 1215 |
| 25 | 1573 | 49 | 2346 | 425 | 10374 | 3952 |
| 29 | 5434 | 64 | 2622 | 475 | 11466 | 4368 |
| 33 | 19006 | 81 | 9702 | 756 | 58650 | 10625 |

Maximisers:
- **k = 1:** rotations of (abaa)^m a, i.e. Φ = (ab)^m a.
- **k = 2:** a^4 b a (a^4 b a)^j-type words, i.e. Φ = a^3 b a^3 b ….
- **k = 3:** (a^6 b a)-blocks.

Growth verdicts:
- **lit k = 1:** the ratio per +4 letters is 3.25 → 3.50 and rising toward 4. This is exponential, consistent with the Catalan bound.
- **fix k = 1:** A(n) = ((n+3)/4)² exactly, so the growth is quadratic.
- **fix k = 2, 3:** the log-log slopes over n = 17..33 are about 3.1 and 3.5, below the proved degrees 3 and 4.

## 2. builder3.md: union 𝒰

### 2.1 Grammar

**No grammar exists in builder3.** 𝒰 is defined by the C membership tests in `R4/../scripts/builder3/cov.c`:
- the families D, GB, RD, RGB, EP, PAR, L\*_{ℓ≤8}, BGB, T1–T3 and TG2;
- TA = BASE ∪ T(BASE) ∪ T²(BASE), with B = 3 and ANYT = 1.

Context-freeness is argued only via closure properties and PDA sketches. So amb_𝒰 is undefined until someone fixes a grammar, and an exact A_G(n) cannot be computed.

### 2.2 Language check [computational, re-run of cov.c]

- **Soundness:** no non-primitive word of length ≤ 22 is accepted.
- **Coverage:** every Lyndon word of length n ≤ 25 is covered.
- **First discrepancy, n = 26:** two primitive necklaces are not in 𝒰:
  - `aaaaaaabbbbabbaabaabbabbbb`
  - `aaaabaabbabbaabaaaabbbbbbb`
- n = 27: no necklace is missed. n = 28: 60 necklaces are missed (builder3's file; not re-run).

So L(𝒰) ≠ Q.

### 2.3 Witness-count proxy [computational; NOT a tree count]

The natural grammar is S → S_1 | … | S_13, where each S_i guesses its witness and then verifies it:
- the witness is a rotation, axis, sign, (letter, ℓ, s), Parikh line, or canonical rotation at each T-level;
- tree counts add over the union;
- a T-level multiplies by the number of canonical rotations.

If every verifier is unambiguous (an assumption, not checked), then amb = W(w), where W(w) is the total witness count. All primitive words of length ≤ 20 have W > 0, which matches cov.c.

| n | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
|---|---|---|---|---|---|---|---|
| max W | 600 | 1586 | 2616 | 5058 | 8068 | 12598 | 20076 |

- **Maximiser:** always a^{n−1}b. The term TA = T²(BASE) dominates (20001 of 20076 at n = 20).
- **Growth on a^{n−1}b:**
  - W = 209752 at n = 40, 2023092 at n = 80 and 6644500 at n = 120;
  - the local log-log slopes fall 3.66 → 3.39 → 3.27 → 2.93;
  - so the growth is about n³, i.e. polynomial.
- **Upper bound for this proxy (structural):** each family has O(n) witnesses, and each T-level contributes a factor D ≤ n. So W = O(n³) for TA.
- **C_exp:** cannot be checked, because no grammar exists. The internal fold and one-counter verifiers would need to be written out.

## 3. Verdict

No grammar here is both polynomially ambiguous and equal to Q:

| grammar | language | ambiguity |
|---|---|---|
| walk G_k (as printed) | ⊊ Q | exponential (C_exp) |
| walk G′_k (repaired) | the same ⊊ Q | polynomial, degree ≤ k+1 |
| builder3 𝒰 | ≠ Q (fails at n = 26) | no grammar; proxy ≈ n³ |

Nothing needs to be flagged for the main problem.
