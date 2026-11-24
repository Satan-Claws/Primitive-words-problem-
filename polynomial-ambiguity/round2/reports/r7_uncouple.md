# r7_uncouple.md — R7-A: dissolving the length coupling (affirmative side)

Scripts (in `scripts/`):
- `r7_uncouple_A.c`: exhaustive run over eight uncoupled split variants X·Y for n ≤ 24. Output: `r7_uncouple_A_out.txt`.
- `r7_uncouple_B.c`: rotation coverage of L_A, L_B and Ch, exhaustive for n ≤ 24 and Monte Carlo up to n = 10⁴. Outputs: `r7_uncouple_B_exh.txt`, `r7_uncouple_B_mc.txt`.
- `r7_uncouple_check.py`: exhaustive n ≤ 16 check of the identities used in Thm U2 and Prop U3.

## Verdict

**No sound, CF, poly-ambiguous, rotation-dense L was found.** FOLD-COUNTER and DENSE-SOUND remain OPEN.

Approach (A) is closed negatively, with an exact proof. Approach (B) reduces to the same one-vs-rest comparison, and the natural normal forms do not remove it.

1. **Thm U1 (collapse)** [written proof + exhaustive n ≤ 24]. Without a length constraint, D_b·P⁺ = P, where P = {w : every nonempty suffix is a-heavy} = (D_b a)⁺. The Dyck prefix adds nothing. Hence PS ∩ NonPrim = {u^p : u ∈ P, p ≥ 2} exactly. All eight variants contain P's powers (or the b-initial ones), so the excluded family E contains P ∩ NonPrim. Excluding E soundly is the original problem restricted to H ≥ 1.
2. **Thm U2 (what the coupling is)** [written proof + exhaustive n ≤ 16]. L_A = P ∩ {h ≤ 0 on [0, ⌈n/2⌉]}. Soundness needs only L_B = {H ≥ 1, h ≤ 0 on [0, ⌈n/2⌉]} ⊆ Q, and Rot(L_A) = Rot(L_B) exactly. L_B is not CF (Prop N transfers). The coupling is precisely "the walk stays ≤ 0 for half the length".
3. **Prop U3 (cycle-lemma normal form)** [written proof]. On P, w ↦ its block sequence (D₁,…,D_H) over the infinite alphabet D_b is a bijection that commutes with powers and with the H rotations inside P. So P ∩ Q = primitive block sequences.
   - L_A is the "dominant first letter" certificate. "Unique deepest/longest block" is sound and probably rotation-dense, but it is a one-vs-each comparison, which is non-CF.
   - Mapping blocks to a finite alphabet φ gives CF lifts σ(L′) with amb preserved. This only reduces the problem at length n to the same problem at length H ≈ √n (no base case).
4. **Coverage numbers** (not CF, diagnostic only): Rot(L_A ∪ swap) misses ≈ 0.35–0.39 of primitive words (n = 24 to 10⁴). Rot(Ch) misses ≈ 0.2/√n.

## 1. Approach (A): uncoupled split languages

