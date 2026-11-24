# r13_padding.md — R13-A: padding rigidity

Status: **padding rigidity PROVED for every model with long "level" blocks on both tapes (Thm PR2), and for one-tape
models (Thm PR1)** [written proofs; PR2 cites one cone-exit bound (Denisov–Wachtel), checked numerically]. The proof uses
**no class maxima and no Dyck orientation**. The mechanism is not a re-split. It is a **measure squeeze**:
- G⁻ plus "level" padding forces a valley shape, which costs a cone of angle 3π/4 (density n^{−2/3});
- injectivity plus square-root tails forces pair measure ≳ N^{1/2} up to length N, but the valley set only has N^{1/3}.

**Not proved:** the one-sided case (level blocks on one tape only), for which §5 gives a sketch only, and "steep" models with no level
blocks at all. **T8_unamb stays OPEN**; the exact remaining gap is in §6. No counterexample was found: every candidate
class with level blocks is now excluded.

Script: `scripts/r13_padding_cone.py` → `scripts/r13_padding_cone_out.txt`.

## 0. Setting and precise statement
Notation follows r10–r12. P is the centred prefix walk. A(k) := P(k) and B(k) := P(n) − P(n−k), the suffix excess. Then
W ∈ G⁻ ⟺ A(k) < B(k) for all 1 ≤ k ≤ n/2, by the chord form.

Pair model (r10 §2): fix a critical linear SCC C, a nonterminal X ∈ C, a context S ⇒* pXq and an exit X ⇒* w.
- First-return loops at X give i.i.d. tokens (u, v) with law π(u, v) = 2^{−|u|−|v|} and Σπ = 1.
- Word: W = p u₁⋯u_r w v_r⋯v₁ q. **Both A and B read the tokens in path order, from the outside in.**
- Unambiguity ⇒ the sequence ↦ word map is injective.

**Definitions.**
- A lower block B, on the V side of some C-rule, is **V-level** if for every L₀ some x ∈ B with |x| ≥ L₀ has suffix-excess
  profile D(x) − P_x(|x|−j) ≤ K for all j.
- A lower block on the U side is **U-level** if it has arbitrarily long words with prefix profile P_x(j) ≥ −K for all j.
- Examples: E and D⁻ are both U-level and V-level, through the flat words b(ba)^{m−1}a and (ba)^m. a* is U-level only.
  b* is V-level only.

**Tail hypothesis (T½).** For every lower block B in a C-rule, Σ_{ℓ>y}|B_ℓ|2^{−ℓ} = O(y^{−1/2}).
This holds for E, D⁻, every finite-mean block, and every block with exponent ≤ −3/2. It excludes only blocks with
exponent −1−1/2^k for k ≥ 2.

**Padding rigidity (precise form, r12 §4 generalised).** Let (C, p, w, q) be critical with heavy one-tape blocks under (T½).
If {pUwVq} ⊆ G⁻, the pair map is not injective. Equivalently, L is ambiguous.

## 1. Lemma MS (lag freedom ⇒ one-sided height bounds) [written proof]
If some C-rule carries a V-level block, then C_U := sup{P_W(k) : W ∈ L, k ≤ |pU|} < ∞.
Mirror: if some C-rule carries a U-level block, then C_V := sup{P_W(j) − P_W(n) : j ≥ |pUw|} < ∞.

*Proof.*
1. Fix a closed path ρ at X that uses the V-level rule, with fixed lower-block words except one V-level block word x of
   length L. Let β be the bounded suffix excess of q and the v-letters that ρ puts to the right of x.
