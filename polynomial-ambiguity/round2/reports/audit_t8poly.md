# audit_t8poly.md — gated audit of r18_gend2 and of the T8_poly assembly (G⁻)

Script: `scripts/audit_t8poly_checks.py` → `scripts/audit_t8poly_checks_out.txt` (~5 s). Steps ±1, A(k)=P(k),
B(k)=P(n)−P(n−k), G⁻ = {A(k) < B(k), 1 ≤ k ≤ n/2}. Theorem LL is audited separately; here it is taken as given.

## Verdicts
| candidate | verdict |
|---|---|
| r18_gend2: Lemma RP, Prop NC, Cor NC′, ρ_R count, Thm GE⁻-RH | **SURVIVES** (caveats A1–A3) |
| T8_poly assembly for poly-ambiguous rotation-dense L ⊆ G⁻ | **INCOMPLETE** — one uncovered configuration (M1), closable by a short tilted count that is not written; plus unaudited links (U1–U4) |

## 1. r18_gend2 — first-flaw search
**Lemma RP.** Re-derived. W′ = W[0,s) u_ρ W[s,e) α x β q is a legal yield (cycle at ν's label through the RH rule, x
in L(Y) under H ⇒* s_H Y t_H). n′ ≥ 2n + 3|u_ρ|, so every k′ ≤ e + |u_ρ| has k′ ≤ n′/2; and |x| ≥ n + 2|u_ρ| ≥ e + |u_ρ|,
so the suffix of length k′ stays inside q β x. With B_x(j) ≤ K (V-level = sx ≤ K, THEOREM_T8 §1.3), B_{W′}(k′) ≤
max_{j≤|q|}B_W(j) + |β| + K, and the shift D(u_ρ) gives the claim. ✓ Independent check (1): random W, u, α, β and
b-biased V-level x, 1,865 instances with W′ ∈ G⁻, 13,480 values of k, **0 violations**.

**Prop NC.** Pumping (s,t) m times directly below ν₀ keeps ν₀ a T-node with the same right context q and puts position
s₀+m|s| inside its span; RP's ceiling grows like log m, the left side like m·D(s). ✓ Constants depend on the state
only (finitely many cycles through the RH rule). ✓

**Cor NC′.** Cycle deletion removes contiguous chunks of the left-label word, each with D ≤ 0; residue ≤ N_T simple
steps + 2 partial blocks. ✓ Note NC′ uses only "all T-cycles have D(s) ≤ 0", not RH.

**Count.** ρ_R = 2cos(π/(2R+3)) exact for R ≤ 8; count from r=0 is ≤ (R+1)ρ_R^ℓ (max ratio 1.0, check (2)).
h/R² = log⁴n/O(log²n) = Ω(log²n). Long blocks: block languages are G_bad left-sibling yields, radius > ½ by r18_gend
Step 2. ✓

**Caveats.**
- A1 (input). V-level supply for the critical nonlinear Y below H. Mitigation found: Y lies on a side of its own loop,
  so by r17_gstruct SU Cor (a) (audited) L(Y) is generated **unambiguously**. Lemma L/SM/HL then apply to Y's
  sub-grammar in their audited unambiguous form. Still a citation, not re-proved here.
- A2 (§0 for non-critical T). "A radius-½ right part reaches a critical nonlinear SCC" is justified via Lemma ST(i)
  only for critical T. For non-critical T a loop side reaching a critical linear SCC has infinite mass at ½ and
  pumping the T-loop gives exponential ambiguity ([z^N]y^r with r = Θ(N)). True, but unwritten; gend2's claim
  "non-critical RH T covered" needs it.
- A3 (scope). gend2's Corollary "R⁻ = light/light only" is wrong as a statement about r18_gend's R⁻: the 4.1 list
  only treated **critical** T. See M1.

No fatal flaw in gend2.

## 2. Assembly — full case split
Fix h = log⁴n. For a word W, "good-left" = some derivation has a left-good node (U-level insertion, bounded companion)
with span start < h; mirror for good-right.