Notation: h is the prefix walk (#a − #b), and H = h(n). A split s is a zero of h with x = w[0,s) and y = w[s,n) nonempty.

X variants:
- X0: b-first Dyck, h ≤ 0 on [0,s].
- X1: a-first Dyck, h ≥ 0.
- X2: any balanced x.
- X3: X0 with x ≠ ε.

Y variants:
- Y0: every suffix of y strictly a-heavy, i.e. h < H on [s,n).
- Y1: weak (h ≤ H) and H ≥ 1.

**Thm U1.** X0·Y0 = P (for |y| ≥ 1).

*Proof.* (⊇) Take x = ε. (⊆) On [0,s], h ≤ 0 < H. On [s,n), h < H. So h(j) < H for all j < n, which is exactly "every suffix a-heavy". ∎

**Consequences.**
- u^p ∈ P ⟺ u ∈ P, so PS ∩ NonPrim = {u^p : u ∈ P}.
- Every variant with x = ε allowed contains P. X3 contains {u^p : u ∈ P, u starts with b} ∋ (baa)².
- So E is never a "thin" family. It contains the powers of a positive-proportion one-counter language.

**Reduction.** By the cycle lemma, every w with H ≥ 1 has exactly H rotations in P. With Theorem C and swap, a poly-ambiguous CFG for (a rotation-dense part of) P ∩ Q gives one for Q ∩ {H ≠ 0}. So "PS ∖ E" is the original problem, not a relaxation.

**Exhaustive (n ≤ 24, `r7_uncouple_A_out.txt`).**

| check | X0 | X1–X3 |
|---|---|---|
| nonprimitive member ⟹ primitive root is a member | 0 violations | 0 violations |
| member root ⟹ its power is a member (converse) | 0 violations | fails: 44–119 counterexamples at n = 24 |
| X·Y ⊆ P (`notP`) | 0 | — |
| members at n = 24 | 1352078 = C(23,11) = \|P₂₄\| | — |
| \|X·Y ∩ NonPrim\| at n = 24 | 494 (Y0) / 844 (Y1) | X1: 494 / 844; X2: 504 / 845; X3: 405 / 666 |

- Natural grammar X·Y: exact max ambiguity (number of splits) = ⌊n/2⌋ for X0–X2 and ⌊n/2⌋ − 1 for X3. This is linear, but irrelevant because the languages are unsound.
- For X1·Y0, NonPrim ∩ X1Y0 = P ∩ NonPrim. Proof: on u^p, a zero s with h ≥ 0 on [0,s] must have s < |u|, so the walk is < H everywhere. The counts (494 = 494) agree.

## 2. Approach (B): rotation normal forms

**Normal-form transfer (trivial but decisive).** All rotations of u^p are p-th powers of rotations of u. So for any rotation choice N, N(u^p) is again a p-th power. A rotation choice never makes powers disappear; it can only make the certificate's shape special. Concretely:
- **Lyndon form:** N(Q) = Lyndon words, which are known not to be CF (Berstel–Boasson; recalled, not re-checked).
- **Cycle-lemma form:** N(Q) ⊆ P ∩ Q, covered by Prop U3.
- **Start at a strict minimum / after the longest a-run:** these are the reversal/swap of the P form, or "longest run unique" (one-vs-each, see below).

**Thm U2.**
- (i) L_A (split definition of Lemma SA) = P ∩ {h(j) ≤ 0 for j ≤ ⌈n/2⌉}. Take s = τ − 1, where τ is the first passage to +1. Then |x| ≥ |y| ⟺ τ − 1 ≥ n/2.
- (ii) L_B := {H ≥ 1, h ≤ 0 on [0, ⌈n/2⌉]} ⊆ Q, without P. If w = u^p, then |u| ≤ n/2 and h(|u|) = H/p > 0.
- (iii) Rot(L_B) = Rot(L_A). Let M = max_{[0,n)} h.
  - If M ≤ H − 1, rotation 0 is already in P, hence in L_A.
  - Otherwise M ≥ H, so M ≥ 1 and its first attainment i* lies after ⌈n/2⌉. The rotation at i* is in P because i* is the first argmax. Its walk stays ≤ 0 on [i*, n + ⌈n/2⌉], because h(j − n) + H ≤ H ≤ M. That stretch has length ≥ ⌈n/2⌉. ∎
- (iv) L_B is not CF. For l ≥ 2, every word of the slice b⁺a⁺ba⁺ with H ≥ 1 is in P, so L_B ∩ slice = L_A ∩ slice. The Prop N pumping argument then applies verbatim.

**Checks.** (i), (ii) and (iii) were verified exhaustively for n ≤ 16 (`r7_uncouple_check.py`: 0 mismatches). (iii) also holds in the exhaustive n ≤ 24 runs, where the miss counts for L_A and L_B coincide exactly.

**Prop U3 (block picture).**
- P = (D_b a)⁺ unambiguously, and w ↔ (D₁,…,D_H).
- w = u^p ⟺ the block sequence is (D₁…D_{H/p})^p.
- The H rotations of w inside P are exactly the rotations of the block sequence.

Sound certificates on block sequences, and what each would need:

| certificate | soundness | what a CFG would need | status |
|---|---|---|---|
| L_A: \|D₁\| > Σ_{i≥2}(\|D_i\| + 1) | sound | one length comparison that crosses two independent stacks | non-CF (Prop N) |
| depth(D₁) > depth(D_i) ∀ i ≥ 2, or global floor min_y h > H − depth(D₁) | sound: a periodic sequence repeats D₁ at level H/p | one-vs-each comparisons. The slice {b^d a^{d+1} b^k a^{k+1} b^l a^{l+1} : k < d−2, l < d−1} is non-CF by pumping (sketch) | non-CF |
| finite-alphabet image φ(c) ∈ L′ ⊆ Q₂ | sound | substitution σ(0) = a, σ(1) = D_b⁺ a gives a CF, amb-preserving lift σ(L′) | only reduces length n to length H ≈ √n with the same unsolved L′: circular |

**Remark (Parikh certificates are thin) [sketch].**
- Any additive cyclic statistic F (pattern counts) satisfies F(u^p) = p·F(u).
- {gcd(F, G) = 1} is not semilinear. Two-dimensional linear subsets of it are impossible, since they hit every residue class mod large primes.
- So CF Parikh-type certificates live on finitely many lines, such as F − G = ±1, and have density O(n^{−1/2}).

## 3. Coverage of the (non-CF) sound certificates

Ch = {n·h(j) − j·H < 0 for 0 < j < n} is the strict below-chord language. It is sound, and Rot(Ch) = {unique argmax of T}, as in Lemma A of r6_miss.

| n | missLA = missLB | missCh |
|---|---|---|
| 20 | 0.3938 | 0.0453 |
| 23 | 0.2536 | 0 (n prime) |
| 24 | 0.3892 | 0.0471 |
| 64 (MC 4000) | 0.374 | 0.021 |
| 1000 | 0.358 | 0.0070 |
| 4096 | 0.375 | 0.0040 |
| 10000 | 0.346 | 0.0018 |

- Rows n ≤ 24 are exhaustive over primitive words (swap included). Larger n are MC with 4000 samples.
- Odd n do better because the period bound is n/3 there, but the fixed threshold ⌈n/2⌉ was kept.
- Rot(L_A) caps at ≈ 0.63 coverage. Even a hypothetical CF L_A is not rotation-dense in the "almost every" sense. Ch is dense, but its coupling (the slope H/n) is worse.

## 4. Assessment

- Every sound certificate found has the form "one component's measure vs. the rest/each other component". In the P-normal form these components are Dyck blocks, each needing its own stack. The cyclic closure is exact, so the rotation choice is free, but it cannot remove the comparison: N(u^p) is always a power.
- The uncoupled language is just P, which is closed under powers. So approach (A) carries no information.
- The remaining affirmative hope is unchanged: a branching mechanism that compares one Θ(n) Dyck component against the rest on a positive-density set (FOLD-COUNTER).

## Status

| claim | label |
|---|---|
| U1: D_b·P = P; PS ∩ NonPrim = P's powers; all 8 variants unsound with E ⊇ powers of a one-counter language | written proof + exhaustive n ≤ 24 |
| U2: L_A = P ∩ half-nonpositive; L_B ⊆ Q; Rot L_A = Rot L_B; L_B not CF | written proof + exhaustive n ≤ 16 (Rot equality also n ≤ 24) |
| U3: block bijection; φ-lift is CF and amb-preserving but circular | written proof |
| one-vs-each depth certificates non-CF | pumping sketch |
| Parikh certificates have density O(n^{−1/2}) | sketch |
| coverage: Rot L_A misses ≈ 0.35; Rot Ch misses ≈ 0.2/√n | exhaustive n ≤ 24, MC n ≤ 10⁴ |
| sound CF poly-amb rotation-dense L | **NOT FOUND (OPEN)** |
