# Report of agent "builder2" (positive direction: generalised reflection certificates)

**Claim status: no proof of either resolution.** I found one new soundness principle that covers the
reflection certificates of builder.md, cl1.md and kk.md together: the **orbit-count lemma**. Its full
(non-CF) form is a sound primitivity certificate that, numerically, covers essentially every word. Its
CF fragments cover every primitive necklace up to n = 17, but their coverage provably goes to 0. The gap between
the two is exactly one arithmetic condition, coprimality of two fold counts. I prove that no semilinear
(hence no CF-Parikh) mechanism can supply that condition in more than one dimension.
Scripts: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/builder2/` (`certs.py`, `mc.py`, `misses.py`; outputs `out_cov2.txt`,
`out_mc.txt`, `out_miss.txt`). Every run is under 3 minutes on one core.

Notation: Σ = {a,b} with a = 0, b = 1; the reflection is ρ_c(i) = c − i on Z_n.
For a word w, D^c_i := w_i − w_{c−i} ∈ {−1,0,1}. Then m_c := #{i : D^c_i = +1} is the number of mismatched mirror pairs,
and r_c := n − 2m_c is the number of positions in matched pairs or on the axis.
At run level, let the cyclic run sequence have lengths ℓ_0..ℓ_{K−1} (K even, letters alternating). Use only even c, so
that a-runs map to a-runs. Put E^c_i := ℓ_i − ℓ_{c−i}, and let mm_c be the number of mismatched run pairs.

## 1. Orbit-count lemma (PROVED)

**Lemma O.** Let x: Z_K → V be σ_d-invariant, (σ_d x)_i = x_{i+d}, with d ≢ 0 (mod K), and let ρ be any reflection
of Z_K. Put D = x − x∘ρ (any V with subtraction; only "D_i = v" sets are used). Then for every value v the set
{i : D_i = v} is a union of σ_d-orbits. All these orbits have size p' = K/gcd(K,d) > 1, and p' | K. The same holds
for {i : D_i > 0}.

*Proof.* D_{i+d} = x_{i+d} − x_{c−i−d} = x_i − x_{c−i} = D_i, so D is σ_d-invariant, and so is each level set.
Every orbit of the translation by d on Z_K has exactly K/gcd(K,d) elements. ∎

**Corollary G (PROVED).** Suppose that for some axis c, gcd(m_c, n) = 1, or equivalently gcd(m_c, r_c) = 1. Then w is
primitive. If w = u^p with |u| = d, apply Lemma O to {D = +1}: its size m_c is divisible by p' > 1 with p' | n. ∎

**Corollary RG (PROVED).** Suppose w is not unary and, for some even c on the run cycle, some value class of E^c, or the
class {E^c > 0} (of size mm_c), has size coprime to K. Then w is primitive. *Proof.* If w = u^p, its run cycle
is σ_{K/p}-invariant (the run cycle of a non-unary power is periodic), and Lemma O applies. ∎

**What this unifies.**
- cl1.md Theorems 1–2 ("x − Rx = e_j − e_{Rj}") are the case "the class {E > 0} has size 1" at block level.
- builder's Theorem D is *not* a count statement. It uses the geometry of the half arc. Lemma O and Lemma D
  are the two independent uses of "translation∘reflection = reflection".
- cl1 Theorem 3 (E = T − σ_ℓT) is a third, difference-of-shifts use.

## 2. CF fragments and their union (PROVED sound and CF; coverage COMPUTER-CHECKED)

Fix B (B = 3 is used below).
- **GB:** ∃c with (m_c ≤ B or r_c ≤ B) and gcd(m_c, r_c) = 1. This is a linear fold language with finite control.
  If m ≤ B, keep m exactly (capped) and r mod lcm(1..B). If r ≤ B, keep r exactly and m mod lcm(1..B).
  The cyclic closure of a CFL is CF (LITERATURE, Oshiba/Maslov). There are two fold types (edge cut or vertex
  cut), as in builder's S → Y | XY.
- **RGB:** the same at run level, with (mm, K − 2mm). Mirrored runs are generated as nested a^i … a^j with
  "i = j" or "i ≠ j", which is CF. This contains cl1's L and L_gen (the case mm = 1).
- **RD:** run-length dominance: ℓ_i ≤ ℓ_{c−i} on the half arc between the two fixed runs, with one strict pair.
  It is sound by builder's Lemma D applied verbatim on Z_K, including the special case d = K/2. It is CF by nested
  a^i…a^j, i ≤ j. It catches builder's missed family F1 = bba^m baba^m: take c through a^m and b, and use the pairs
  (bb, b) and (a, a^m).
- **D:** builder's Theorem D.

Soundness of all six predicates (including the ceilings G and RG) is exhaustively checked on all words of
length ≤ 14.

**Primitive necklaces missed** (`out_cov2.txt`). CFU = D ∪ GB ∪ RD ∪ RGB, ALL = CFU ∪ G ∪ RG:

| n | ≤8 | 9–17 | 18 | 19 | 20 |
|---|---|---|---|---|---|
| D | 0 | (builder) | 1873 | 4228 | 9673 |
| CFU | 0 | **0** | 57 | 4 | 50 |
| G alone | 0 | 0 except n = 12 (51) | 334 | 0 | 1385 |
| ALL | 0 | 0 | 0 | 0 | 0 |

So **Cyc(CFU) is a CF subset of Q containing every primitive word of length ≤ 17**. The first misses are listed in
`out_miss.txt`, e.g. aaaaababaaabaaabab (n = 18), aaaababbaabbbaabbab (n = 19).

**This is a small-n artefact.** Monte Carlo, 300 random words per n (`out_mc.txt`), fraction certified:

| n | 24 | 36 | 48 | 60 | 90 | 120 | 200 |
|---|---|---|---|---|---|---|---|
| CFU | .97 | .70 | .29 | .12 | .01 | 0 | 0 |
| G (non-CF) | .99 | 1 | 1 | 1 | 1 | 1 | 1 |

**Density of the CF fragments → 0.**
- D: PROVED in builder.md.
- GB: PROVED. For one axis, m_c is a sum of ⌊n/2⌋ independent fair indicators, so
  P(m_c ≤ B or r_c ≤ B) ≤ 2·n^B·2^{−⌊n/2⌋}. A union bound over 2n fold types gives density ≤ 4n^{B+1}2^{−n/2}.
- RD and RGB: sketch only, not written. K ≥ n/4 with probability 1 − e^{−Ω(n)}. Runs are i.i.d. Geometric(1/2)
  given K, and P(ℓ_i = ℓ_j) = 1/3, so each axis needs Ω(n) independent pair events of probability bounded below 1.

## 3. The barrier: the missing ingredient is coprimality (PROVED parts marked)

G (density apparently → 1) and CFU (density → 0) differ only in how the count pair (m_c, r_c) is tested.

**Lemma S (PROVED).** Let S ⊆ N² be semilinear and S ⊆ Cop := {(x,y) : gcd(x,y) = 1}. Then S is a finite union of
points and of linear sets with exactly one period. Consequently |S ∩ {x + y = N}| = O(1), while
|Cop ∩ {x + y = N}| = φ(N) → ∞ along primes N.

*Proof.* Take a linear set c + Np_1 + Np_2 ⊆ S with p_1, p_2 linearly independent. Let I = [Z² : Zp_1 + Zp_2] and let
q be a prime with q ∤ I. Then Zp_1 + Zp_2 surjects onto (Z/q)², so some t_1, t_2 ∈ [0,q) give
c + t_1p_1 + t_2p_2 ≡ 0 (mod q). Add q·p_1 so the point is nonzero. That point lies in S with both coordinates
divisible by q, which contradicts S ⊆ Cop. A one-period linear set c + Np, with p ≠ 0 and p ∈ N², meets each
antidiagonal in at most one point. ∎

**Proposition N (PROVED).** Fix the cut (no cyclic closure). Let G_0 = { w : the central fold of w has gcd(m, n) = 1 }.
Then G_0 is not CF.
*Proof.* Take w = b^j a^k with 1 ≤ j ≤ k. For t < ⌊n/2⌋ we have w_{n−1−t} = a, and w_t = b iff t < j. So m = j and
gcd(m, n) = gcd(j, k). Hence G_0 ∩ b*a* ∩ {j ≤ k} = { b^j a^k : j ≤ k, gcd(j,k) = 1 }. If G_0 were CF this set
would be a bounded CFL, so its Parikh set would be semilinear (Parikh). By Lemma S it would then meet the
antidiagonal j + k = N in O(1) points, but it meets it in φ(N)/2 points. ∎

**What this means.**
- Every CF fragment of G that I found keeps the count pair (m_c, r_c) on finitely many lines (bounded m, or
  bounded r, or residues). By Lemma S this is unavoidable for any CF mechanism that decides through the pair
  (m_c, r_c) of a fixed fold.
- (IDEA) The counts of a random word concentrate at (n/4 ± O(√n), n/2 ± O(√n)). Lines through that region
  (for example n − 4m = k with gcd(m,k) = 1) would need the fold count to equal a linear function of n. Testing
  that needs a second counter alongside the fold stack. On a^*b^*a^*b^* it gives a Ginsburg cone with
  3-sparse extreme rays (1,1,0,2) and (0,2,1,1), so it is not stratified (sketch).
- So I CONJECTURE: every CF subset of G has density → 0. I have **no proof** that a CF certificate outside the
  dihedral/count families cannot do better.

**Families missed by G itself.** These are not CF-relevant, only diagnostic. All 51 G-misses at n = 12 have every
m_c even or divisible by 3. RG catches all of them for n ≤ 20. ALL = CFU ∪ G ∪ RG is complete for n ≤ 20, but it is
not CF.

## 4. Variants tried
- (i) Block level = run level: RD, RGB, RG above.
- (ii) Reflection + count: the count-coprimality certificates G/GB, which is the right "count" version. The
  imbalance-type counts are covered by density4's Theorem P and builder §3(b).
- (iii) Other orders: any relation pair S ⊆ R with S⁻¹ ∩ R = ∅ on bounded windows or run lengths is sound by
  Lemma D. But every such "∀ pairs on a half arc" condition forbids a configuration of probability ≥ c > 0 on
  Θ(n) disjoint pairs, so its density is ≤ e^{−Ω(n)} (same proof as builder's D-density). Universal dominance
  therefore cannot give positive density, whatever the order.
- (iv) Unions: CFU above. A finite union of density-0 languages has density 0.

## Registry entry
1. **Aim:** a CF L ⊆ Q with Cyc(L) = Q, via generalised reflection certificates.
2. **Proved:**
   - Lemma O (orbit counts of x − x∘ρ under a period) and the sound certificates G and RG, which contain cl1's
     L and L_gen.
   - The CF fragments GB, RGB and RD. Cyc(D ∪ GB ∪ RD ∪ RGB) ⊆ Q is CF and contains **all primitive words of
     length ≤ 17** (COMPUTER-CHECKED). Its misses are 57/4/50 necklaces at n = 18/19/20, and its density → 0
     (proved for D and GB, sketched for RD and RGB).
   - Lemma S and Proposition N: the full count certificate needs coprimality of fold counts, which is not
     semilinear.
3. **Missing step:** a CF L ⊆ G (or any CF L ⊆ Q) of positive density, which would need a non-Parikh way to
   certify gcd(m_c, n) = 1. Negative-side target: "every CF L ⊆ Q has density → 0" (stronger than Q ∉ CF), or the
   same restricted to linear fold languages with arbitrary CF control.
4. **Counterexamples:**
   - F1 (builder) is caught by RD.
   - The first CFU misses are listed in out_miss.txt.
   - G misses 51 necklaces at n = 12, all caught by RG.
5. **Strength:** the density-0 conjecture is stronger than "Q not CF". Lemma S and Proposition N are barriers
   only.
6. **What would reopen:** a CF mechanism certifying gcd(m_c, n) = 1, or a "some value class coprime to K" test,
   on a positive fraction of words without semilinear count tests. For example, choosing the axis c so that m_c
   is prime and does not divide n is still arithmetic. On the negative side: show that any linear fold
   certificate with CF control has density → 0.
