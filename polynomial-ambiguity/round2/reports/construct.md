# construct — laminar covers of Q ∩ (ab*)^30 (agent W1-D, constructive side)

Scripts (all in `R2/../scripts/`): `construct_atoms.py` (atoms, realisation test, certified primes),
`construct_cover30.py` (sparse exhaustive test), `construct_k3.py` (3-chord atoms, vectorised),
`construct_check30.py` (exhaustive small norm + random ply).
Order: linear block order 0 < 1 < … < 29 (PA/poly_P.md §2 (i), laminarity of pair supports; PROOF.md §3(f)).

## 0. Verdict
(a) **Fails** for the natural extension of the rectangle construction (all "chord-dominance" atoms with
≤ 3 chords, combined by laminar conjunction). The failure is *exactly* a fibre obstruction (§3), the
three-prime analogue of the n = 36 failure. (b) is proved for n = pq only. (c) obstruction lemma in §3;
it is an obstruction for conjunctive certificates, **not** for laminar covers in general (S4U local piece).

## 1. The atom family (generalised rectangles) — realisability [written proof]
Atom = k pairwise non-crossing chords (s_i < t_i) with distinct endpoints, d_i := x_{t_i} − x_{s_i}.
Region R = ⋃_{(j,σ) allowed} {σ d_j > Σ_{i≠j} |d_i|}.
Realisation of {σ d_j > Σ_{i≠j}|d_i|} for a fixed sign pattern of the d_i (i ≠ j), top := t_j (σ=+) or s_j:
  c = e_top + Σ_{i: d_i<0} (e_{s_i}+e_top),  V = {e_{s_i}+e_{t_i}}_i ∪ {e_{end_i}+e_top}_{i≠j} ∪ {e_top} ∪ {e_m : m ∉ supp},
  end_i = t_i if d_i ≥ 0 else s_i.
V is linearly independent and unimodular (triangular), c + ℕV equals the integer points of that sign cell
exactly, the cells are disjoint, and different allowed (j,σ) are disjoint (σd_j > |d_i| and σ'd_i > |d_j|
cannot both hold). (j,σ) is *allowed* iff the pairs are non-crossing for every sign pattern (checked
combinatorially, depends only on the shape). So **each atom is an unambiguous laminar union; ply 1**.
k = 1: a chord, region d ≠ 0. k = 2, nested: exactly S2K's rectangle pieces; k = 2 side-by-side: also allowed.
k = 3: shapes ((01)(23)(45)) and ((05)(12)(34)) allow every dominant; nested chain only the middle chord.

Certified primes: C(atom) = {p : some signed sum Σ ε_i d_i ∈ V_p^⊥}; on R every such sum is ≠ 0, so
R ∩ V_p = ∅ for p ∈ C. A *system* = atoms with disjoint supports and mutually non-crossing pair sets with
⋃C = {2,3,5}; product of pieces is laminar, region ⊆ E, ply 1 per system.
Off W_30 use P1 (PA/poly_T1.md): φ(30) = 8 one-counter forms, ply ≤ 8.
Useful reduction [written proof]: in a conjunctive system a general form L ∈ V_p^⊥ with support S can be
replaced by a single orbit chord inside S (L(x) ≠ 0 ⇒ x non-constant on some p-orbit ∩ S), so arbitrary
forms add nothing to chord atoms; only *compound* atoms (k ≥ 2) add power.

## 2. Two primes, n = pq: the rectangle cover is correct [written proof]
A = n/p, B = n/q. On W = V_p + V_q write x = a + b (a A-periodic, b B-periodic). For R_i:
w + u = 2(b_{i+A} − b_i), w − u = 2(a_{i+B} − a_i). Let I_b = {i : b_{i+A} ≠ b_i} (a union of classes mod B,
nonempty iff x ∉ V_p) and I_a = {i : a_{i+B} ≠ a_i} (classes mod A, nonempty iff x ∉ V_q).
gcd(A,B) = 1 (CRT) ⇒ I_a ∩ I_b ≠ ∅ ⇒ some R_i has |u| ≠ |w|. Cover: n rectangles × 4 disjoint pieces
plus P1 ⇒ **ply ≤ n + φ(n)** (each rectangle contributes ≤ 1). This proves S2K's conjecture for all
squarefree pq.
**Where it fails.** For n = p^a q^b the same identity holds but gcd(A,B) = g := n/(pq) > 1; the rectangle
family covers x iff I_a, I_b meet a common class mod g. For n = 36 = (2·3)², g = 6: the failure set is
exactly {x = a + b : the 2-witness and 3-witness fibres (classes mod 6) are disjoint}, i.e. the fibre
structure of S_N (PA/poly_A2.md). Example S2K: n = 12, x = (1,2,3,3,1,3,3,2,1,3,3,3).

