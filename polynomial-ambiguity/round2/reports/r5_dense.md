# r5_dense.md — R5-B: DENSE-SOUND (affirmative side)

Script: `scripts/r5_dense_fold.py`. It runs the exhaustive soundness and density check for n ≤ 22, Monte Carlo up to n = 16384 (4000 samples per n), and the Lemma B check for n ≤ 14. Running it takes about 1 minute.

## Verdict

DENSE-SOUND is **not resolved**. I found no positive-density CF language inside Q. This round gives three results.

1. **A sound certificate of positive density whose checking is "one counter run along a fold"** [written proof + computational]. The language F_K ⊆ Q has density → (2/π)·arcsin√(2/3) ≈ 0.608. A variant F_δ has density → 1 − O(√δ). Both are folds of deterministic one-counter languages, recognisable unambiguously by a linear-indexed grammar or TAG. Whether some positive-density subset of either is CF is **OPEN**. This is the sharpest affirmative lead so far: the only missing ingredient is "counter along a fold".
2. **An obstruction to every count-based mechanism** (Theorem P_K) [written proof, local CLT cited as standard]. This covers Parikh lines, factor-count lines, and the Bézout/Christoffel split idea (a).
3. **The unique-longest-run lead (UMR) from R5-A.** Its sound relaxations that compare against a bounded set of runs are unsound (Prop U). UMR itself resists pumping, and whether it is CF is OPEN.

## 1. The interval fold certificate F_K [written proof]

Let d_k(w) = #a(w[0,k)) − #a(w[n−k,n)) for 1 ≤ k ≤ n/2, i.e. the a-count of the length-k prefix minus that of the length-k suffix. Put K_n = [⌈n/3⌉, ⌊n/2⌋] and

  **F_K = { w : d_k(w) ≠ 0 for all k ∈ K_n }.**

**Lemma F.** F_K ⊆ Q.

*Proof.* Let w = u^p with p ≥ 2 and m = n/p. Put j = ⌊p/2⌋, so j/p ∈ [1/3, 1/2] for every p ≥ 2 and k = jm ∈ K_n. Then prefix_k = u^j = suffix_k, so d_k = 0. ∎

The same proof works for any K_n that contains, for every prime p | n, some multiple jn/p with 1 ≤ j ≤ p/2. This gives

  **F_δ:** K = [⌈(1/2 − δ)n⌉, ⌊n/2⌋] ∪ {⌊p/2⌋·n/p : p prime, p | n, p ≤ 1/δ}.

The interval contains a multiple of n/p for every p > 1/δ. The finitely many extra points need only n mod p for a fixed finite set of p, which is regular.

**Pure sign.** d_k changes by at most 1 per step, so on an interval "≠ 0" means "same sign throughout". Hence F_K = F_K⁺ ⊔ F_K⁻, and membership has a unique certificate (ambiguity 1 if realised).

**Density** [computational; Brownian motion heuristic]. d_k is a lazy ±1 walk (pairs (w_i, w_{n−1−i})). For the interval, P(no zero of BM on [1/3, 1/2]) = (2/π)arcsin√(2/3) = 0.6082.

| n | 8 | 12 | 16 | 20 | 22 | 64 (MC) | 1024 | 4096 | 10000 | 16384 |
|---|---|---|---|---|---|---|---|---|---|---|
| \|F_K∩Σⁿ\|/2ⁿ | .570 | .549 | .614 | .592 | .613 | .614 | .620 | .613 | .603 | .603 (±.008) |
| F_{0.1} | .727 | .549 | .699 | .657 | .674 | .695 | .714 | .712 | .703 | .702 |
| F_{0.02} | | | | | | .849 | .870 | .873 | .866 | .875 |

The exhaustive soundness check found no non-primitive word in F_K ∪ F_{0.1} for n ≤ 22.

**Realisability.** Write π_i = (w_i, w_{n−1−i}) and e_i = [π_i=(a,b)] − [π_i=(b,a)]. Then F_K⁺ = fold(D), where D ⊆ Π* is the deterministic one-counter language "prefix sums of e are > 0 on the depth window K_n". Here fold(z) = left letters of z · reverse(right letters of z).
- fold(z₁z₂) = L(z₁)·fold(z₂)·R(z₁). So concatenation in D becomes *adjunction* in w, and fold(D) is a TAG/LIG language with an unambiguous grammar.
- **Why a CFG does not obviously do it.** Every CF subtree is either one-sided or contains the centre, and the centre spine carries only finite state.
  - Ballot certificates of positivity match a "−" pair at depth j with a "+" pair at depth i < j. In w, these arcs (i, j on the left, and their mirrors) cross every through-centre arc of intermediate depth.
  - The Hall/greedy reformulation (the t-th a from the outside on the left vs on the right, with left depth ≤ right depth) needs a cumulative length comparison. That is again a crossing ballot (§1 of `R2/r3_offw.md` R1 makes the same assessment).
