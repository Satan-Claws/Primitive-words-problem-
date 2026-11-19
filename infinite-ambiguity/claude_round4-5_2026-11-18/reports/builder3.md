# Report of agent "builder3" (positive direction: patching the CF certificate union)

**Claim status: I claim no proof of either resolution.** I extend builder2's union of certificates with four new sound
families, all context-free. I then close it under walk.md's T-operator. The resulting single CF language
𝒰 ⊆ Q covers **every primitive word of length ≤ 25 and of length 27**. At n = 26 it misses 2 necklaces and at n = 28 it misses 60.
**Every remaining miss is balanced (|w|_a = |w|_b).** Monte Carlo coverage of 𝒰 stays at 0.96–0.98 for odd n and
0.81–0.90 for even n, up to n ≈ 800. In the same range, builder2's union falls to 0. I argue (§4) that for each fixed
tower depth the density still tends to 0, but only at astronomically large n.
The exact obstruction is "a balanced level occurs somewhere in the first-passage tower".

Scripts are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/builder3/`:
- `cov.c` (C, one core): modes `sound`, `cov` and `mc`;
- `classify.py`, `achiral.py`;
- `miss_n.txt`: the residual necklaces for n = 18..28.

Build with `gcc -O2 -o cov cov.c`. Commands:
- `./cov sound 1 24 3 8 1 0 2`
- `./cov cov 18 28 3 8 1 0 2`
- `./cov mc 25 2000 3 8 1 1000 2`

Each run takes under 2 minutes; n = 28 is exhaustive over 9.59M necklaces in 95 s.
Notation: a = 0, b = 1; Cyc = cyclic closure (CF-preserving: Maslov/Oshiba, LITERATURE).

## 1. Reproduction and the families added

COMPUTER-CHECKED: I reimplemented builder's D and builder2's GB, RD and RGB (B = 3). The miss counts match builder2's
`out_cov2.txt` exactly (n ≤ 20: 57/4/50 at 18/19/20). Their union (CFU) misses:

| n | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CFU (builder2) | 57 | 4 | 50 | 708 | 410 | 298 | 10522 | 4326 | 26504 | 178294 | 291924 |
| CFU + T(E′),T²(E′),T³(E′),T²(E′∪G) | 35 | 0 | 40 | 46 | 190 | 20 | 5948 | 278 | 14638 | 16086 | 181952 |
| ALL = above + EP, PAR, L*, BGB | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 18 | 84 |
| 𝒰 = ALL ∪ T²(BASE) (§2) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 60 |

**Effect of walk.md's operators, as the coordinator asked (n = 18–22).**
- T(E′), T²(E′) and T³(E′) are empty at even n.
- At odd n they are strong: T³(E′) alone misses only 1380 of 27594 necklaces at n = 19 and 5220 of 99858 at n = 21.
- On top of CFU they reduce the misses from 57/4/50/708/410 to 35/0/40/46/190.
- At even n, only the weighted variant G (T²(E′∪G) misses about half of the necklaces) does anything.

New families (all PROVED sound and CF):

- **EP:** |w|_b − |w|_a = ±1 (E′).
- **PAR:** gcd(|w|_a, |w|_b) = 1, provided that either min(|w|_a, |w|_b) ≤ B, or α|w|_a − β|w|_b = ±1 for some α, β ≤ B.
  - Sound: u^p has both counts divisible by p.
  - CF: this is a finite union. Each part is either regular (a bounded letter count plus a residue condition) or one-counter (the line).
- **BGB** (block-level orbit count):
  - Take the block vector x over Z_K, where K = #b, x_i = the a-run before the i-th b. Do the same with a and b swapped.
  - Take any reflection s, and let mm = #{i : x_i > x_{s−i}}.
  - The condition: mm ≥ 1, (mm ≤ B or K−2mm ≤ B), and gcd(mm, K−2mm) = 1.
  - Sound by builder2's Lemma O: if w = u^p, then x is σ_{K/p}-invariant with p | K, so p divides both mm and K−2mm.
  - CF exactly like RGB: a fold pairs a^P b … a^Q b with P > Q, P < Q or P = Q, using finite counters capped at B and residues mod lcm(1..B).
- **L\*_ℓ, ℓ ≤ 8** (strengthening of cl1's L_ℓ). Let R(i) = s − i, with **any** s ∈ Z_K. Require ℓ | K and K ≥ 2ℓ.
  The fixed classes are the residue classes c mod ℓ with 2c ≡ s. With D = x − x∘R:
  - exactly one fixed class f contains a single mismatched pair {j, Rj}, with j ≠ Rj and **D_j = t ≠ 0 arbitrary**;
  - the other fixed classes have D ≡ 0;
  - each swapped class is single-signed.

  *Soundness (PROVED).* Suppose σ_d x = x. Then D is σ_d-invariant.
  - If ℓ | d: D_{j+d} = t with j+d ∈ f. The only nonzero entries of D on f are at j and Rj. The case j+d = j is impossible since d ≢ 0, and j+d = Rj would give t = D_{Rj} = −t.
  - If ℓ ∤ d: j+d and Rj+d lie in the class f+d ≠ f, and Rj ≡ j (mod ℓ). They carry +t and −t, which contradicts both "≡ 0" and "single-signed".

  *CF:* a linear fold grammar with finite control. The control holds i mod ℓ, the class flags, one "unequal pair already used" bit for f, and the sign choice per swapped pair of classes. There are two fold types (through a block or between blocks).

  The arbitrary offset t covers near-powers with a *multi-letter* insertion. Examples: a^7·X·a^3·X with X = babbabb, and (aabaababbb)²·b⁴. These were the ALL-misses at n = 24 before t was freed (misses with t = ±1 only: 4/8/32 at n = 24/25/26).

Soundness of every family (D, GB, RD, RGB, EP, PAR, L\*, BGB, T1–T3, TG2, and T²(BASE)) is COMPUTER-CHECKED exhaustively: no
non-primitive word of length ≤ 24 is accepted (≤ 22 for T²(BASE)).

## 2. The T-closure patch (PROVED modulo walk.md Lemmas 2–3, which are under audit)

Let BASE = D ∪ GB ∪ RD ∪ RGB ∪ EP ∪ PAR ∪ L\* ∪ BGB ∪ G. Each family is closed under rotation, so BASE is CF, Cyc-closed and contained in Q.
By walk.md, T(M) = Cyc σ(M) ∪ swap(·) is CF and contained in Q for every such M.
So **𝒰 := ALL ∪ T(BASE) ∪ T²(BASE)** is a CF subset of Q.

Membership test, as implemented:
1. Swap the letters if Δ < 0.
2. Rotate to the first argmax of the prefix walk. This rotation ends at a strict maximum.
3. Cut into first-passage pieces and form the type word Φ.
4. Test Φ against BASE, or recurse once more.

T(BASE) therefore certifies every w with Δ ≠ 0 whose type word Φ (of length |Δ|) is in BASE. In particular, since BASE ⊇ all primitive words of length ≤ 23, it certifies every w with 1 ≤ |Δ(w)| ≤ 23 for which Φ is primitive. Φ is automatically primitive when w is: this is Lemma 3 read backwards.

## 3. Classification of the misses and the trajectory (COMPUTER-CHECKED)

- **ALL misses at n = 24–26 before the T-closure: near-powers with a long insertion.** They have the form u^2 with one block changed by t ≥ 2. Freeing t in L\* closed them.
- **ALL misses at n = 25–27: all achiral** (2/2/18 of 2/2/18). These are cyclic palindromes p·q.
  - For an achiral w with axis c0, every other reflection count equals a *translation* correlation: D^c = w − σ_{c0−c}w.
  - So all reflection families degenerate to shift-correlation tests. This is the small-n reason they are missed.
  - T²(BASE) catches all of them at n = 27.
- **𝒰 misses: n = 26: 2; n = 28: 60. All 62 are balanced, |w|_a = |w|_b.** 32 of the 60 at n = 28 are achiral.
  - They have 10–20 runs, Hamming distance 2–11 from the nearest power, and the best-approximating period varies (p = 2, 4, 7, 14).
  - Their distinguishing feature is not "random-looking": it is Δ = 0, where the walk tower cannot start, together with failure of every bounded-count fold test.
- **Trajectory.** Each patch closes everything up to some n0, and new misses appear just above it:
  - builder2: n0 = 17;
  - with L\*, BGB and PAR: n0 = 24;
  - with the T-closure: n0 = 25, plus 27.

  The new misses are always in the next even length with many divisors (24, 26, 28). Here, by Fact-B/Lemma-O arithmetic, all counts tend to share factors with n. At even n the residual sits in the balanced slice.

**Monte Carlo** (`cov mc`; 600–1000 random primitive words per n; fraction certified):

| n (odd) | 25 | 43 | 63 | 103 | 207 | 415 | 831 |
|---|---|---|---|---|---|---|---|
| CFU (builder2) | .997 | .458 | .107 | .002 | 0 | 0 | 0 |
| 𝒰 | 1 | .999 | .975 | .957 | .962 | .975 | .972 |

| n (even) | 24 | 42 | 62 | 102 | 200 | 400 | 800 |
|---|---|---|---|---|---|---|---|
| CFU (builder2) | .988 | .513 | .107 | .002 | 0 | 0 | 0 |
| 𝒰 | 1 | .997 | .884 | .808 | .838 | .885 | .897 |

The dip around n ≈ 60–100 has a cause:
- BASE has lost coverage at length n;
- level 1 has length |Δ| ~ √n, which is still too long for BASE, and it is balanced with probability ~ n^{−1/4}.

After the dip, the coverage rises again as the levels shrink.

## 4. What the persistent misses need (IDEA / CONJECTURED, with the proved parts marked)

- **(PROVED-level facts.)** Let m_0 = n and m_{j+1} = |Δ| of level j. Then T^k(BASE) misses w only in one of two cases:
  - some level j < k has Δ = 0;
  - level k has a type word outside BASE.

  Heuristically, the m_j's behave like m_{j+1} ≈ |N(0, m_j)|, so P(Δ_j = 0) ≍ m_j^{−1/2}. For fixed k the last level has m_k ≈ n^{2^{−k}} → ∞. BASE has density → 0 (builder's and builder2's bounds, and the L\*/BGB/PAR analogues: each needs Θ(K/ℓ) independent pair events or a Parikh line). So T^k(BASE) has density → 0 for each fixed k, but only once n^{2^{−k}} ≫ 100. The misses therefore do **not** form a positive fraction in any computable range.
- **Positive density would need one of the following.**
  - (i) An *unbounded* tower: iterate decoding until length O(1), i.e. walk.md's N_∞ with depth ~ log log n.
  - (ii) A certificate for the balanced level. This means dense primitivity witnesses inside {Δ = 0}, which has density ≍ n^{−1/2}, so it is not needed for positive density. The tower then has to restart: either through a different statistic (e.g. G-weights or a k-gram functional) whenever Δ_j = 0, or through a fallback inside BASE.
- **Why (i) looks non-CF (IDEA).**
  - The natural PDA keeps the stack as one segment per level: the level-k counter at the bottom and the level-1 Dyck depth on top. Pieces nest properly, so this works for fixed k.
  - A level-j counter is only accessible after popping the j−1 empty segment separators above it. A cascade (one letter completing pieces at levels 1..j at once, which happens unboundedly often mid-word) must push back **exactly** j−1 separators.
  - A PDA cannot carry j across that cascade. If the number of separators is guessed instead, soundness is lost, because the level identities shift.
  - Equivalently, the union ⋃_k T^k(BASE) is an infinite union whose k-th member needs about k nested "stack zones". This is the same as needing a stack of stacks (an indexed-language / 2-level-PDA feature).
  - I have no proof that every CF language of positive density inside Q must fail; this is only why the natural construction fails.
- So the correct reformulation of "the certificate that seems non-CF" is:
  - **not** a coprimality test (builder2's barrier is bypassed by the walk route),
  - **but** an unbounded-depth recursive first-passage decoding.

  The density question becomes: is N_∞, or any positive-density subset of it, CF? CONJECTURED: no.

## Registry entry
1. **Aim:** an explicit CF L ⊆ Q covering every primitive necklace, built by patching certificate unions; and a diagnosis of the persistent misses.
2. **Proved:**
   - The new sound CF families L\*_ℓ (any axis, arbitrary insertion offset t), BGB (block-level orbit count) and PAR.
   - 𝒰 = ALL ∪ T(BASE) ∪ T²(BASE) is a CF subset of Q, assuming walk.md Lemmas 2–3.
   - COMPUTER-CHECKED: 𝒰 contains every primitive word of length ≤ 25 and of length 27. It misses 2 necklaces (n = 26) and 60 (n = 28), all with |w|_a = |w|_b.
   - Monte Carlo coverage ≥ 0.95 (odd n) and ≥ 0.8 (even n) for n ≤ 831.
3. **Missing step:** a CF certificate of positive density for all n. Concretely, either:
   - a CF implementation of an unbounded first-passage tower (N_∞ or a positive-density subset), or
   - a proof that every CF L ⊆ Q has density → 0 along a subsequence.
4. **Counterexamples:**
   - The residual lists `scripts/builder3/miss_{18..28}.txt`. Only 26 and 28 are nonempty for the final union; at 18–24 the files are empty.
   - Near-powers with multi-letter insertions (a^7 X a^3 X) escape cl1's L_ℓ but not L\*_ℓ.
   - Achiral words defeat all reflection-count families: they collapse to translation correlations.
5. **Strength:** both positive density of N_∞ ∩ CF and "every CF L ⊆ Q has density → 0" are stronger than the main problem, in their respective directions.
6. **Reopen/kill:**
   - Kill the density route: show N_∞ (with mirroring flags) or a positive-density subset of it is CF.
   - Advance the negative side: prove that a cascade-restoring stack discipline is necessary, e.g. via a bounded slice of N_∞ that is not CF.
