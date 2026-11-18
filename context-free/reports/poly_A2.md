# poly_A2: upper-bound attack on the candidate S_N = (ab*)^n, n = P_N² (agent A2)

Result: **no polynomially ambiguous construction found.** The two natural canonical laminar choices are
refuted: one by proof (Lemma A), one by computation. The conjecture itself is NOT refuted. What remains open
is exactly the sign-only (full-dimensional) piece case, which is gap G1.
Script: `scripts/poly/a2_witness.py [small|prod36|lemmaA]` (all runs below take < 15 s).

## Setting
Write n = P_N², P = P_N, fibre r = {i ≡ r mod P}, index t = ⌊i/P⌋ ∈ Z_P. On the product region
x = B + Σ_k e_k (B ∈ V_P large, e_k ∈ E_k), the restriction e_k^{(r)} of e_k to fibre r is a p_k-periodic,
mean-zero function of t. Then x ∈ V_{p_k} ⇔ e_k^{(r)} = 0 for every r. So x is primitive ⇔ for every k there is a fibre r with
e_k^{(r)} ≠ 0. **[PROVED, direct]** Every valid mismatch pair (i, j) for p_k (j − i ≡ 0 mod n/p_k)
lies inside one fibre. Each fibre is a copy of the squarefree problem n' = P (compare bounded.md L8).

## 1. AG strict witness model (one pair per prime, pairs disjoint and non-crossing; bounded.md L4/L5)
[computational, exhaustive over {0,1,2}^n]
| n | primes | primitive vectors | uncovered | min/mean/max #systems | lex-canonical piece stratified |
|---|---|---|---|---|---|
| 4 | 2 | 72 | 0 | 1/1.5/2 | 75.0% |
| 9 | 3 | 19656 | 0 | 2/6.0/9 | 66.8% |
| 12 | 2,3 | 530640 | 7092 | 0/5.3/12 | 0% |

n = 36, product region x = 2 + e_2 + e_3 (entries in {0..4}, because {0,1,2} cannot hold both perturbations), 4000 random samples:
- All 72 vectors with e_2 and e_3 supported in one common fibre are **uncovered**: a fibre is a copy of n = 6, where every primitive pattern is uncovered (poly_AG).
- On covered vectors, #systems ≈ 5·m_2·m_3, where m_k = #{r : e_k^{(r)} ≠ 0}. The ratio is 4.5–5.25 in every (m_2, m_3) cell, with a maximum of 180 at m = (6, 6). The lex-canonical piece is realizable for 0 vectors.
So the ply of a witness union is multiplicative, ∏_k Θ(m_k), and it reaches ∏_k P = n^{N/2} at generic points. This is the conjectured order of ply.

## 2. Lemma A (exact-equality canonicalisation is impossible) [PROVED; checked by `lemmaA`]
Let c + ℕP be a stratified piece with V_P ⊆ span P, as forced by the base family (L8 Dickson argument). Suppose the piece lies in
{e_k^{(r)} = 0}.
(a) If p_k ≥ 3, this is impossible.
(b) If p_k = 2, it can hold for at most one fibre r. More generally, two fibres can never both carry an exact equality.

*Proof.* Let F be the space of p_k-periodic mean-zero functionals on fibre r. Then F ⊆ (span P)^⊥ = span{g_C} (L7), and the
g_C have disjoint supports. So every f ∈ F restricts on each block C to a multiple of g_C. The blocks that carry F
lie inside fibre r and cover it. Each such block has rank(F|_C) = 1, and g_C sums to zero, so |C| ≥ 2. For p ≥ 3, rank(F|_C) = 1
forces C into one class t mod p. Adjacent t lie in different classes. A non-crossing partition of a line into
monochromatic blocks of size ≥ 2, with adjacent points of different colours, does not exist: take a block of minimal span; the
point just after one of its elements belongs to a block nested strictly inside it. The same descent works for two fibres r ≠ r', whose points alternate. ∎
Check: admissible partitions are 0 for (L, p) = (6,3), (10,5), (12,3) out of 132 / 16796 / 208012, and positive for p = 2.

**Consequence.** "First non-zero fibre for prime k" (lexicographic, unambiguous) needs e_k^{(r)} = 0 for all r < r_k.
By Lemma A this cannot be realized. A canonical choice therefore has to use sign constraints only, while overlapping
per-prime choices multiply ply (§1). A sign-only canonical fan, for example "the fibre with the largest |e_k^{(r)}|", needs a
coordinate compared with several others, and that is blocked by bounded.md L5(a) ({a>b, a>c} is not stratified). It is not proved
that every sign-only cover fails; that general case is G1.

## Status
- canonical laminar choice: REFUTED (equality form: proved; AG strict form: computational)
- poly(n) construction: NOT FOUND
- candidate: survives. The open residue is G1, restricted to sign-only pieces.