- **Failed counterpart.** {xy : |x| = |y|, #a(x) = #a(y)} is **not CF** [written proof]. Intersect it with a⁺b⁺a⁺b⁺. The part with the centre in b^j is {a^i b^j a^i b^l : j ≥ l}. Apply Ogden to a^N b^N a^N b^N with block 1 marked: every pump up breaks i = k, or breaks j = l together with k ≥ i.
  So "equality across the fold" is not CF. The strict pure-sign version F_K is CF-undecided: its bounded intersections are given by inequalities between *outer* blocks, which are fold-nested (stratified in Ginsburg's sense). So no non-CF proof via bounded slices is available.

**Exact open target (FOLD-COUNTER).** Is there a CF L ⊆ F_δ (any δ) of positive density, with polynomial ambiguity? A yes answer gives DENSE-SOUND, with amb ≤ 2 if L = F_δ.

## 2. Obstruction: count certificates (Theorem P_K) [written proof]

Fix K. For w, let occ(w) ∈ ℕ^{Σ^K} be its cyclic K-window counts.

**Theorem P_K.** Let L be CF with L ⊆ {w : gcd(occ(w)) = 1}. Then |L ∩ Σⁿ| = O(2ⁿ n^{−1/2}).

*Proof.*
1. Annotate each word by its windows (R_K, an injective DFA product, as in `R2/r4_core.md`). The Parikh image of L-annotated is semilinear, a finite union of linear sets b + ℕP.
2. If b ∈ span_ℚ P, then for every large prime q there is t ∈ ℕ^P with b + Σt_i p_i ≡ 0 (mod q), contradicting gcd = 1. So there is an integer functional φ with φ(P) = 0 and φ(b) ≠ 0, and φ(occ(w)) = φ(b) is constant on the linear set.
3. φ(occ) is an additive functional of the de Bruijn Markov chain.
   - If it is cohomologous to κ·1, then φ(occ) = κn and the linear set meets only one length.
   - Otherwise its variance is ≍ n, and the lattice local CLT gives P(φ(occ) = c) = O(n^{−1/2}). ∎

**Corollaries.**
- (i) Every LIN/FL gadget and every finite union of them has density O(n^{−1/2}). This proves the §4 sketch of r4_core.
- (ii) **Idea (a), the Bézout split, is capped.** Lemma B below shows that the split *exists* for every word with g = 1, so the certificate set has density 6/π². But any CF L ⊆ {g = 1} is covered by Theorem P_K with K = 1, so its density is O(n^{−1/2}). A Christoffel/Stern–Brocot witness cannot help: the Parikh image alone kills it.
- (iii) A dense L must contain a positive fraction of words with g > 1 that have varying prime factors. Its certificate must be positional, not a count. F_K is exactly such a certificate.

**Lemma B** [written proof; checked exhaustively for n ≤ 14]. g = gcd(A,B) = 1 iff some cyclic factor x has n·#a(x) − A·|x| = ±1, which is det(ψx, ψw) = ±1.

*Proof (⇐).* The determinant is a multiple of g.

*Proof (⇒).* Take ℓ ≡ −A⁻¹ (mod n). The cyclic windows of length ℓ have mean a-count c − 1/n, where c = (Aℓ+1)/n. The count moves in steps of ±1 and is not constant, so it hits c. ∎

## 3. The unique-longest-run lead (R5-A F4) [assessment + one written proof]

**Prop U (relaxations of UMR are unsound)** [written proof]. Suppose a certificate checks "run ρ is longer than every run in a set S(ρ, w)", and |S| is bounded or S is determined by positions within distance o(n/p) of ρ. Then the certificate accepts u^p whenever u has a unique longest run. Soundness for a prime p needs S to contain a run at offset ≡ 0 (mod n/p) from ρ, for every p | n. That is one exposed chord per prime, which Theorems V and X forbid. Comparisons nested around ρ inherit this.

So a sound UMR-type certificate must compare ρ with Θ(#runs) runs, and that reuses the number m = |ρ| unboundedly often.

**UMR itself.** Standard and Ogden pumping both fail to refute CF-ness. Pumping a letter a merges two runs, which only *creates* a longer unique maximum. Bounded slices are stratified, since all comparisons share the block of ρ. The CF status is **OPEN**. I conjecture that it is not CF: it needs m to be copied to every run.

UMR and F_K are the two known sound certificates of positive density. UMR is "count = 1 of a globally defined feature". F_K is "pure-sign counter along a fold". Both sit just above CF.

## 4. Idea (b): hidden multi-frequency folds

Every pure-sign letter fold, as in G_fold, LF, PF and RLF, needs Θ(n) mirror pairs to agree, so its density is e^{−Ω(n)}.

F_K is the "integrated" version: it asks only for sign persistence of the *cumulative* fold difference over a window of length Θ(n). That turns an exponentially rare event into a constant-probability one. One fold through the centre already handles every prime, because ⌊p/2⌋/p ∈ [1/3, 1/2]. No multi-frequency structure is needed.

## Status

| claim | label |
|---|---|
| Lemma F (F_K, F_δ ⊆ Q) | written proof; exhaustive n ≤ 22 |
| density of F_K ≈ 0.608, F_δ → 1 | MC to n = 16384 + BM heuristic |
| F_K = fold of a deterministic one-counter language (TAG, unambiguous) | written |
| F_K, or a dense subset of it, is CF | OPEN (FOLD-COUNTER) |
| {xy : \|x\|=\|y\|, #a(x)=#a(y)} not CF | written proof (Ogden on a bounded slice) |
| Theorem P_K, Corollaries (i)–(iii), Lemma B | written proof (local CLT cited); Lemma B also checked n ≤ 14 |
| Prop U | written proof (reduction to Theorems V/X) |
| UMR CF? | OPEN (conjecture: no) |
