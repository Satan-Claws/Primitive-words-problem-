# Report of agent "walk": a CF counterexample to (Q½)

**Headline (PROVED): (Q½) is FALSE.** There is an explicit context-free L ⊆ Q with |L_n| ≥ c·2^n·n^{-1/4} for all odd n.
Iterating the construction gives, for every k, a CF L_k ⊆ Q with density ≍ n^{-2^{-(k+1)}} on odd n. The k ≥ 2 lower bound is PROVED in outline and COMPUTER-CHECKED.
For example, T³(E′) has density 0.867 at n = 100001 (Monte Carlo).

Consequences:
- The density route in the form "(Q½) ⇒ Q not CF" is dead.
- dense.md's CRH conjecture is refuted.
- Any "CF ⊆ Q ⇒ density O(n^{-ε})" statement is also dead for each fixed ε.

Positive density by a CF subset of Q remains open (§4). **No proof of either resolution of the main problem is claimed.**

Scripts are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/walk/`:
- `walk.py`: exhaustive soundness and density, n ≤ 18;
- `exact.py`: exact counts of T(E′);
- `mc.py`: Monte Carlo up to n = 10^5;
- `crosscheck.py`: the literal substitution+rotation construction equals the certificate test, n ≤ 14.

## 1. The operator T (all PROVED)

**Notation.**
- a = +1, b = −1, Δ(w) = |w|_a − |w|_b, S_t is the prefix walk.
- B = {z : every prefix sum of z is ≤ 0 and Δ(z) = 0}. This is the Dyck language with b as the opening bracket; it is CF.
- P = {z a : z ∈ B}, the *first-passage pieces*.

**Lemma 1 (unique decomposition).** Let w satisfy D = Δ(w) ≥ 1 and S_t < D for all t < n ("w ends at a strict maximum"). Then w = f_1⋯f_D with f_j ∈ P, uniquely: f_j ends at the first passage time to level j. Conversely, every concatenation of D ≥ 1 pieces is such a word.

**Definition.**
- Let σ be the substitution σ(a) = {a}, σ(b) = {z a : z ∈ B, z ≠ ε}. Both images are CF.
- For such w, let Φ(w) ∈ {a,b}^D be the type word: the j-th letter is a iff f_j = a.
- For M ⊆ Σ^+, set T(M) = Cyc(σ(M)) ∪ swap(Cyc(σ(M))), where swap exchanges a and b.

**Lemma 2 (CF).** If M is CF, then T(M) is CF.
- CF languages are closed under substitution by CF languages (LITERATURE: Hopcroft–Ullman, Thm 6.2).
- They are closed under cyclic shift (LITERATURE: Maslov 1973 / Oshiba 1972).
- They are closed under homomorphism (swap) and under union.

**Lemma 3 (soundness).** If M ⊆ Q, then T(M) ⊆ Q.

*Proof.*
1. Q is closed under rotation and swap, so it suffices to show σ(M) ⊆ Q.
2. Let w ∈ σ(M). Then w = f_1⋯f_D with f_j ∈ σ(v_j) and v = v_1⋯v_D ∈ M. By Lemma 1, this is the first-passage decomposition of w, and Φ(w) = v.
3. Suppose w = x^p with p ≥ 2 and d = |x|. Then e = Δ(x) = D/p ≥ 1, and S_{t+d} = S_t + e.
4. If S_t ≥ e for some t < d, then S_{t+(p−1)d} ≥ D with t + (p−1)d < n. This is impossible.
5. So x ends at a strict maximum, and x = f_1⋯f_e by Lemma 1.
6. The walk after time d is a translate, so f_{j+e} = f_j. Hence v = (v_1⋯v_e)^p, which contradicts v ∈ Q. ∎

**Explicit grammar for σ(E′)**, where E′ = {Δ = ±1}:

    S → K X K | K Y K
    K → ε | X K Y K | Y K X K
    X → a
    Y → Z a
    Z → b W a W
    W → ε | b W a W

Then T(E′) = Cyc(L(S)) ∪ swap(Cyc(L(S))).

Directly, T(E′) is the set of words with |D| ≥ 1 whose cyclic sequence of first-passage pieces satisfies #(pieces equal to a) − #(pieces with nonempty z) = ±1.

Note: this is NOT a k-gram-count certificate. It counts pieces at the running maximum, so Theorems P and P^R do not apply. This is the "non-count" information that dense.md asked for. It is realized with ONE stack: the counter sits at the bottom of the stack and the Dyck stack of the current piece sits on top, because pieces are sequential.

## 2. Density of T(E′) (PROVED)

**Exact formula.**
- The number of canonical words (ending at a strict maximum) of length n with D pieces, k of which have nonempty z, is C(D,k)·N(k,m).
- Here m = (n−D)/2 and N(k,m) = [y^m](C(y)−1)^k = [y^{m−k}] C(y)^{2k} = (k/m)·C(2m, m−k) for k ≥ 1.
- Each cyclic class with D ≥ 1 has exactly D canonical rotations (cycle lemma), and Φ is the same up to rotation for all of them.
- Therefore

      |T(E′)_n| = 2 Σ_{D odd} (n/D) Σ_{k=(D±1)/2} C(D,k)·N(k,m).

  This is nonzero only for odd n, because D ≡ n mod 2.
- The formula matches exhaustive enumeration for n ≤ 17 (0.8223 at n = 17).

**Lower bound.** Restrict to odd D ∈ [√n, 2√n] and k = (D−1)/2. Using C(D,k) ≥ c2^D/√D, and C(2m, m−k) ≥ c4^m/√m since k = O(√m), each term satisfies

    (n/D)·C(D,k)·(k/m)·C(2m,m−k) ≥ c·2^n·D^{-1/2}·n^{-1/2} ≥ c′·2^n·n^{-3/4}.

There are about √n/2 such terms, so |T(E′)_n| ≥ c″·2^n·n^{-1/4}. ∎

Asymptotically, density ~ (8/π)·2^{-3/4}·Γ(1/4)·n^{-1/4} ≈ 2.74·n^{-1/4}.

**Exact values of density·n^{1/4} (COMPUTER-CHECKED, `exact.py`).** Compare with E′·n^{1/2} → 1.596.

| n | 101 | 1001 | 10001 |
|---|---|---|---|
| density·n^{1/4} | 1.985 | 2.265 | 2.455 |
| density | 0.626 | 0.403 | 0.245 |

## 3. Iteration (PROVED in outline + COMPUTER-CHECKED)

T^k(E′) is CF and contained in Q for every k (Lemmas 2 and 3).

*Density, in outline.*
1. Given D and m, the number of canonical words with Φ = v depends only on #_b(v) = k, through the weight N(k,m) ∝ k·C(2m, m−k)/m.
2. For k = D/2 + O(√D log D), this weight is constant up to a factor 1 + o(1), because (k² − k′²)/m = O(n^{-1/4} log n). The other values of k carry negligible mass.
3. So, given D, Φ is uniform on {a,b}^D up to 1 + o(1), and dens_{T(M)}(n) ≈ E[dens_M(D)] with D ≈ |N(0,n)|.
4. Hence density exponent α ↦ α/2, and T^k(E′) has density ≍ n^{-2^{-(k+1)}} on odd n.

**Monte Carlo (`mc.py`, 2000 samples each; columns k = 0..3).**

| n | k = 0 | k = 1 | k = 2 | k = 3 |
|---|---|---|---|---|
| 1001 | .045 | .402 | .805 | .927 |
| 10001 | .017 | .249 | .699 | .901 |
| 100001 | .004 | .135 | .567 | .867 |

**Exhaustive checks.**
- 0 non-primitive words for n ≤ 18 in E′, T(E′), T²(E′), T³(E′) and the even-n variant G.
- G uses the weight g(a) = 1, g(ba…) = −2, g(bb…) = 0 on pieces, with the condition Σg = ±1. It is CF by the same stack layout and sound by the same proof.
- G has density ≈ 0.3 at n = 18 and ≈ 0.06 at n = 10^5 (∝ n^{-1/4}, all n).
- T^k(E′ ∪ G) covers even n with slower growth (MC).

## 4. What remains: positive density (open)

The task's question (2) is answered in the negative for its intended direction. Walk-based certificates CAN be CF with density n^{-ε} for any ε > 0, so no class theorem of the form "walk-window certificates CF ⇒ density O(n^{-1/2})" is true.

The window certificate W itself was not proved non-CF.
- CONJECTURED: W0 ∩ b⁺a⁺b⁺a⁺ is not CF.
- Sketch (IDEA): on the sub-slice b^i a^{i+1} b^j a^l, the Parikh set is {2i ≥ j+l, l ≥ j}. This has the extreme ray (1,1,1,1) on blocks (b,a,b,a), and every cone vector with j > 0 has full support. So it is not stratified, and by Ginsburg's theorem the slice is not CF. Not written out carefully; the exact slice identity was not verified.

Positive density would follow from the infinite tower N_∞ = {w : the iteration Φ, Φ², … (with mirroring) reaches a single letter}.
- N_∞ ⊆ Q by Lemma 3 and induction.
- Heuristically N_∞ has density → 1 on odd n: failures need D = 0 at some level, and the probabilities Σ m_k^{-1/2} with m_{k+1} ≈ √m_k are dominated by the last O(1) levels.
- A single rotation is canonical at all levels simultaneously, since level-(ℓ+1) piece boundaries are a subset of level-ℓ ones.
- Is N_∞ (or a union over k) CF? The natural PDA keeps one Dyck segment per level, but a letter emitted through j consecutive empty levels requires restoring j markers. So it is probably not CF. This is OPEN.

## Registry entry
1. **Aimed at:** a CF L ⊆ Q of density ≫ n^{-1/2} (refuting (Q½)), or else non-CF-ness of walk-window certificates.
2. **Proved:**
   - T(M) := Cyc σ(M) ∪ swap preserves "CF and ⊆ Q".
   - T(E′) ⊆ Q is CF with |T(E′)_n| ≥ c2^n n^{-1/4} for odd n (exact formula).
   - Therefore **(Q½) is false and CRH (dense.md) is false.**
   - T^k(E′) has density ≍ n^{-2^{-(k+1)}} (outline + MC).
3. **Missing step:** for the density route, "every CF L ⊆ Q has lim inf |L_n|/2^n = 0" (or lim sup). It is open whether ⋃_k T^k(E′) or N_∞ is CF.
4. **Counterexamples found:**
   - T(E′), T^k(E′) and G refute (Q½), CRH, and any polynomial-rate density bound.
   - No positive-density CF L ⊆ Q was found.
5. **Strength:** the remaining density statement ("CF L ⊆ Q ⇒ density → 0") is still STRONGER than "Q not CF". Polynomial-rate versions are FALSE.
6. **Reopen or kill:**
   - Kill the density route entirely: a CF positive-density L ⊆ Q, e.g. by a CF implementation of the unbounded tower N_∞.
   - Reopen it: a proof that every CF L ⊆ Q has density o(1), which must now allow n^{-ε} decay. Theorem P-type counting cannot do this.
