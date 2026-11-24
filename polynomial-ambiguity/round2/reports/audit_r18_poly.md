# audit_r18_poly.md — gated audit of the T8_poly partial results (r17_gword, r17_gwordp, r17_gstruct, r18_gend)

Script: `scripts/audit_r18_poly_checks.py` → `scripts/audit_r18_poly_checks_out.txt` (~6 s). Steps ±1.

## Verdicts
| candidate | verdict |
|---|---|
| r17_gword Lemma FR, |F_n(c)| bound, rotation density, Thm G-word | **SURVIVES** |
| r17_gwordp FR-pos, T-tol, Prop CT(a,b), Thm G-geo | **SURVIVES** (G-geo modulo cited transfer; CT(c) was never claimed) |
| r17_gstruct IF, SU, Trunk Lemma, Prop P | **SURVIVES**, with a wording caveat on Cor (b) |
| r18_gend Thm GE-Q + Cor (T8 for L ⊆ Q(C), poly-ambiguous) | **SURVIVES**, with two repairable gaps (C4, C5) |

No fatal flaw was found. The first-flaw search for each candidate is below.

## 1. FR (r17_gword)
- **Centre shift, re-derived.**
  - For |δ| ≤ k ≤ n − |γ|, suf_{k+|v|}(W′) = (suffix of M)·vδ.
  - We need k + |v| ≤ n′/2, where n′ ≥ 2n + c₀ + |v|. This reduces to |v|/2 ≤ |γ| + c₀/2, which is true. So every such
    suffix lies before the fold centre, which now sits inside x.
  - The end pieces cost at most h₀. Hence B_W(k) ≥ −C − c₀ − h₀ holds for **all** 1 ≤ k ≤ n, not just k ≤ n/2.
  - The mirror argument gives A_W(k) ≤ C₁. So max P ≤ min(C₁, P(n) + C₁) = min(0, P(n)) + C₁. ✓
- **Independent brute force (1).** I used adversarial x: b-biased on the left, a-biased on the right, so that W′ and W″
  survive in Q. Out of 35,200 instances with W′, W″ ∈ Q(C), **0** had W ∉ F(C + c₀ + 2h₀).
- **Reflection count (2).**
  - The formula matches brute force for all n ≤ 16 and c ≤ 3.
  - sup over n ≤ 3000, c ≤ 8 of n^{3/2}|F_n(c)|2^{−n}/(c+1)³ is 1.595, attained at c = 0 (Catalan, 2^{3/2}/√π).
  - The proof steps check out: |y| ≤ c, 0 < z − |y|, z ≤ 3c + 2, and the ratio bound 1 − 2t²/n.
- **Rotation (3).**
  - Rot(F_n(c)) ⊆ {|P(n)| ≤ c} holds exactly for n = 12 and 16.
  - The density O(c/√n) is asymptotic. At n = 16 it is still 0.55 for c = 2.
- **Caveat.** The G⁻ variant (frozen floor) is only sketched. It is not used by GE-Q.

## 2. FR-pos / T-tol / CT / G-geo (r17_gwordp)
- **FR-pos.**
  - Suffixes of W of length ≤ n − p correspond to suffixes of W′ of length ≤ n − p + c₀ ≤ n′/2.
  - The conclusion on [p, q] is correct.
  - The side decoupling is legitimate: only L-membership of W′ and of W″ is used.
  - Minor: the true bound is |P(n)| ≤ C′ + h (stated as C′ + 2h; harmless).
- **T-tol bookkeeping, re-derived.**
  - Rot preserves P(n). For W ∈ E_n with P(n) > K, P(n) − P(n−h) > K − C. Hoeffding gives e^{−(K−C)²/(2h)}, and each
    class contributes ≤ n.
  - With K = C + 2√(h ln n) the tail term is 2/n.
  - The point term is (2K+1)·O(n^{−1/2}). So the bound → 0 iff h log n = o(n) and C = o(√n). ✓
  - Exact check (3′), n ∈ {12, 16}, C ≤ 1, h ≤ 3: the bound holds and |P(n)| ≤ C + h holds on E. 0 violations.
- **CT(b).** "bad words ≤ bad derivations" is the correct direction, so no ambiguity is lost.
- **G-geo, class (i).** This step needs coefficient asymptotics n^{α′}, α′ < −1. Finite mass alone does not give it.
  It is supplied by the cited N-algebraic transfer, so "modulo transfer" is correctly labelled.
- **CT(c)** is false generically (r18_gend §5). r17_gwordp labelled it "not automatic" and G-geo does not use it.

## 3. IF / SU / Trunk / Prop P (r17_gstruct)
- **SU, re-derived.**
  - Pump X ⇒⁺ αXβ m times. Each of the m B-copies independently takes one of two trees for the same z.
  - The result is one word of length O(m), with 2^m trees on a common skeleton, differing at B-nodes with equal spans.
  - Reachability transfers ambiguity upward.
  - Toy check (5): X → BX | c, B → b | D, D → b. CYK gives trees(b^m c) = 2^m. ✓
  - Corollary (a) is correct: Y ⇒⁺ αYβYγ puts Y on a side of its own loop, and the rest of the SCC is reachable from Y.
