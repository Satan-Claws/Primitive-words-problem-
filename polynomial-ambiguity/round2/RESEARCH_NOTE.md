# Polynomial ambiguity of the primitive words: research note on rounds 2–11

Consolidation of the round-2 campaign (`polynomial-ambiguity/round2/`, 2026-11-24, rounds 2–11). It is written to be read
without the reports. Every statement carries the status label it has in its source report, and no label has been upgraded.
Proofs given here are either short complete arguments copied from the reports or are explicitly marked **sketch**.

**Bottom line.** The problem is **not resolved** in either direction. After eleven rounds every live route reduces to one of
three precise open statements (§3). They are: (i) uniform certification of typical words (FOLD-COUNTER and its negative
counterpart, FSC rigidity); (ii) ¬P_cop; (iii) EQ-2q.

Path prefixes:
- `R2/` = `polynomial-ambiguity/round2/reports/`;
- `PA/` = `polynomial-ambiguity/claude_2026-11-18_to_11-19/reports/`;
- `R4/` = `infinite-ambiguity/claude_round4-5_2026-11-18/reports/`.

The campaign log is `polynomial-ambiguity/round2/REGISTRY.md`. The stop report for waves 1–5 (round 2 proper) and its addenda
for rounds 3–4 are in `polynomial-ambiguity/round2/STOP_REPORT.md`.

---

## 1. Problem, definitions, status labels, prior results

### 1.1 The problem

Σ = {a, b}. A word w ∈ Σ⁺ is *primitive* if w ≠ uᵏ for every u ∈ Σ⁺ and k ≥ 2. Q denotes the set of primitive words.
For a cycle-free CFG G, amb_G(w) is the number of derivation trees of w. G is *polynomially ambiguous* if
amb_G(w) ≤ C|w|ᵏ for all w, with C and k constants of G.

> **Problem.** Is there a cycle-free CFG G with L(G) = Q that is polynomially ambiguous?

The conjectured answer is no. By Wich's dichotomy [published: Wich, DLT 1999], for cycle-free G the function
A_G(n) = max_{|w| ≤ n} amb_G(w) is either 2^{Θ(n)} or O(n^d). So "no" is equivalent to: every cycle-free grammar for Q is
exponentially ambiguous. PCFL denotes the class of languages that have a polynomially ambiguous grammar. Wich (MFCS 2001)
[published] characterises it: L ∈ PCFL iff L = h(L′) for an unambiguous CFL L′ and a projection h that erases only
Parikh-bounded marker symbols. For a language L, write **P(L)** for "L ∈ PCFL".

Allowed exact transfers (prompt §5, §7): DFA products and CNF conversion never increase tree counts. Pullback along certain
codes and along the rotation construction (Theorem C_rot, §2.4) preserves tree counts exactly. Nothing else may be used to move
ambiguity bounds between languages.

### 1.2 Notation used throughout

