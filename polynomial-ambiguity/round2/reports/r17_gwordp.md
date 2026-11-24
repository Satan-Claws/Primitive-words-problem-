# r17_gwordp.md — R17b G-word′: how much context the fold-centre escape tolerates, and where the context comes from

Status (honest):
- **Tolerance: much larger than o(n^{1/6}).** The rotation-image gain survives context h = o(n/log n) on each side and
  level constant C = o(√n) [written proof]. Numerically the true threshold is h = o(n): hit density ≈ √(h/n).
  The o(n^{1/6}) figure comes from the count |F_n(c)|·n. The weight argument used here is far stronger.
- **Sides decouple** [written proof]: the left and right insertions may come from *different derivations and different
  SCCs*. Only the distance of each insertion point from *its own* end matters.
- **G-word′ proved for geometric context** [written proof modulo the N-algebraic transfer already cited in r9 Thm M]:
  - Assumption: every derivation either passes through a two-sided flat-loop critical SCC C whose context grammar is
    strictly subcritical at ½, or lies in a finite-measure remainder.
  - Then L(G) ⊆ Q(C) (or G⁻ with level loops) is **not rotation-dense**, at **any polynomial ambiguity**.
  - This upgrades Thm G-word from "bounded context for every word" to "geometrically distributed context".
- **T8_poly: still OPEN.** The residual gap (G-end, §5) is critical SCCs *stacked* above the flat one with polynomial
  (Beta-split) context, unless the stack's top end-adjacent SCC itself supplies a flat end insertion.

Script: `scripts/r17_gwordp_tolerance.py` → `scripts/r17_gwordp_tolerance_out.txt` (~1 s). Steps are ±1; notation is
r17_gword's: P is the prefix walk, A(k) = P(k), B(k) = P(n) − P(n−k).

## 1. Lemma FR-pos (positional, side-decoupled) [written proof]
**Hypotheses.** L ⊆ Q(C). W ∈ L has length n. Fix two positions 0 ≤ p ≤ q ≤ n.
- **(left)** Some W′ ∈ L arises from W by inserting a word x with |x| ≥ n + c₀ at position p, plus a bounded word v
  (|v| ≤ c₀) at some position ≥ p.
- **(right)** Some W″ ∈ L arises by inserting y with |y| ≥ n + c₀ at position q, plus u (|u| ≤ c₀) at some position ≤ q.
- W′ and W″ may come from **different derivations**, and the two loops may lie in **different SCCs**. Only membership
  in L is used.

**Conclusion.** P(j) ≤ min(C, P(n) + C) + c₀ for p ≤ j ≤ q.

*Proof.* This is r17_gword §1, step for step.
1. Every suffix of W′ that does not reach x is (suffix of W) with v possibly spliced in. Such a suffix has length
   ≤ n − p + c₀ ≤ n′/2, so it lies before the fold centre, which now sits inside x.
2. W′ ∈ Q(C) therefore gives B_W(k) ≥ −C − c₀ for k ≤ n − p.
3. The mirror argument with W″ gives A_W(k) ≤ C + c₀ for k ≤ q. ∎

**Corollary.** With h := max(p, n − q) and Δ_h(W) := max_{j≤h}(|P(j)| + |P(n) − P(n−j)|), we have
  W ∈ E_n(C′, h) := {P(j) ≤ min(C′, P(n) + C′) on [h, n−h]} ⊆ F_n(C′ + 2Δ_h(W)), with C′ = C + c₀.
- In particular |P(n)| ≤ C′ + Δ_h(W) ≤ C′ + 2h.
- Brute-force check (script (1)): 190,214 triples (W, C, h) with n ≤ 14, **0 violations**.

**G⁻ form.** In the G⁻ variant of r17_gword §1, the frozen floor −h₀ − c₀ − K becomes −max_{j≤p}|P(j)| − c₀ − K.
So the same conclusion holds, with C′ = K + O(c₀) + O(Δ_h). [Same proof; constants as in r17_gword.]

## 2. Tolerance theorem [written proof]
**Theorem T-tol.** Let S_n ⊆ E_n(C, h). Then
  |Rot(S_n)|/2ⁿ ≤ (2K + 1)·max_y P(S_n = y) + 2n·e^{−(K−C)²/(2h)},
