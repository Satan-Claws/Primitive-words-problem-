# Round 3 / M: Gap G — status report

Researcher M. **Verdict: Gap G is TRUE (proved below, direction (b)).** The proof is short and uses only round-2 tools (H's Theorem 5, Lemma 4, facts F1–F3). The new ingredient is applying Theorem 5 **across different buffer candidates**, not just across the exponents of one candidate.

Consequences:
- **Corollary M3 (colour Bar-Hillel for Q, proved modulo H's Cor 5.3).** For every s there is p such that every primitive z with |z| ≥ p, under every s-colouring of its cut points, has a good colour-loop decomposition with |vwx| ≤ p. Equivalently, every π⁻¹(Q) ∩ R (π letter-to-letter, R regular) satisfies the Bar-Hillel pumping lemma.
- Direction (a), a counterexample built from isolated rigid runs and buffers, is **impossible**. In one buffer, all large-exponent kills must create the *same* new run at the *same* place, whatever q, i or the target run. So Sturmian or Thue–Morse buffers plus factorial run lengths cannot work.
- **What is still open:** OG(Q) for **sparse markings**, stated as Gap G_sp in §6. G and M3 do not reach it, because colour loops between sparse marks are long and their lengths are unbounded. So OG(Q), and hence the question "can closure chains plus Ogden refute Q?", remains open. Only the Bar-Hillel (full-marking) half is now settled, and only for letter-to-letter annotations. §5 explains why that matters.

H's §7 said "defeating G means one primitive word that is a q-th power after one local edit per candidate, for ≈ p/s² triples (edit, i\*, q)", and called G theorem-strength. That description is right, but such a word cannot exist. Every large-exponent edit splits **the same gap word** of the run skeleton into two labels. Theorem 5 allows at most one such split to produce a proper period. The "unboundedly many primes" worry disappears because Theorem 5 is purely about labels and does not care which divisor d (equivalently which q) is used.

All proofs here are mine and **unaudited**. Code and outputs are in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/r3_g/`. They are evidence only.

---

## 0. Notation and imported facts

z ∈ {a,b}⁺ is primitive, n = |z|, cut points 0..n. A one-sided pump at α of length ℓ is v = z[α, α+ℓ), with z_i = z[0,α) vⁱ z[α+ℓ,n). It is *good* if z_i ∈ Q for every i ≥ 0. ρ = |root(v)|, so ρ | ℓ.

Fix s ≥ 1 and put π₀ := s. All loops used below have ℓ ≤ s, so ρ ≤ π₀.

**T-skeleton.** For a threshold T ≥ 2π₀, Sk_T(W) is the set of maximal cyclic runs of the cyclic word W with minimal period ≤ π₀ and length ≥ T. Order them by start. Gap word g_m = W[start_m, start_{m+1}).

Imported from H (round 2), with the proofs re-checked here:
- **F1.** Distinct runs with minimal periods π, π′ overlap in fewer than π + π′ − gcd(π,π′) positions.
- **F2.** Distinct skeleton runs have distinct starts.
- **F3.** For a nonempty skeleton, W ∉ Q ⇔ the cyclic gap sequence (g_m) has a proper period. The proofs need only T ≥ 2π₀.
- **Theorem 5.** h : ℤ_R → X with R ≥ 3 and S = {j, j′} non-antipodal (for example, adjacent). Then at most one h′ that agrees with h off S has a proper period. Re-verified exhaustively for **arbitrary** relabellings of S (not only the integer lines H checked): R ≤ 9, 3 labels (2 for R ≥ 8), every non-antipodal pair and every single site, 0 violations. See `t5_check.py` and `t5_out.txt`.
- **Lemma 4 (clustering).** Fix ℓ and i ∈ {0, 2, 3, …}. Let one-sided pumps of length ℓ at α < α′ both fail at exponent i, with α′ − α + max(i−1,0)ℓ ≤ n_i/6, where n_i = n + (i−1)ℓ. Then z[α, α′+ℓ) has period ℓ.
  - I re-derived the i ≥ 2 step: cancelling gives v^{i−1}Y = Y v′^{i−1} with Y = z[α,α′), so Yv′ is a prefix of v^∞.
  - Lemma 4a was re-checked: the two cases P = P′ and P ≠ P′ (P + P′ ≤ 5N/6 ≤ |A|, then Fine–Wilf).
- **Lemma 3.** A bad i ≥ 2 has (i−1)ℓ ≤ n − 2. Not needed below.

---

## 1. Statement

**Theorem M1 (Gap G).** Let s ≥ 1 and λ ≥ 2s. There is an explicit p = p(s,λ) such that the following holds.
- Let z be primitive, χ any s-colouring of the cut points of z, and B a factor of z of length p that contains no factor with a period ≤ s and length ≥ λ.
- Then there is a cut-point pair c < c′ in B with χ(c) = χ(c′), c′ − c ≤ s, such that the one-sided pump v = z[c,c′) is good.

In particular vwx = v ⊆ B, v contains a mark under full marking, and |vwx ∩ D| ≤ s. This is Gap G with π₀(s) = s, and Λ(s) = λ any value ≥ 2s.

**Parameters.**
- T := λ + 2s + 1 (skeleton threshold).
- i₀(ℓ) := ⌈T/ℓ⌉. Exponents i ∈ {0} ∪ [2, i₀(ℓ)) are *small*; exponents k ≥ i₀(ℓ) are *large*.
- μ := T + λ + 2s + 2 (margin).
- C := 1 + Σ_{ℓ=1}^{s} (i₀(ℓ) − 1) ≤ 1 + T(1 + ln s) (number of bad clusters).
- w := (s+1)·(C·(⌈1.5λ/(s+1)⌉ + 2) + 1) (working-window length).
- p := max(2μ + w, 6(w + T) + s).

So p = O(λ² log s).

The working window is W := B[μ, μ+w). Since n ≥ |B| = p ≥ 6(w+T) + s, every pair of sites in W satisfies the distance hypothesis of Lemma 4 for every small exponent. Indeed α′ − α + (i−1)ℓ ≤ w + T ≤ (n−s)/6 ≤ n_i/6.

---

## 2. The local skeleton lemma

**Lemma M1.1 (where T-runs can be).** Every T-run M of z meets B in fewer than λ positions, and that intersection is a prefix or a suffix of B. Hence no T-run of z meets B[λ, p−λ). All of B[λ, p−λ) lies inside one gap of Sk_T(z), from start(S_R) to start(S_1), if R := |Sk_T(z)| ≥ 1.

*Proof.* M ∩ B is a factor of B with a period ≤ s, so |M ∩ B| < λ. Since |M| ≥ T > λ and |B| = p > λ, the interval M sticks out of B on exactly one side. ∎

**Lemma M1.2 (pumping in the buffer creates exactly one skeleton run).** Let α ∈ W, ℓ ≤ s, v = z[α,α+ℓ), and k ≥ i₀(ℓ). In z_k, let N be the maximal ρ-periodic cyclic interval containing the block K = [α, α+kℓ), and write N = [β, α+kℓ+e′) with e := α − β. Then:
1. e + ℓ + e′ < λ, and N has minimal period ρ ≤ s and length ≥ kℓ ≥ T.
2. Sk_T(z_k) = Sk_T(z) ∪ {N}. Positions outside K are identified in the obvious way.
3. If R ≥ 1, N lies in the gap of S_R and S_1. The gap words g_1, …, g_{R−1} of z_k are those of z, and g_R is replaced by the two labels X = z[start S_R, β) and Y = z_k[β, start S_1).

*Proof.*
1. z_k[β, α+kℓ+e′) = z[β,α) vᵏ z[α+ℓ, α+ℓ+e′) is ρ-periodic. Deleting v^{k−1} (length ≡ 0 mod ρ) from inside a ρ-periodic word leaves a ρ-periodic word, so z[β, α+ℓ+e′) is ρ-periodic. Its truncation z[α − min(e,λ), α+ℓ+min(e′,λ)) lies in B, because the margin μ > λ + s. So e < λ and e′ < λ, the whole factor lies in B, and e + ℓ + e′ < λ. The minimal period of N is ρ, since N ⊇ vᵏ with k ≥ 2 and root(v) is primitive. N is not the whole cycle, since |N| < kℓ + λ < n_k.
2. Let M ≠ N be a T-run of z_k with period π′ ≤ s.
   - By F1, |M ∩ N| < 2s, so |M ∩ K| < 2s. M cannot contain K (that would give |M ∩ K| ≥ kℓ ≥ T > 2s).
   - (i) Suppose M meets K or is adjacent to it, say on the right. Then the part of M after K starts at z-position α+ℓ and has length ≥ T − 2s = λ + 1. Its first λ+1 letters are z[α+ℓ, α+ℓ+λ+1) ⊆ B (margin), with period π′ ≤ s. This contradicts the hypothesis on B. The left side is symmetric.
   - (ii) Otherwise M and its two neighbouring letters avoid K. Then M is literally a cyclic interval of z with the same letters and the same maximality witnesses, so M ∈ Sk_T(z).
   - Conversely, every T-run of z, with its neighbours, lies at distance ≥ μ − λ − 1 > 0 from [α, α+ℓ) by M1.1. So it is unchanged in z_k.
3. By M1.1 no T-run of z starts in B[λ,p−λ). β ∈ [α−λ, α] lies in B[λ, p−λ) by the margin. So N's start falls in the gap from start(S_R) to start(S_1), and only that gap word changes. ∎

---

## 3. Large exponents: one split, one run

**Proposition M1.3.** Let F_L be the set of triples (α, ℓ, k) with α ∈ W, ℓ ≤ s, k ≥ i₀(ℓ) and z_k ∉ Q, and let β(α,ℓ,k) be the start of N.
- (R = 0) F_L = ∅.
- (R ≥ 2) All triples in F_L have the same β.
- (R = 1) The values β over F_L lie in an interval of length < λ/2.

In every case the sites α of F_L lie in an interval of length < 1.5λ, because 0 ≤ α − β < λ by M1.2(1).

*Proof.*
- **R = 0.** Sk_T(z_k) = {N}, a single run. By F2 and F3, a rotation by 0 < P < n_k fixing the skeleton would fix N's start, which is impossible. So z_k ∈ Q.
- **R ≥ 2.** Label the ring ℤ_{R+1} by g_1, …, g_{R−1} at positions 1..R−1, with positions R and R+1 free; these are adjacent. Since R+1 ≥ 3, they are non-antipodal.
  - By M1.2(3) every triple in F_L yields a relabelling (X, Y) of these two positions, and by F3 the relabelled sequence has a proper period.
  - By Theorem 5 at most one relabelling has a proper period. So all triples in F_L give the same (X,Y), hence the same |X| = β − start(S_R), hence the same β.
- **R = 1.** Ring of size 2. By F3, z_k ∉ Q ⇔ X = Y, where X = z_k[s₁, β) and Y = z_k[β, s₁+n_k), and s₁ = start(S_1).
  - Rotation by |X| is an automorphism of z_k that sends S_1 to N. So |N| = |S_1| and Y = N·U with N the run word.
  - Undoing the pump inside N gives z read from s₁ as X · N⁻ U = N U N⁻ U, where N⁻ = z[β, β+|N|−(k−1)ℓ) is the ρ-periodic factor of M1.2(1), with |N⁻| < λ.
  - Hence n = 2|N| + 2|U| − |N| + |N⁻|, so β − s₁ = |X| = |N| + |U| = (n + |S_1| − |N⁻|)/2.
  - For two triples, n and |S_1| are the same, so |β − β′| = ||N⁻| − |N′⁻||/2 < λ/2. ∎

**Remark (why q is irrelevant).** Theorem 5 forbids two different relabellings of the split gap from both being periodic, *for any two divisors d, d′ of R+1*. The target run (the image of N under the rotation), the prime q, the exponent and the length n_k may all differ between candidates. It makes no difference. This is the step H's N4 left open: H applied Theorem 5\* only along the exponent line of one candidate.

---

## 4. Small exponents and the count

**Proposition M1.4.** For fixed ℓ ≤ s and a small exponent i, the sites α ∈ W whose length-ℓ pump fails at exponent i lie in an interval of length < λ.

*Proof.* Take two such sites α < α′. By the choice of p, Lemma 4 applies, so z[α, α′+ℓ) has period ℓ ≤ s. This factor lies in B, so α′ + ℓ − α < λ. ∎

**Proof of Theorem M1.**
1. Every bad (α, ℓ, i) with α ∈ W lies in one of at most C "bad intervals", each of length < 1.5λ:
   - one interval per (ℓ, small i), from M1.4;
   - one interval for all large failures together, from M1.3.

   Exponent i = 1 is always fine.
2. Split W into ⌊w/(s+1)⌋ disjoint blocks of s+1 consecutive cut points. A bad interval meets at most ⌈1.5λ/(s+1)⌉ + 2 blocks. By the choice of w some block meets no bad interval.
3. By pigeonhole two of its s+1 cut points c < c′ share a colour, so v = z[c,c′) is a colour loop with 1 ≤ c′−c ≤ s.
4. Its site c avoids every bad interval, so v fails for no small i (M1.4) and for no large i (M1.3). Hence v is good. ∎

The proof uses only one-sided pumps. Two-sided pumps and long loops are not needed in the dense case.

---

## 5. Corollary: colour Bar-Hillel for Q

**Corollary M3.** For every s there is p such that every primitive z with n ≥ p and every s-colouring χ admit a good colour-loop decomposition with |vwx| ≤ p.

*Proof sketch.* Every step is rigorous given H's Lemma 5.1, Lemma 5.2, Theorem 5\* and Cor 5.3, used with skeleton threshold T′ in place of 2π₀. Their proofs only use T′ ≥ 2π₀.
- Let π₀ = s and T′ := Λ_H = (8+4s²)s² + 2, the run length required by Cor 5.3. Apply M1 with λ := T′ to get p_G. Take p = p_G + O(s²π₀²) + 2T′, so that Cor 5.3's mark count M fits.
- **(i) Some gap between consecutive T′-runs, or the whole of z if R = 0, contains a factor B of length p_G that is disjoint from all runs.** Then B has no factor with period ≤ s and length ≥ T′. Such a factor would extend to a T′-run starting strictly between two consecutive runs. Apply M1.
- **(ii) R = 1 and the complement of σ is shorter than p_G + 2T′.** Then |σ| > n − p_G − 2T′ is huge. By H Thm 2(b), a colour loop of length jπ ≤ s² sits deep inside σ. By Theorem 5\* (single site, R = 1) it is good for all i.
- **(iii) R ≥ 2 and all gaps are < p_G + 2T′.** Take consecutive σ, σ′ (non-antipodal) and apply Cor 5.3 with F near σ's end.

These cases are exhaustive. ∎

**Consequences and limits.**
- **What M3 gives.** By Theorem 1 of H (the Bar-Hillel version: D = all positions), M3 says that π⁻¹(Q) ∩ R satisfies Bar-Hillel for every letter-to-letter π and regular R.
- **What M3 does not give.** It does **not** follow that every rational transduction of Q satisfies Bar-Hillel. A's Theorem A(a) transfers pumping through erasing morphisms only with Ogden marks on the non-erased letters, and that is a *sparse* marking on the annotated preimage.
- So M3 rules out "letter-to-letter annotation + ∩R + Bar-Hillel" refutations, but not general "closure chain + pumping". For those, Gap G_sp below is exactly what remains.

---

## 6. What remains: sparse markings (Gap G_sp)

**Gap G_sp.** For every s there is p such that for every primitive z, every s-colouring χ, and every mark set D whose window holds p marks with all consecutive marks at distance > g (g arbitrary, possibly ≫ p), there is a good colour-loop decomposition meeting the Ogden conditions.

Combined with M1/M3 via a density dichotomy this would give OG(Q). That combination is itself not written out: the mixed regimes, where some regions are dense and some sparse, need the same care as M3.

**Why the M1 method stops here** (precise failure points):
1. **Loop lengths.** Colour loops containing marks now have length ≈ (number of marks crossed)·g, with unboundedly many distinct values of ℓ. A wall colouring (H Thm 2(d)) forces every marked loop to cross ≥ s marks. Lemma 4 clusters failures only for **equal** (ℓ, i), so the count C of bad clusters is unbounded. A cross-length clustering lemma for small exponents would be needed. Lemma 4a breaks for different lengths n_i ≠ n_{i′}.
2. **Skeleton period threshold.** The large-exponent argument needs π₀ ≥ ρ(v). With long loops, π₀ must grow, and the unmarked stretches may contain long runs of period ≤ π₀. Then the "buffer" hypothesis of M1 is not available, and the new run may merge with or split existing ones (M1.2(2)(i) fails).
3. **Help available.**
   - Lemma U removes all i ≥ 1 failures for loops with a fresh conjugate. The decomposer has great freedom in sparse regimes: under the wall colouring, c and c′ range over whole unmarked gaps. So freshness is plausibly achievable, which would leave only deletions (i = 0).
   - Unmarked runs inside the window are free partner sites, as in the partner principle.

   I could not turn this into a proof. I do not see a reason to call G_sp theorem-strength. It is the single remaining piece, and it looks like it needs a "deletion clustering across lengths" lemma.

**Non-uniform remark (not proved in detail).** When marks have bounded gaps ≤ g, the M1 argument with π₀ = s·g appears to go through with p = p(s,g). This is useless for OG(Q), which needs p independent of g.

---

## 7. Direction (a): why the suggested designs cannot work

- **Every Sturmian, Thue–Morse or random buffer B with no factor of period ≤ s and length ≥ λ fails once |B| ≥ p(s,λ).** This holds whatever isolated factorially-rigid runs sit elsewhere, and whatever their lengths are. By M1.3, the factorial freedom in the isolated runs can arrange at most **one** large-exponent kill site cluster per buffer (one split of the buffer's gap word). By M1.4, small exponents give at most C clusters of size < λ.
- **The prover's best possible buffer** kills short loops on ≤ C·1.5λ = O(λ² log s) cut points. That lower-bounds any valid p but does not threaten G.
- **The q-th power idea is blocked by the same fact.** "Make each pumped word an exact q-th power for some i" fails because every such power, for every q, requires the *same* relabelling of the split gap (Theorem 5).

---

## 8. Computational evidence (evidence only)

| script | what | result |
|---|---|---|
| `t5_check.py` → `t5_out.txt` | Theorem 5, arbitrary relabellings of 1 or 2 non-antipodal sites, R ≤ 9 | 0 violations (≈106k (h, S) cases) |
| `claims.py` (s=2: `claims_s2.txt`; s=3: `claims_s3.txt`) | Words built from near-squares X·X⁻, multi-run words with Fibonacci/Thue–Morse/random buffers, and random words. For every buffer: (L) all large-exponent failures share β (R ≥ 2), spread < λ/2 (R = 1), none (R = 0); (S) per-(ℓ,i) clustering < λ. Uses *smaller* constants than the proof (T = 5s, margin 3s), so the test is harsher than the theorem. | s=2: 1023 buffers, 307 with large-exponent failures, **0 violations**. s=3: 531 buffers, 143 with large failures, **0 violations**. |
| `adversary.py` | Prover hill-climbing (O + B + O′) maximising surv = longest cut-point interval in B admitting an s-colouring with every short one-sided colour loop bad | surv = 1 in all runs (s=2, λ ∈ {4,6}, \|B\| = 40): the prover found essentially no bad short loops |
| `designs.py` → `designs_s2.txt` | Designed prover families: near-square a^K U a^j U, factorial family with buffers, two-defect near-squares | max surv = **5** (near-square, one cluster at the short run, as M1.3 predicts) |

---

## 9. Summary of rigorous content

1. **Lemma M1.2:** pumping a short loop deep in a run-free buffer adds exactly one T-skeleton run and splits exactly one gap word.
2. **Proposition M1.3:** all large-exponent failures in a buffer share the same new run start (R ≥ 2, via Theorem 5 across candidates), or lie within λ/2 (R = 1, via a length identity), or do not exist (R = 0).
3. **Proposition M1.4:** small-exponent failures cluster per (ℓ, i) (H Lemma 4).
4. **Theorem M1 = Gap G**, with p = O(λ² log s), one-sided pumps of length ≤ s.
5. **Corollary M3:** colour Bar-Hillel for Q, i.e. OG(Q) restricted to full markings and letter-to-letter annotations.
6. **Open:** Gap G_sp (sparse markings). This is now the exact residual of OG(Q). The new evidence is still consistent with OG(Q) being true, which would mean closure chains plus Ogden cannot refute CF-ness of Q.

**Audit request.** Lemma M1.2(2) (the margin bookkeeping), the R = 1 length identity in M1.3, and the generalisation of H's Lemma 5.1 and Cor 5.3 to threshold T′ in M3 should be checked line by line.
