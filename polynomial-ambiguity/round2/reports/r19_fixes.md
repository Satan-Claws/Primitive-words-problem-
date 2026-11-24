# r19_fixes.md — R19: repairs to the T8_poly links (U2, U3, A2) and the combined statement (U4)

Status (honest):
- **U2 (r18_gend §4 G⁻ transfer, infinite labels): REPAIRED** [written proof, §1; unaudited]. Step 1's
  "complete DFA component" is replaced by two pieces:
  - pumping at **non-spanning** nodes, which forces the grammar property NC;
  - Lemma W, a word count for concatenations of light blocks under NC.
  The gain is **sub-exponential**: #words ≤ C·2^ℓ·exp(−c ℓ^{1/3}). It is not a growth bound g < 2. It is enough at
  h = log⁴n, but **no longer at r18's h = K log n**. A true growth < 2 is plausible (toy check (2) decays at rate
  ≈ 0.105/letter) but not proved.
- **U3 (LL one-sided remark): REPAIRED** [written proof, §2]. Pure-left T either has a cycle with D(s) ≥ 0, which
  makes it left-good via sⁱ, or satisfies NC, which puts it in the gend2/Lemma W count. LG(b) is no longer cited.
- **A2 (gend2 §0 for non-critical T): WRITTEN** [§3, Lemma SP]. A radius-½ side of **any** cycle reaches a critical
  **nonlinear** SCC. Otherwise the side has a simple pole, and pumping gives exponential ambiguity. Criticality of T is
  not used. This also justifies "left parts of a left-bad T are light or finite" for every T.
- **U4: combined statement written** [§4]. **T8_poly is CONDITIONAL on M1/M1′**, the spanning light SCC with a
  positive cycle, which is handled in `R2/r19_m1.md` (**pending**, not reviewed here). Every other row of the case
  table is closed, with the audit labels shown.
  - Note added at write-up time: REGISTRY now lists R19-M1 as "M1/M1′ CLOSED (written, unaudited)". It has not been
    checked against the (M1/M1′) hypothesis of §4.

Script: `scripts/r19_fixes_checks.py` → `scripts/r19_fixes_checks_out.txt` (~2 s).
- (1) Lemma SP toy: X → HX | a, H → aH | bH | a. trees/2^N grows like 1.5^N.
- (2) Lemma W toy: #U*_ℓ/2^ℓ decays from 0.375 to 0.083 for ℓ = 4…18.
- (3) ρ_R = 2cos(π/(2R+3)), re-checked for R ≤ 6.

Notation: as in r18_gend / r18_gend2. Steps are ±1, A(k) = P(k), B(k) = P(n) − P(n−k), and
G⁻ = {A(k) < B(k) for 1 ≤ k ≤ n/2}. G is reduced, ε-free and polynomially ambiguous (≤ n^κ trees per word), with
L(G) ⊆ G⁻. Put h := log⁴n and C_W := max_{j≤n/2} B_W(j) + h.

A π_h-node with span [a, b), a < h, is **spanning** if b > n/4 and **non-spanning** if b ≤ n/4. A maximal same-SCC
segment of π_h is cut at its first non-spanning node, so it splits into a spanning part and a non-spanning part. There
are then ≤ 2N_SCC parts, and the factor count c₁ of r18 at most doubles.

---

## 1. U2 — the G⁻ transfer of r18_gend §4 without finite labels

**Where finiteness was used.** In r18 GE-Q, Step 1 shows that the left-label language Lft_K is regular with
growth < 2, using the complete component of a DFA. In G⁻ the left siblings of a π_h-segment can be trees of infinite
light languages, or of K itself when K is light nonlinear. Then Lft_K is context-free, and there is no DFA to argue
with.

Counting **derivations** cannot replace it. Even under unambiguity the left-label derivations can outnumber the left
words exponentially. For example, X → aX₁b | aX₂c, X₁ → X, X₂ → X is unambiguous, yet the left word aᵐ has 2ᵐ
left-derivations. So ρ(M(½)) ≥ 1 for the naive left transfer matrix says nothing. The repair counts **words**.

### Lemma NS (positive cycles cannot occur at non-spanning nodes) [written proof]
**Statement.** Let K be an SCC (linear or not) that has a cycle Z ⇒⁺ sZt with D(s) ≥ 1. The left siblings may be any
G-trees. Then there is n₀(G) such that for n ≥ n₀ no W ∈ L_n with C_W ≤ √n·log n has a derivation containing a
K-node with span [a, b), a < h, b ≤ n/4.

