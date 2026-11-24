# r18_gend.md — R18-B: G-end (stacked critical SCCs)

Status (honest):
- **Q(C) form: G-end PROVED, with h_n = K log n, at any polynomial ambiguity** [written proof below; inputs are
  r17 FR-pos + T-tol and standard Perron/renewal/Hoeffding facts]. Stacking plays **no role**: the argument is a
  word-level count of length-h prefixes, not a derivation-measure (context-law) argument.
  - **Corollary (T8 for Q(C)):** a polynomially ambiguous CFL L ⊆ Q(C) is not rotation-dense.
- **G⁻ form: reduced, not closed.** Every piece of the left boundary is handled except one: **spanning** nodes,
  meaning nodes whose span starts in [0, h) and ends beyond n/4. These are exactly the "top SCC adjacent to both ends"
  of the brief. The exact residual R⁻ is stated in §4. Its light-both-sides case reduces to an (AM)-type multiplicity
  bound (R18-A).
- **CT(c) exponent condition α_y + α_c + 2 < 0 is FALSE generically.** It holds in 16 of 124 B–D exponent
  combinations, and fails e.g. for a light yield with a Dyck side branch (sum = +½). So the derivation-measure route
  cannot close G-end. It is **bypassed**: a heavy side branch is a critical nonlinear block, whose nodes are themselves
  left-good (§1).
- **Brief's question "does a critical linear SCC always have flat end-loops?":**
  - mean drift: **yes**. E_π D(u) = E_π D(v) = 0 is forced under poly ambiguity (§4.2, written sketch);
  - bounded-companion long flat insertion: **no**. Finite U-parts give none (§4.1).

Script: `scripts/r18_gend_checks.py` → `scripts/r18_gend_checks_out.txt` (~10 s).

Steps are ±1; A, B, P are as in r17_gword. Polynomial ambiguity means amb(W) ≤ |W|^k, with a reduced, ε-free grammar.

## 1. Left-good nodes
**Definition.** A node ν of a derivation tree of W ∈ L_n with span start p is **left-good** if its label Z admits
Z ⇒* x Z v with |x| ≥ n + c₀ and |v| ≤ c₀, where:
- in the Q(C) case x is arbitrary;
- in the G⁻ case x is U-(log-)level.

Then W′ = W with x inserted at p and v at a position ≥ p is in L. This is exactly the (left) hypothesis of FR-pos.
Right-good is the mirror notion.

**Lemma LG [written proof].**
- (a) [Q] Every node in a recursive **nonlinear** SCC K is left-good.
  - Some rule has two K-occurrences: Z₁ → α′Z₂β′Z₃γ′. Every Z ∈ K satisfies Z ⇒* σZ₁τ and Z₃ ⇒* sZt.
  - So Z ⇒* (σα′x′β′s) Z (tγ′τ) with x′ ∈ L(Z₂) arbitrary (L(Z₂) is infinite) and a fixed right part.
- (b) [Q] In a linear SCC, a node is left-good if some cycle Z ⇒⁺ sZt has L(s) infinite, or if s ≠ ε and t = ε
  (pump x = sⁱ). Call a linear SCC **left-finite** if every cycle has L(s) finite.
- (c) [G⁻] Every node of a critical nonlinear SCC is left-good. More generally, so is every node of an SCC that has a
  cycle whose left part derives into a critical nonlinear SCC.
  - Proof: as in (a), but choose x′ U-(log-)level. Such words exist in L(Y_bot) for the bottom critical nonlinear SCC
    below, by SM + HL (r15_side, r14), and they are padded by fixed connectors.
  - SM's Step 2 needs only "trees ≤ poly·words", which polynomial ambiguity gives. The bottom SCC's lower SCCs have
    radius > ½: a critical **linear** SCC below a critical nonlinear one would push its radius below ½ (Lemma ST(i)
    argument).
  - Lengths are geometric, so |x| ∈ [n, 3n + c]. This is Lemma L's mechanism, applied at an arbitrary node.

Consequence: heavy side branches (critical nonlinear) and heavy U-tokens are always left-good. Only **light or finite**
left material can be left-bad.

## 2. The h-path decomposition [written proof]
Fix h ≤ n/16 and a derivation t of W. Let π_h be the path from the root to the leaf at position h.
- **Bad-left:** every node with span start < h is left-bad. Such nodes are exactly the nodes of π_h together with the
  nodes in the left-sibling subtrees of π_h, which lie entirely in [0, h).
- **Factorisation:** W[0, h) is the concatenation, along π_h, of the left siblings' yields. Group π_h into maximal
  same-SCC segments; there are at most N_SCC of them.
  - **(L)-factors.** Inside a segment of a left-finite linear SCC K, the left siblings form a word of the regular
    "left-label" language Lft_K(X → X′) (labels from finite sets).
  - **(S)-factors.** At the at most c₁ = N_SCC·max|rule| between-SCC steps, the left siblings are all-bad subtrees
    with yields y ∈ L_bad(Y) (trees in G_bad, the grammar restricted to left-bad nonterminals).
