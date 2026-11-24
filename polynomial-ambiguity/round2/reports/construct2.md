# construct2 — transfer atoms close the fibre obstruction at n = 30 (constructive side)

Scripts (`R2/../scripts/`): `construct2_transfer.py` (transfer atoms, system search),
`construct2_verify.py` (explicit cell pieces: exactness, disjointness, laminarity, rational LP certificates),
`construct2_enum.py` (exhaustive primitive W_30 ∩ ℕ^30 up to D_30), `construct2_cover.py` (coverage),
`construct2_ft.py` (Lemma FT check), `construct2_random.py` (larger norms), `construct2_ply.py` (greedy
subfamily and its ply), `construct2_n12.py` (n = 12 control). Order: linear block order 0 < … < 29; crossing
of pair supports is a cyclic notion, so every statement below is D_30-invariant.

## 0. Verdict
* Lemma O is **not** an obstruction once tops may be shared: one *transfer atom* (ply 1, exact laminar
  pieces) covers each of the 60 sparse vectors. For fibre-supported vectors this is a **written proof** for
  every squarefree n = pqr (Lemma FT, §2).
* Dominance atoms (k ≤ 2) plus transfer atoms cover **all** primitive x ∈ W_30 ∩ ℕ^30 with ‖x‖₁ ≤ 10
  (22 620 points, 424 dihedral classes; 8 classes need a transfer atom) [computational]. Random larger-norm
  tests did not finish (§3).
* No uncovered vector found ⇒ no Lemma-O-type obstruction for the enlarged family. A proof for general
  x ∈ E ∩ W_30 is **open** (§4 gives the exact gap). Ply: see §3 (greedy subfamily, evidence only).
* For the programme this changes little: squarefree n is capped anyway; at n = 36 the zero-cost mechanism
  that makes transfer atoms work is absent (§5).

## 1. Transfer atoms [written proof]
T = (τ; P; D): top τ, partner set P, chords D = {(s_i, t_i)}, all points distinct, d_i := x_{t_i} − x_{s_i}.

  **Region** R_T = { x ∈ ℕ^n : x_τ − Σ_{a∈P} x_a > Σ_i |d_i| }.

Cells δ ∈ {+,0,−}^D (sign of d_i); hi_i = t_i if δ_i = + , s_i if δ_i = −. Piece of cell δ:

  c_δ = e_τ + Σ_{δ_i≠0} (e_{hi_i} + e_τ),
  V_δ = {e_τ} ∪ {e_a + e_τ : a ∈ P} ∪ {e_{s_i} + e_{t_i} : i} ∪ {e_{hi_i} + e_τ : δ_i ≠ 0} ∪ {e_m : m ∉ supp T}.