**Proof.**
1. *Move the cycle to the node's label.* Let X be the node's label. Fix X ⇒* σZτ and Z ⇒* σ′Xτ′ through K, with
   shortest yields for the side nonterminals, and put c := |σσ′ττ′|. Then X ⇒* σ sᵐ σ′ X τ′ tᵐ τ for every m.
2. *Pump.* Graft this at the node:
   W′ = W[0, a) · σsᵐσ′ · W[a, b) · τ′tᵐτ · W[b, n) ∈ L.
   Here n′ ≥ n.
3. *Prefix side.* Let k₀ := a + |σsᵐσ′|. Then A_{W′}(k₀) = A_W(a) + D(σσ′) + m·D(s) ≥ −h − c + m.
4. *Suffix side.* Take m := C_W + c + 1 ≤ 2√n log n. Then k₀ ≤ h + c + m|s| ≤ n/2 for n ≥ n₀.
   - So k₀ ≤ n′/2.
   - Also k₀ ≤ n/2 ≤ n − b. All inserted material lies left of W[b, n), so the suffix of W′ of length k₀ equals that
     of W. Hence B_{W′}(k₀) = B_W(k₀) ≤ C_W − h.
5. *Contradiction.* Then A_{W′}(k₀) ≥ m − h − c > C_W − h ≥ B_{W′}(k₀), which contradicts W′ ∈ G⁻. ∎

**Consequence.** Every SCC with a non-spanning π_h-node, in a word counted here, satisfies **NC**: every cycle has
D(s) ≤ 0. This is a property of the grammar.

The pumping is legitimate here, and not in the spanning case, because both s and t are inserted left of b ≤ n/4.
This is the audit's U2 remark, made precise.

### Lemma PD (path drift) [written proof]
**Statement.** If K satisfies NC, then there is c_K such that every K-spine path Z ⇒* s Z′ t, with any side trees,
has D(s) ≤ c_K.

**Proof.** Close the path with a fixed path Z′ ⇒* s₀Zt₀ that uses shortest side yields. NC gives D(s) + D(s₀) ≤ 0,
so D(s) ≤ |s₀| ≤ c_K. ∎

### Lemma W (word count for light blocks under NC) [written proof]
**Statement.** Let 𝓛 be a set of words with the following property. Every s ∈ 𝓛 has a factorisation s = b₁⋯b_r
such that:
- (i) every b_i ∈ U, where |U ∩ Σʲ| ≤ C₁·z₁^{−j} for some z₁ > ½;
- (ii) D(b_{p+1}⋯b_q) ≤ c_K for all 0 ≤ p ≤ q ≤ r.

Then for every ℓ and every integer L ≥ 1,

  #(𝓛 ∩ Σ^ℓ) ≤ 2^ℓ·[(R+1)·cos(π/(2R+3))^ℓ + ℓ·C₂·(2z₁)^{−L}],  where R := 2L + c_K and C₂ := C₁/(1 − (2z₁)^{−1}).

Taking L = ⌈ℓ^{1/3}⌉ gives #(𝓛 ∩ Σ^ℓ) ≤ C·2^ℓ·exp(−c·ℓ^{1/3}), with c, C depending only on C₁, z₁, c_K.

**Proof.**
1. *Long blocks.* Suppose s has no factorisation with all blocks of length < L. Then it has a block b_i ∈ U of length
   j ≥ L. The number of such s is at most
   Σ_{start} Σ_{j≥L} C₁z₁^{−j}·2^{ℓ−j} ≤ ℓ·C₂·2^ℓ·(2z₁)^{−L}.
2. *Short blocks.* Otherwise, fix a factorisation with all blocks < L, and take i < j in [0, ℓ]. Let i lie in block p
   and j in block q.
   - The rise P(j) − P(i) is at most (rest of block p) + D(b_{p+1}⋯b_{q−1}) + (start of block q).
   - This is ≤ L + c_K + L = R, using (ii).
   - So the walk of s has every rise ≤ R. The words of length ℓ with this property number ≤ (R+1)·ρ_R^ℓ, with
     ρ_R = 2cos(π/(2R+3)). This is the transfer matrix on r = P − running min ∈ [0, R]: r18_gend2 §3, audited exact,
     re-checked by script (3).