- In the Q(C) case, G_bad has only linear SCCs (by LG(a)), all of them left-finite (by LG(b)).

## 3. Theorem GE-Q [written proof]
**Statement.** Let G be polynomially ambiguous with L(G) ⊆ Q(C), and let h = K log n. Then the bad-left words satisfy
|Rot(Bad_n)| ≤ n·(h+1)^{c₁}·c·(g/2)^h·2ⁿ for some g < 2. This is o(2ⁿ) for K large. The mirror bound holds for
bad-right words.

**Walk budget.** Any replacement or pumping that keeps a modified region inside [0, n′/4] preserves W′ ∈ L ⊆ Q(C),
so the modified prefix walk is ≤ C. The walk before position h is ≥ −h. So every factor sits under the ceiling
C_W := C + h = O(log n) ≪ √n.

**Step 1 [(L)-factors have growth < 2].**
- Suppose Lft_K(X → X′) had growth 2. Then its trim DFA has a *complete* component, and that component contains u aᵐ v
  for every m.
- Re-route the segment through that path. Its right parts go beyond h, so the left region grows by O(m) ≤ n/8.
- The walk then reaches ≥ −h − |u| + m > C_W at a position ≤ n′/2. This contradicts Q(C).
- No criticality is needed for this step.

**Step 2 [(S)-factors have radius > ½].** Suppose the all-bad Y-trees had radius ½.
- G_bad is finite-index, so by IFT applied bottom-up there is a lowest critical SCC K ⊆ G_bad: ρ(J_K^bad(½)) = 1, and
  all of its side branches have radius > ½. So the tokens are **light**, and for a fixed exit and connector the number
  of K-trees of length m is ≥ c·2ᵐ along a progression (simple pole).
- Replace the K-subtree inside the region by K-trees of length m ≤ n/4. These stay in [0, n′/2] and under C_W.
- **λ := E_π|s| > 0.**
  - Pumping excludes cycles with D(s) > 0, because the pumped cycle stays inside the region.
  - So, as in Step 1, Lft(K) has growth g_K < 2.
  - By Cramér, all but exponentially few trees have |S| ≥ λm/2. Those trees yield at most
    m·Σ_{j≥λm/2} g_K^j 2^{m−j} distinct words.
  - So some word has exponentially many trees, contradicting polynomial ambiguity.
- **λ = 0** (every cycle has s = ε; left recursion).
  - Pumping gives D(t) ≤ 0 for every token.
  - If E_π D(t) < 0, Hoeffding plus large deviations again force exponential ambiguity. So D(t) ≡ 0.
  - Distinct token sequences give distinct words w·t_r⋯t₁. If two coincided, pumping would give 2ʳ trees.
  - So #words = #trees ≥ c·2ᵐ. But every one of these words has drift exactly D(w), and such words number ≤ c·2ᵐ/√m.
    Contradiction.

**Step 3 [count].**
- W[0, h) is a concatenation of at most 2c₁ factors, each from a language of growth ≤ g < 2. Prefix-skeleton choices
  number ≤ (h+1)^{c₁}.
- So |{W[0, h)}| ≤ c(h+1)^{c₁}gʰ.
- Rotation multiplies the count by at most n. ∎

**Corollary (T8 for Q(C)) [written, modulo r17 FR-pos + T-tol].**
- Words that are good on both sides lie in E_n(C′, K log n). Their rotation image is O(log n/√n) by T-tol.
- Bad words have rotation image o(2ⁿ) by GE-Q.
- Hence a polynomially ambiguous L ⊆ Q(C) is not rotation-dense.

Stacking never enters the argument. The (S)/(L) factors are whatever SCCs the h-path happens to cross. The polynomial
CT(c) tails disappear, because heavy side branches are left-good (LG(a)/(c)).

## 4. G⁻: what survives and the exact residual
**What transfers [written].**
- In G⁻ the pointwise ceiling is A(k) < B(k). For k ≤ n/2, B(k) is read on the last n/2 letters.
- A modification inside [0, n/4] leaves those letters untouched.
- So Steps 1–2 run with C_W := max_{j≤n/2} B(j) + h.
  - Words with C_W > √n·log n are super-polynomially rare (count × n → 0).
  - Step 1's pumping needs only C_W ≪ n.
  - Step 2's λ = 0 contradiction uses the fixed drift and **not** C_W.
- G_bad may now contain light nonlinear SCCs, and light infinite left parts without U-level words. Both have radius > ½,
  so they only help the count.
- **Conclusion:** GE⁻ holds for every derivation whose h-path nodes with span end ≤ n/4 cover ≥ h/2 of [0, h).