| case | killed by | status |
|---|---|---|
| good-left & good-right | FR-pos **G⁻ form** + T-tol (C′ = K + O(Δ_h) = O(log⁴n) = o(√n), h log n = o(n)) | FR-pos/T-tol audited; G⁻ form only sketched (U1, re-derived here ✓) |
| C_W = max_{j≤n/2}B(j)+h > √n log n | Hoeffding (×n rotation) | ✓ |
| bad-left, ≥ h/c letters of [0,h) in **non-spanning** factors | r18_gend §4 (Steps 1–2 with C_W) | written, **unaudited for G⁻** (U2) |
| spanning segment in heavy-left SCC (any right), incl. heavy/heavy | left-good by LG(c) general clause | ✓ (A1 input) |
| spanning critical nonlinear SCC | left-good, LG(c) | ✓ |
| spanning **critical** linear, light/finite-left, RH right | gend2 | SURVIVES |
| spanning critical linear, light/light two-sided | Thm LL (vacuous) | parallel audit |
| spanning one-sided pure-left T (all t = ε) | LL Remark cites LG(b), which is **Q-form only** | gap in citation; closes: a cycle with D(s) ≥ 0, t = ε gives U-level sⁱ ⇒ left-good; else all D(s) < 0 ⇒ NC′ ⇒ gend2 count (U3) |
| spanning **non-critical** linear RH | gend2 (no ρ = 1 used) | ✓ modulo A2 |
| spanning **non-critical** linear, light/light, with a positive cycle | **nothing written** | **M1 — uncovered** |
| spanning **light (non-critical) nonlinear** SCC | **nothing written** | **M1′ — uncovered** |
| right end (bad-right) | mirror of all rows; heavy-left/light-right at the right end = mirror of gend2 | ✓ (G⁻ is φ∘R-invariant; LG(c), RP, NC mirror) |
| multiple / stacked critical SCCs | ≤ N_SCC segments; product prefix bound + pigeonhole on h | ✓ (needs one combined statement, U4) |
| side branches with polynomial tails (CT) | bypassed: prefix-word count, heavy side branches are left-good nodes | bypass valid for non-spanning factors and for gend2's segments; **not** for M1 (prefix count has no gain there) |

**M1 (exact missing case).** Spanning, left-bad, **subcritical** linear T with light/finite sides on both sides,
left-label growth 2, and some cycle with D(s) > 0. Example (check (3)): X₀ → bXaa, X → aXaa | bXaa | a. L ⊆ G⁻
(verified r ≤ 8), unambiguous, X left-bad (companions (aa)ⁱ unbounded), not RH, not critical (M(½) = ¼), cycle
(a, aa) has D(s) = +1 so NC fails, and the length-h prefixes are all 2^{h−1} words starting with b: **no prefix-count
gain at all**. It is in r18_gend's R⁻ but in neither gend2 nor LL. M1′ is the nonlinear analogue.

**Suggested closure (auditor's sketch, not audited).** Count *trees*, not prefixes. Split a tree at the top and
bottom of the T-segment: outer context, segment, inner subtree. Outer and inner counts are ≤ poly(n)·2^len, by poly
ambiguity and a fixed filler. Subcritical T means ρ(M(½)) < 1 with finite M(½). The left material is light, so it has
exponential moments, and the left-tilted ρ(M_θ(½)) < 1 for small θ > 0. Segments with ≥ h/c left letters therefore
number ≤ C·2^b·e^{−θh/c}. In total there are ≤ poly(n)·2ⁿ·e^{−θ log⁴n / c} trees. Rotation costs a factor n, which is
o(2ⁿ). The same works for M1′ with J_θ(½). This needs to be written and audited.

**Unaudited links.**
- U1. FR-pos G⁻ form. It is only sketched in r17_gwordp; I re-derived it in one pass: left U-level x gives
  P(j) ≤ P(n) + C′ for j ≥ p, and right V-level y gives P(j) ≤ C′ for j ≤ q. ✓
- U2. r18_gend §4: the G⁻ transfer of Steps 1–2. audit_r18_poly audited the Q(C) case only. There is also a
  sub-gap: Step 1's "complete DFA component" argument needs **finite** labels. Non-spanning light-infinite labels
  need NC′-style pumping instead. That pumping is valid here, since both s and t stay left of centre.
- U3. LL Remark 5 (one-sided). It cites LG(b), which is Q-only. The repair is in the table above.
- U4. The combined theorem (non-spanning factors + gend2 + M1-count + LL + mirror, with h = log⁴n) is nowhere stated
  as one statement. r18_gend uses h = K log n, and gend2 correctly notes that log⁴n is compatible.

## Summary
- gend2 **SURVIVES**, with caveats A1–A3.
- T8_poly assembly **INCOMPLETE**. The missing pieces are:
  - M1/M1′: spanning non-critical light/light linear SCCs, and spanning light nonlinear SCCs. Likely closable by a
    tilted tree count; this is unwritten.
  - Unaudited links: U2 (the G⁻ transfer of r18_gend §4) and LL itself.