3. *Choice of L.* Use 1 − cos x ≥ x²/4 for 0 ≤ x ≤ 1. With L = ℓ^{1/3}:
   - the first term is ≤ (R+1)·exp(−π²ℓ/(4(2R+3)²)) = exp(−Θ(ℓ^{1/3}));
   - the second term is ≤ ℓ·exp(−ℓ^{1/3}·log 2z₁). ∎

**Application to a π_h-segment of an SCC K.**
- The left label of the segment is b₁⋯b_r, where b_i is the yield of the left-sibling string α_i of step i.
- U is the finite union over rules of L_bad(α). Its word count is ≤ the G_bad-tree count, and this has radius > ½
  once every nonterminal in α is light. That holds by induction (below).
- (ii) is Lemma PD.
- The language "U-words" is context-free, so it only enters through its **radius**, as required.

### Induction order (repairs the Step 1 ↔ Step 2 dependency)
r18 Step 2, case λ > 0, uses "Lft(K) has growth g_K < 2, as in Step 1". Process the SCCs of G_bad bottom-up.
- **Hypothesis.** Every lower G_bad tree language has radius > ½.
- **For K.** All blocks of K are light, except for K-subtrees inside α when K is nonlinear.
- **Critical K.** Suppose K is critical, i.e. its tree radius is ½.
  - K is not nonlinear: a critical nonlinear K is left-good by LG(c) (caveat A1), so it is not in G_bad.
  - So K is linear, with all blocks light.
  - Step 2's replacement puts K-trees of length m ≤ n/4 inside [0, n/4]. Lemma NS, applied to these words, gives NC.
  - Lemma W replaces "g_K < 2":
    #words ≤ m·2^m·max_{j≥λm/2} C·exp(−c·j^{1/3}) = 2^m·exp(−Ω(m^{1/3})).
  - This is against ≥ c·2^m trees for a fixed exit (audit C5), so some word has ≥ exp(Ω(m^{1/3})) trees. That is
    **super-polynomial** ambiguity, a contradiction.
  - Step 2's λ = 0 branch is unchanged: it pumps t at b ≤ n/4 (non-spanning) and needs no labels.
- **Conclusion.** No G_bad SCC is critical. Trees ≤ n^κ·2ⁿ excludes radius < ½, so every G_bad tree language has
  radius > ½, and the induction closes. Nonlinear light K are now covered too, because their K-subtrees in α are
  light by this conclusion.

### Theorem GE⁻-NS (repaired r18 §4 "what transfers") [written proof; inputs: Lemma NS/PD/W, r18 Step 2 (+C5), LG(c)]
**Statement.** Let h = log⁴n. Count the words W ∈ L_n with C_W ≤ √n log n that have a derivation which is bad-left
and in which ≥ h/2 letters of [0, h) are left-sibling letters of **non-spanning** π_h-nodes. Their rotation image is
≤ 2ⁿ·exp(−c·log^{4/3}n) = o(2ⁿ).

**Proof.**
1. W[0, h) is the concatenation of ≤ 4c₁ factors: (L)-parts of non-spanning segments, (S)-factors, and spanning
   parts. The skeleton has ≤ (h+1)^{4c₁} choices.
2. The non-spanning factors have total length ≥ h/2, so one of them has length ℓ ≥ h/(8c₁).
   - If it is an (L)-part, its SCC satisfies NC by Lemma NS. Lemma W bounds it by C·2^ℓ·exp(−c·ℓ^{1/3}).
   - If it is an (S)-factor, its radius is > ½ by the induction, which gives C·z₁^{−ℓ}, better still.