2. Take W ∈ L with P_W(k) = H at a U-position k.
3. Build W' from the sequence (loops of ρ) · (W's loops) · exit w. This is a legal derivation, so W' ∈ L.
4. At k' = k + |U_ρ| we have A(k') = H + O(1), with the O(1) depending only on ρ.
5. Choose L ≥ k'. Then the suffix of length k' lies inside q·(v-letters of ρ)·x, so B(k') ≤ β + K. Also n' ≥ L + k' ≥ 2k'.
6. If H > β + K + O(1), then A(k') ≥ B(k') with k' ≤ n'/2, so W' ∉ G⁻. Hence H is bounded.

The mirror case is the same with a long U-level block freezing A from below while B is pumped. ∎

Lags are free because block lengths are free. So the finite-state coupling cannot synchronise the heights across the
tapes. This is the rigorous form of "padding destroys the zipping".

## 2. Lemma V (valley) and Lemma K (the cone cost) [written proof / cited bound + check]
**Lemma V.** Under both halves of MS, every W ∈ L satisfies max_j P(j) ≤ max(0, P(n)) + C, where C = C_U + C_V + |w|.
Call this set Valley_C.
- If P(n) ≥ 0, then B(k) ≥ −C for all k ≤ n/2.
- If P(n) < 0, then A(k) ≤ C for all k ≤ n/2.

**Lemma K.** |G⁻_n ∩ Valley_C| ≤ c_C·2ⁿ·n^{−2/3}.

*Proof.* Under the uniform measure, (A(k), B(k)) for k ≤ n/2 is a planar walk with i.i.d. steps (±½, ±½). It is isotropic,
centred and bounded. G⁻ ∩ Valley_C forces it to stay ⌊n/2⌋ steps in one of two wedges:
- W₁ = {A < B, B ≥ −C};
- W₂ = {A < B, A ≤ C}.
Each has opening angle 3π/4. By Denisov–Wachtel (Random walks in cones, Ann. Probab. 2015), P(τ > m) = O(m^{−π/(2θ)}) =
O(m^{−2/3}). ∎ [cited]

Check (`r13_padding_cone_out.txt`, exact DP to m = 1024):
- the local exponent of the W₁ survival is −0.648, −0.658, −0.662, −0.665, −0.666, −0.666 (C = 0);
- the half-plane (G⁻) exponent is −0.500;
- the ratio W₁/G⁻ falls from 0.74 to 0.37;
- exact enumeration for n ≤ 20 gives |G⁻ ∩ Valley_0|/|G⁻| = 1.00 → 0.949.

## 3. Lemma R (renewal lower bound) [written proof, elementary]
Let f be the law of the loop length |u| + |v|, with F̄(y) = f(>y), and let U(x) = Σ_{m≤x} u(m) be the renewal mass.
Then U(x) ≥ x/m(x), where m(x) = E[X ∧ x].

*Proof.* Let τ be the first n with S_n > x. Every Xᵢ with i < τ is ≤ x, so S'_τ := Σ_{i≤τ}(Xᵢ ∧ x) ≥ x. Wald's identity gives
U(x) = Eτ ≥ x/m(x). Here τ ≤ x + 1, because no loop is empty (that would make the grammar infinitely ambiguous). ∎

Under (T½), F̄(y) = O(y^{−1/2}):
- a first-return path has a geometrically-tailed number of steps, since ρ(M restricted to C∖X) < 1;
- each step emits ≤ K items, and the weights factorise;
- a union bound then gives F̄(y) ≤ Σ_s cρ'^s·Ks·c_B(y/Ks)^{−1/2} = O(y^{−1/2}).

So m(x) = O(√x) and U(x) ≥ c√x.

## 4. Theorem PR2 (two-sided padding rigidity) [written proof modulo the cited cone bound]
Suppose C, under (T½), has a U-level block and a V-level block, and suppose L ⊆ G⁻. Then the pair map is **not injective**.
Hence no unambiguous counterexample to T8 has such an SCC.

*Proof.*
1. Injectivity gives Σ_{n≤N}|L_n|2^{−n} ≥ 2^{−|pwq|}U(N − |pwq|) ≥ c√N, by Lemma R.
2. Lemmas MS, V and K give Σ_{n≤N}|L_n|2^{−n} ≤ Σ_{n≤N} c_C n^{−2/3} = O(N^{1/3}).
3. These are incompatible. ∎

**Corollary.** Multiplicity O(n^{1/6−ε}) is also impossible, since dividing by the multiplicity keeps the bound above N^{1/3}.
This is the first polynomial-ambiguity lift in this line, though it is tiny. Prop HS (≤ n+1 parses) is consistent with it.

Consistency checks:
- HS {(bEⁱ, Eʲa)} and No-go 2 {(E, ε), (b, Eᵏa)} are two-sided, so PR2 says they are ambiguous, which matches the computations.
- No-go 3 (the lazy zipped model) is not FSC: its tokens are not one-tape blocks. So PR2 correctly does not apply. G⁻ itself has
  density n^{−1/2} > n^{−2/3}, and PR2's cone cost is exactly what zipping avoids.

## 5. One-tape and one-sided models
**Thm PR1 (one-tape, v ≡ ε, or its mirror) [written proof].**
Suppose there is a block that is both U-level and V-level (for example E or D⁻), and L ⊆ G⁻.
1. The proof of MS applies with both the frozen block and the pumped loops on the same tape, placed first or last in the
   sequence. It gives max P ≤ min(0, P(n)) + C.
2. Hence |P(n)| ≤ C and P ≤ C, so L lies among the bridges under a barrier. These number O(2ⁿn^{−3/2}), so μ(L) < ∞.
3. Since μ(L) = ∞ under injectivity, the map is not injective.

This covers the r10 one-sided survivors X → Xa | XE, which were refuted at n = 28.

**One-sided case (U-level block only, and P(v ≠ ε) = q > 0) [proof sketch].**
1. The mirror of MS gives B(k) ≥ −C on the V-region, whose length is ≥ c·r with exponentially high probability. The tokens are
   i.i.d., so this follows from a large-deviation bound.
2. Sequences with r ≤ N^{1/2−δ} carry total renewal mass ≤ N^{1/2−δ}.
3. Bound the probability as wedge for the first m steps, then half-plane:
   P(wedge for m steps, half-plane for n/2 steps) ≲ m^{−1/6}n^{−1/2}.
   This uses E[dist·1{τ_W₁ > m}] ≲ m^{−1/6} together with the ballot bound. It is stated from the Denisov–Wachtel conditional
   limit and has not been checked in detail.
4. With m ≍ n^{1/2−δ}, the sum is Σ_{n≤N} = O(N^{5/12+δ/6}) = o(√N), which again contradicts injectivity.

## 6. Exact remaining gap
1. **Steep models.** No lower block on either tape is level: every long U-block word dips unboundedly, and every long V-block
   word climbs unboundedly. Then MS is unavailable, and the heavy blocks themselves carry drift.
   - Lemma SF still applies, so the blocks are fold-oriented.
   - No CF heavy example of this kind is known. Typical Dyck-type blocks contain flat words.
   - A proof would need "full-entropy fold-oriented ⇒ contains level words of unbounded length", which is plausible via Lemma Fac
     plus substitution, but **OPEN**.
2. **Tails heavier than square-root** (block exponent −1−1/2^k with k ≥ 2): Lemma R gives only N^{β} with β ≤ 1/4 < 1/3, so the squeeze fails.
3. The one-sided sketch (§5) needs the conditional-moment step written out.
4. Lifting from the SCC to T8_unamb is as in r9 Cor H, which supplies a critical linear SCC with a heavy block. Cases 1–2 are
   exactly what is left.

F1 check: everything uses the fold geometry (A < B, together with the cone wedges) and the density n^{−1/2} of G⁻. Q has density 1, so
no wedge bound applies to it. Nothing here implies Q is non-CF.

## Status
| claim | label |
|---|---|
| Lemma MS: a level block on one tape bounds the heights on the other tape (lag freedom) | written proof |
| Lemma V + Lemma K: L ⊆ Valley_C ∩ G⁻, density O(n^{−2/3}) | written proof + cited Denisov–Wachtel; numerical exponent −0.666 |
| Lemma R: U(x) ≥ x/m(x); under (T½), pair mass ≥ c√N | written proof |
| **Thm PR2**: two-sided level padding + (T½) + G⁻ ⇒ ambiguous; ambiguity is in fact ≥ n^{1/6−ε} on average | written proof modulo the cited cone bound |
| Thm PR1: one-tape models with an E/D⁻-type block are ambiguous | written proof |
| One-sided case | proof sketch |
| Steep models / heavier tails; heavy-block lemma; T8_unamb | **OPEN** (§6) |
| Unambiguous counterexample | none; all level-padded classes excluded |