- **IF.** Distinct nodes with the same span are nested; ε-free plus cycle-free then forces them equal. ✓
- **Caveat on Cor (b).** As worded ("every lower block of every SCC that has a loop is unambiguous"), it is **false**
  for exit blocks.
  - Counterexample: X → aX | Z, Z → b | B, B → b. Here Z is below X's loop but not on a loop side. Each a^m b has 2
    trees, so the grammar is polynomially ambiguous.
  - The proof of (b) only covers the other children of rules that have a C-child. TR uses only that correct form.
  - Prop P item 4 is still fine, by a different route: an unambiguous X makes everything reachable from X unambiguous.
- **TR.** Trunk nodes inside an SCC form a path. Spans of the junctions determine the spines by (c) and the sides by
  SU. ✓

## 4. GE-Q (r18_gend)
- **LG(a), (b).**
  - Nonlinear SCC: Z ⇒* (σα′x′β′s)Z(tγ′τ), with x′ ∈ L(Z₂) arbitrarily long and a fixed companion. ✓
  - Left-finiteness is an SCC property (a cycle through Z′ transfers to every Z). ✓
  - So in Q(C), G_bad consists of left-finite linear SCCs and trivial nodes.
- **Step 1 (left-label growth < 2).**
  - A regular language over {a, b} with growth 2 has a trim-DFA SCC with every out-degree 2 (Perron row sums), so it
    contains u aᵐ v.
  - Re-routing the K-segment X → X′ through that path is a legal derivation, and W′ ∈ L ⊆ Q(C).
  - **Gap C4 (repairable):** "≤ n/8" is not the right control. Re-routing may *shrink* the old right parts, which can
    be Θ(n), so n′ is not ≥ n.
  - Fix: take m ≥ 4h + 4|u| + 2C + 2. The climb past C then happens by position 2h + 2|u| + C + 1 ≤ (|u| + m)/2 ≤ n′/2.
    Q(C) applies to W′ of any length. ✓
- **Step 2 (radius > ½ for complete left-sibling subtrees).** This is the key claim, re-derived. It holds under
  **per-word** polynomial ambiguity.
  - **λ > 0:**
    - The left labels have growth g_K < 2, by the Step 1 argument.
    - Cramér gives |S| ≥ λm/2 for all but e^{−cm} of the trees.
    - So #words ≤ m·2^m·(g_K/2)^{λm/2}, against ≥ c·2^m trees for a fixed exit.
    - Hence some single word has exponential ambiguity. ✓
  - **λ = 0 (left recursion):**
    - Pumping gives D ≤ 0 on every cycle. E_π D < 0 gives exponential ambiguity by LD.
    - So every cycle has D = 0, and fixed-exit paths have drift D(w) ± O(1).
  - **Gap C5 (repairable).** The injectivity "distinct token sequences ⇒ distinct words" holds only for a **fixed exit
    yield w**.
    - Two distinct K-paths from Z to the same exit state with the same yield, closed by a return path Q, give two
      pumping trees with the same interface, hence C_exp (IF). ✓
    - With the exit free, a word w·t_r⋯t₁ can have up to m + 1 trees, one per exit split. Trees/words ≥ √m is then
      consistent with polynomial ambiguity, and the √m contradiction disappears.
    - The report does say "for a fixed exit and connector", so the proof is right as written. It must, however, count
      the c·2^m trees for one exit yield. Simple pole: e^T(I − J(z))^{−1}e_exit·z^{|w|}. ✓
  - **Finite-token sanity check (6).** I sampled 4,825 sets of balanced tokens of length ≤ 6 with Kraft sum ≥ 1.
    **0** were uniquely decodable (Sardinas–Patterson), so all of them are C_exp. This agrees with the classical fact
    that a complete finite code contains a power of each letter.
- **Step 3.**
  - The left siblings along π_h tile [0, h) exactly.
  - There are ≤ 2c₁ factors from finitely many fixed languages, each counted ≤ c·g^j.
  - Bad words ≤ prefixes × 2^{n−h}, and rotation costs a factor n. With h = K log n the total is o(2ⁿ). ✓
- **Assembly.**
  - A word that is not bad-left or bad-right has a left-good node at p < h and a right-good node at q > n − h, possibly
    in different derivations.
  - FR-pos puts it in E_n(C + c₀, h), and T-tol gives density O(log n/√n).
  - Per-word vs total ambiguity: ambiguity is used only inside Step 2 (one word with 2^{Ω(m)} trees), never as a
    count-only sandwich.
- **Scope.** The result is for **Q(C), not G⁻**. T8_poly for G⁻ stays OPEN: the spanning residual R⁻, the
  light-U/heavy-V case, is untouched, and §4.2 is only a sketch.

## Summary
- All four candidates SURVIVE.
- Repairs to make in the write-up:
  - C4: in Step 1, pick m by position (m ≥ 4h + 4|u| + 2C + 2), not by "≤ n/8".
  - C5: in the λ = 0 case of Step 2, state the fixed-exit injectivity explicitly (via return path + IF).
  - r17_gstruct Cor (b): restrict to loop-side children.
- Upgrades to label "audited": FR, FR-pos, T-tol, SU/IF/TR, and GE-Q ⇒ "poly-ambiguous CFL ⊆ Q(C) is not
  rotation-dense".
