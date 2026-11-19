# poly_R3a: spaced slices R_m^S (free blocks + fixed spacers) vs G3**

Setting as poly_P.md / poly_T2b.md / poly_G3.md. Fix a spacer word S ∈ (ab⁺)^* (no empty block), and
  R_m^S := a·(S·ab⁺)^{M}·a·(S·ab⁺)^{M},  free coords x_1..x_M, y_1..y_M (the ab⁺ blocks), all other
  blocks fixed by the DFA (S's exponents, and the two isolated a's = the only empty blocks).
G_m^S := ((G''×D_{R_m^S})×D_n) reduced (n = 2m(1+|S|_a)).

## 1. What transfers (PROVED)
**Lemma 1^S.** w ∈ R_m^S is primitive ⇔ x ≠ y. (Proof of PROOF.md Lemma 1: the empty blocks are exactly
the two isolated a's, so a period shift is n/2; shift n/2 fixes S-blocks, so invariance ⇔ x = y.) ∎
**Lemma Z (rings avoid fixed blocks).** Every ring vector v_π vanishes on fixed blocks. (If v_π had a b in a
fixed block, one more turn yields a word of L(G_m^S) ⊄ R_m^S; G_m^S is reduced.) So every ring pair is
{s,t} ⊆ free (after the F2 shrink), and offsets c_σ equal the fixed exponents there. ∎
**Lemma I (invariance).** Deleting the fixed coordinates maps skeleton data of G_m^S to data
(c_σ, V_σ) on ℝ^{2M} that is laminar for the induced order x_1<…<x_M<y_1<…<y_M, avoids Δ, covers NE_M,
with ‖v‖₁ ≤ K, ‖c_σ‖₁ ≤ nK. Hence PROOF.md §4 (Lemma X), poly_P §3 (cases 1–4, ⌈m/2⌉), Lemmas C, K, G and
the statement of G3** run verbatim on R_m^S. ∎

## 2. Where the lever fails (exact step)
Claimed step "a laminar chain e_i + 2e_{i+1} needs consecutive free blocks, which spacers prevent" is FALSE:
adjacency is in the *induced* order of free blocks, and a G''-ring A ⇒⁺ b^p A b^q has an unbounded middle,
which may contain any fixed spacer. Explicit fixed fragment (size O(|S|), independent of m):
  Y → b Y bb | T,   T ⇒ (S'' := the spacer between two consecutive free blocks, written a·S·a-style).
Y yields b^j·(spacer)·b^{2j}; Y Y ⋯ Y across the free blocks gives x_{i+1} = 2j_i + j_{i+1}, i.e. ring list
{e_1} ∪ {e_i + 2e_{i+1}} in free coordinates: ℤ^{ρ+1}/ℤV ≅ ℤ/2^ρ, facet normal ((−2)^{ρ−i})_i — the
poly_T2b §1 chain survives the spacing unchanged. G''-translation invariance gives nothing new: this chain is
itself translation invariant (one G''-cycle with (p,q)=(1,2) used at every free pair). Any choice of the free
set F ⊆ blocks with |F| = 2M diagonal-paired coords is isomorphic, by Lemma I, to R_m; |F| bounded is the
registry-BLOCKED fixed-block-count slice.

## 3. Status
- PROVED: Lemmas 1^S, Z, I (spacing is invisible to ring geometry).
- BLOCKED (route): spacer/free-block slice design cannot bound Λ_S, apex, θ_S; G3** on R_m^S ≡ G3** on R_m.
- OPEN (unchanged): whether such chains can be type-4 members of a valid Δ-avoiding NE_M cover (poly_G3 §4).