for every K.

*Proof.*
1. Rotation preserves the weight P(n), so Rot(S_n) ⊆ {|P(n)| ≤ K} ∪ Rot(S_n ∩ {|P(n)| > K}).
2. If W ∈ E_n(C, h) and P(n) > K, then P(n) − P(n−h) > K − C, because P(n−h) ≤ C.
3. If P(n) < −K, then P(h) < −(K − C), because P(n) ≥ P(h) − C.
4. By Hoeffding, each of these events has density ≤ e^{−(K−C)²/(2h)}. Each rotation class has at most n words. ∎

**Choice of K.** Take K = C + 2√(h ln n). Then the density is ≤ (2C + 4√(h ln n) + 1)·√(2/(πn)) + 2/n.

**Consequence.** The words admitting two-sided long insertions (Lemma FR-pos) within distance h_n of the ends, at level
C_n, are **not rotation-dense** provided h_n = o(n/log n) and C_n = o(√n).
- Log-level constants C + c·log n (r17_oh_level, audit_r17) are covered with a large margin.
- The F_n count alone (c³n^{−3/2}, times n) would have needed c = o(n^{1/6}). It is the wrong tool for the rotation
  image. It matters only for the *mass* form (Σ c_n³ n^{−3/2} < ∞).

**Numerics (script (2)).** The table gives the fraction of uniform words with some rotation in E_n(C, h); 400 words for
n = 400, 150 words for n = 1600.

| n, C | h = 0 | h = √n | h = n/ln n | h = n/8 | h = n/4 |
|---|---|---|---|---|---|
| 400, 0 | .055 | .207 | .380 | .335 | .485 |
| 1600, 0 | .013 | .120 | .313 | .313 | .487 |
| 1600, 3 | .040 | .220 | .400 | .380 | .567 |

- These fit ≈ √(h/n): for example, √(1/4) = .5 against .487.
- So h = θn gives **no gain**, consistent with r17_gword §4.
- The true threshold is very likely h = o(n). The log n in the proof is an artefact of the union bound.

## 3. Reduction: G-word′ ⇒ G-end
By §1–2, T8 for a grammar G (any ambiguity, L ⊆ Q(C) or G⁻ with level loops) follows from the following property.

> **(G-end)** All but a rotation-negligible set of words of L have a *left* long-flat insertion point within
> h_n = o(n/log n) of the left end, and a *right* one within h_n of the right end, possibly in different derivations.

This is strictly weaker than G-word′ as posed, which asked for one SCC with small context on both sides.

## 4. Context law under the derivation measure [written proof modulo N-algebraic transfer]
**Setting.**
- G is polynomially ambiguous, so the derivation counts d_n satisfy d_n ≤ n^k|L_n|. Every derivation GF is N-algebraic
  with radius ≥ ½.
- Fix a critical linear SCC C (Lemma F) and an entry X ∈ C.
- The derivations whose first C-node is X factor as context × yield. Their mass at length n is
  Σ_ℓ c_ℓ y_{n−ℓ}, with c_ℓ, y_m the context and yield masses (·2^{−length}).

**Prop CT.**
- (a) **Finite context ⇒ tight context.** Suppose Σ c_ℓ < ∞ and y diverges (y_m ≍ m^{α_y} with α_y > −1; α = −1 is
  excluded by Banderier–Drmota, as in r9 Thm M). Then the share of this derivation mass at length n with context > H
  is ≤ O(tail_c(H)) + O(n^{α_c+1}) → 0 uniformly in n, as H → ∞.
  - Here c_ℓ = O(ℓ^{α_c}) with α_c < −1, or c is geometric.
  - *Proof:* split at ℓ = n/2. On ℓ ≤ n/2 use y_{n−ℓ} ≤ C n^{α_y}. On ℓ > n/2 use c_ℓ ≤ Cn^{α_c} and
    Σ_{m≤n/2} y_m = O(n^{α_y+1}).