- |w| = n; #a(w), #b(w) are the letter counts; ψ(w) = (#a w, #b w); **g(w) = gcd(#a w, #b w)**.
- **Cop** = {w : g(w) = 1}. By L1 (§2.4), Cop ⊆ Q.
- **P_cop** is the statement "some CFL L with Cop ⊆ L ⊆ Q is in PCFL".
- **row_N** = {w : #a(w) = N}. ℙ is the set of primes, 2ℙ = {2q : q ∈ ℙ}, and 2^ℕ is the set of powers of 2.
- For #a(w) = N ≥ 1, write w = b^s a b^{y_1} a ⋯ a b^{y_{N−1}} a b^t. The **cyclic gap sequence** is
  γ(w) = (y_1, …, y_{N−1}, s + t). It is a complete invariant of the conjugacy class.
- NonPow_p = {w : w ≠ u^p}; NonSq = NonPow_2. Not2P = {w : γ(w) is not cyclically 2-periodic}.
- **Rot(L)** is the closure of L under conjugation (rotation). L is **rotation-dense** if |Rot(L) ∩ Σⁿ| ≥ δ2ⁿ for some δ > 0 and
  all large n. Since a class has at most n elements, rotation-density forces |L ∩ Σⁿ| ≥ δ2ⁿ/n.
- The *density* of L is lim |L ∩ Σⁿ|/2ⁿ when it exists.
- **Fold quantities.** For 1 ≤ k ≤ n/2, **d_k(w) = #a(w[0,k)) − #a(w[n−k,n))**: the a-count of the length-k prefix minus that of
  the length-k suffix. The pair sequence is π_i = (w_i, w_{n−1−i}).
- **G⁻** = {w : d_k(w) < 0 for all 1 ≤ k ≤ n/2}. Equivalently, with the centred prefix walk P(j) = #a(w[1..j]) − j/2:
  w ∈ G⁻ ⟺ P(k) + P(n−k) < P(n) for all 1 ≤ k ≤ n/2 (`R2/r10_heavy.md` §1).
- **F_K** = {w : d_k(w) ≠ 0 for all k ∈ [⌈n/3⌉, ⌊n/2⌋]}.
  **F_δ**: the window is [⌈(1/2 − δ)n⌉, ⌊n/2⌋] ∪ {⌊p/2⌋·n/p : p ∈ ℙ, p | n, p ≤ 1/δ}.
- **T_w(i) = n·#a(w[0,i)) − i·#a(w)**, read cyclically: the drift-corrected walk.
- **Slice geometry** (prompt §4.3–4.4). For w ∈ (ab*)ⁿ, w = a b^{x_1} ⋯ a b^{x_n}, exp(w) = x ∈ ℕⁿ.
  - V_p ⊆ ℝⁿ is the set of shift-(n/p)-invariant vectors. W_n = Σ_{p|n} V_p.
  - For n = P_N² with P_N = p_1⋯p_N, U = ∩_k V_{p_k}. The subspaces E_k ⊆ ∩_{j≠k} V_{p_j} satisfy E_k ∩ V_{p_k} = 0.
  - S_N is the slice family near tω + δ with δ ∈ ⊕E_k. There, x is primitive iff every δ_k ≠ 0.
- **Off** = {w : x̂_w(1) ≠ 0}, where x is the b-indicator of w and x̂ its discrete Fourier transform. Equivalently Off = {Φ_n ∤ B_w}
  (`R2/r3_offw.md` §2).

### 1.3 Status labels

These are the labels of prompt §4, used verbatim:
- **[published]**;
- **[Lean-checked]**;
- **[audited report]**: written proof plus an independent red-team audit (the audit file is named);
- **[written proof]**: not audited;
- **[computational]**: finite computation, which is evidence and not proof;
- **[assessment]**: someone's analysis, not checked;
- **[conjecture]**.

Two further markers are used. **sketch** means the source report itself calls the argument a sketch. **OPEN** marks a statement
that is formulated precisely but unresolved. "Modulo X" means the proof cites X without re-proving it.

### 1.4 Prior results (before round 2)

1. **[Lean-checked; audited] No finitely ambiguous CFG generates Q** (`finitely-ambiguous/PROOF.md`,
   `finitely-ambiguous/lean/FiniteAmbiguity/Main.lean`). On R_m = a(ab⁺)^{m−1}a(ab⁺)^{m−1}, some word has ≥ ⌈m/2⌉ trees.
2. **[written proof] Theorem P** (`PA/POLY_FINAL.md` §1). Every cycle-free CFG G with L(G) = Q has
   A_G(L) = Ω(√(log L / log log L)). Its foundations were reconstructed in round 2 (`R2/recon.md`): Structure (c) and Lemma 3P are
   confirmed, and Lemma F is repaired (§6.1). Theorem P survives with m = 2p − 1.
3. **[written proof] Lemma 3P** (`PA/poly_P.md` §2, reconstructed in `R2/recon.md`). For a grammar G_n for Q ∩ (ab*)ⁿ with
   amb ≤ C|w|ᵏ:

   amb(w) = Σ_σ P_σ(exp(w) − c_σ).

   - σ ranges over ≤ exp(O(n)) skeletons, with ‖c_σ‖₁ ≤ nK.
   - P_σ is the vector partition function of a list V_σ of ring vectors. Each is supported on one block or on a pair of blocks,
     with ‖v‖₁ ≤ K, and K depends only on G.
   - The pairs of one skeleton are laminar, and the degree is d_σ ≤ k.
   - The pieces L_σ = c_σ + ℕV_σ cover exactly the primitive exponent vectors, and amb ≥ ply = #{σ : x ∈ L_σ}.
4. **[conjecture] Candidate S_N** (`PA/poly_T1.md` P4). On S_N the natural cover has ply ∏ d_k ≥ n^{N/2}. The negative programme
   (Lemma G* = TILE_k + G3**) asked that every valid laminar cover of S_N have a point of ply n^{ω(1)} at norm n^{o(N)}.
5. Other published facts used:
   - Petersen 1996: Q is not unambiguous [published; second-hand per `R2/r4_cite.md`].
   - Kászonyi–Katsura: Q ∩ (ab*)ⁿ is CF when n has ≤ 3 distinct primes (1997 Thm 1, VERIFIED-PRIMARY), or when Σ1/p < 4/5
     (1999, VERIFIED-REVIEW). These are per-n constructions with no grammar, no uniformity in n, and no ambiguity statement
     (`R2/r4_cite.md`).

---

## 2. Main results of rounds 2–11

### 2(a) The per-slice route through S_N is blocked (near U, audited)

**A1. Theorem A/B: TILE_k holds with ply 1.** [audited report: `R2/tile2.md` + `R2/audit_tile2.md`, SURVIVES with fix C1]
> Let μ satisfy fold μ = 0 with a fixed sign pattern. Let F_c be the non-crossing bichromatic trees that are dual-feasible for the
> transport cost c_ij = h(|y_i − y_j|), with h increasing and strictly concave, and **rooted at a positive vertex** (fix C1).
> (i) At every x at most one T ∈ F_c is valid. (ii) If no proper (cyclic) arc of supp μ is identically balanced, every generic x
> lies in exactly one validity cone K_T. With the lex rule on walls (η ∈ W), every point has ply exactly 1.

*Proof sketch.* Validity of T is positivity of the tree flows, which is complementary slackness for a transport LP. Strict
concavity makes the optimum unique, which gives (i). An identically balanced proper arc is the only way non-crossing components
can split, which gives (ii). The audit found that the x-level root condition sgn μ_root = sgn τ was missing (C1, §6.2).
Consequence: q_k = 1, so on S_N ply ≤ ply_VC. The arc condition for the actual facets is "Lemma C". For LAM facets Lemma C holds
for all k and N ≤ 45 [written proof + computational, `R2/lemmaC.md`].

**A2. Theorem BD: bounded-data pair facets near U.** [audited report: `R2/realise.md` part (1) + `R2/audit_realise.md`, SURVIVES near U]
> The pair facets μ_k = (1 − T^{n/p_k})ν_k, with one ±1 per fibre in nested windows, satisfy Lemma C for all N. Combined with A1
> they tile the near-U region with ring vectors of ℓ¹-norm ≤ 2 (K = 2 for every n), offsets ≤ 2n, unimodular bases and laminar
> pieces. Total ply ≤ n^{1+o(1)}.

Caveats from the audit:
- The ply bound uses the Littlewood–Offord / VC step, Lemma 4, which is a sketch.
- Coverage of ∏(E_k ∖ 0) needs windows of width p_k and N ≥ 4. The width-1 family for N = 3 does not cover.
- The scope is the near-U region R⁰ only.

Meaning: near U, no per-slice condition known to the programme (Lemma 3P data bounds, ply, laminarity) separates Q from a
polynomially ambiguous grammar on S_N.

**A3. Extensions and the mixed-type region.**
- **G1** [written proof + exhaustive check, `R2/global.md`]: multi-root slack-transport forests tile {x ≥ 0 : μ(x) ≥ 1} with ply 1,
  NC, unimodular and K = 2 globally, with no Lemma C needed. So the pair-facet family covers all primitive (U ⊕ ⊕E_k) ∩ ℕⁿ.
- **G2/G3** [written proof]: disjoint single-prime facets miss x = t·1 + 1_D + 1_T (D a 2-cycle, T a 3-cycle) for N ≥ 6. A
  matching piece covers it, so it is not a negative candidate.
- **G5** [written proof, `R2/gglob.md`]: at K = 2 the level-t lineality of a piece lies in span{e_p − e_q : pq ∈ M} for a single
  non-crossing matching M. So mixed-type certification is "∃M ∀k: d_M(y) ∉ d_M(V_k)".
- **Lemma I2** [audited report: `R2/r3_i2.md` + `R2/audit_r3_i2.md`]:
  > For every y ∉ ∪_k V_k there is S ⊆ ℤ_n with no two cyclically consecutive points and |S| ≤ 2N, containing a k-witness for
  > every k.

  With the explicit distribution 𝒟 (isolated adjacent Bernoulli(1/3) pairs) this gives G-glob′(i) with Pr ≥ (16/729)^N = n^{−o(1)}.
- **G-glob′(ii) per facet** [written proof + exact, `R2/r3_sep.md`]: with partial matchings (no completion), condition (H2) is
  automatic and ±1 facets suffice. O1⁺: a separating chord cannot be repaired by any finite M-laminar K = 2 family.
- **Lemma D1** [written proof, `R2/r3_depth.md`]:
  > Any exact facet-tuple family in which each facet touches ≤ s fibres has a point of norm ≤ (2N+1)n with ply ≥ (P/(2s))^N.

  I2 witnesses have s = 2, so **the I2 route to G-glob is dead as a construction**. The bound is paradigm-relative, and its
  adversary is pure ⊕E_k, so it is not a lower bound for Q.
- **OPEN (SPREAD-JOINT).** A poly-size family of facet tuples is needed that is spread (each facet touches ≥ P/N^{O(1)} fibres),
  has disjoint non-crossing witness chords, and covers every two-level point t·1 + sδ + η.

**A4. No other slice family helps.** [written proof + computational, `R2/newslice.md`]
DFA sub-slices are locally ℝ^J ∖ ∪_{p∈A(ω)} V_p. Cross-prime defects only reduce factor counts. Deep prime powers, lower strata
and fibre-restricted sub-slices are all S_N-type, with 0 W-balanced arcs and rule ply 1 checked up to n = 27000.

**A5. Explicit covers.**
- n = pq: Q ∩ (ab*)^{pq} has a laminar cover of ply ≤ n + φ(n) [written proof, `R2/construct.md` §2].
- n = 30: transfer atoms close the 60-vector fibre obstruction (Lemma FT) [written proof, `R2/construct2.md`]. All primitive
  W_30 ∩ ℕ^30 with ‖x‖₁ ≤ 10 is covered [computational].
- n = 36 (Lemma 36): E ∩ W_36 is covered by 72 chord-dominance systems, ply ≤ 2n + φ(n) = 84 [written proof + computational,
  exhaustive to ‖x‖₁ ≤ 16, `R2/construct36.md`]. The mechanism is multiplicative (≈ n^{N/2}) for N ≥ 3 [assessment].

**A6. Length side.**
- Lemma D [written proof, `R2/finv.md` §4]: asymptotic density ρ(ω) = Σ 1/idx ≥ q forces f ≥ q at norm poly(m, K, q, ‖ω‖)·h,
  where h is the facet height.
- CRT pieces [written proof, `R2/finv.md` §3] show that ray-asymptotic ply does not transfer to short witnesses.
- Prop BC [written proof, `R2/g3.md` §2] reduces G3** to TILE^ℤ plus per-piece data.

**Net for (a)** [assessment, Round 4 rationale]: per-slice geometry no longer supplies a negative mechanism near U. The campaign
therefore moved to uniformity across n, at the word and grammar level (§2(b)–(f)). SPREAD-JOINT was not closed, so "blocked"
means blocked near U and modulo SPREAD-JOINT off U.

### 2(b) Uniformity obstructions: what a single grammar cannot expose

All results in this subsection are **restricted-class results** (prompt §7). They constrain grammars that *expose* certificates as
marks, or that use regular sorters. None of them is a lower bound for Q.

**Theorem W** (two primes, one exposed mismatch pair each). [written proof, `R2/uniform.md` §2]
> Let p < q be primes, and let L contain w_m = a^{n−2}bb with n = pqm for infinitely many m. Then L has no (p, q)-witness-exposing
> grammar: no CFG over Σ × {0, 1, 2} whose words carry exactly one mismatch pair (i, i + n/p) marked 1 and one (j, j + n/q) marked 2,
> with L ⊆ π(L(G′)).

*Proof sketch.* In w_m the admissible marks force the three a-runs between marks to have lengths (n − n/p, n/p − n/q, n/q) − O(1),
all with positive slope in m. Intersecting with a regular shape gives a bounded CFL whose Parikh image would have to contain
infinitely many points on a 3-gap proportional ray. Ginsburg–Spanier stratification forbids this. All chord orders were checked to
be non-stratified [computational, `uniform_marked.py`].

**Theorem X** (exposed two-prime certificates). [written proof, `R2/r3_offw.md` §3]
> Let p ≠ q be primes, and G′ a CFG over Σ × {0,1} whose words have length n ∈ pqℕ and ≤ K marks. Suppose the marks contain
> distinct a, b, c with b ≡ a (mod n/p) and c ≡ b (mod n/q). This holds whenever the marks contain supp y for some
> y ∈ (V_p + V_q)^⊥ ∖ 0, hence for every y ∈ W_n^⊥ ∖ 0. Then L(G′) is finite.

It contains Theorem W and the rectangle case of Theorem R. Also, every y ∈ W_n^⊥ ∖ 0 has |supp y| ≥ 2^{ω(n)}, with equality for
Möbius cubes [written proof; MILP check].

**Theorem R** (≥ 3 marks at fixed fractions). [written proof, `R2/l6.md`]
> Let G′ be a CFG over Σ × {0,1} whose words have exactly k marks. Suppose the gaps g_0, …, g_k between them satisfy
> |g_t − γ_t n| ≤ C for fixed γ_t ≥ 0 and C. If at least 3 of the γ_t are positive, then L(G′) is finite.

*Proof sketch.* Map unmarked letters to c and marks to μ. The result is a bounded CFL in c*μc*⋯μc*, and Ginsburg–Spanier
stratification is incompatible with ≥ 3 proportionally growing gaps. Consequence: the rectangle covers of `R2/construct.md` are
inherently per-slice.

**Theorem R°** (modulo rotation). [written proof, `R2/r3_l6grammar.md` §2]
> Same as Theorem R with *cyclic* gaps: the wrap gap g_0 + g_k is treated as one gap. If ≥ 3 cyclic fractions are positive, L(G′)
> is finite.

This kills rotation-section and "cube witness at fold depth m" routes for L₆ = NonSq ∩ NonCube ∩ Σ^{6ℕ}.

**Theorem R′ / Cor R″** [written proof, `R2/thmR_unif.md`]: Theorem R is **not** a non-uniformity mechanism against all grammars for Q.
Fractional marked trees lie on 2-gap pump orbits, so a contradiction arises only for pump-closed families. S_N words are not
pump-closed.

**Theorem S** (L₆ is not "chord + regular"). [written proof, `R2/l6.md`]
> L₆ is not a finite union of languages NonSq ∩ R, NonCube ∩ R′ and R″, with R, R′, R″ regular.

The witness family is a^{L+D} b (a^L b)^5.

**Theorem V** (one varying prime). [written proof + computational, `R2/r4_pp.md` §3]
> Let G′ be a CFG over Σ × {0,1} such that every word has exactly two marks, at a mismatched pair, and the pair is a valid chord
> (span ≡ 0 mod n/p for some p | g) whenever g(w) is a prime power ≥ 2. Then only finitely many words a^p b^p (p prime) lie in
> π(L(G′)), at any ambiguity.

*Proof sketch.* Reduce to a semilinear set of tuples (x, y, z, t). Pick a ray containing infinitely many primes m (Dirichlet). On the
ray, prime powers m* = q^{φ(v_m)+1} also occur, and validity at primes and at prime powers forces incompatible span ratios.
Checked on 423 163 rays with 0 unresolved.

**Theorem T** (no regular sorter on rows 2q). [written proof + computational check of witnesses, `R2/r11_eq2q.md` §2]
(Not to be confused with the TILE_k theorem that `STOP_REPORT.md` also calls "Theorem T"; see §6.8.)
> Fix an odd q ≥ 3 and regular R_1, R_2, R_3. Let C_1 ⊇ P_q (q-th powers v^q with #a(v) = 2) and C_2 ⊇ Sq ∩ Not2P ∩ row_{2q}. Then
> L = (C_1 ∩ R_1) ∪ (C_2 ∩ R_2) ∪ R_3 does not satisfy L ∩ row_{2q} = Q ∩ row_{2q}.

*Proof (complete).* Let N be at least the number of DFA states and M = N!. In any w with all gaps ≥ N, each b-run of the accepting
run contains a loop b^t with t | M. So each R_i is *gap-saturated*: w ∈ R_i implies that every γ′ ≥ γ with γ′ ≡ γ (mod M)
componentwise is in R_i. Take:
- w with γ = (N, …, N, N + M), which is primitive;
- p = (a b^{N+M} a b^{N+2M})^q ∈ P_q;
- the square s with γ″_k = N + M·[k ∈ {q, 2q}], which lies in Not2P.

Then w ∈ R_3 gives p ∈ L; w ∈ C_1 ∩ R_1 gives p ∈ L; w ∈ C_2 ∩ R_2 gives s ∈ L. ∎

**Prop U** [written proof, `R2/r5_dense.md` §3]: certificates of the form "run ρ is longer than every run in S(ρ, w)", with |S|
bounded or S local, accept u^p. So sound unique-longest-run certificates must compare ρ with Θ(#runs) runs.

**Reading of (b)** [assessment, Round 4 synthesis]: every exposed or regular-sorted certificate for typical words, which have
several varying primes dividing g, is excluded. A uniform affirmative must hide its certificate.

### 2(c) Uniform constructions (affirmative side)

**C1. NonPow_p grammar G_p.** [written proof + exhaustive check, `R2/uniform.md` §1]
> For each prime p, NonPow_p has a single CFG G_p for all lengths, with
> amb_{G_p}(w) = #{i < (p−1)n/p : w[i] ≠ w[i + n/p]} if p | n, and 1 otherwise. So the ambiguity is exactly linear.

Rules: S → R_r with R_r → C^r | C^p R_r (for n ≢ 0 mod p); S → P[c,σ] M[p−2−c,τ] (σ ≠ τ);
P[c,σ] → C^{p−1} P[c,σ] C | C^c σ; M[d,τ] → C M[d,τ] C^{p−1} | τ C^d. The ratio counters place σ and τ exactly n/p apart.

**C2. Fold grammar G_fold.** [written proof + exhaustive n ≤ 15, `R2/r3_offw.md` §4]
> One CFG with no counting, with L(G_fold) ⊆ Off ⊆ Q and amb(w) ≤ |w| (observed maximum n − 1).

The certificate (m, +) uses the reflection R_m: k ↦ m − k. Split w = u·v at m. Every mirror pair of u is ≠ (a, b), every mirror pair
of v is ≠ (b, a), and some pair is strict. Then Σ_k x_k sin(2π(k − m/2)/n) > 0, so x̂(1) ≠ 0.
Coverage of Off is 100% for n ≤ 8 and n = 10, and 81.5% at n = 20, but it tends to 0 on random words [computational, §5].

**C3. Gadget library and Lemma S (r4).** [audited report for soundness: `R2/r4_core.md` + `R2/audit_r4.md`]
> **Lemma S (r4_core).** If w = u^p with p ≥ 2, then (i) every window-feature indicator x^φ is (n/p)-shift-invariant, so
> Σ_k x^φ_k ≡ 0 (mod p) and x̂^φ(1) = 0; (ii) if w is not unary, the cyclic run sequence is (r/p)-periodic, so α̂(1) = β̂(1) = 0.

This yields sound, uniform, O(n)-ambiguous gadgets:
- LIN: Parikh lines;
- FL: factor-count lines c_1 occ_f − c_2 occ_h = ±1;
- LF/PF: folds on factor indicators;
- RLF: fold on run lengths.

The audit confirmed soundness independently (8 714 non-primitive words with n ≤ 24, 0 accepted). The RLF wrap needs a canonical
split of the partner run; the naive split costs a factor ≤ n, still polynomial. Coverage: with G_fold, U_n = ∅ for n ≤ 19 and
21–23; the uncovered sets at n = 20, 24–28 have 40/48/400/780/1242/3248 words, all in Off [computational]. The covered fraction of
random words decays like n^{−1/2} [MC + sketch].

**C4. Theorem N.** [written proof + computational, |w| ≤ 15, `R2/r9_pcop.md` §2]
> Let N_a = {v^m : m ≥ 2, #a(v) = 1} and L_P = Σ⁺ ∖ ({b^m : m ≥ 2} ∪ N_a). There is an explicit cycle-free CFG G_P for L_P with
> amb(w) = #{i ≤ N−2 : y_i ≠ y_{i+1}} + [y_{N−1} ≠ s + t] ≤ max(1, #a(w) − 1). Moreover Q ⊆ L_P, and every w ∈ L_P ∖ Q is v^d with
> d ≥ 2 and #a(v) ≥ 2, so #a(w) is composite. Hence L_P ∩ row_p = Q ∩ row_p for every prime p.

*Proof (complete modulo the grammar).* For N ≥ 2, w ∈ N_a iff γ(w) is constant (Lemma 1). The grammar generates one witness of
non-constancy per parse: an internal y_i ≠ y_{i+1} (W1), or the wrap y_{N−1} ≠ s + t split into three disjoint cases (W2). The
non-primitive words not excluded have roots with ≥ 2 a's. ∎
- Two-letter version L_P2 = Σ⁺ ∖ (N_a ∪ N_b ∪ {a^m, b^m : m ≥ 2}): a PCFL, ambiguity ≤ |w| + O(1), and every extra word has #a and #b
  both composite [written proof + computational].
- Corollary N1: L_P is inherently ambiguous with linear ambiguity (by U′, §2(d)) [written proof].
- Generalisation L_M (fixed M): every extra word v^d has #a(v) ∤ M [sketch; set-level claims computational for M = 2, 3, 4, 6].

**C5. Theorem N2.** [written proof + computational, `R2/r10_2q.md` §2]
> There is an explicit PCFL L** with amb ≤ |w| such that (a) Cop ⊆ L**; (b) every w ∈ L** ∖ Q has #a(w), #b(w) ∉ ℙ ∪ 2ℙ ∪ 2^ℕ;
> (c) L** ∩ row_N ∩ {#b odd} = Q ∩ row_N ∩ {#b odd} for N ∈ 2ℙ.

Construction: split by parity region (#a mod 2, #b mod 2):
- oo: L_P2;
- eo: [contains bb] ∩ L₂, or [no bb] ∩ sw(L_P);
- oe: the swap of eo;
- ee: nothing.

Here L₂ = {#a = 2} ∪ {#a ≥ 4 even, γ not 2-periodic} has a grammar G₂ with amb ≤ N − 2. G₂ needs only one wrap comparison: for even
N, γ is 2-periodic iff y_i = y_{i+2} for all internal i and y_{N−2} = s + t.
*Key point.* On eo every root exponent is odd, so on row 2q only d = q (#a(root) = 2) survives.
Checked exhaustively for |w| ≤ 16, and on rows 4, 6, 10, 14 for |w| ≤ 20.

**C6. Partial and conditional constructions.**
- Lemma F interval fold, G⁻, Lemma SA: see §2(e).
- L₆ partial grammar C_k: sound, amb ≤ 7n/6 + 1, but misses a⁶(bᵏaᵏ)⁶ [written proof, `R2/l6.md`].
- L₆ has rational GF Σ(2^{6m} − 2^{3m} − 2^{2m} + 2^m)z^{6m}, so there is no analytic obstruction even to unambiguity
  [written proof, `R2/r3_l6grammar.md`].
- Theorem M (r3_l6grammar): fold pumps never reach cubes [written proof + exhaustive N ≤ 2].

### 2(d) Reductions

**D1. Prop H chain.** [audited report: `R2/r4_pp.md` + `R2/audit_r4.md`]
> Fix a prime p and h_p(a) = a^p, h_p(b) = b^p. If L is a CFL with ambiguity f and {w ∈ Q : g(w) = p} ∩ h_p(Σ*) ⊆ L ⊆ Q, then
> L′ = h_p^{−1}(L) ∪ {a, b} satisfies Cop ⊆ L′ ⊆ Q and amb_{L′}(u) ≤ f(p|u|) + 1.
> Hence P(Q) ⇒ P(Q_pp) ⇒ P(Q ∩ {g = p^k}) ⇒ P_cop, where Q_pp = {w ∈ Q : g(w) = 1 or a prime power}.

*Proof (complete).* Block lemma: for non-unary u, h_p(u) ∈ Q ⟺ u ∈ Q, and g(h_p(u)) = p·g(u). If p ∤ r = |v| for a period v of
h_p(u), every block boundary would join equal letters. Pullback along the uniform code h_p is a DFA product followed by block
decoding, so tree counts are preserved exactly. ∎
- The audit checked 6 240 random grammars with 0 tree-count mismatches.
- So **¬P_cop ⇒ ¬P(Q)**. Any proof of ¬P_cop must use the ambiguity bound, because pumping alone would show Q non-CF.
- **Cor U_p** [written proof, conditional on the unaudited Theorem U]: for each fixed p there is no unambiguous L with
  {w ∈ Q : g = p} ⊆ L ⊆ Q.
- Q_pp itself is not CF [written proof].

**D2. L1, L2, L3, T1.** [written proof, `R2/cyclic.md`]
- **L1** (active primes): w ∉ Q ⟺ w = v^p for some prime p | g(w). In particular Cop ⊆ Q.
- **L2**: a non-erasing morphism with Parikh matrix M multiplies g by a multiple; if det M = ±1, g is preserved.
- **L3**: on (ab*)ⁿ, g = gcd(n, Σx) is regular. On Π_d = {g = d}, w ∈ Q iff x ∉ V_p for every prime p | d.
- **T1**:
  > Let P_{≥2} say: some CFG G with L(G) ⊆ Q meets every primitive class with g ≥ 2 with class mass Σ_{r∈[w]} amb_G(r) ≤ C|w|ᵏ.
  > Then P_{≥2} ⟺ P(Q). The same holds with "g ≥ 2" replaced by "#a = #b".

  *Proof sketch.* Use C_rot below, then σ(x) = ab, σ(y) = aabb, which lands in balanced classes and is exact.
- **Theorem C_rot** (named "Theorem C" in `R2/cyclic.md`; renamed here, §6.8) [written proof + computational]: for G in CNF there is
  a cycle-free G′ with amb_{G′}(w) = Σ_{j<|w|} amb_G(rot_j w).

**D3. P_cop and Theorem U.** [written proof, not audited, `R2/pcop.md`]
- P1: Cop is not CF.
- P2: a semilinear S with ψ(Cop) ⊆ S ⊆ ψ(Q) misses only finitely many points, finitely many lines through 0, and finitely many
  sets qℤ².
- **Theorem U.**
  > No unambiguous CFL L satisfies Cop ⊆ L ⊆ Q. More precisely, for every unambiguous CF L ⊆ Q and every large prime p, L misses
  > some w with #a w = p and gcd(p, #b w) = 1.

  *Proof sketch.* G = 1/(1−x−y) − F_L is algebraic. All row series g_p have singularities in a fixed finite set S. But the support of
  row p lies in pℕ with infinitely many nonzero terms and radius 1, which forces p singularities on the unit circle.
- **U′** (`R2/r9_pcop.md` §1): the proof uses only Cop ⊆ L and L ∩ row_p ⊆ Q for infinitely many primes p.
- P4: P(Q) ⇒ P_cop holds (D1). Whether P_cop ⇒ P(Q) is OPEN. The union route is circular (T1).

**D4. Self-similarity and Lemma RG.** [written proof, `R2/r9_selfsim.md`]
- A1: P(L_k) ⇒ P(Q) for all k ≤ ∞, in particular P(𝒜 ∩ Q) ⇒ P(Q), where 𝒜 = (D_b a)⁺ (§2(e)).
- A2: P(Q) ⇒ P(L_k) for every finite k. So P(L_k) ⟺ P(Q); the converse for k = ∞ is OPEN.
- **Lemma RG**:
  > A renormalisation inequality amb(n) ≥ C·amb(n^α)^s excludes polynomial ambiguity iff sα > 1 (or sα = 1 with C ≥ n^δ).

  The block self-similarity gives s = 1 and α = ½, which is vacuous. The invariant certificate lands in Q ∩ (b*a)⁺, which is the
  full problem via the code {ba, bba}.

**D5. U1–U3 (r7, the length coupling).** [audited report: `R2/r7_uncouple.md` + `R2/audit_r7.md`, SURVIVES]
(Distinct from the uniformity conditions U1–U3 of `R2/realise.md`; see §6.8.)
Let 𝒜 = (D_b a)⁺ = {w : every nonempty suffix has more a's than b's}; the report calls it P.
- **U1** [written proof + exhaustive n ≤ 24]:
  > D_b·𝒜 = 𝒜, so PS ∩ NonPrim = {u^p : u ∈ 𝒜, p ≥ 2}. Dropping the length coupling leaves exactly the original problem.
- **U2** [written proof + exhaustive n ≤ 16]:
  > L_A = 𝒜 ∩ {h ≤ 0 on [0, ⌈n/2⌉]}; L_B = {H ≥ 1, h ≤ 0 on [0, ⌈n/2⌉]} ⊆ Q; Rot L_A = Rot L_B.

  L_B is not CF (pumping sketch).
- **U3** [written proof]:
  > On 𝒜, w ↦ (D_1, …, D_H) is a bijection to sequences over the infinite alphabet D_b. It commutes with powers and with the H
  > rotations inside 𝒜, so 𝒜 ∩ Q = primitive block sequences.

  A finite-alphabet lift reduces length n to length H ≈ √n with no base case (circular, [assessment]).

**D6. Exchange blindness.** [written proof, `R2/r3_nonunif.md`; `R2/r5_generic.md`]
- Lemma FE0: forbidden exchange across slices ⟺ L(G) ⊆ Q.
- Prop 1: one-level exchange data has cover multiplicity ≤ |V|L² for every CFG for Q. So any lower bound using only
  exchange/interchange data would prove Q ∉ CFL.
- H* collapses: interchange-family soundness is FE0. Wich's normal form bounds neither branching (Strahler ~ log₄ n for an
  unambiguous G_D) nor rates.

### 2(e) Density results

**E1. Prop P** (Parikh-closed certificates). [written proof, `R2/r5_generic.md` §3]
> If L ⊆ Q is CF and Parikh-closed, then |L ∩ Σⁿ| ≤ c_L √(2/(πn)) 2ⁿ.

*Proof (complete).* Every off-axis point of ψ(L) has gcd 1. A linear component with two independent periods hits a point
≡ 0 mod p for a prime p ∤ det(v_1, v_2), which has gcd ≥ p. So every component lies on a line, which meets {x + y = n} at most
once. ∎ The K-window analogue is a sketch.

**E2. Theorem P_K.** [written proof, local CLT cited, `R2/r5_dense.md` §2]
> Let occ(w) be the cyclic K-window count vector. Any CF L ⊆ {w : gcd(occ(w)) = 1} has |L ∩ Σⁿ| = O(2ⁿ n^{−1/2}).

Corollary: every LIN/FL gadget and the Bézout split (Lemma B: g = 1 ⟺ some cyclic factor has det(ψx, ψw) = ±1) have density
O(n^{−1/2}). A dense certificate must be positional.

**E3. Lemma F (interval fold).** [written proof + exhaustive n ≤ 22, `R2/r5_dense.md` §1]
> F_K ⊆ Q, and F_δ ⊆ Q.

*Proof (complete).* If w = u^p with m = n/p, put j = ⌊p/2⌋. Then j/p ∈ [1/3, 1/2], so k = jm ∈ K_n, and prefix_k = u^j = suffix_k
gives d_k = 0. ∎
- Since d_k changes by ≤ 1 per step, "≠ 0 on the window" means a constant sign, so each word has a unique certificate.
- Density of F_K → (2/π) arcsin √(2/3) ≈ 0.608, and F_δ → 1 − O(√δ) [MC to n = 16384 + Brownian heuristic].
- F_K is the fold of a deterministic one-counter language, recognisable unambiguously by a TAG/LIG. Its CF status is OPEN.
- (r5 §1) {xy : |x| = |y|, #a(x) = #a(y)} is not CF [written proof].

**E4. Lemma M (r6_miss, windows).** [written proof + exact search, `R2/r6_miss.md` §1]
> For K ⊆ [1, n/2], F_K = {w : d_k ≠ 0 ∀k ∈ K} ⊆ Q_n iff for every prime p | n, K contains a multiple of n/p.

*Proof (⇒).* If K misses (n/p)ℤ, then w = (a b^{m−1})^p (m = n/p) has d_k = 1 for all k ∈ K. ∎
So [1/3, 1/2] is the unique interval window sound for all n. Residue-dependent windows give densities 0.69–0.76.

**E5. Lemma A (argmax rotation).** [written proof + exhaustive n ≤ 18, `R2/r6_miss.md` §1]
> Let v be the rotation of w starting at an argmax r of T_w. Then d_k(v) = T(r+k) + T(r−k) − 2T(r) ≤ 0. If the argmax is unique
> mod n, then v ∈ G⁻. Since G⁻ ⊆ F_K ⊆ Q, Rot(G⁻) ⊇ {unique argmax} ⊇ Cop.

The miss rate of Rot(G⁻) is ≤ P(tie) ≈ 0.43/√n [MC to n = 7680]. The tie family lies in {g ≥ 2}.
Related results in `R2/r6_miss.md` [written proof]:
- Lemma A′: Rot(F_K)-misses have g ≥ 2 and tied argmax/argmin.
- Lemma R_rot (rotation rigidity, named "Lemma R" in the report): Rot(F_max) = Q_n at prime-power n.
- Exhaustively for n ≤ 30, every primitive word is certified by Rot(F_K), the feature folds or the r4 library [computational].

**E6. Prop K** (regular fold conditions are sparse). [written proof + 2977/2977 random DFAs fooled, `R2/r6_build.md` §1]
> Let D be a DFA over the pair alphabet Π = Σ² with finite centre information. If fold(D) ⊆ Q, then
> |fold(D) ∩ Σⁿ| ≤ 2ⁿ(1 − 4^{−ℓ})^{⌊n/2ℓ⌋} for some ℓ = ℓ(D).

*Proof sketch.* Fix z₀ whose image lies in the kernel K of the transition monoid. If y with φ(y) ∈ K were accepted, let e = g^j be
the idempotent power of g = φ(yδȳ). Then u^{2j+1} has pair sequence (yδȳ)^j y with image e·φ(y) = φ(y), so it is accepted but
not primitive. Hence accepted words avoid z₀. ∎
Fold certificates therefore need unbounded spine memory.

**E7. Lemma SA** (G⁻ reduces to one length coupling). [written proof + exhaustive n ≤ 18, `R2/r6_build.md` §2]
> L_A = {x·y : x is a b-first Dyck word, every nonempty suffix of y has more a's than b's, |x| ≥ |y|} ⊆ G⁻ ⊆ Q.

- Rot(L_A ∪ swap L_A) has density ≈ 0.62–0.67 [MC, n ≤ 1024].
- Dropping |x| ≥ |y| is unsound: baa·baa.
- Prop N: L_A is not CF [written proof; slice description partly computational].

**E8. Prop B (UMR).** [written proof + computational, `R2/r5_generic.md` §4]
UMR (unique longest b-run) ⊆ Q is a disjoint union of ≤ n² boxes per n, with density ≈ 0.36 [MC]. Its CF status is OPEN
[conjecture: not CF].

**E9. G⁻ threshold.** |G⁻_n| = (1 + o(1)) 2ⁿ/√(2πn), and |G⁻_n| = C(n−1, n/2) for even n
[DP exact to N = 2000 + standard asymptotics, `R2/r8_propS.md` §0; closed form confirmed in `R2/audit_r7.md`]. So a
rotation-dense L ⊆ G⁻ must contain a ≍ n^{−1/2} fraction of G⁻.

### 2(f) Negative tools and their limits

**F1. Q0: Lemma Q as stated is false.** [audited report: `R2/r7_lemmaQ.md` + `R2/audit_r7.md`]
The r6 Lemma Q asked: does a CF L ⊆ G⁻_{t,h} have density ≤ c·min(1, h/√n)^{1+η}? The quotient P^{−1}G⁻S^{−1} is not a function
of (t, h). With P = b and S = b^r a^{m+1}, every P x S ∈ G⁻, so the density is 1 at h = 1.

**F2. Lemma R_rect** (centre rectangles; named "Lemma R" in r7). [audited report, modulo KMT + Prékopa (cited)]
> If X, Y ⊆ Σ^N and X·c·Y ⊆ G⁻, then |X||Y| ≤ C (log N)² 4^N / N.

This is exactly the rotation threshold, so rectangles alone give nothing.

**F3. Prop S** (fixed spine). [audited report, modulo non-strongly-connected N-algebraic residue-class asymptotics (cited loosely)]
> Let G be unambiguous with L(G) ⊆ G⁻, and fix a centre spine s (recording child indices). Then
> |{w ∈ L_n : centre spine s}| ≤ C_s 2ⁿ n^{−3/2} for n ≥ n_0(s).

**F4. Theorem C_circ** (circularity; named "Theorem C" in `R2/r8_propS.md`). [written proof]
> For every unambiguous G and every position a: Σ_s |X_{s,a}|·|Y_{s,n−1−a}| = |L_n|.

*Proof.* Each word has one tree, and that tree has one spine to position a. ∎
Consequences:
- Prop S never uses L ⊆ G⁻; it holds for Σ*. So it is a count-level fact (§6.4).
- Every uniform per-spine bound (gap G1) reduces to the tautology |L_n| ≤ C|L_n|.
- G2 (word distinctness) fails: S → bAaBa, A → aA | ε, B → aB | ε has amb(b a^{n−1}) = n − 2 inside G⁻.
- Positive by-product: anchored rectangles satisfy ≲ 4^N N^{−4/3} via a cone of angle 3π/4 [cone-exit cited + DP; optimality over g
  is a conjecture].

**F5. Heavy-block reductions (unambiguous T8).** Write T8_unamb: every unambiguous CFL L ⊆ G⁻ has |L_n| < δ2ⁿ/n eventually.
- **Thm M (r9)** [written proof + cited N-algebraic asymptotics, `R2/r9_packing.md`]:
  > rotation-dense ⇒ μ(L) = Σ_n |L_n|2^{−n} = ∞; for unambiguous L, T8 ⟺ μ(L) < ∞, since there is no exponent α = −1.
- **Lemma F_loc (r9)** [written proof modulo Drmota–Lalley–Woods]: divergence sits in a linear SCC C whose context matrix has
  ρ(M(½)) = 1.
- **Lemma Rn** [written proof modulo the renewal theorem]: if every lower block in C has finite mean, then
  limsup |L_n|/2ⁿ > 0, which contradicts L ⊆ G⁻.
- **Cor H**: a counterexample needs a heavy-tailed, full-entropy lower block B (for example |B_ℓ| ≍ 2^ℓ ℓ^{−3/2}) feeding a
  critical linear SCC, with α ∈ (−1, −½] [proof (structure) + heuristic].
- **Ambiguity-collapse example** [written proof]: A → EA | AE | bAa | ε, L = bAa. The context measure is infinite, but the word set
  is the negative excursions, of finite measure.

**F6. No-gos 1–3.**
- **No-go 1** [written proof, `R2/r10_heavy.md` §3]: for a Dyck-oriented giant block x (D(x) = 0, P_x ≤ 0), the centre-region
  constraint reduces to P(|α|) < D(β), uniformly in the offset. So offset randomisation cannot violate G⁻.
- **No-go 2** [written proof + exhaustive check, §4]: 𝒫 = {(E, ε)} ∪ {(b, Eᵏa)} is critical, heavy-tailed and injective on two tapes,
  with a strictly negative outer walk. All 45 tested (p, w, q) are ambiguous through centre-word recurrence, and none violates G⁻.
- **No-go 3** [written proof + check n ≤ 16, `R2/r11_rigid.md` §1]: G⁻ ∩ {even n} is itself an injective, critical,
  heavy-tailed pair model (zipped lazy walk; tokens 0-steps, −1 steps and lazy negative excursions; Σπ = ½ + ¼ + ¼ = 1). So the
  abstract pair statement "critical + heavy-tailed + all in G⁻ ⇒ ambiguous" is **false**.
- **Lemma Fac** [written proof]: full entropy ⇒ every fixed w occurs ≥ εℓ times in almost all block words.
- **Centre-count bound** [written proof + check n ≤ 21]: mult(W) ≤ Σ_c N(c). Centre shifts give ≤ n + 1 parses per (context, exit),
  so a superpolynomial mechanism would have to be two-tape re-tokenisation.

**F7. Lemma S (r11, row 2q).** [written proof + computational, rows 4, 6, 10, 14, |w| ≤ 20, `R2/r11_eq2q.md` §1]
(Not to be confused with Lemma S of r4_core, §2(c) C3.)
> For q an odd prime: Q ∩ row_{2q} = ({D ≠ 0} ∩ Not2P) ⊔ ({D = 0} ∩ NonSq), intersected with row_{2q}. For q = 2:
> Q ∩ row_4 = Not2P ∩ row_4.

Here D(w) = #(b's in odd gaps) − #(b's in even gaps) (Lemma D of r10: squares have D = 0; P_q words have D = ±q(x − y) ≠ 0).
*Proof.* On row 2q a non-primitive word is a square or in P_q; combine with Lemma D. ∎

**F8. The EQ-2q pumping attempt** (`R2/r11_eq2q.md` §3, [written analysis]). It fails at three points:
- P1: the pump partner may carry a's;
- P2: a pure-b partner at gap j ≢ i (mod q) is harmless;
- P3: laminarity allows only O(1) square-neutral pumps per tree [written proof], but a correct grammar needs none.

No step uses ambiguity, so a successful version would prove Q ∉ CFL.

**F9. FOLD-COUNTER negative tools** [`R2/r6_nofold.md`]:
- Lemma L: an edit of size r moves every d_k by ≤ r [written proof].
- Lemma M_up (named "Lemma M" in r6_nofold): G⁻ is an up-set under b-insert left, a-insert right and outward flips
  [written proof + exhaustive n ≤ 14].
- N1 (bounded pumps), N2 (macroscopic pumps, ≈ 0.9 survive, MC) and N3 (interchange, sketch) cannot refute any CF L ⊆ G⁻.

---

## 3. The three remaining cores

Each core is a precise open statement. The notation is that of §1.2.

### 3(i) Uniform certification of typical words

**Why typical words.** Theorems P_K and Prop P cap every count-based CF certificate at density O(n^{−1/2}). The gadget library
covers a fraction ≈ n^{−1/2} of random words. Theorems W, X, R, R°, V and T forbid exposed or regular-sorted certificates. Typical
words have g ≥ 2 with several varying primes. By T1, these classes carry the whole problem.

**Open statement (affirmative form): FOLD-COUNTER.**
> **FOLD-COUNTER** [OPEN]. Is there a CFL L ⊆ F_δ (for some δ), of positive density, with polynomial ambiguity?

The sharpened version uses G⁻:
> **ROT-FOLD-BALLOT** [OPEN]. Is there a polynomially ambiguous CFL L ⊆ G⁻ that is rotation-dense?

Equivalently, by Lemma SA and U2: can a polynomially ambiguous CFG realise the single length coupling |x| ≥ |y| between a
b-first Dyck prefix and an a-heavy suffix on a rotation-dense set? Prop K shows finite-state memory is not enough. U1 shows the
uncoupled version carries no information.

**Open statement (negative form): T8 and FSC rigidity.**
> **T8** [OPEN]. No polynomially ambiguous CFL L ⊆ G⁻ is rotation-dense; that is, |L ∩ Σⁿ| = o(2ⁿ/n).

For unambiguous L, T8 ⟺ T8_μ (Σ_n |L_n|2^{−n} < ∞), by Thm M. By Cor H, T8_unamb follows from:
> **Heavy-block lemma** [OPEN]. No critical linear SCC C with a heavy-tailed lower block B can keep all of its renewal words
> p·(u-blocks)·w·(v-blocks)·q inside G⁻.

No-go 3 shows that the abstract pair-model version is false, so the correct target uses CF shape:
> **FSC rigidity** [OPEN, `R2/r11_rigid.md` §1]. Let 𝒫 be a pair model from a finite linear SCC with independent one-tape lower
> blocks (finite-state coupling). Suppose it is critical and has a heavy one-tape block B (|B_ℓ| ≍ 2^ℓ ℓ^{−3/2}). If
> {pUwVq} ⊆ G⁻, then the map (pair sequences) ↦ words is not injective.

The polynomial lift additionally needs N(c) ≥ n^{ω(1)} for some split (two-tape re-tokenisation). Centre shifts provably give only
n + 1 (§2(f) F6).

**How (i) would bear on the problem.**
- Affirmative FOLD-COUNTER / ROT-FOLD-BALLOT gives a poly-ambiguous CFL Rot(L) ⊆ Q of positive density, using C_rot.
  This is DENSE-SOUND. It would refute the heuristic that generic words are the hard core [assessment, Round 5–6 syntheses].
  It would **not** by itself give P(Q). The tie family 𝒯 ⊆ {g ≥ 2} remains, with density Θ(n^{−1/2}), and by T1 gcd ≥ 2 classes
  carry the full problem.
- ¬DENSE-SOUND (no poly-ambiguous CFL L ⊆ Q of positive density) would imply ¬P(Q), since Q itself has density 1.
- T8 would kill only the fold route, not the affirmative in general [assessment, Round 7 synthesis].

### 3(ii) ¬P_cop

> **¬P_cop** [OPEN]. No CFL L with Cop ⊆ L ⊆ Q has a polynomially ambiguous grammar.

**Effect.** By Prop H (audited), ¬P_cop ⇒ ¬P(Q). It is the weakest-looking statement known to give the negative resolution.
Theorem U is its unambiguous analogue [written proof, unaudited].

**Limits (model-theoretic, proved).**
- Theorem N: L_P2 is a PCFL with Cop ⊆ L_P2, sound on all words with #a or #b prime. So no argument whose hypotheses are only
  "PCFL + Cop ⊆ L + L ∩ {#a or #b prime} ⊆ Q" can prove ¬P_cop. This covers marker patterns, roots-of-unity evaluation,
  singularity analysis of rows, and inclusion–exclusion.
- Theorem N2 extends this to rows in ℙ ∪ 2ℙ ∪ 2^ℕ (in either letter), refuting the r9 §5 conjecture (§6.5).
- L_M [sketch]: the deficits used must come from roots v with #a(v) ∤ M, for every fixed M.
- U* [written proof]: no algebraic series with nonnegative coefficients vanishes exactly on coprime classes and has infinite
  support with radius ≥ 1 on infinitely many prime rows, for any language.

**Requirement R** (`R2/r9_pcop.md` §5 + `R2/r10_2q.md` §2). A proof of ¬P_cop must use L ⊆ Q on powers v^d whose #a and #b lie
outside ℙ ∪ 2ℙ ∪ 2^ℕ in both letters, and whose roots have unboundedly divisible a-counts. The first rows still open are 4q, q²,
pq, …. On such words, membership in Q is a statement about the global period of an unboundedly long gap sequence. So
**core (ii) contains core (i)** [assessment; the model statements are proved].

### 3(iii) EQ-2q

> **EQ-2q** [OPEN]. Is there a PCFL L with L ∩ row_{2q} = Q ∩ row_{2q} for every prime q?
> **Conjecture** [conjecture, `R2/r10_2q.md` §3]: no.

**Effect.** If L = Q, equality holds on every row. So ¬EQ-2q ⇒ ¬P(Q). Unlike the containment form, no known model kills a row-2q
argument for ¬P(Q). EQ-2q is a sub-problem of ¬P(Q), **not** of ¬P_cop.

**Reduction** (Lemma S, r11). On row 2q the target is
({D ≠ 0} ∩ Not2P) ⊔ ({D = 0} ∩ NonSq). Equivalently, beyond the band {#b even, 0 < |D| < #a}, which is an unambiguous one-counter
CFL, it is H₀ = {D = 0} ∩ NonSq and H₊ = {|D| ∈ #a·ℕ⁺} ∩ Not2P on even #b. The sorter D is a one-counter quantity; each piece
crosses it with an arch certificate.

**Known obstacles.**
- Theorem T: no gap-saturated (in particular no regular) sorter works, on any single row.
- r10 §3 items 1–3:
  - {a^x b^y c^{x+y} : x ≠ y} is not CF [proof];
  - {u c v : |u| = |v|, #a = #b} restricted to a slice is not CF [proof];
  - among index-mod-k b-weightings, only multiples of D vanish on all squares [sketch].
- For fixed q, Q ∩ row_{2q} is CF. The difficulty is uniformity in q. This rests on a KK-type citation that is unverified
  (prompt §6).

**Exact gap.** There is no lemma turning "the sorter must be non-saturated" (Theorem T) into a lower bound on amb(w). Pumping and
interchange (P1–P3) never use ambiguity.

### 3.4 Logical map

```
¬P_cop ──(Prop H, audited)──► ¬P(Q) ◄──(trivial)── ¬EQ-2q
   │                             ▲
   └─ contains (i) [assessment]  └──(trivial)── ¬DENSE-SOUND
T8 (no poly-amb rotation-dense L ⊆ G⁻)  ⇒  only the fold route dies
FOLD-COUNTER yes  ⇒  DENSE-SOUND  ⇒  (not P(Q) by itself: tie family ⊆ {g ≥ 2} remains)
T8_unamb ⟸ heavy-block lemma ⟸ FSC rigidity (unambiguous case)
```

---

## 4. Blocked routes (one-line reasons)

| route | reason | source |
|---|---|---|
| TILE_k with superpolynomial ply on S_N | transport rule gives ply exactly 1 [audited] | `R2/tile2.md`, `R2/audit_tile2.md` |
| Per-slice data bounds near U on S_N | pair facets: K = 2, offsets ≤ 2n, unimodular [audited] | `R2/realise.md`, `R2/audit_realise.md` |
| I2-witness facets for G-glob | Lemma D1: s = 2 fibres forces ply n^{N/2} | `R2/r3_depth.md` |
| Other slice families (DFA sub-slices, deep powers, strata) | all reduce to S_N product geometry | `R2/newslice.md` |
| KKM / Sperner / Lebesgue covering for TILE_k | bound closure multiplicity; half-open cones have ply 1 | `R2/tile.md` §2 |
| Ray-asymptotic ply ⇒ near ply | false (CRT pieces) | `R2/finv.md` §3 |
| Ply-set arguments for G3** over abstract covers | Stanley refinement puts 2^ρ-pieces in every ply-set | `R2/g3.md` §3 |
| "All ply ≥ 3 points at norm 2^{Ω(n)}" on S_N | Cor F′ gives ply p at n·exp(O(p² log pK)) | `R2/g3.md` §4 |
| Multi-split inside/outside linkage | both branches collapse to §6 routes (Lemmas B, T, M of newmech) | `R2/newmech.md` |
| 1:1 cycle-lemma replacement at gcd ≥ 2 | exact self-reduction; ratio reappears one level down | `R2/cyclic.md` §3 |
| Exposed one-witness-per-prime grammars | Theorems W, X | `R2/uniform.md`, `R2/r3_offw.md` |
| Exposed ≥ 3 fractional marks (also modulo rotation) | Theorems R, R° | `R2/l6.md`, `R2/r3_l6grammar.md` |
| Theorem R as a non-uniformity mechanism vs all G | collapses to pumping (R′) | `R2/thmR_unif.md` |
| Forbidden exchange / U2 across slices | equals soundness; ambiguity-blind (FE0, Prop 1) | `R2/r3_nonunif.md` |
| H* (Wich structure ⇒ bounded linear invariants) | branching and rates unbounded | `R2/r5_generic.md` |
| Exposed chord for a varying prime | Theorem V | `R2/r4_pp.md` |
| Prime-power sandwiches isolate the varying prime | each contains P_cop (Prop H) | `R2/r4_pp.md` |
| Count / Parikh / window-count certificates | density O(n^{−1/2}) (Prop P, Theorem P_K) | `R2/r5_generic.md`, `R2/r5_dense.md` |
| Finite libraries of local gadgets | coverage ≍ n^{−1/2} on random words | `R2/r4_core.md` |
| Regular fold conditions | Prop K: e^{−Ω(n)} density | `R2/r6_build.md` |
| Uncoupled split languages | U1: D_b·𝒜 = 𝒜, closed under powers | `R2/r7_uncouple.md` |
| Rotation normal forms to remove the coupling | N(u^p) is always a power (U3) | `R2/r7_uncouple.md` |
| Lemma Q (density in G⁻_{t,h}) | false as stated (Q0) | `R2/r7_lemmaQ.md` |
| Prop S + G1 + G2 for T8 | circular (Theorem C_circ) | `R2/r8_propS.md` |
| Offset randomisation of a giant block | No-go 1 | `R2/r10_heavy.md` |
| Outer walk / two-tape injectivity alone | No-go 2; abstract pair statement false (No-go 3) | `R2/r10_heavy.md`, `R2/r11_rigid.md` |
| Centre-shift ambiguity for poly lift | ≤ n + 1 parses per (context, exit) | `R2/r11_rigid.md` §3 |
| Self-similar amplification | exact transfers; Lemma RG needs sα > 1, structure gives s = 1, α = ½ | `R2/r9_selfsim.md` |
| Theorem-U-type row arguments for ¬P_cop | Theorem N (prime rows), N2 (rows ℙ ∪ 2ℙ ∪ 2^ℕ) | `R2/r9_pcop.md`, `R2/r10_2q.md` |
| Exact algebraic series vanishing on coprime classes | U*: does not exist for any language | `R2/r9_pcop.md` |
| Regular sorter for EQ-2q | Theorem T | `R2/r11_eq2q.md` |
| b-pumping for ¬EQ-2q | P1–P3; never uses ambiguity (would prove Q ∉ CFL) | `R2/r11_eq2q.md` §3 |
| Test grammars walk / builder3 | neither generates Q | `R2/testgram.md` |

---

## 5. Computational data

All entries are [computational] unless marked. "MC" means Monte Carlo; "exh" means exhaustive.

### 5.1 Coverage of Q by the uniform gadget library (`R2/r4_core.md`, K = 3)

Uncovered sets U_n after LIN + G_fold + FL + LF + PF + RLF (exhaustive):

| n | ≤ 19 | 20 | 21–23 | 24 | 25 | 26 | 27 | 28 |
|---|---|---|---|---|---|---|---|---|
| \|U_n\| | 0 | 40 | 0 | 48 | 400 | 780 | 1242 | 3248 |
| classes | 0 | 1 | 0 | 1 | 7 | 10 | 17 | 40 |

All U_n ⊆ Off (x̂(1) ≠ 0). Random-word coverage (MC), cumulative library:

| n | 32 | 64 | 128 | 256 | 1024 | 4096 | 16384 | 65536 |
|---|---|---|---|---|---|---|---|---|
| S0 (LIN + FOLD) | .56 | .013 | .010 | 0 | | | | |
| S4 (all) | 1 | 1 | .97 | .87 | | | | |
| LIN ∪ FL | | | | .84 | .56 | .34 | .20 | .095 |

### 5.2 Coverage by G_fold of Off (`R2/r3_offw.md`)

| n | ≤ 8, 10 | 20 | 64 | ≥ 128 |
|---|---|---|---|---|
| fraction of Off covered | 1.0 | .815 | ≈ .012 (random words) | 0 (random words) |

|Q_n ∖ Off_n| for 2 ≤ n ≤ 20 (exh): 24 at n = 12, 432 at n = 18, 120 at n = 20, and 0 otherwise.

### 5.3 Fold-certificate densities

| language | density / miss rate | source |
|---|---|---|
| F_K | .570 (n = 8), .613 (22, exh); .620 (1024), .603 ± .008 (16384, MC); limit (2/π)arcsin√(2/3) ≈ .608 [BM heuristic] | `R2/r5_dense.md` |
| F_{0.1} | .727 (8), .674 (22), .714 (1024), .702 (16384) | `R2/r5_dense.md` |
| F_{0.02} | .849 (64), .870 (1024), .875 (16384) | `R2/r5_dense.md` |
| residue-dependent windows | .69–.76 | `R2/r6_miss.md` |
| Rot(F_K) without features | misses 1200, 2392, 432, 5040, 31080 words at n = 24, 26, 27, 28, 30 (exh) | `R2/r6_miss.md` |
| Rot(F_K) ∪ features ∪ r4 library | misses 0 for n ≤ 30 (exh) | `R2/r6_miss.md` |
| Rot(G⁻) | miss ≤ P(tie) ≈ 0.43/√n (e.g. .0048 at n = 7680, MC) | `R2/r6_miss.md` |
| Rot(L_A ∪ swap L_A) | ≈ .62 (n = 64), .67 (256), .62 (1024) (MC); r7 reports misses ≈ .35–.39 | `R2/r6_build.md`, `R2/r7_uncouple.md` |
| Rot(Ch) | misses ≈ 0.2/√n | `R2/r7_uncouple.md` |
| UMR | ≈ 0.36 (MC), also on {p \| g} | `R2/r5_generic.md` |
| L_1, L_2, L_3 (truncation certificates) | L_1 miss ≍ n^{−1/2}; L_2 ≈ 10× less; L_3 ≈ 0 at n = 4096 (MC) | `R2/r9_selfsim.md` |

### 5.4 G⁻ and the heavy-block search

| quantity | value | source |
|---|---|---|
| \|G⁻_n\|·√(2πn)/2ⁿ | → 1 (DP to N = 2000; 0.9975 at n = 100 via C(n−1, n/2)) | `R2/r8_propS.md` |
| P·√N for the fold ballot | 0.2821 = 1/(2√π), N = 125 … 2000 | `R2/r8_propS.md` |
| partial measure Σ_{n≤2000} \|G⁻_n\|2^{−n} | 17.35 (grows like √(2n/π)) | `R2/r9_packing.md` |
| E = bDa: \|E_n\|·n/2ⁿ at n = 20, 60, 200, 2000 | .0927, .0522, .0283, .0089; G⁻: 1.76, 3.08, 5.64, 17.8 | `R2/r9_packing.md` |
| best unambiguous L ⊆ G⁻ in 240k random small grammars | Catalan (42/132 at n = 12/14), α = −3/2 | `R2/r9_packing.md` |
| No-go 2 model, ambiguous words | 2, 20, 125 at n = 15, 17, 19; no G⁻ violation to N = 20 | `R2/r10_heavy.md` |
| No-go 3 model | equals G⁻_n for even n ≤ 16 (1, 3, 10, 35, 126, 462, 1716, 6435), multiplicity 1 | `R2/r11_rigid.md` |
| centre-count model (bb, aab, aa) | max multiplicity 1, 1, 2, 2, 3, 3 at n = 11 … 21 | `R2/r11_rigid.md` |
| anchored rectangles (DP) | per-side exponents −.660, −.663, −.665 (m = 200, 400, 800); product −1.329 (prediction −4/3) | `R2/r8_propS.md` |
| Lemma R_rect DP | fitted exponent −0.999 at λ = 0 | `R2/r7_lemmaQ.md` |

### 5.5 Rows and grammars

| check | scope | result | source |
|---|---|---|---|
| G_P (Theorem N) | all 65 534 words, \|w\| ≤ 15 | language, Q ⊆ L_P, composite rows, amb ≤ max(1, N−1): 0 failures | `R2/r9_pcop.md` |
| L** (Theorem N2) | exh \|w\| ≤ 16; rows 4, 6, 10, 14 with \|w\| ≤ 20 | all claims hold | `R2/r10_2q.md` |
| Lemma D (r10) | rows 6, 10, 14, \|w\| ≤ 20 | 0 failures | `R2/r10_2q.md` |
| Lemma S (r11) | rows 4, 6, 10, 14, \|w\| ≤ 20 (20 349 / 116 280 / 352 716 / 54 264 words) | 0 failures | `R2/r11_eq2q.md` |
| Prop K | 3000 random DFAs (2–8 states) | 2977/2977 fooled by u^{2j+1}, length ≤ 115 | `R2/r6_build.md` |
| Lemma I2 | n = 36 exh 2-residue binary 24 120 + 22k random; n = 900: 635 | 0 failures (audit) | `R2/audit_r3_i2.md` |
| Lemma 36 | ‖x‖₁ ≤ 16, 4.6M points | 0 uncovered | `R2/construct36.md` |
| W_30 cover | ‖x‖₁ ≤ 10, 22 620 points | all covered (8 need transfer atoms) | `R2/construct2.md` |
| newslice rule ply | n ≤ 27000 | 0 W-balanced arcs, ply 1 | `R2/newslice.md` |
| Lemma C (LAM facets) | N ≤ 45 | holds | `R2/lemmaC.md` |
| walk.md grammar | n = 33 | A(4m+1) ≥ Catalan, 19 006 | `R2/testgram.md` |
| builder3 𝒰 | n ≤ 25 | sound n ≤ 22, complete n ≤ 25, first miss n = 26 | `R2/testgram.md` |

---

## 6. Errata and corrections made during the campaign

### 6.1 Lemma F (face restriction) repair (`R2/recon.md` §4)
The PA Lemma F claimed that face restriction gives a valid cover of NE_r "with the same K", including ‖c_σ‖₁ ≤ n_r K with
n_r = 2(r+1). Only ‖c_σ‖₁ ≤ 2mK (the original n = 2m) follows. A toy grammar (S → aU, U → BUA | a, …) puts Θ(n) b's into one block.
Repaired Lemma F: a valid cover with ‖v‖₁ ≤ K, r_σ ≤ 2r + k and ‖c_σ‖₁ ≤ 2mK. Cor F′: ply ≥ p at norm 2m + m·exp(O(p² log pK)).
Theorem P is intact with m = 2p − 1. Separately, the S3D refinement to d_σ = 0 keeps ply but loses the offset bound.

### 6.2 Audit C1: root condition in TILE_k (`R2/audit_tile2.md`)
`R2/tile2.md` rooted every tree at v₀ = supp[0] and imposed only non-root conditions. When μ_{v₀} < 0, every tree is invalid on
R_k(u), so coverage is 0, not 1. Example: N = 2, k = 1, ν = [−30, 24, −3, −17, 44, −44, −1, 50, 39, 25, 26, −19] gives
μ_{v₀} = −60. **Fix**: cut the circle before a positive vertex. Lemma C must then hold for cyclic arcs, which was checked for
N = 2, 3 (exact) and N = 4 (one ν). The audit also noted that "written proof N ≤ 4" was mislabelled: Lemma C there is computational.
The audit of I2 (`R2/audit_r3_i2.md`) raised a separate caveat: the gglob "factor C per halving" accounting gives superpolynomial
ply. `R2/r3_depth.md` showed this is the wrong accounting (ply = #{σ : x ∈ R_σ}), and then killed the I2 route by Lemma D1 anyway.

### 6.3 Q0: Lemma Q false as stated (`R2/r7_lemmaQ.md`, audited in `R2/audit_r7.md`)
The r6 target "CF L ⊆ G⁻_{t,h} has density ≤ c·min(1, h/√n)^{1+η}" (`R2/r6_nofold.md`) is false: the quotient depends on the
paired window of the context, not only on (t, h). Density 1 is attained at h = 1. The correct object is the centre-spine rectangle.

### 6.4 Prop S circularity (`R2/r8_propS.md` Theorem C_circ)
`R2/r7_lemmaQ.md` asserted that Prop S is "not a §6 count-only route", because it uses set-level uncoupled closure inside G⁻.
That is **wrong**: the identity Σ_s |X_{s,a}||Y_{s,n−1−a}| = |L_n| holds for every unambiguous grammar, so Prop S holds for Σ* and
never uses G⁻. Uniformity over spines (G1) is a tautology, and G2 fails. Prop S stays true (audit) but is not a route to T8.
The audit's caveat about non-strongly-connected asymptotics affects Prop S step 2 only, not Theorem C_circ.

### 6.5 r9 conjecture refuted by Theorem N2 (`R2/r10_2q.md`)
`R2/r9_pcop.md` §5 conjectured that no PCFL L ⊇ Cop has L ∩ row_{2q} ⊆ Q for all primes q. Theorem N2 constructs one, L**.
So row-2q containment arguments are dead for ¬P_cop. The equality form EQ-2q was split off; it is a sub-problem of ¬P(Q).

### 6.6 devil.md attribution (`R2/r4_cite.md` §1)
`context-free/reports/devil.md` §4 is substantively right, but:
- the Σ1/p < 4/5 theorem is **Kászonyi–Katsura 1999** (Publ. Math. Debrecen 54 Suppl.), not "Kászonyi 2010", which only quotes it;
- "≤ 3 prime powers" means ≤ 3 **distinct primes** with arbitrary exponents.

The n = 6 case is attested by three author self-citations, but the FCT'93 primary text is unseen. The Dömösi–Ito book chapter
contents were not read, so any "book proves Q ∩ L CF for every bounded/slender L" claim is unverified.

### 6.7 Smaller corrections
- `R2/r7_uncouple.md` Verdict item 1 writes "D_b·P⁺ = P"; the audit (`R2/audit_r7.md`) identifies this as a typo for D_b·P = P.
  The U2(iv) and one-vs-each non-CF claims are pumping sketches.
- `R2/audit_realise.md`: the nesting inequality holds for N = 4..12, including N = 5, which `R2/realise.md` omitted. It fails at
  N = 3. The coverage probability bound improves from 1/(4p_k) to 1/(2p_k).
- `R2/audit_r4.md`: RLF wrap needs a canonical split of the partner run. The naive split gives ≤ n× trees, which is still
  polynomial.
- `R2/audit_r7.md`: spines must record child indices, otherwise X_s is not a product. Prop S step 2 cites residue-class asymptotics
  for non-strongly-connected N-algebraic systems loosely.

### 6.8 Naming collisions across reports (renamed in this note)

| name in reports | meanings | name used here |
|---|---|---|
| Theorem T | TILE_k ply 1 (`STOP_REPORT.md` §1); no regular sorter (`R2/r11_eq2q.md`) | "Theorem A/B" for TILE_k; "Theorem T" for the sorter |
| Theorem C | rotation closure (`R2/cyclic.md`); circularity (`R2/r8_propS.md`) | C_rot; C_circ |
| Lemma S | gadget soundness (`R2/r4_core.md`); row-2q decomposition (`R2/r11_eq2q.md`) | Lemma S (r4_core); Lemma S (r11) |
| Lemma M | ambiguity skeleton (`R2/newmech.md`); windows (`R2/r6_miss.md`); G⁻ up-set (`R2/r6_nofold.md`) | Lemma M (newmech); Lemma M (windows); Lemma M_up |
| Lemma R | rotation rigidity (`R2/r6_miss.md`); centre rectangles (`R2/r7_lemmaQ.md`) | Lemma R_rot; Lemma R_rect |
| Lemma F | PA face restriction; interval fold (`R2/r5_dense.md`); fibre lemma (`R2/l6.md`); divergence location (`R2/r9_packing.md`) | Lemma F (PA); Lemma F; Lemma F (l6); Lemma F_loc |
| Lemma D | density transfer (`R2/finv.md`); single defect (`R2/r3_nonunif.md`); one-counter D (`R2/r10_2q.md`) | named with file |
| Theorem M | fold pumps (`R2/r3_l6grammar.md`); measure form (`R2/r9_packing.md`) | Theorem M (r3_l6grammar); Thm M (r9) |
| U1–U3 | uniformity conditions (`R2/realise.md`); coupling theorems (`R2/r7_uncouple.md`) | U1–U3 in §2(d) D5 are r7's |
| Lemma A | one-witness-per-prime failure (`PA/poly_A2.md`); argmax rotation (`R2/r6_miss.md`) | Lemma A = argmax rotation |

---

## 7. File index

- Syntheses: `polynomial-ambiguity/round2/REGISTRY.md` (waves 1–5 and rounds 3–11); `polynomial-ambiguity/round2/STOP_REPORT.md`.
- Problem statement and labels: `polynomial-ambiguity/round2/prompt.md`.
- Audits: `R2/audit_tile2.md`, `R2/audit_realise.md`, `R2/audit_r3_i2.md`, `R2/audit_r4.md`, `R2/audit_r7.md`.
- Reports by subsection:
  - §2(a): `tile.md`, `tile2.md`, `lemmaC.md`, `realise.md`, `global.md`, `gglob.md`, `gglob_i.md`, `gglob_ii.md`, `r3_i2.md`,
    `r3_sep.md`, `r3_depth.md`, `newslice.md`, `construct.md`, `construct2.md`, `construct36.md`, `g3.md`, `finv.md`, `recon.md`;
  - §2(b): `uniform.md`, `r3_offw.md`, `l6.md`, `r3_l6grammar.md`, `thmR_unif.md`, `r4_pp.md`, `r11_eq2q.md`;
  - §2(c): `uniform.md`, `r3_offw.md`, `r4_core.md`, `r9_pcop.md`, `r10_2q.md`;
  - §2(d): `r4_pp.md`, `cyclic.md`, `pcop.md`, `r9_selfsim.md`, `r7_uncouple.md`, `r3_nonunif.md`, `r5_generic.md`, `newmech.md`;
  - §2(e): `r5_generic.md`, `r5_dense.md`, `r6_miss.md`, `r6_build.md`, `r8_propS.md`;
  - §2(f): `r6_nofold.md`, `r7_lemmaQ.md`, `r8_propS.md`, `r9_packing.md`, `r10_heavy.md`, `r11_rigid.md`, `r11_eq2q.md`;
  - other: `testgram.md`, `r4_cite.md`.
- Scripts: `polynomial-ambiguity/round2/scripts/`.