**Residual R⁻ (exact gap).** Consider the derivations in which ≥ h/2 letters of [0, h) are left parts of cycles of
**spanning** π_h-nodes (span ⊇ [h, n/4]) in left-bad SCCs, and whose left-label language has growth 2.
- Here pumping a left cycle (s, t) also moves the right part t across the centre, so A < B can be rebalanced.
- Pair counting of (prefix, suffix) loses only polynomially (ordered-walk ballot ≍ 1/h), so entropy alone cannot work.

### 4.1 Reductions of R⁻
- Heavy U-tokens or a nonlinear critical spanning SCC: left-good by LG(c). Not in R⁻.
- **Spanning critical linear T, light tokens on both sides, fixed context and exit.**
  - The family has ≥ c·2ⁿ trees, but |G⁻_n| ≍ 2ⁿ/n (cross-section).
  - So the **average** exit-slide multiplicity must be ≥ c·n. The bound m ≤ occ_w ≤ n is r17_gtrunk Lemma 1.
  - Hence this case is excluded by any (AM)-type bound E_n[m] = o(n). That is R18-A's object; it is weaker than (AM)
    as posed.
- **Spanning critical linear T with finite or light U-parts and heavy V-parts (β < 1):** counting gives nothing
  (2ⁿn^{β−1} trees). **This is the irreducible remainder.**
  - It is the poly-ambiguous analogue of r17_oh_level Thm OH (one-sided heavy, there with unambiguity).
  - Right-end insertions are fine (V-side heavy ⇒ V-level by Lemma L). Only the left end lacks a bounded-companion
    flat insertion.

### 4.2 Flat loops in a critical linear SCC [written sketch]
Let T be critical linear in a poly-ambiguous G with L ⊆ G⁻, with light tokens (u, v).
1. **Total drift:** E[D(u) + D(v)] = 0. Otherwise Hoeffding makes the words exponentially rare against c·2ⁿ/poly
   trees.
2. **Left drift positive is impossible:** if E D(u) > 0, the LLN gives A(k) ≈ k·μ_A > 0 > k·μ_B ≈ B(k). Typical trees
   would then violate G⁻, which holds deterministically.
3. **Left drift negative is impossible:** if E D(u) < 0, the Θ(n) U-region has linear negative slope, which is
   exponentially rare.

Hence E D(u) = E D(v) = 0. This does **not** give an end insertion:
- a pumped zero-drift loop uⁱ has companion vⁱ, which is unbounded;
- FR-pos with an unbounded companion needs |x| ≥ n + |vⁱ| and D(vⁱ) ≤ c₀, i.e. |u| > |v| and D(v) ≤ 0. That is a
  special case only.

**Check (2b):** single-nonterminal T → uTv | w with finite tokens, |u| + |v| ≤ 8, D(u) = D(v) = 0, compatible with G⁻
when pumped alone.
- The only such tokens are (x, ε) with x mirrored-Dyck. These are **pure-left, hence left-good**.
- Their mass is 0.375, 0.469, 0.539 for L = 4, 6, 8. That mass is < 1 and tends to 1 only through infinitely many
  (i.e. heavy) tokens.
- For the exits w = ab and aab there are no compatible tokens at all.
- Without the balance restriction, mass ≥ 1 is reached only by exponentially ambiguous sets (e.g. (b, ε), (bb, ε)),
  which are excluded.

This is evidence that R⁻ with **finite** U-parts is empty. It is not a proof.

## 5. CT(c) exponent check
(Script (1).) Take α_c = −1 − 2^{−k} for a finite-mass heavy side branch and α_y = −1 + m2^{−j} for a divergent yield,
with B–D exponents k ≤ 4 and j ≤ 4.
- The condition α_y + α_c + 2 < 0 holds in **16 of 124** combinations.
- Example failure: a light critical yield (α_y = 0) with a Dyck side branch gives +½.

So r17_gwordp CT(c) **fails in general**. GE-Q replaces it with a word-level argument, in which a heavy side branch is
a left-good node, not a context cost.

## Status table
| item | label |
|---|---|
| Lemma LG (which nodes are end-good; G⁻ via SM/HL in poly-ambiguous form) | written proof |
| Thm GE-Q: G-end in Q(C), h = K log n, any poly ambiguity, stacking irrelevant | written proof |
| Cor: poly-ambiguous L ⊆ Q(C) not rotation-dense | written, modulo r17 FR-pos/T-tol |
| G⁻: GE⁻ except spanning residual R⁻ | written reduction |
| R⁻ light/light ⇐ (AM)-type E_n[m] = o(n) | written reduction |
| R⁻ light-U / heavy-V spanning critical linear SCC | **OPEN** (exact remainder) |
| E D(u) = E D(v) = 0 for critical linear SCCs in G⁻ | written sketch |
| CT(c) exponent condition | false generically (16/124); bypassed |
| finite balanced G⁻ tokens are pure-left (L ≤ 8) | numerical evidence |
