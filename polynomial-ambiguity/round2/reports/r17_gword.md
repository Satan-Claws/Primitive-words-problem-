# r17_gword.md — R17b G-word: set-level gain from outermost flat insertions

Status:
- **(G-word) as posed: YES** [written proof, elementary, ambiguity-free].
- **T8_poly: still NOT proved.** The gain applies only to words that admit the two-sided outermost insertion with
  **bounded (more generally o(n)) context**. With ambiguity, the rotation-dense mass need not sit on such words (§5).

Script: `scripts/r17_gword_full.py` → `scripts/r17_gword_full_out.txt` (runs in ~25 s). Steps are ±1 (a = +1, b = −1);
the repo's ±½ scale doubles every C.

## 0. Setting
P is the prefix walk of W, with n = |W|, A(k) = P(k) and B(k) = P(n) − P(n−k).
- Q_n(C) = {A(k) ≤ C and B(k) ≥ −C for k ≤ n/2}. Its density is ≍ 1/n, a rotation cross-section (L3).
- **Full-range set:** F_n(c) := {W : max_{0≤j≤n} P(j) ≤ min(0, P(n)) + c}. Both endpoints of the walk lie within c of
  its maximum.

## 1. Lemma FR (fold-centre escape) [written proof]
**Hypotheses.**
- L ⊆ Q(C). (Alternatively, L ⊆ G⁻ with U-/V-level flat words; see the variant below.)
- W = γ M δ ∈ L with |γ|, |δ| ≤ h₀.
- Both outermost insertions are in L:
  - W′ = γ α x β M v δ;
  - W″ = γ u M α′ y β′ δ;
  - α, β, v, u, α′, β′ are fixed words with |·| ≤ c₀, and |x|, |y| ≥ n + c₀.

**Conclusion.** W ∈ F_n(C₁), where C₁ = C + c₀ + 2h₀.

*Proof.*
1. For |δ| ≤ k ≤ n − |γ|, the suffix of W′ of length k + |v| is (suffix of M)·v δ. So
   B_{W′}(k + |v|) = B_W(k) + wt(v).
2. Since n′ ≥ 2n + |v|, we have k + |v| ≤ n′/2. The fold centre of W′ lies inside x, beyond every such k.
3. W′ ∈ Q(C) therefore gives B_W(k) ≥ −C − c₀ on [|δ|, n − |γ|]. The end pieces of length ≤ h₀ cost at most h₀ each,
   so B_W(k) ≥ −C₁ for all 1 ≤ k ≤ n.
4. The mirror argument (W″, with prefix A_{W″}(k + |u|) = A_W(k) + wt(u)) gives A_W(k) ≤ C₁ for all k.
5. Together these say P(j) ≤ C₁ and P(j) ≤ P(n) + C₁ for every j. ∎

*Remarks.*
- With the Q(C) hypothesis, x and y only need to be **long**; flatness is not used.
- **G⁻ variant.** If instead L ⊆ G⁻, use the frozen lower bound A_{W′} ≥ −h₀ − c₀ − K on the x-stretch (x U-level,
  as in r16 step 4). That gives the same conclusion with C₁ = K + O(h₀ + c₀).
- This is exactly MS⁺ with the window k ≤ n/2 removed. audit_r17 §1 noted that the window was unnecessary
  ("constrains B_W(k) for all k ≤ n − |p|"), but that observation had not been used.
- Exhaustive check: 150 random instances with |M| ≤ 11. 5034 words had W, W′, W″ ∈ Q(C), and **0** were outside
  F(C + O(1)).

## 2. Counting F_n(c) [written proof + exact]
**Exact count (reflection).** With N(n, y) = binom(n, (n+y)/2),
  |F_n(c)| = Σ_{y=−c}^{c} [N(n, y) − N(n, 2(min(0,y) + c + 1) − y)].
This matches brute force for n ≤ 16 and c ≤ 3.

**Upper bound.**
- Each term is N(n, y) − N(n, z) with |y| < z ≤ 3c + 2.
- The ratio N(n, t)/N(n, 0) = Π_{i≤t/2}(n/2 − i + 1)/(n/2 + i) is ≥ 1 − 2t²/n.
- So |F_n(c)| ≤ (2c + 1)·2(3c + 2)²·binom(n, n/2)/n ≤ c′(c + 1)³·2ⁿ·n^{−3/2}.

**Constant at c = 0.** |F_n(0)| = Catalan(n/2), so n^{3/2}·density → 2^{3/2}/√π ≈ 1.5958 on even n.

n^{3/2}·density for n = 10², 10³, 10⁴, 4·10⁴:

| c | 10² | 10³ | 10⁴ | 4·10⁴ |
|---|---|---|---|---|
| 0 | 1.561 | 1.592 | 1.5954 | 1.5957 |
| 1 | 6.06 | 6.35 | 6.380 | 6.382 |
| 2 | 22.0 | 23.7 | 23.92 | 23.93 |
| 4 | 85.1 | 101.6 | 103.5 | 103.7 |

