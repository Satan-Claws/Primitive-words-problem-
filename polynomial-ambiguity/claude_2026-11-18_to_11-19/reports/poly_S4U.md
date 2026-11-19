# poly_S4U — local laminar pieces at the S4T-uncovered sparse vectors (n = 30) [computational]

Scripts: `scripts/poly/s4u_local.py` (search: enumerate laminar G_S on supp x, entries ≤ 2, x ∈ int cone(G_S) in ℝ^S;
then MILP choosing one extension generator h_j ∈ {e_j, e_j+a e_s, 2e_j+e_s} per j ∉ S, all supports non-crossing in
0<1<…<29, and separating functionals L_p ∈ V_p^⊥ with L_p(x)=1, L_p ≥ 0 on every generator),
`scripts/poly/s4u_run.py` (independent verification + run over the S4T uncovered list).

## 1. v = 2e_0+e_10+e_15+e_20: piece FOUND (COMPUTER-CHECKED)
P = v + ℕG, |G| = 30, rank 30, G_S = {e_0, e_10, e_15, e_0+e_20} plus 26 extensions
(e.g. e_1+e_20, …, e_19+e_20, e_9+2e_10, e_11+2e_15 …, e_21+2e_0, …, e_29+2e_0; singletons e_3,e_6,e_7,e_18,e_23,e_26).
L_2 = e_20−e_5 + e_4−e_19 + ½(e_17−e_2) (orbit sums mod 15 vanish), L_3, L_5 similar; L_p ≥ 0 on G, L_p(v)=1,
so L_p ≥ 1 on P ⇒ P ∩ (V_2∪V_3∪V_5) = ∅. Supports pairwise non-crossing (stars at 0, 15, 20 nested inside (0,20)/(0,2x)).
P contains the ray kv ((k−1)v = (k−1)(e_0+e_10+e_15+(e_0+e_20)) ∈ ℕG) and an orthant-neighbourhood of it
(v ∈ int cone G_S in ℝ^S, plus one generator in each direction e_j, j ∉ S). Independent check: 20000 random points
of P all primitive.

Why S4T missed it: S4T used only chord witnesses x_s ≠ x_t (L = e_s − e_t). Here L_2 is a *sum of three chords*
with mixed signs, positive on v only through 20>5; the correction terms let the e_0+e_20 generator and
the stars at 15/20 coexist. The "peak obstruction" of S4T §3(c) is an artefact of the chord-only family.

## 2. The S4T uncovered list
S4T's "120 uncovered" = 60 distinct vectors (each counted twice across support shapes).
Run over all 60 (`python3 s4u_run.py`) was started but NOT finished within the 13-min budget: remaining-uncovered count UNKNOWN (only v verified).

## 3. Interpretation (no overclaim)
* Local pieces exist ⇒ no candidate non-CF certificate at these vectors; nothing contradicts the (second-hand,
  UNVERIFIED) Kászonyi–Katsura claim that Q∩(ab*)^30 is CF.
* This is LOCAL: each piece has base x itself (or a finite set of translates c with L_p(c)>0 covering a
  neighbourhood of the ray). A finite global cover of E∩W_30 still needs a finite family of (G, L) patterns
  whose cones cover the whole cone; not attempted. Separation by a linear L_p is sufficient, not necessary
  (parity-type avoidance not searched).