(Parametrisation: x_{lo_i} = u_i, x_{hi_i} = u_i + w_i with w_i ≥ 1 (δ_i ≠ 0) or w_i = 0 (δ_i = 0);
x_a free; x_τ = 1 + Σ x_a + Σ w_i + slack.) V_δ is triangular ⇒ linearly independent, unimodular on its span,
d_σ = #V − rank V = 0; c_δ + ℕV_δ = R_T ∩ cell δ exactly; distinct cells are disjoint. Pair supports:
{τ,a}, {s_i,t_i}, {τ,hi_i}; cell δ is *allowed* iff these are pairwise non-crossing (only allowed cells are
used; the atom's region is the union of its allowed cells). So **each atom is a ply-1 laminar union**, all
ring vectors 0/1 with support ≤ 2, ‖c_δ‖₁ ≤ 1 + 2|D|.

**Certificates.** On R_T, for a ∈ P, I ⊆ D, ε ∈ {±1}^I:
  F = x_τ − x_a + Σ_{i∈I} ε_i d_i ≥ (x_τ − Σ_P x_a) − Σ|d_i| > 0.
If F ∈ V_p^⊥ (balanced on every class mod n/p) then R_T ∩ V_p = ∅. C(T) := {p : such an F exists}.
|P| = 1 gives exactly the chord-dominance atoms of `R2/construct.md` §1 (dominant chord = {τ, a});
the new freedom is **several partners at one top** (a star, never self-crossing) and **transfer forms**
F = (x_τ − x_s) + (x_t − x_a) with s ≡ τ, t ≡ a (mod n/p): a p-chord at τ glued to a p-chord at a through
the bounded chord (s, t). One chord can serve two primes with opposite signs (x0 example below).
`construct2_verify.py` rebuilds the cells of sample atoms, checks exactness in a box, disjointness, laminarity
of allowed cells, and finds a rational LP certificate L_p ∈ V_p^⊥, L_p ≥ 0 on V_δ ∪ {e_m}, L_p(c_δ) ≥ 1, for
every allowed cell and p ∈ {2,3,5} [computational check of the written argument].

Example (x0 = 2e_0 + e_10 + e_15 + e_20, the S4T/Lemma O vector): T = (0; {4,5}; {(10,24),(15,20)}):
2 − 0 − 0 > |0 − 1| + |1 − 1|; F_2 = x_0 − x_5 + x_20 − x_15, F_3 = x_0 − x_4 + x_24 − x_10,
F_5 = x_0 − x_4 − (x_24 − x_10). Pairs {0,4},{0,5},{10,24},{15,20},{0,10}: laminar.

## 2. Lemma FT (fibre transfer) [written proof, all n = pqr]
Let n = pqr squarefree, r one of the primes, F a fibre (class mod r) and x ∈ E ∩ W_n with supp x ⊆ F.
Then a single transfer atom covers x.

*Proof.* Fibre index k ↦ r_0 + rk identifies F with ℤ_{pq}; shifts n/p, n/q act on F as shifts by q, p. As
x(z) = z^{r_0} y(z^r) and ζ ↦ ζ^r maps primitive n-th roots onto primitive pq-th roots, x ∈ W_n ⇔ y ∈ W_{pq};
x primitive ⇒ y ∉ V_p ∪ V_q. By the pq rectangle theorem (`R2/construct.md` §2) some rectangle on F with
chords {i, i+A+B}, {i+A, i+B} (A = n/p, B = n/q) has |w| ≠ |u|: dominant chord {τ, a} (τ the larger-valued
endpoint), other chord o; its forms σw ± u lie in V_p^⊥, V_q^⊥. Put g = τ+1, s = τ + pq, and
  T = (τ; {a, g}; {o, (s, s+1)}).
g, s, s+1 ∉ F (r ∤ 1, r ∤ pq), and they are distinct from each other and from F. Hence x_g = x_s = x_{s+1} = 0,
and R_T at x reduces to the rectangle condition x_τ − x_a > |d_o|. Certificates: the two rectangle forms
(p, q) and F_r = x_τ − x_g + x_{s+1} − x_s ∈ V_r^⊥ (τ ≡ s, g ≡ s+1 mod pq). Laminarity: rectangle pairs plus
the transfer pair {τ, hi_o} are laminar (2-chord atoms allow every dominant); {τ, g}, {s, s+1} join cyclically
adjacent blocks, so they cross nothing ({0,29} also crosses nothing in the linear order); {τ, a}, {τ, g},
{τ, hi_o} form a star. The chord (s, s+1) has d = 0 at x, so it adds no transfer pair. ∎

Check: all 60 sparse vectors and all 13 fibre-supported classes with ‖x‖₁ ≤ 10 (fibres mod 2, 3, 5) are
covered by such a T (`construct2_ft.py`). For x0: T = (0; {25, 1}; {(10,15), (6,7)}); all 9 cells allowed,
exact, LP-certified.
Why conjunctive systems missed it: Lemma O needs the r-witness in a *separate* atom; here the r-form shares
the top τ and is routed through two cyclically adjacent pairs, which never cross.

## 3. Coverage and ply tables [computational]
| test | family | result |
|---|---|---|
| W_30 ∩ ℕ^30 primitive, ‖x‖₁ ≤ 8 (2 820 points, 58 classes) | dom k≤2 / + transfer | 54 / **58** covered |
| same, ‖x‖₁ ≤ 10 (22 620 points, 424 classes) | dom k≤2 / + transfer | 416 / **424** covered |
| 60 sparse vectors (5 fibres × 6 rot × 2 patterns) | single FT atom | **60 / 60** |
| fibre-supported classes ‖x‖₁ ≤ 10 (13: r=2:1, r=3:4, r=5:8) | single FT atom | 13 / 13 |
| random larger-norm W_30 points (`construct2_random.py`, generic / exotic / fibre+noise) | dom + transfer | NOT finished in budget (killed after ~12 min, no output); no claim |
Test sets include the non-polygonal vanishing sum e_5+e_6+e_12+e_18+e_24+e_25 (norm 6, in W_30 but not an
ℕ-sum of polygons); the old sparse test missed such points. Off W_30: T1-P1 forms, ply ≤ φ(30) = 8.

**Ply (evidence only).** The full family (all systems of ≤ 3 atoms, |P| ≤ 3, ≤ 1 chord per form) has
n^{O(1)} members, so ply ≤ n^{O(1)}; at x0 it contains 834 016 systems, which is not a meaningful number. A
greedy D_30-invariant subfamily (`construct2_ply.py`, cap 6 candidates per class) covering all 58 classes
with ‖x‖₁ ≤ 8 has 11 system orbits = 510 systems; on those classes, plus P1 off W, its **exact ply** is
min 2 / mean 16.3 / **max 44** (argmax x = blocks 9,10,16,17,27,28,29). This subfamily is tuned to the test
set and is NOT claimed to cover anything beyond it. All 8 transfer-needing classes (norm ≤ 10) are covered by a
single rectangle-plus-star atom T(τ; {a, g}; {o}) (g a 5-partner of τ with x_g = 0).

## 4. Toward a proof for all of E ∩ W_30 (and pqr): what is proved, what is the gap
Proved: (i) pq-rectangles certify {p,q} wherever their dominance holds (any n = pqr); (ii) Lemma FT for
fibre-supported x; (iii) every atom/system piece is exact, laminar, certified.
Proof sketch for general x (NOT complete). Take r with x ∉ V_r. Choose a fibre F mod r on which the
restriction y_F = x|_F is not in V_p ∪ V_q *and* a rectangle on F dominates with margin
μ = x_τ − x_a − |d_o|. Attach the r-certificate through adjacent pairs exactly as in Lemma FT; the cost is now
κ = x_{τ+1} + |x_{s+1} − x_s| (s = τ + k·pq, k = 1..r−1, and also the mirror choice g = τ−1, s−1) instead of 0.
The atom works iff μ > κ for one of the 2(r−1) routings, or some other p,q-rectangle on another fibre works.
**Gap (precise).** Cover the set
  B = { x ∈ E ∩ W_n : for every fibre F mod r, every dominating {p,q}-rectangle on F and every adjacent routing,
        μ ≤ κ }  (for every choice of r),
by systems in which the r-witness is a separate atom (the k ≤ 2 dominance systems of construct.md). The tests
say B ∩ {‖x‖₁ ≤ 10} is covered by dom systems; no structural reason is known. A proof needs a quantitative
version of the CRT step of construct.md §2 for three periodic components x = a + b + c (a ∈ V_2, b ∈ V_3,
c ∈ V_5): the rectangle forms on F are w ± u = 2Δ(b or a) + (c-terms), and the c-terms are what destroys the
clean "I_a ∩ I_b ≠ ∅" argument.
Ply for pqr: every atom/system has O(1) support points, so any such family has ≤ n^{O(1)} members and ply
≤ n^{O(1)} trivially; a full cover would therefore give ply poly(n) (and K = 2, ‖c‖₁ = O(1)).

## 5. What this means for the programme; n = 36
A complete cover for n = pqr would only confirm the known cap: squarefree slices give at most ~linear
ambiguity lower bounds (prompt §6), so it neither helps the negative side nor builds a grammar for Q; the
real target is n = P_N² (S_2 = 36). At n = 36 the fibres are the classes mod g = 6 (PA/poly_A2.md); *every*
witness chord for 2 and for 3 lies inside one fibre (n/2 = 18, n/3 = 12 ≡ 0 mod 6), there is no third prime,
and the failure set of the rectangle family is "2-witness fibres and 3-witness fibres disjoint". Lemma FT
works at 30 because off-fibre blocks are **zero** (free partners) and the third prime's classes mod pq cross
fibres. Neither holds at 36: on A2's product region x = B + e_2 + e_3 with B ∈ V_6 ⊇ constants large, every
partner costs ≈ B, so x_τ − Σ_P x_a > 0 forces |P| = 1 (on constant B), i.e. transfer atoms collapse to
construct.md's chord-dominance atoms (with chords between fibres allowed). With |P| = 1 a transfer form
F = (x_τ − x_s) + (x_t − x_a), s ≡ τ, t ≡ a (mod 18 or 12), *can* glue a witness in fibre r to one in fibre
r' = fibre of a (e.g. a = τ+1, t = s+1: two cyclically adjacent pairs), which is a genuinely new routing for
the disjoint-fibre configurations, but it still certifies one prime per atom when B separates fibres
(both rectangle-type chords then carry the B-gap |B_r − B_{r'}|), so the multiplicative ply ∏_k m_k of A2 is
untouched. [assessment] Control experiment at n = 12 (g = 2, the smallest p²q case), all
primitive x = a + b with a 6-periodic and b 4-periodic, entries 0..3 (979 200 points): **all covered already by
chord-dominance systems with k ≤ 2 (arbitrary chord positions)**; transfer atoms were not needed, and the S2K
example (1,2,3,3,1,3,3,2,1,3,3,3) is covered [computational]. So the n = p²q failure in construct.md §2 is a
failure of the *rectangle* family only, not of k ≤ 2 dominance systems. The n = 36 test (k ≤ 2 dominance
systems on the disjoint-witness-fibre set, then ply growth in m_2·m_3) is the next concrete computation; it was
not run here.