3. Every other factor is bounded by 2^{length}.
4. Bad words number ≤ (#prefixes)·2^{n−h}, and rotation costs a factor n. So
   |Rot| ≤ n·(h+1)^{4c₁}·C·2ⁿ·exp(−c(log⁴n/8c₁)^{1/3}).
   The exponent is −Θ(log^{4/3}n), which beats every polynomial. ∎

**Remark (h).** With r18's h = K log n the gain would only be exp(−c(log n)^{1/3}), which is not enough. So T8_poly
must use h = log⁴n throughout. That choice is compatible with the rest of the chain:
- T-tol needs h log n = o(n);
- FR-pos needs C′ = O(log⁴n) = o(√n), as in the audit table.
The Q(C) theorem GE-Q is unaffected, since there all labels are finite and Step 1 stands.

---

## 2. U3 — Theorem LL's one-sided remark, without LG(b)

LL Remark 5 dismisses one-sided T by citing LG(b). LG(b) is the Q(C) statement: "pure-left ⇒ left-good with x = sⁱ".
In G⁻, x must be U-level, i.e. depth(x) bounded, and sⁱ is U-level only when D(s) ≥ 0.

**Proposition OS [written proof].** Let T be a linear SCC that is **pure-left**: every T-rule has an empty right
part. (Every rule lies on a cycle, so "all t = ε" forces this.) Suppose its π_h-part carries ≥ ℓ letters of [0, h).
Then either
- (a) every T-node is left-good, or
- (b) T satisfies NC, and its left label is counted by Lemma W.

In both cases these words fall into a row of §4 that is already closed. Criticality and the spanning condition are
**not** used.

**Proof.**
- (a) Suppose some cycle has D(s) ≥ 0. Move it to the node's label X as in Lemma NS: X ⇒* σsⁱσ′X. Pure-left means
  the right parts, and hence the companion, are ε.
  - depth(σsⁱσ′) ≤ |σ| + |s| + |σ′|, because each copy of s starts at a level ≥ the previous start.
  - Take i with n + c₀ ≤ |σsⁱσ′| ≤ n + c₀ + |s|. This is a U-level left insertion with companion v = ε. That is
    exactly the hypothesis of left-good (r18 §1, G⁻ case).
- (b) Otherwise every cycle has D(s) ≤ −1, so NC holds. The left parts of T are light or finite: a radius-½ left
  part would reach a critical nonlinear SCC by Lemma SP (§3), and then T is left-good by LG(c), giving case (a)'s
  conclusion.
  - So Lemma PD and Lemma W apply with U light.
  - The prefix count is r18_gend2's GE⁻-RH count, or Lemma W's sub-exponential form. Its proof uses only NC′ and
    light blocks, never RH and never the spanning condition. ∎

A pure-**right** T (all u = ε) contributes no letters to [0, h), so it never carries the ℓ letters. Mirrored, it is
pure-left for bad-right words.

**Edit to LL Remark 5.** Replace "This is not needed for R⁻: pure-left T is left-good (LG(b)) or carries no left
letters" with: "For R⁻, pure-left T are handled by r19_fixes Prop OS: either a cycle with D(s) ≥ 0 gives a U-level
sⁱ and the node is left-good, or NC holds and Lemma W / gend2 counts the prefix."

---

## 3. A2 — radius-½ sides of a cycle reach a critical nonlinear SCC (any T)

**Lemma SP (side pole) [written proof].** Let T be any SCC, and let H be a nonterminal occurring in a side (left or
right) of some cycle X ⇒⁺ αXβ of T. Suppose L(H)'s tree GF y_H has radius ½. Then the lowest radius-½ SCC C\*
reachable from H is **nonlinear**, so H ⇒* sYt with Y critical nonlinear.

**Proof.**
1. *Setting up C\*.* C\* exists and is non-trivial, as in THEOREM_T8 §3 steps 2–3 (B1). Its lower SCCs have radius
   > ½. Suppose C\* is linear.
2. *C\* is critical.* Write y = A + M(z)y. As in THEOREM_T8 §3 step 4, ρ(M(½)) ≥ 1.
   - ρ(M(½)) > 1 is impossible. Monotonicity would give ρ(M(z₀)) = 1 at some z₀ < ½, so the radius would be < ½.
     That contradicts #trees ≤ n^κ·2ⁿ.
   - So ρ(M(½)) = 1: C\* is critical, with light tokens.
3. *Pole-type growth.* Fix a state Z ∈ C\* and an exit. The first-return token law has mass exactly 1 (Schur
   complement; LL §0 argument) and finite mean (lightness). The renewal theorem then gives #{C\*-trees of length j}
   ≥ c·2ʲ for j in a progression j ≡ j₀ (mod d), j ≥ j₁.
   - Since H ⇒* s′Zt′, the same holds for H: a_j := [zʲ]y_H ≥ c·2ʲ on a progression (shift j₀).
4. *Pump the T-cycle.* Pump X ⇒⁺ αXβ r times inside a fixed context S ⇒* pXq and a fixed exit X ⇒* w.
   - Every side nonterminal except one H-occurrence per copy gets a shortest yield. Each H gets an independent tree.
   - Distinct choices give distinct trees.
   - For N in a suitable progression, with M := N − c₀ − r·c₁ (c₀, c₁ the fixed lengths):
     #trees of length N ≥ [z^M] y_H^r ≥ c^r·2^M·#{compositions of M into r parts ≡ j₀ mod d, ≥ j₁′}.
   - The composition count is ≥ binom((M − r·j₁′)/d + r − 1, r − 1) ≥ (1/(2εd))^{εN} for r = εN and ε small.
5. *Contradiction.* Words of length N number ≤ 2ᴺ, so some word has ≥ 2^{−c₀}·[c·2^{−c₁}/(2εd)]^{εN} trees. Choose
   ε < c·2^{−c₁}/(4d). The bracket is then > 2, so the ambiguity is exponential, contradicting polynomial ambiguity. ∎

Script (1) runs the toy X → HX | a with H → aH | bH | a: trees/2ᴺ ≈ 1.5ᴺ.

**Remark.** Heavy sides of Dyck type ([zʲ] ≍ 2ʲj^{−3/2}) do **not** contradict polynomial ambiguity. For them the
same composition bound loses a factor ε^{3r/2}. This is why only the **linear** C\* (simple pole, β = 0) is excluded.

**Corollaries.**
- **(i) gend2 §0 holds for every T, critical or not.** A radius-½ right part reaches a critical nonlinear SCC, so it
  is RH. gend2's claim "non-critical RH T covered" is now fully justified: Lemma RP and Prop NC never used ρ = 1.
- **(ii) Left parts of a left-bad T are light or finite, for every T.** A radius-½ left part reaches a critical
  nonlinear SCC, and then LG(c)'s general clause makes T left-good.
- **(iii) Every radius-½ nonlinear SCC is left-good (via (ii)).** A nonlinear T whose radius is ½ only because of
  heavy lower parts has a T-occurrence Z₂ in a cycle side (LG(a) shape), and Z₂ has radius ½. So it is left-good by
  (ii) and LG(c). The only left-bad nonlinear SCCs are therefore **light** ones (radius > ½), which is M1′'s scope.

---

## 4. The combined statement (U4)

**Theorem T8_poly (conditional on M1/M1′).** Let L ⊆ G⁻ be generated by a reduced, ε-free, polynomially ambiguous
CFG G. Assume **(M1/M1′)**, defined below. Then |Rot(L)_n| = o(2ⁿ). In particular L is not rotation-dense.

**(M1/M1′) hypothesis** (`R2/r19_m1.md`, **pending**). The following words have rotation image o(2ⁿ): the words with
a bad-left derivation in which ≥ h/(4N_SCC) letters of [0, h) are left letters of **spanning** nodes of a single SCC T,
where T is either
- **(M1)** linear, two-sided, non-critical, with light or finite sides, and with some cycle D(s) ≥ 1; or
- **(M1′)** nonlinear and light (radius > ½), with some cycle D(s) ≥ 1.

The same hypothesis is required for the mirror image (bad-right, with D(t) ≤ −1).

**Unconditional corollary [written].** The conclusion holds without (M1/M1′) for every such G in which every
**non-critical** SCC that is linear and two-sided with light/finite sides, or nonlinear with radius > ½, satisfies
NC (all cycles D(s) ≤ 0) and mirror-NC (all cycles D(t) ≥ 0). These are exactly the SCCs of rows 3g/3h and their
mirrors.

**Proof (case split).** Fix n, h = log⁴n and C_W as above. Every W ∈ L_n falls in one of the rows below, and each row
has rotation image o(2ⁿ). There are ≤ 2N_SCC + 2 rows per side, so the union is o(2ⁿ).

| # | case for W (one derivation fixed when "bad") | killed by | label |
|---|---|---|---|
| 0 | C_W > √n·log n | Hoeffding: n·2ⁿ·exp(−(log²n)(1 − o(1))/2) | audited (r18 §4 / audit_t8poly) |
| 1 | good-left and good-right (U-level left insertion at p < h, V-level right at q > n−h) | FR-pos G⁻ form + T-tol (C′ = O(log⁴n) = o(√n), h log n = o(n)) | FR-pos/T-tol audited; G⁻ form re-derived by audit_t8poly (U1) ✓ |
| 2 | bad-left, ≥ h/2 letters in **non-spanning** factors | **Thm GE⁻-NS (§1)** | **written, unaudited** (this note) |
| 3 | bad-left, ≥ h/2 letters in spanning parts ⇒ some spanning SCC T with ≥ h/(4N_SCC) letters (pigeonhole, product prefix bound) | rows 3a–3h according to T | — |
| 3a | T nonlinear with radius ½ (critical, or heavy below) | left-good: LG(c), Lemma SP (iii) — not bad-left | LG(c) written (A1); SP written |
| 3b | T linear, some left part of radius ½ | left-good: Lemma SP (ii) + LG(c) | written |
| 3c | T linear or nonlinear with **NC** (all cycles D(s) ≤ 0), light/finite left parts | NC′/Lemma W prefix count (gend2 §3 count) | gend2 count audited; Lemma W variant written |
| 3d | T linear, right side radius ½ (RH) | Prop NC ⇒ in 3c | gend2 SURVIVES (A1); non-critical T via Lemma SP (A2 closed) |
| 3e | T pure-left with a cycle D(s) ≥ 0 | left-good (Prop OS(a)) | written (§2) |
| 3f | T linear, critical, light, two-sided | does not exist (Thm LL) | LL audited SURVIVES (caveats: Lemma 1/IF, terse Step 3, periodicity) |
| 3g | **T linear, non-critical, two-sided, light/finite, some cycle D(s) ≥ 1 (M1)** | tilted tree count (audit sketch) | **OPEN — `r19_m1.md` pending** |
| 3h | **T nonlinear light, some cycle D(s) ≥ 1 (M1′)** | tilted count with J_θ(½) | **OPEN — `r19_m1.md` pending** |
| 4 | bad-right | mirror of rows 2–3 under φ∘R (G⁻ invariant; LG(c), RP, NC, NS, W, SP, OS all mirror) | as the mirrored row |

Note that pure-right T are covered without a separate row: they carry no letters in [0, h).

**Exhaustiveness of row 3.**
- If T is nonlinear: radius ½ is 3a. Radius > ½ is 3c when NC holds and 3h otherwise.
- If T is linear: a heavy left part is 3b. Otherwise:
  - NC holds: 3c.
  - NC fails and T is pure-left: 3e.
  - NC fails and the right side is heavy: impossible, since RH ⇒ NC (3d).
  - NC fails and the sides are light/finite and two-sided: critical gives 3f (vacuous), non-critical gives 3g.

**Summation.** |Rot(L)_n| ≤ |Rot(E_n)| + n·#{row 0} + n·Σ_{rows 2–4}#bad
≤ O(log⁴n/√n)·2ⁿ + o(2ⁿ) + 2ⁿ·n·(h+1)^{4c₁}·[exp(−c log^{4/3}n) + exp(−c log²n) + gain(M1)].

So T8_poly follows once r19_m1 supplies gain(M1) = exp(−ω(log n)) for prefixes of length h. The audit's tilted sketch
gives e^{−θh/c}, which is ample.

**Caveats carried by the combined statement.**
- **A1 (input).** V-level/U-level supply for critical nonlinear Y (LG(c) and its mirror) is a citation of SM/HL in
  unambiguous form, applied to the unambiguous Y-subgrammar (SU Cor (a)). It is not re-proved.
- **LL audit caveats 1–3.** These are inherited by row 3f.
- **§1 and §2–3 of this note are unaudited.** The step most worth an independent check is Lemma NS's choice
  m = C_W + c + 1 ≤ 2√n log n, together with "suffix untouched because k₀ ≤ n − b".
- **Gain.** Lemma W gives only exp(−cℓ^{1/3}). This forces h = log⁴n, and any later change to h must keep
  h^{1/3} ≫ log n.

## Status table
| item | label |
|---|---|
| Lemma NS: positive cycle ⇒ no non-spanning node (C_W ≤ √n log n) | written proof |
| Lemma PD: NC ⇒ path drift ≤ c_K | written proof |
| Lemma W: light blocks + NC ⇒ #words ≤ C·2^ℓ·e^{−cℓ^{1/3}} | written proof (exponential version open; toy decays exponentially) |
| Induction order Step 1 ↔ Step 2 (G⁻), incl. light nonlinear K | written proof |
| Thm GE⁻-NS (U2 repaired), needs h = log⁴n | written proof, unaudited |
| Prop OS (U3: LL one-sided remark without LG(b)) | written proof |
| Lemma SP (A2: radius-½ loop side ⇒ critical nonlinear below, any T) | written proof + toy check |
| Theorem T8_poly | **conditional on M1/M1′** (`r19_m1.md` pending); unconditional for NC/mirror-NC light SCCs |