- (b) **Geometric context ⇒ word-level, any polynomial ambiguity.** Suppose c has radius > ½. This holds iff the hole
  path from S to X crosses no critical SCC and all side branches have radius > ½. Then with h_n = K log n, the
  derivations with context > h_n number ≤ n^{α−κK}2ⁿ. So the **words** all of whose derivations are bad number
  o(2ⁿ/n) for K large. This is the step where derivation mass converts to a word count with no ambiguity loss: a word
  is bad only if all its derivations are bad, so bad words ≤ bad derivations.
- (c) **Polynomial side branches.** Suppose c_ℓ ≍ ℓ^{α_c} (for example, Dyck side branches with α_c = −3/2). Then with
  h = n^{1−ε}, bad words ≤ 2ⁿ n^{α_y}(h^{α_c+1} + n^{α_c+1}). That is o(2ⁿ/n) iff α_y + α_c + 2 < 0, roughly.
  This is a real exponent condition, not automatic.

**Theorem G-geo [written, modulo transfer + r17_gword's insertion hypothesis].**
- **Hypotheses.**
  - G is polynomially ambiguous and L(G) ⊆ Q(C), or ⊆ G⁻ with level flat loops.
  - Every critical linear SCC of G has two-sided flat loops with bounded companions, which is the G-word insertion
    hypothesis.
  - Every critical linear SCC has geometric context (no critical SCC above it on a hole path).
- **Conclusion.** L(G) is not rotation-dense.
- *Proof.*
  1. Split the derivations into three classes:
     - (i) those through no critical SCC. These have finite measure (Lemma F contrapositive), so they produce
       2ⁿn^{α′} words with α′ < −1, and rotation image o(2ⁿ).
     - (ii) those through C with context ≤ K log n. Their words have rotation image O(log n/√n) by T-tol.
     - (iii) the bad ones. These give o(2ⁿ/n) words by CT(b).
  2. A word is outside classes (i) and (ii) only if all its derivations are of type (iii). ∎

## 5. What remains (exact gap) [heuristic + example]
**Stacked critical SCCs.** The divergent mass need not have finite context. Suppose a critical SCC T sits above C on
the hole path, for example T → bT | ET | X with E the negative excursions (μ = ½ + ½, heavy). Then the length split
between T's part and C's part is Beta(β_T, α_X + 1)-distributed, so C's context is **Θ(n) for almost all mass**.
- In this example, T is itself end-adjacent. Its loop T → ET inserts a (level) E-word at position 0, so the *left*
  insertion comes from T with context 0. The *right* insertion comes from X, whose right context is 0.
- (G-end) therefore still holds here, through the side-decoupling of §1.

**Remaining gap (G-end, precise).** Consider a polynomially ambiguous G with L ⊆ G⁻ rotation-dense, and order the
critical SCCs met by the hole paths from S top-down. The gap: show that the **topmost critical SCC adjacent to each
end**, meaning one with o(n/log n) context on that side, has a long flat insertion on that side.

Equivalently, the obstruction is a top critical SCC whose end-side loop insertions are **non-flat**, sitting above all
flat-loop SCCs. Candidates:
- non-level heavy blocks: r17_oh_level's Lemma L says heavy blocks *are* U- and V-level, which is evidence against this
  candidate;
- critical loops whose companion is unbounded.

This is exactly where G-word′ meets G-trunk (r17_gtrunk), so it is not duplicated here. Also open: the
polynomial-side-branch case of CT(c), whose exponent condition is unchecked for G⁻.

## Status table
| item | status |
|---|---|
| Lemma FR-pos (side-decoupled, cross-derivation) | written proof + brute force (0/190,214) |
| T-tol: h = o(n/log n), C = o(√n) suffice; numerically h = o(n) | written proof + Monte Carlo |
| G-word′ ⇒ (G-end) reduction | written proof |
| Prop CT(a) tight context; CT(b) word-level under geometric context | written modulo N-algebraic transfer (r9) |
| Thm G-geo (T8 for geometric-context two-sided-flat grammars, any poly ambiguity) | written modulo transfer + G-word insertion hypothesis |
| Stacked critical SCCs: Θ(n) context, rescued only through end-adjacent flat loops | example + heuristic |
| T8_poly | OPEN: gap (G-end) / polynomial side branches CT(c) |