## 3. Three primes, n = 30: computation and the fibre obstruction
| test | atoms | result |
|---|---|---|
| sparse W_30 (generators 0/1, supports (2,1,1),(1,2,1),(1,1,2)), 16 680 primitive | k ≤ 2 (105 chords, 3870 two-chord) | 60 uncovered |
| same 60 vectors | + all 3-chord atoms (C(30,6)·5) | 60 uncovered |
| 3-chord atoms certifying all of {2,3,5} | exhaustive | **none exist** |
| exhaustive W_30 ∩ ℕ^30, ‖x‖₁ ≤ NMAX | k ≤ 2 | see §5 |
| random W_30 (entries of a,b,c in 0..3) | k ≤ 2 | see §5 |
[computational]

**The 60 uncovered vectors** = 5 fibres × 6 rotations × 2 patterns: x supported on one class r mod 5,
x_{r+5t} = y_t with y a rotation of (2,0,1,1,1,0) or (2,1,1,1,2,0) on ℤ_6
(e.g. x0 = 2e_0 + e_10 + e_15 + e_20, the S4T example).

**Lemma O (fibre obstruction for conjunctive certificates).** [written proof for x0; computational for all 60]
Let n = pqr squarefree, fibre = class mod r (preserved by the p- and q-shifts n/p, n/q, both ≡ 0 mod r;
moved by the r-shift pq). Let x be supported on one fibre. Then (i) every r-witness chord {s, s+k·pq}
has an endpoint in supp x and jumps over a neighbouring fibre point (pq > r); (ii) every p- or q-witness
lies inside the fibre. For x0 at n = 30: the {2,3}-witness chords are {0,15},{5,20},{10,25} and
{0,10},{0,20},{5,15},{15,25}; every 2-chord/3-chord pair shares an endpoint or crosses, so {2,3} needs a
compound atom; the {2,3}-certifying rectangles at x0 have supports {0,10,15,25} or {0,5,15,20}, and the
remaining support point (20 resp. 10) has no 5-partner (±6, ±12) inside the gap that contains it; no
3-chord atom certifies three primes. Hence **no system of chord-dominance atoms (k ≤ 3) certifies x0**.
**Not an obstruction for laminar covers in general:** PA/poly_S4U.md gives a laminar piece around x0
(generators e_0, e_10, e_15, e_0+e_20, stars e_j+e_20, e_j+2e_0): it uses *shared-endpoint transfer*
generators (two certificates meet at block 20), which no conjunctive system can, and which chains cannot
replace ({x_0 > x_20 > x_5} has extreme ray e_0+e_5+e_20, support 3, not laminar).

## 4. What remains (exact gap for (a))
A finite cover needs, besides the k ≤ 2 atoms, pieces covering a conic neighbourhood of each fibre-
supported bad pattern *and* of all W-points whose restriction to some fibre is such a pattern with the
other fibres not supplying a gap-compatible 5-witness. Candidate: S4U pieces (one per (fibre, pattern),
i.e. 60 pieces) — **not verified** to cover a neighbourhood large enough to close the arrangement; the
correct test is a z3/LRA check over W (the uncovered set is a finite union of subspaces of W intersected
with the orthant), not yet run. So (a) is OPEN; no ply bound for n = 30 is claimed.
General three-prime construction: none; the fibre obstruction (Lemma O) is the three-prime analogue of
the n = p²q failure in §2 and of A2's fibre structure.

## 5. Small-norm / random numbers
`construct_check30.py 6 40` (all primitive x ∈ W_30 ∩ ℕ^30 with ‖x‖₁ ≤ 6, then 40 random W-points with
ply = #systems) was started but did NOT finish within the budget (pure-Python enumeration of ~2·10^6
vectors); its rows in the §3 table are therefore EMPTY. Run it to completion before relying on "only
fibre-supported vectors fail". The sparse result (16 620 of 16 680 covered) is the only coverage evidence.