The values are bounded and converge.

## 3. Theorem G-word (bounded context) [written proof, any ambiguity]
Let L ⊆ Q(C) (or L ⊆ G⁻ with level flat loops). Let S ⊆ L be the set of words admitting both outermost flat insertions
with context ≤ h₀. Then:
- |S_n| ≤ c(C₁ + 1)³·2ⁿ·n^{−3/2} = o(2ⁿ/n), so the mass Σ|S_n|2^{−n} is **finite**.
- Rot(S_n) ⊆ Rot(F_n(C₁)) ⊆ {|P(n)| ≤ C₁}, which has density O(C₁ n^{−1/2}) → 0. A rotation of W moves its weight
  P(n) not at all, and F forces |P(n)| ≤ c. So **S is not rotation-dense, by a margin n^{1/2}**.

In particular, if **every** word of a CFG G (of any ambiguity) lies in Q(C) and admits the two-sided outermost flat
insertions with bounded context (the task's hypothesis), then L(G) is not rotation-dense. This is a **genuine set-level
gain**: n^{−3/2} against the cross-section's n^{−1}, and the rotation closure collapses from everything to the balanced
words.

**F1 check (passes).**
- The hypothesis is containment in a cross-section (Q(C) or G⁻) plus insertion closure. Q itself satisfies neither
  (Q ⊄ G⁻), so F1(a)'s obstruction does not apply.
- The theorem is a statement about all sets, not only CFLs. Its proof never touches primitivity, so it cannot prove
  "Q ∉ CF".

## 4. The task's "all centre shifts" family [exact DP; asymptotic numerical]
Requiring the quadrant for every fold-centre shift s ∈ [−r, r] gives
  H_n(C, h) = {P ≤ C on [0, n−h], P(j) − P(n) ≤ C on [h, n]}, with h = n/2 − r.

The values of n·density(H_n) are stable in n (n = 200, 400, 800):

| C | θ = h/n = .5 | .375 | .25 | .125 | .0625 |
|---|---|---|---|---|---|
| 0 | 1.272 | 0.986 | 0.736 | 0.483 | 0.333 |
| 2 | 11.37 | 8.83 | 6.61 | 4.37 | 3.05 |

With h = 2, n^{3/2}·density ≈ 2.39 (C = 0) and 28.4 (C = 2).

So the density is ≈ f(θ)/n with f(θ) ≈ 1.3√θ [numerical], i.e. density ≍ √(h/n)/n. **Shifts by a fixed fraction of n
gain only a constant.** The gain is o(1/n) iff h = o(n). A long outermost insertion is the extreme case h = O(1), and
that case is what gives n^{−3/2}.

## 5. Why T8_poly is still open: exact remaining gap
1. In the reduction chain, the words that provably admit the outermost insertion are the **pair-model words**
   p·M(s)·q of one critical SCC, with fixed context (audit_r17 C1). For them, the improvement is that word mass goes
   from O(log N) to O(1).
2. So the PR2⁺ squeeze improves to m_N ≥ cN^{β₀}, with the log removed. That is still polynomial, and polynomial
   ambiguity can pay it.
3. For a general word routed through C, the context (γ, δ) is arbitrary. In the G⁻ form, the bound becomes
   R_M(t) ≤ min(0, R_M(m)) + D + C with D = wt δ − wt γ unbounded. In the Q(C) form, it becomes H_n(C, h) with
   h = max(|γ|, |δ|), and by §4 contexts of size Θ(n) give only a constant gain.

**(G-word′), the exact gap.** In any CFG with rotation-dense L ⊆ G⁻, show that the words having *some* derivation
through a two-sided critical SCC whose outermost entry has context o(n) on both sides have divergent mass (or a
rotation-dense image). Theorem G-word then gives a contradiction at every ambiguity.
- Equivalently, the obstruction is a grammar in which the dense part of L enters every flat-loop SCC only at linear
  depth on at least one side, i.e. inside a Θ(n)-long context.
- This is a structural (spine-position) statement, analogous to REGISTRY Prop S ("rotation-dense ⇒ spines escape to
  infinity"). Not proved here.

## Status table
| item | status |
|---|---|
| Lemma FR (full range from outermost insertion) | written proof + exhaustive check (0/5034) |
| \|F_n(c)\| ≤ c′(c+1)³2ⁿn^{−3/2}; C = 0 constant 2^{3/2}/√π | written proof + exact |
| Thm G-word (bounded context, any ambiguity) | written proof |
| H_n(C, θn) density ≍ √θ/n | exact DP, asymptotics numerical |
| T8_poly | OPEN; gap (G-word′) = o(n)-context entry for the dense part |
