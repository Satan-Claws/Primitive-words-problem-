# Round 2 registry: polynomial ambiguity of Q

Task: `polynomial-ambiguity/round2/prompt.md`. Started 2026-11-24 00:11 UTC.
Prefixes: `PA/` = `polynomial-ambiguity/claude_2026-11-18_to_11-19/reports/`,
`R4/` = `infinite-ambiguity/claude_round4-5_2026-11-18/reports/`, `R2/` = `polynomial-ambiguity/round2/reports/`.
Status labels: [published] [Lean-checked] [audited report] [written proof] [computational] [assessment] [conjecture].
Agents: append at most a few lines to the section that fits. Do not rewrite other lines.

## Approach families

| family | mechanism | status | owner / file |
|---|---|---|---|
| TILE_k (ply of tree-validity fans on S_N) | ply / covering | ply 1 claimed (transport rule), AUDIT pending; Lemma C open for N>=5 | W1-A, W1-H, `R2/tile.md`, `R2/tile2.md` |
| G3** (apex, covering radius, inradius) | length / lattice | reduced to G-rho (density) + G-h (facet height); ray-transfer false | W1-B, W1-I, `R2/g3.md`, `R2/finv.md` |
| Lemma 3P + Lemma F reconstruction | structural | 3P confirmed; F repaired (offsets <= 2mK) | W1-C, `R2/recon.md` |
| Laminar covers of n = 30 / S_2 slices | constructive | n=pq ply <= n+phi(n) proved; n=30 open (60 vectors) | W1-D, W2-J, `R2/construct.md`, `R2/construct2.md` |
| R4 walk / builder3 ambiguity growth | constructive / measurement | DONE: neither generates Q | W1-E, `R2/testgram.md` |
| Cyclic-closure class mass, gcd >= 2 | reformulation | gcd>=2 = full problem; P_cop open; Thm U (unamb.) | W1-F, W1-G, `R2/cyclic.md`, `R2/pcop.md` |

## Proved lemmas (with labels)
- [written proof] n=pq squarefree: rectangle family R_i covers E∩W_n (w±u = 2Δb, 2Δa; I_a, I_b classes mod A, B, gcd(A,B)=1 ⇒ meet); Q∩(ab*)^{pq} ply ≤ n+φ(n). Fails for p^a q^b exactly when witness fibres mod n/(pq) are disjoint (n=36). `R2/construct.md` §2.
- Prop BC [written proof] (`R2/g3.md` §2): on S_N, G3** ⇐ TILE^ℤ (integer δ in open tangent cones) + per-piece exponent E_σ=O(log n), facet height poly; no d_σ=0 used.

- [written proof, reconstructed] W1-C `R2/recon.md`: Structure (c) and Lemma 3P CONFIRMED (pair support, laminarity, no double count; K indep. of n since the D_n state is fixed by position; needs O(1) slice-DFA states per block). S3D refinement keeps ply but NOT ‖c‖₁≤nK (laminar d=1 example with offsets 2^{ρ-1}).
- [written proof] W1-C `R2/recon.md` §4: Lemma F REPAIRED: face offsets are only ≤ 2mK (original n), not 2(r+1)K (toy grammar); Cor F′: ply ≥ p at norm 2m + m·exp(O(p² log pK)) via CGST proximity. Theorem P intact (take m = 2p−1).
- [written proof] W1-F `R2/cyclic.md`: T1 P_{>=2} (CF L⊆Q, poly class mass on gcd>=2 or balanced classes) ⇔ full problem; L3 fixed-#a slice witnesses need ω(gcd)→∞; L2 morphisms only multiply gcd. Open sub-question P_cop (poly-amb CFL between {gcd=1} and Q): ¬P_cop ⇒ negative, invisible to slices.

- [written proof] W2 `R2/pcop.md`: Thm U: NO unambiguous CFL L with {gcd=1} ⊆ L ⊆ Q (strengthens Petersen; cross-slice: singularities of [x^p]G lie in a fixed finite set, but supp ⊆ pℕ forces p singularities). P1 Cop not CF; P2 semilinear S ⊇ P misses only finitely many lines + qℤ², q∈ finite Π.
- [written proof] W1 `R2/tile2.md` Thm A/B: TILE_k(1) — min-cost-transport rule (cost h(|y_i−y_j|), h incr. strictly concave): c-dual-feasible NC trees F_c have ply ≤1 everywhere (LP uniqueness) and cover iff no proper arc identically balanced (NC components ⇒ balanced arc). ⇒ q_k=1, S_N ply ≤ ply_VC: S_N BLOCKED geometrically modulo Lemma C (all N), realisability, G3**.
- [written proof] W2 `R2/realise.md` §1: PAIR FACETS mu_k=(1-T^{s_k})nu_k, one ±1 per fibre (nested windows): admissible, entries ±1, LEMMA C FOR ALL N (no balanced arc), pieces K=2 (edges e_p+e_q, root b-loop e_t), ||c||<=2n, UNIMODULAR (cov. radius 0), laminar; ply_VC<=n^{1+o(1)} [sketch]. LAM facets have unbounded ring vectors (ratio heights). Exact checks N=3,4.
- [assessment] W2 `R2/realise.md` §2: uniformity (U1 regular skeleton slices, U2 cross-slice/position exchange) formulated; 3P data ⇏ U (prime toy); single-split U = blocked rank route; transport-vs-U undecided; NONUNIF ≡ S_N negative statement. S_N survives only modulo one-grammar realisation.

## Blocked routes (with reasons)
- [computational+written] Conjunctive chord-dominance certificates (generalised rectangles, ≤3 chords, laminar conjunction) do NOT cover E∩W_30: 60 fibre-supported vectors (one class mod 5, fibre pattern rot of (2,0,1,1,1,0)/(2,1,1,1,2,0)) uncovered; no 3-chord atom certifies {2,3,5}. Lemma O (fibre obstruction), `R2/construct.md` §3. Not a lower bound: S4U shared-endpoint piece covers x0.
- G3** "poly data for some ply-set S" over all abstract valid covers: refinement (Stanley decomp. into chain pieces) keeps f but puts E=h=2^ρ pieces in every ply-set; need refinement-invariant argument (`R2/g3.md` §3).
- Obstruction "all ply≥3 points at norm 2^{Ω(n)}" on S_N: impossible, Lemma F_S + Cor F′ give ply p at n·exp(O(p² log pK)) (`R2/g3.md` §4).
- TILE_k via KKM/Sperner/Lebesgue covering: blocked [written proof]; they bound closure multiplicity, any sub-fan has half-open ply 1 (S2P §1(b)). `R2/tile.md` §2.
- W1-F: 1:1 cycle-lemma replacement at gcd>=2 = exact self-reduction (inner ratio free); pumping/interchange per-class lower bound reduces to S_N ply (TILE_k+G3**), no new mechanism (`R2/cyclic.md` §3).

- W2 `R2/pcop.md`: P_cop ⇒ full not obtainable: union route circular (T1), §5 transfers keep g(src)|g(tgt). Extending Thm U to poly ambiguity = count sandwich (no exact vanishing at coprime vectors).

## Computed tables
- [G/testgram] walk.md G_k=T^k(E') as printed: L ⊊ Q (misses `ab`), EXPONENTIALLY ambiguous: C_exp at K (K⇒YXYX·K two ways) [written proof]; A(4m+1)≥Catalan, 19006 at n=33 [computational]. Repaired K (first-return) same L: amb ≤ n^{k+1} [written proof]. `R2/testgram.md`
- [G/testgram] builder3 𝒰: no grammar exists (membership tests only); L(𝒰)≠Q, first miss n=26 (2 necklaces), sound n≤22, complete n≤25 [computational]. Guess-and-verify witness proxy max ≈ n^3 (20076 at n=20, argmax a^{n-1}b) [computational, proxy].
- TILE min-ply over ALL NC-tree cones, abstract generic μ: ply-1 fan exists in every instance, P=3 exact (m≤11, 43/43), P=4 LP (m=11, 8/8) [computational]. TILE_k reduces exactly to chamber exact-cover [written proof]. `R2/tile.md` §§1,3.
- [computational, exact] `R2/tile2.md` §3–4: actual μ_k is W-arc-generic for N=2,3,4 all k (Lemma C), but NOT ω-arc-generic for N≥3 (cluster arcs fold≡0: tile.md ω-chamber reduction ill-posed, walls need η∈W); rule exact-partitions P=3 m=9,11 (80/80); μ_k: N=2 T* valid 120/120 (ω+x), N=3 x-level 12/12, 0 ply violations.
- [AUDIT tile2] Thm A/B SURVIVES with mandatory fix C1: x-level K_T must include S2P root condition sgn μ_root = sgn τ (>0 on R_k(u)); rooting at v₀=supp[0] fails when μ_{v₀}<0 (N=2 example). Fix: cut before a positive vertex; Lemma C verified for all cyclic arcs N=2,3 exact, N=4 one ν. 'written proof N≤4' mislabelled (Lemma C computational). `R2/audit_tile2.md`.

## Round syntheses (root, <= 15 lines each)
- [written proof] `R2/finv.md` §3: CRT pieces (chain {2e_j+e_{j+1}} + e_0+e_t, D_t=2^t−1, K=3, full rank, laminar) added to any valid cover give f = f₀+Θ(m/log m) far out but f ≤ f₀+O(1+log R/m) on R-ball ⇒ "asymptotic (lim-sup/QP pointwise) ply ⇒ near ply" is FALSE, refinement-invariantly.
- [written proof] `R2/finv.md` §4 Lemma D: asymptotic DENSITY ρ(ω)=Σ1/idx (refinement-invariant) ≥ q ⇒ f ≥ q at norm poly(m,K,q,‖ω‖)·h, h = facet height at ω of the coarsest representation; lcm/covering radius drop out. Gap: density-TILE + h. QP onset (Szenes–Vergne) not a bottleneck.

**Wave 1 synthesis (root, 00:37 UTC).**
- Foundations hold: Structure (c) and Lemma 3P reconstructed; Lemma F needs offsets <= 2mK (Cor F'); Theorem P intact.
- Ply side: TILE_k appears to hold with ply 1 (min-cost transport tree selection, `R2/tile2.md`), which would BLOCK S_N
- [written proof + computational, exact] `R2/lemmaC.md`: Lemma C (cyclic, audit C1) ⇔ BLOCK(N,k), a statement about block-unions of h=(1−X^{P/p_k})∏_{j≠k}(1−X^{p_j}) mod X^P−1 (fine→coarse decoupling + shift-difference). Holds for all k, N≤45 (`lemmaC_blocks.py`); for all N given H (zero-runs of ∏_{j≠k}(1−X^{p_j}); checked 10≤N≤45), with `lemmaC_ends.py`. No counterexample; the choice of ν is not needed for generic u_k.
  geometrically (ply <= sqrt(n) polylog). Under gated audit; Lemma C (arc-genericity of actual mu_k) checked N <= 4 only.
- Length side: ray-asymptotic ply does not transfer (CRT); density does (Lemma D). Gap = G-rho + G-h.
- Constructive: n = pq slices have laminar covers of ply <= n + phi(n); n = 30 leaves a 60-vector fibre obstruction.
- Reformulations: gcd>=2 classes carry the whole problem; Theorem U (no unambiguous CFL between coprime words and Q).
- Test grammars walk/builder3: neither generates Q; closed.
- Net: no route unblocked. If the audit passes, the S_N candidate dies and wave 2 must find slice families where
  the transport tiling fails (balanced arcs, non-pair-supported structure, deeper prime powers) or a non-slice mechanism.
- [written proof + computational] W2 `R2/newslice.md`: NO new slice candidate. Any DFA sub-slice is locally ℝ^J∖∪_{p∈A(ω)}V_p (DFA ⇒ only coordinate restrictions); Lemma VC-gen: convex ply always poly; cross-prime defects (types, τ(δ)) only REDUCE factor count, E_k of S_N is extremal; deep powers n=∏p^a, lower strata, fibre-restricted sub-slices are S_N-type: 0 W-balanced arcs + rule ply-1 checked up to n=27000 (`newslice_check.py`). Live gap stays Lemma C (all N) + realisability + G3**.
- [written proof] W2 `R2/construct2.md` §§1–2: transfer atoms T=(τ;P;D), region x_τ−Σ_P x_a > Σ|d_i|, exact laminar 0/1 pieces (ply 1). Lemma FT: for every n=pqr, every primitive fibre-supported x∈W_n is covered by ONE transfer atom (rectangle + adjacent-pair routing τ→τ+1, τ+pq→τ+pq+1). So Lemma O is not an obstruction once tops may be shared.
- [computational] `R2/construct2.md` §3: dom(k≤2)+transfer atoms cover ALL primitive W_30∩ℕ^30 with ‖x‖₁≤10 (22 620 pts, 424 D_30-classes; 8 need transfer), all 60 sparse; greedy subfamily ply ≤ 44 on norm≤8. General E∩W_30 proof OPEN (gap B, §4). At n=36 off-fibre blocks are ≈B, not 0: transfer atoms collapse to |P|=1 dominance atoms (§5, assessment).
- [written proof+computational] `R2/newmech.md`: Lemma B (top-balanced exact identity, ≤|V|n² split terms ⇒ one-level multi-split linkage gains only poly), Lemma T (amb(uxv) ≥ out_A(u,v)·in_A(x); interchange gives no multiplicity), Lemma M (disjoint locally-ambiguous nodes multiply ⇒ ambiguity skeleton of every tree has ≤ k log₂|w|+log₂C leaves). Checked 8837 words/12 random CNF grammars (`newmech_check.py`).
- BLOCKED (`R2/newmech.md` §4): multi-split linkage. Width branch = "local defects washed out" (§6); path branch = laminar nested choices = S_N ply. G′ rotation linkage = Z_n-symmetrised laminar cover, factor n only. Open sufficient criterion: W-forcing (ω(log n) disjoint forced-ambiguous subwords).
- [computational] `R2/construct2.md` §5: n=12 (p²q), all primitive a(6-per)+b(4-per), entries 0..3 (979 200 pts): covered by k≤2 chord-dominance systems with arbitrary chord positions. So the construct.md §2 p²q failure belongs to the rectangle family only; the analogous n=36 test has not been run.
- [audit] `R2/audit_realise.md`: realise.md part (1) SURVIVES (near-U scope). Pair-facet family covers ∏(E_k∖0) (Pr[u_k>0] ≥ 1/(2p_k) needs window width p_k, N ≥ 4; N=3 width-1 family does NOT cover — structural checks only); Lemma 2 correct for all N; q_k=1, K=2, unimodular, nesting OK N=4..12. Caveats: scope R⁰ only, ply_VC n^{1+o(1)}, Lemma 4 a sketch.

**Wave 2 synthesis (root, 01:00 UTC).**
- TILE_k: ply-1 transport tiling SURVIVES gated audit (fix C1: root at a positive vertex). Lemma C proved N <= 45 for LAM facets.
- Pair facets (`R2/realise.md`): K = 2, offsets <= 2n, unimodular, Lemma C for all N; SURVIVES gated audit (`R2/audit_realise.md`)
  near U only. So per-slice data bounds + ply cannot kill a polynomially ambiguous grammar near U on S_N.
- No slice family defeats the transport tiling (`R2/newslice.md`): DFA sub-slices, deep prime powers, lower strata, two-prime defects
  all reduce to S_N product geometry.
- Multi-split inside/outside mechanism (`R2/newmech.md`): criterion W (omega(log|w|) disjoint ambiguous subwords) suffices but both
  branches collapse to §6 routes.
- Constructive: transfer atoms close the n = 30 fibre obstruction (Lemma FT, pqr fibre-supported); W_30 covered to norm 10 [computational].
- Open, ranked: (a) uniformity NONUNIF (one grammar across n) — the remaining S_N lever; (b) W far from U and off-W points (not covered
  by the pair-facet family); (c) G-rho / G-h on the length side; (d) n = 36 explicit covers.
- [written proof + computational] `R2/construct36.md` Lemma 36: E∩W_36 (S_2, whole slice) is covered by 72 k≤2 chord-dominance systems (12 fibre rectangles + 60 cross-fibre chord pairs), so Q∩(ab*)^36 has ply ≤ 2n+φ(n) = 84. Exhaustive check to ‖x‖₁≤16 (4.6M pts, 64 634 D_36-classes) with 0 uncovered; transfer and k=3 atoms are not needed.
- [assessment] `R2/construct36.md` §4: the mechanism is one system per tuple of distinct witness fibres, which is multiplicative (~n^{N/2}) for N≥3. So S_2 is uninformative for S_N, and S_3 (n=900) is the first real test.
- [written proof + computational] `R2/uniform.md`: NonPow_p = {w ≠ u^p} has a uniform CFG G_p (chord of span n/p via ratio counters P → C^{p−1}PC | C^cσ, M → CMC^{p−1} | τC^d) with amb = #{i<(p−1)n/p : w[i]≠w[i+n/p]}, exactly linear (exhaustive check, `uniform_nonpow.py`). Evades Lemma A for ONE prime (union, not canonical).
- [written proof] `R2/uniform.md` Thm W: for primes p<q no CFG exposing one marked mismatch pair per prime covers {a^{n−2}bb : pq | n} ⊆ Q (pump the 3 a-runs ≈ (n−n/p, n/p−n/q, n/q)); all chord orders non-stratified [computational, `uniform_marked.py`]. Word-level form of §6 "one witness per prime"; BLOCKED. Non-exposing grammars / CF-status of NonPow_2∩NonPow_3∩Σ^{6ℕ}: OPEN; NONUNIF not decided.
- [written proof + exhaustive check] W3 `R2/global.md` G1: slack-transport FORESTS (multi-root) tile {x≥0: mu(x)≥1} with ply 1, NC, unimodular, K=2 GLOBALLY (no Lemma C needed) ⇒ realise pair-facet family covers ALL primitive (U⊕⊕E_k)∩ℕ^n (far from U, U-part 0, zeros), same ply_VC; facet-defined pieces have no patching loss.
- [written proof] W3 `R2/global.md` G2: realise-type disjoint single-prime facets MISS x=t·1+1_D+1_T (D 2-cycle, T 3-cycle; near U, δ∉⊕E_k) for N≥6 (5-point support); spread lemma L>n(1−Π_K), gap-compatible ⇒ Π_A+Π_B>1. G3: matching piece 1_{D∪T}+ℕ{e_{2b}+e_{2b+1}} covers it (overlapping dual certificates) ⇒ NOT a negative candidate; G4 local criterion δ∉L+V_p.
- OPEN W3 `R2/global.md` §5 G-glob: bounded-offset poly-ply cover for large-scale sparse multi-type defects (pair-split σ/d recursion, per-prime OR); construction gap only.
- [written proof] `R2/l6.md` L6 = NonPow2∩NonPow3∩Σ^{6ℕ} (= T): Thm R — any CFG exposing ≥3 marks at fixed fractions of n (rectangle {i,i+n/3,i+n/2,i+5n/6}, any pairing; also block-level i,i+N/p,i+N/q,..) has FINITE language (Ginsburg–Spanier stratification) ⇒ construct.md rectangles are inherently per-slice. Thm S — L6 is not a finite union of NonSq∩R, NonCube∩R′, R″ (R regular): family a^{L+D}b(a^Lb)^5.
- [written proof + computational] `R2/l6.md` Lemma F: w∈L6 iff fibres (mod n/6) are not all in V2(6) and not all in V3(6); "mixed" words (every fibre in V2∪V3) defeat all single-fibre certificates (24 at n=12, 432 at n=18). Partial grammar C_k = G2×R_{3,k} ∪ G3×R_{2,k} ∪ R_{2,k}∩R_{3,k} is sound, amb ≤ 7n/6+1, misses U_k ∋ a^6(b^ka^k)^6 for every k.
- Status: L6 CF / poly-ambiguous OPEN; surviving mechanism must be non-regular, non-exposed, cross-fibre (run-length comparisons) — the NONUNIF frontier. Lower bounds for L6 do not transfer to Q directly.
- [written proof] `R2/thmR_unif.md`: Thm R is NOT a non-uniformity mechanism vs all G for Q. Thm R′: fractional marked trees (≥3 gaps) lie on 2-gap GS pump orbits leaving the fractions ⇒ contradiction only for pump-closed families (Cor R″ = R relativised; Thm W is an instance); S_N words are not pump-closed (fixed-n pumps are b-only, a-pumps leave near-U); toy a^m b^m c^m d^m has universal fractional trees and is CF. Collapses to §6 pumping.
- [written proof + numerical] `R2/thmR_unif.md` Lemma E: a facet μ_k ⊥ V_{p_k} has chord system of cyclic extent ≥ n/p_k (tight), which is only an inequality (semilinear). Lemma N: admissible μ_k = (1−T^{s_k})·alt with all ring spans ≤ 2 (n = 36, 900); validity/low ply of short-chord facets = TILE_k, OPEN. No ring span ≈ γn or ≡ 0 mod n/p is forced.
- [written proof] W4 `R2/gglob.md` G5: at K=2 a piece's level-t lineality has L1^perp ⊆ span{e_p−e_q : pq∈M}, M ONE non-crossing matching (ballot decomposition) ⇒ G4 ⇔ ∃M ∀k d_M(y)∉d_M(V_k) (both levels). The σ/d per-prime OR (2^N f(n/2)^2) is an artifact of fixing M0; correct recursion = ∃M∀k + signed d_M sub-instance. G6: {M0,M1} fail on explicit primitive y (n=36).
- [computational] `R2/gglob.md` §3: random NC matchings certify all tested sparse mixed defects (n=36: ≥183/200; n=900: 20/20; two-level G-glob condition 202/202, 22/22). (A) collapses (no laminarity content beyond the choice of M). OPEN G-glob′: (i) Pr_M[∀k ok] ≥ n^{-O(1)} (correlation; heuristic (1/4)^N=n^{-o(1)}), (ii) signed slack-forest tiling on d_M-space.
- [written proof + exhaustive m≤10] `R2/gglob_ii.md` S1: G-glob′(ii) per-facet: for μ∈{±1}^S with face graph G_M(S) connected, switching w=D_μz makes signed rings a DIRECTED network flow (TU; odd cycles only from excluded mass-2 rings ±(e_a+e_b)); rooted-forest bases tile {μ(z)≥1} with ply 1, K=2, NC among arcs AND with M (arcs confined to faces of M). Holds for all ±1 facets when M=M₀,M₁.
- [written proof + exact] `R2/gglob_ii.md` O1/O2: per-facet finite tiling by ‖ring‖₁≤2 M-laminar pieces is IMPOSSIBLE if a chord ∉ supp μ separates supp μ (M={(1,2),(0,3),(4,5)}, μ=z_a−z_b) or |μ| non-constant (μ=(1,2)); (H2) fails for most random NC M ⇒ (ii) OPEN for separated supports / F₁-laminarity.
- [written proof] W4 `R2/gglob_i.md` I0/I1: adjacent pairs {a,a+1},{b,b+1}∈M with a≡b mod s_k, z_a≠z_b (z=Dy) certify k; so G-glob′(i) ⇐ Lemma I2 (∃ gap-≥2 set S, |S|≤2N, containing a k-witness ∀k), with explicit 𝒟 (iid Bernoulli(1/3) isolated adjacent pairs + adjacent completion), Pr ≥ (16/729)^N = n^{-o(1)}. I2 proved for N=2 and in the residue-transversal case.
- [computational] `R2/gglob_i.md` §3: I2 has no counterexample (n=36: 410 adversarial restarts + 13 377 structured; n=900: 1 749 structured); M_S certifies exactly (rank) in all tests. I2 for general N (p=2 translation chains) OPEN; (ii) untouched.

**Final synthesis (root, 01:36 UTC).** Stopped after five waves; see `STOP_REPORT.md`. No route unblocked toward a full resolution.
- Audited: TILE_k ply 1 (transport rule, fix C1); bounded-data pair-facet tiling near U (K = 2). So S_N is blocked per slice near U.
- Open: G-glob′ (i) Lemma I2 (proved N = 2) and (ii) without H2; NONUNIF (one grammar across n); L₆ = NonSq ∩ NonCube.
- Waves 3–5 turned up no new negative mechanism (Theorem R, multi-split linkage and mixed-type defects all collapse); affirmative-side evidence grew.

## Round 3 (started 01:45 UTC). Reports: `R2/r3_*.md`, scripts `scripts/r3_*.py`.
| task | mechanism | owner / file |
|---|---|---|
| L6 affirmative: run-length comparison grammar | constructive | R3-A, `R2/r3_l6grammar.md` |
| NONUNIF lower bound across slice lengths | uniformity / negative | R3-B, `R2/r3_nonunif.md` |
| Lemma I2 for all N | covering / probabilistic | R3-C, `R2/r3_i2.md` |
| G-glob' (ii) without H2 (separating chords) | tiling | R3-D, `R2/r3_sep.md` |
| Uniform realisation of the off-W part (T1-P1) | constructive / uniformity | R3-E, `R2/r3_offw.md` |
- [written proof] R3-B `R2/r3_nonunif.md`: forbidden exchange (U2 across slices: shared L_A∩Σ^ℓ, no filler completing a context to a power) ⇔ L(G)⊆Q (Lemma FE0, downward closed); single-defect Lemma D (every tree's defect path separates x from x̂) forces no 2nd tree; Lemma C1 |Comp_ℓ(C)| ≤ τ′(L)+2^{ℓ−L/2} (sparse conflicts; check L≤14).
- [written proof] R3-B Prop 1: one-level exchange data is ambiguity-blind (cover multiplicity ≤ |V|L² for EVERY CFG for Q) ⇒ an FE/U2-only lower bound would prove Q non-CF. COLLAPSES to cross-slice W-forcing (`newmech` §5) / NONUNIF, OPEN.
- [written proof + computational] R3-C `R2/r3_i2.md`: Lemma I2 PROVED for all N (minimum residue cover I; |I|≥3 or non-adjacent ⇒ minimality gives a shared free CRT coord on each adjacent pair, path 2-colouring works even for p=2; I={r,r+1} ⇒ projection count 2|B_o|<∏p fails only for B_o={2}, swap roles). Hence G-glob′(i) unconditional, Pr ≥ (16/729)^N; construction verified for 10 prime sets up to n=44100 (`r3_i2_construct.py`).
- [audit] `R2/audit_r3_i2.md`: R3-C Lemma I2 (all N) ⇒ G-glob′(i) SURVIVES (F4 CRT adjacency, path 2-colouring for p=2, Case B disjointness, (16/729)^N all checked; indep. SAT: n=36 exhaustive 2-residue binary 24 120 + 22k random, n=900 635, 0 failures). Caveat: gglob "factor C per halving ⇒ n^{O(log C)}" gives superpoly ply for C=(729/16)^N — interface of (i) to the ply bound unresolved; (ii) still OPEN.
- [written proof + exact] R3-D `R2/r3_sep.md`: G-glob′(ii) per facet CLOSED via 𝒟′ (isolated adjacent pairs, NO completion; I1 unchanged): every chord on the outer face ⇒ (H2) always, W_k^⊥ has a ±1 basis ⇒ O2 never needed, F₁ := M ⇒ F₁-laminarity = M-laminarity (Part A: 180 cells, ply 1). O1⁺: a separating chord is unrepairable by ANY finite M-laminar K=2 family (≈50 % of pair facets separated under the original 𝒟).
- OPEN R3-D `R2/r3_sep.md` §4: joint multi-prime laminarity. (N*) + Lemma C1: pair facets tile jointly iff witness chords are disjoint and NC; I2 ⇏ I2-NC (n=36: 76/100, 45/292); bites for arc-needing level-s primes and ≥2 deferred primes (N≥3, e.g. η=e_q); 4-chord ±1 repair of shared chords exists.
- [written proof] R3-E `R2/r3_offw.md`: word-level off-W set Off = {x̂_w(1) ≠ 0} = {Φ_n ∤ B_w} ⊆ Q (Galois), Off_n = Q_n for n = p^a (and n = pq via de Bruijn [cited]). T1-P1 is per-slice (Θ(n) states, φ(n) DOC components). Thm X: any CFG exposing ≤K marks containing a p-step then q-step (e.g. supp y, y ∈ W_n^⊥∖0; min support 2^ω(n), MILP-checked) has FINITE language, which subsumes Thm W and the rectangle case of Thm R.
- [written proof + exhaustive n≤15] R3-E fold grammar G_fold (S → A1 B | A0p B1 | B1 A | B0p A1; mirror pairs of u = w[0..m] never (a,b) and of v never (b,a), strict somewhere): uniform, no counting, L ⊆ Off ⊆ Q, amb = #(m,±) certificates ≤ n (max n−1). Covers a^{n−2}bb and L6 U_k at all lengths. Coverage of Off: 100% (n ≤ 8, n = 10), 81.5% (n = 20), but → 0 on random words (1.2% at n = 64, 0 at n ≥ 128) [computational].
- OPEN R3-E: a poly-ambiguous CFG L with Off ⊆ L ⊆ Q (the full uniform off-W part). "No such L" ⇒ main negative, so it is not separately refutable. Missing piece: certifying the fold sum Σ x_k sin(2π(k−m/2)/n) ≠ 0 when the folded signs are mixed.
- [written proof] R3-A `R2/r3_l6grammar.md`: L6 has RATIONAL GF Σ(2^{6m}−2^{3m}−2^{2m}+2^m)z^{6m} ⇒ no analytic obstruction even to unambiguity; Thm R° (exposure modulo rotation, ≥3 positive cyclic gaps ⇒ finite) kills rotation-section/“cube witness at fold depth m” routes.
- [written proof + exhaustive N≤2] R3-A Thm M: in G2⊗(tree automaton) (“one nested structure”), a-run pumps = R_k-palindromic vectors; every L6 run-word has a chord axis k with anti_k(r)∉V3 ⇒ Theorem S's pumping does NOT lift to 𝒟2∪𝒟3∪Reg (`scripts/r3_l6_mirror.py`).
- OPEN R3-A: no poly-amb CFG for L6 found; residual 𝒟2 task = certify anti_k(r)∉V3 (a fractional comparison); b-containing multi-site pumps on 𝒟2 unsettled.
- [written proof] R3-depth `R2/r3_depth.md`: for exact facet-tuple constructions, ply(x) = #{σ : x ∈ R_σ}; matchings and levels are tiling devices, so audit C1's per-halving factor is the wrong accounting. Essential depth ≤ N + 1, and G-glob proper has depth 2.
- [written proof] R3-depth Lemma D1: facets touching ≤ s fibres ⇒ ply ≥ (P/(2s))^N at norm ≤ (2N+1)n (reproves PA LAM (a)). I0/I2/J-share witnesses have s = 2 ⇒ n^{N/2−o(N)}, so the I2 route to G-glob is dead at any depth. The bound is paradigm-relative and its adversary is pure ⊕E_k, so it is NOT a new negative candidate.
- OPEN R3-depth: SPREAD-JOINT. G-glob needs spread facets (≥ P/N^{O(1)} fibres) that are also C1-compatible (disjoint and NC chords); realise ∪ local overlay is the candidate. SPREAD-CROSS is conjectured, and false for pure types.

**Round 3 synthesis (root, 02:40 UTC).** Still unresolved; no route unblocked.
- Closed: Lemma I2 for all N (audited, `R2/r3_i2.md`, `R2/audit_r3_i2.md`); G-glob′ (ii) per facet via partial matchings (`R2/r3_sep.md`).
- G-glob is not closed: I2-witness facets touch ≤ 2 fibres, and Lemma D1 forces ply n^{N/2} for those (`R2/r3_depth.md`). Remaining gap SPREAD-JOINT:
  a poly-size family of facet tuples that are spread (≥ P/N^{O(1)} fibres) with disjoint, non-crossing witness chords, covering all two-level points.
- Uniformity, negative side: forbidden exchange across slices collapses to soundness (`R2/r3_nonunif.md`). Theorem X (`R2/r3_offw.md`): no grammar exposes a two-prime certificate.
- Affirmative side: G_fold is a uniform, linearly ambiguous grammar inside Off ⊆ Q; it does not cover Off for large n. L₆: rational GF; Theorems R° and M (`R2/r3_l6grammar.md`).
- Exact open forms: SPREAD-JOINT (per-slice), a uniform grammar for Off (mixed-sign fold sums), L₆, NONUNIF.

## Round 4 (started ~02:50 UTC): strategy change. Reports `R2/r4_*.md`.
Rationale: per-slice geometry is answered (low-ply bounded-data covers exist), so the remaining question is uniformity at the word/grammar
level. Switch to a bottom-up loop: union all known uniform poly-ambiguous gadgets, compute the exact uncovered primitive words, then
design gadgets for them or extract a word-level negative family. Split the difficulty using L1 (only primes dividing g = gcd(#a,#b) matter).
| task | owner / file |
|---|---|
| Gadget library + exact uncovered core (coverage loop) | R4-A, `R2/r4_core.md` |
| One varying prime: Q ∩ {g(w) prime power} | R4-B, `R2/r4_pp.md` |
| Citation check: Kászonyi–Katsura, Dömösi–Ito (what is proved, are constructions uniform) | R4-C, `R2/r4_cite.md` |
- R4-C (`R2/r4_cite.md`). Q∩(ab*)^n is CF if n has 3 distinct primes (KK 1997 Thm 1, verified primary) or Σ1/p<4/5 (KK 1999, verified via zbMATH; not Kászonyi 2010, which only quotes it). The 1- and 2-prime cases (incl. n=6) are attested only second-hand (FCT'93 unseen); n=210 is the first uncovered n.
- R4-C. All results are per-n: CF via Ginsburg plus Flip-Flop, with no explicit grammar, no uniform-in-n construction and no ambiguity claim. Dömösi–Ito book Ch. 10 "Kászonyi–Katsura Theory" (pp. 309–342) and the bounded/slender claims were not read (unverified).
- R4-B `R2/r4_pp.md`: [written proof] Prop H: pullback along h_p(a)=a^p,h_p(b)=b^p gives P(Q∩{g=p}-sandwich) ⇒ P_cop for each FIXED p (so P(Q_pp) ⇒ P_cop; Cor U_p: no unambiguous sandwich even for g=p). Q_pp not CF.
- R4-B: isolated core VP (agree with Q on prime-power classes only) OPEN; Theorem V [written proof+comp]: no chord-exposing grammar (span ≡0 mod n/p) covers infinitely many a^p b^p, any ambiguity.
- [written proof + exhaustive n≤28] R4-A `R2/r4_core.md`: Lemma S (window features x^φ and run sequences inherit (n/p)-periodicity) ⇒ new sound uniform O(n)-ambiguous gadgets FL (factor-count lines c₁occ_f − c₂occ_h = ±1), LF/PF (folds on factor indicators), RLF (fold on run lengths). With LIN+G_fold: U_n = ∅ for n ≤ 19, 21–23; |U_n| = 40/48/400/780/1242/3248 at n = 20, 24–28 (1/1/7/10/17/40 classes), all in Off (U ∩ W_n = ∅): sparse, near-reflection-symmetric run sequences.
- [MC + sketch] R4-A: every finite library of this type covers only Θ(n^{−1/2}) of random words (LIN∪FL: .84/.56/.34/.20/.095 at n = 256…65536; the folds are exponentially rare). The asymptotic core is GENERIC words, not a near-periodic family. Open target DENSE-SOUND: a poly-amb CFG L ⊆ Q of positive density (equivalently, a dense poly-amb subset of L₆ on 6ℕ). Main affirmative ⇒ DENSE-SOUND; "no such L" ⇒ main negative.

**Round 4 synthesis (root, ~03:40 UTC).**
- Literature (verified): Kászonyi–Katsura slice results are per-n (Ginsburg + Flip-Flop lemma), with no uniform grammars and no ambiguity statements.
- Reduction chain: P(Q) ⇒ P(Q_pp) ⇒ P(Q ∩ {g = p}) ⇒ P_cop (Prop H, `R2/r4_pp.md`). So ¬P_cop alone gives the negative resolution, and any proof of it
  must use the ambiguity bound (pumping alone would show Q not CF). Theorem V: marked chords for a varying prime fail (cf. Theorems W, X).
- Coverage loop (`R2/r4_core.md`): uniform sound gadgets cover all primitive words of length ≤ 28 except at n ∈ {20, 24..28},
  but the covered fraction of RANDOM words decays like n^{-1/2}. Every known uniform certificate is "local" (Parikh lines, factor counts,
  folds) and certifies only a vanishing fraction of words. The hard core is generic words, not slice families (U ∩ W_n = ∅).
- Strategic consequence: an affirmative construction needs a uniform certificate for TYPICAL words (gcd(#a,#b) with ≥ 2 varying primes),
  exactly what Theorems V, W and X forbid in exposed form. A negative proof should target generic words, not slices.
- New target DENSE-SOUND: is there a poly-ambiguous CFL L ⊆ Q of positive density? ¬DENSE-SOUND ⇒ main negative (a stronger statement).

## Round 5 (started 03:17 UTC). Reports `R2/r5_*.md`.
| task | owner / file |
|---|---|
| Negative: generic words vs Wich structure ("bounded linear invariants") | R5-A, `R2/r5_generic.md` |
| Affirmative: hidden uniform certificate of positive density (DENSE-SOUND) | R5-B, `R2/r5_dense.md` |
| Audit: Prop H + soundness of coverage-loop gadgets | R5-C, `R2/audit_r4.md` |
- [audit] R5-C `R2/audit_r4.md`: Prop H SURVIVES (block lemma any p≥2; unary/ε edge cases fine; literal pullback grammar G′ with ε-leaves gives exact tree-count bijection, 6 240 random-grammar tests, 0 mismatch; Cor U_p conditional on unaudited Thm U). Lemma S + LIN/FOLD/FL/LF/PF/RLF SOUND (independent brute force: 8 714 non-primitive words n ≤ 24, 0 accepted; S0 matches .976/.923); RLF wrap needs a canonical split of the partner run (naive split ⇒ ≤ n× trees, still poly).
- R5-A `R2/r5_generic.md`: H* COLLAPSES. Interchange-family soundness = L(G) ⊆ Q (FE0), so it cannot see ambiguity; Wich's normal form bounds neither branching (unambiguous G_D: Strahler ~ log₄ n) nor rates (A → aAb|bbAa|ε); L≥ = {#a ≥ #b} is an unambiguous language of density 1/2 with no positive-density FR sublanguage [written proof].
- R5-A: Prop P [written proof]: a Parikh-closed CF L ⊆ Q has density O(n^{-1/2}) (the LIN barrier made rigorous). Prop B [written proof + MC]: UMR (unique longest b-run) ⊆ Q is a disjoint union of ≤ n² boxes per n with density ≈ 0.36, also on {p | g}, so set-level skeleton-family arguments fail.
- R5-A: the gap is unchanged (DENSE-SOUND / newmech W-forcing). Is UMR, or a dense poly-ambiguous subset of it, CF? OPEN; it is a test case for R5-B (the 3-run near-diagonal is stratified).
- [written proof + exh n≤22 + MC n≤16384] R5-B `R2/r5_dense.md`: Lemma F: F_K = {w : d_k ≠ 0 ∀k∈[n/3,n/2]} ⊆ Q, d_k = #a(pre_k) − #a(suf_k) (u^p ⇒ d_{⌊p/2⌋n/p}=0); density → (2/π)arcsin√(2/3) ≈ .608 (F_δ variant → 1). F_K = fold of a det. one-counter language (TAG); CF-ness of any dense subset OPEN (FOLD-COUNTER).
- R5-B: Theorem P_K: any CF L ⊆ {gcd of K-window counts = 1} has density O(n^{−1/2}) (kills Parikh/FL/Bézout-split (a); Lemma B: g=1 ⇔ ∃ cyclic factor with det(ψx,ψw)=±1). Prop U: bounded-comparison relaxations of UMR are unsound; UMR CF-status OPEN.

**Round 5 synthesis (root, ~04:00 UTC).**
- Audit (`R2/audit_r4.md`): Prop H and the coverage gadgets SURVIVE (exact tree-count pullback; soundness independently checked to n = 24).
- Negative (`R2/r5_generic.md`): H* collapses (unbounded branching, mixed rates). Prop P: a Parikh-closed CF L ⊆ Q has density O(n^{-1/2}).
- Affirmative (`R2/r5_dense.md`): Lemma F, an interval-fold certificate F_K = {d_k ≠ 0 ∀k ∈ [n/3, n/2]} ⊆ Q, with ONE fold for all primes
  (k = ⌊p/2⌋n/p). Density ≈ 0.61 (variant → 1). TAG-recognisable unambiguously; CF-ness open (FOLD-COUNTER). Theorem P_K: count-based CF
  certificates have density O(n^{-1/2}). UMR relaxations are unsound (Prop U).
- Decisive open question: FOLD-COUNTER. Does F_δ have a positive-density subset that is CF with polynomial ambiguity? A yes kills the
  "generic words are the hard core" heuristic; a no with a robust reason (fold + counter is non-CF on dense sets) is the best negative lead.

## Round 6 (started 03:59 UTC): FOLD-COUNTER. Reports `R2/r6_*.md`.
| task | owner / file |
|---|---|
| Build a CF positive-density subset of F_delta (affirmative) | R6-A, `R2/r6_build.md` |
| Prove no dense subset of F_K-type folds is CF / poly-amb (negative) | R6-B, `R2/r6_nofold.md` |
- [written proof + exh n≤30 + MC n≤10⁴] R6 `R2/r6_miss.md`: Lemma M (F_K sound ⇔ K meets (n/p)ℤ ∀p|n; [1/3,1/2] is the unique all-n window; residue windows give .69–.76). Rotations are free: |E_n| = 0 for n ≤ 30 (Rot F_K misses ≤ 3·10⁻⁵, only near-powers with g ≥ 2). Lemma R: Rot(F_max) = Q at prime-power n.
- R6 Lemma A: the rotation at the unique argmax of T(i) = n·#a(w[0,i)) − i·#a(w) lies in G⁻ = {d_k < 0 ∀ 1≤k≤n/2} ⊆ Q, so Rot(G⁻) has density ≥ 1 − P(tie) ≈ 1 − 0.43/√n (MC). Leftover = the tie family ⊆ {g ≥ 2}. Sharpened target ROT-FOLD-BALLOT (CF L ⊆ G⁻, rotation-dense): OPEN.
- [written proof + 2977/2977 random DFAs] R6-A `R2/r6_build.md`: Prop K: any REGULAR condition on the fold pair sequence (mod-m, any DFA, centre info) that is sound has density e^{−Ω(n)} — fooled by u^{2j+1}, j = idempotent exponent (kernel of the transition monoid); fold certificates need unbounded spine memory.
- R6-A: Lemma SA: L_A = {xy : x b-first Dyck, every suffix of y a-majority, |x| ≥ |y|} ⊆ G⁻ ⊆ Q (exh n ≤ 18); Rot(L_A ∪ swap) density ≈ .62–.67 (MC). G⁻-affirmative reduces to one Θ(n) length coupling of two one-counter parts; L_A itself is not CF (Prop N, pumping on b⁺a⁺ba⁺).
- R6-A: no CF positive-density sub-certificate found; FOLD-COUNTER still OPEN (all attempts fail at length coupling vs counters).
- [written proof + exh n≤14 + MC] R6-B `R2/r6_nofold.md`: FOLD-COUNTER negative NOT resolved. Lemma L (edit of size r moves every d_k by ≤ r; depths below the edit fixed), Lemma M (G⁻ is an up-set: b-insert left / a-insert right / outward flips; rc-invariant). Hence bounded pumps (N1), macroscopic single pumps (N2, MC: ≈0.9 survive) and interchange/one-split rectangles (N3) cannot refute any CF L ⊆ G⁻; slices are stratified (G⁻∩b^i a^j(ba)^m = {i>m}∪{j<i}).
- R6-B: length coupling is a genuine barrier for local/one-split tools only. Only non-F1 handle: Θ(1) exit probability per macroscopic surgery (Q: 2^{−Ω(n)}). Spine reduction ⇒ hanging languages lie in shifted meanders G⁻_{t,h}; exact gap = Lemma Q (CF L ⊆ G⁻_{t,h} has density ≤ c·min(1,h/√n)^{1+η}), OPEN. Fold-type class: REG = Prop K (sparse); one-counter = FOLD-COUNTER itself; CF not pinnable (would touch Q ∉ CF).

**Round 6 synthesis (root, ~06:30 UTC).** FOLD-COUNTER still open; the question is now one precise obstacle.
- Rotated fold certificates cover all of Q for n ≤ 30 (exhaustive); Lemma A: a rotation of every primitive word with a unique balance argmax lies in
  G⁻ = {d_k < 0 ∀k ≤ n/2} ⊆ Q; misses ≈ 0.43/√n (the tie family, g ≥ 2). Lemma M: [n/3, n/2] is the unique all-n window (`R2/r6_miss.md`).
- Prop K: regular (finite-memory) fold certificates that are sound are exponentially sparse (`R2/r6_build.md`). Lemma SA: G⁻ reduces to
  Dyck-prefix · a-heavy-suffix with ONE length coupling |x| ≥ |y|; dropping it is unsound (baa·baa); L_A is not CF (Prop N).
- Negative side (`R2/r6_nofold.md`): bounded pumps, single large pumps and interchange all fail to separate G⁻ from CF; the remaining
  handle is Lemma Q (density of CF L inside shifted meanders G⁻_{t,h}), which needs polynomial ambiguity to enter (F1).
- Decisive open question: can a polynomially ambiguous CFG realise the length coupling on a rotation-dense subset of G⁻?

## Round 7 (started 06:23 UTC): the length coupling. Reports `R2/r7_*.md`.
| task | owner / file |
|---|---|
| Affirmative: dissolve the coupling (uncoupled P·S minus its powers; rotation normal forms) | R7-A, `R2/r7_uncouple.md` |
| Negative: Lemma Q via polynomial ambiguity | R7-B, `R2/r7_lemmaQ.md` |
- R7-B (`round2/reports/r7_lemmaQ.md`): Lemma Q is false as stated (quotient depends on the paired window, density 1 at h = 1). Lemma R: centre rectangles X×Y ⊆ G⁻ have size ≤ C log²n·2ⁿ/n, exactly the rotation threshold (KMT + Prékopa).
- Prop S: for unambiguous L ⊆ G⁻, each fixed centre spine carries O_s(2ⁿn^{−3/2}), via uncoupled-length closure + algebraic regular variation. So rotation-dense ⇒ spines escape to infinity.
- Gaps: G1 uniformity in the spine (correct form of Lemma Q); G2 ambiguity: the disjointness step loses nᵏ, so Prop S is vacuous for poly-ambiguity k ≥ 1/2 without Lemma-M-type distinctness.
| R7-A result: uncoupled D_b·P = P (closed under powers), so (A) carries no information; L_A = P ∩ {h≤0 on first half}, Rot L_A = Rot L_B with L_B = {H≥1, h≤0 on first half} ⊆ Q (not CF) | `reports/r7_uncouple.md` [proof + exh n≤24] |
| R7-A: rotation normal forms cannot remove the coupling (N(u^p) is always a power); in P-form this is block-sequence aperiodicity, where every sound certificate is one-vs-rest/each; no CF candidate, OPEN | `reports/r7_uncouple.md` [proof/sketch; MC n≤10⁴: Rot L_A misses ≈0.35] |

**Round 7 synthesis (root).** Still open. The fold route turns out to reproduce the problem one level down.
- U1: without the coupling the Dyck prefix is useless (D_b·P = P), and PS ∩ NonPrim = {u^p : u ∈ P}; excluding it IS the original problem.
- U3: rotation choices can't remove the coupling (u^p ↦ a power). In cycle-lemma form, P ∩ Q = primitive block sequences over the infinite
  alphabet D_b: the problem is SELF-SIMILAR at length ~√n. Every sound certificate found compares one block against the rest (`R2/r7_uncouple.md`).
- Negative tools (`R2/r7_lemmaQ.md`): Lemma Q as stated is false (Q0). Centre rectangles sit exactly at the threshold (Lemma R).
  Prop S: an UNAMBIGUOUS L ⊆ G⁻ carries O_s(2^n n^{-3/2}) per fixed centre spine, so dense L needs unboundedly many spines.
  Gaps: G1 (uniform constants over spines), G2 (polynomial ambiguity loses n^k).
- Most promising concrete route now: the negative side via Prop S + G1 + G2, which would show no poly-ambiguous CF L ⊆ G⁻ is rotation-dense.
  Caveat: that kills the FOLD route only, not the affirmative in general.

## Round 8 (started 06:33 UTC). Reports `R2/r8_*.md`.
| task | owner / file |
|---|---|
| Prop S gaps G1 (uniform over spines) + G2 (polynomial ambiguity) | R8-A, `R2/r8_propS.md` |
| Audit: Prop S, Q0, Lemma R; U1-U3 | R8-B, `R2/audit_r7.md` |
- R8-B audit (`R2/audit_r7.md`): r7_lemmaQ SURVIVES (Q0, Lemma R, Prop S ok; caveat: Prop S step 2 needs the general non-strongly-connected N-algebraic residue-class asymptotics, cited loosely; spine must record child index). r7_uncouple SURVIVES (U1–U3 brute-forced n≤18, 0 errors; non-CF claims are sketches).
- R8-A (`reports/r8_propS.md`): T8 OPEN. Thm C [proof]: for unambiguous G, Σ_s slice_{s,a} = |L_n| for every a, so Prop S/S′ never use G⁻ (r7's "not count-only" is wrong) and any G1 uniformity is a tautology. G2 is moot; word distinctness fails inside G⁻ (amb ≍ n example).
- R8-A: positive items: |G⁻_n| ~ 2ⁿ/√(2πn) (DP); anchored spine rectangles ≲ 4^N N^{−4/3} via a 3π/4 cone (DP −1.329 at m = 800). Remaining gap: cross-spine packing (spine-local arguments cannot give T8).

**Round 8 synthesis (root).** The Prop S route is circular; T8 remains open even for unambiguous grammars.
- Audit (`R2/audit_r7.md`): Prop S, Q0, Lemma R, U1–U3 SURVIVE as statements (Prop S modulo non-strongly-connected asymptotics).
- Theorem C (`R2/r8_propS.md`): Σ_s |X_{s,a}||Y_{s,n−1−a}| = |L_n| exactly for unambiguous G, so Prop S does not use G⁻ (it is count-only, §6),
  and uniform per-spine bounds (G1) are tautological. G2 fails: shifted copies are distinct trees, not distinct words.
- Gain: cone-exit rectangles ≲ 4^N N^{-4/3} (vs N^{-1}). Exact remaining gap: a cross-spine packing lemma (§4 of the report).
- Assessment after 8 rounds: every route reduces to one of three cores: (i) uniform certification of typical words (fold coupling /
  self-similar block sequences), (ii) ¬P_cop via the ambiguity bound, (iii) cross-spine packing. None is close to closed.

## Round 9 (started 06:53 UTC): one agent per core. Reports `R2/r9_*.md`.
| task | owner / file |
|---|---|
| Core (ii): not-P_cop via Wich structure (fresh eyes) | R9-A, `R2/r9_pcop.md` |
| Core (iii): cross-spine packing lemma | R9-B, `R2/r9_packing.md` |
| Core (i): exploit the self-similar block reduction (both directions) | R9-C, `R2/r9_selfsim.md` |
- R9-A (`reports/r9_pcop.md`): **No-go for every U-type extension.** Theorem N [written proof + computational, |w| ≤ 15]: there is an explicit linearly ambiguous CFG whose language L_P ⊇ Q, and L_P ∖ Q ⊆ {#a composite}. The two-letter L_P2 has both #a and #b composite. U only uses prime rows (U′), so ¬P_cop must use L ⊆ Q on composite rows; idea (2)'s exact series cannot exist for any language (U*).
- R9-A: L_M (§4, sketch): the obstruction must involve roots v with #a(v) ∤ M for every M, so core (ii) contains core (i). By-product: L_P is inherently ambiguous with linear ambiguity (via U′). Next lemma: is there a PCFL ⊇ Cop that is sound on all rows 2q? Open.
- R9-C (`reports/r9_selfsim.md`): self-similarity gives NO amplification. A1/A2 [proof]: depth-k truncation certificates L_k = σ(Q₃∩R_k) ⊆ P∩Q (CF substitution, exact tree counts) satisfy P(L_k) ⇔ P(Q) for every finite k; P(P∩Q) ⇒ P(Q); converse OPEN = uniformity in k.
- R9-C: the invariant certificate lands in the unbounded-H slice Q∩(b*a)⁺, which is the full problem (code {ba,bba}), not a fixed (ab*)ⁿ slice. Lemma RG: amb(n) ≥ C·amb(n^α)^s excludes polynomials iff sα > 1; blocks give s = 1, α = ½ (vacuous); √n contraction is typical-only.
- R9-B (`R2/r9_packing.md`): T8_unamb NOT proved, no counterexample. Thm M: for unambiguous L, T8 ⟺ μ(L)=Σ|L_n|2^{-n}<∞ (no α=−1); Lemma Rn: a finite-mean critical linear SCC is impossible in G⁻ (renewal).
  So any counterexample needs a heavy-tailed full-entropy block (≍2^ℓℓ^{-3/2}) feeding a critical linear SCC, α∈(−1,−½]. Exact gap: the heavy-block lemma.
  Search over 240k grammars: the best unambiguous L ⊆ G⁻ is Catalan (α=−3/2). Ambiguity-collapse example: context measure ∞ but word set = Dyck.

**Round 9 synthesis (root).** All three cores sharpened; none closed.
- P_cop (`R2/r9_pcop.md`): Theorem N, an explicit linear-ambiguity grammar that agrees with Q on all prime rows, so Theorem-U-type (row) arguments can't
  lift to polynomial ambiguity, and core (ii) contains core (i). Next: rows #a = 2q, where two witness checks can cross.
- Self-similarity (`R2/r9_selfsim.md`): exact transfers, so no amplification (Lemma RG needs sα > 1; the structure gives s = 1, α = ½). Gap = uniformity in depth k.
- Packing (`R2/r9_packing.md`): the unambiguous T8 reduces to the HEAVY-BLOCK LEMMA (a critical linear SCC fed by a heavy-tailed Dyck-like block
  language cannot keep every word in G⁻). Polynomial ambiguity needs a separate word-level argument (ambiguity-collapse example).
- Most concrete targets: heavy-block lemma (would give a clean new theorem: no unambiguous CFL inside G⁻ is rotation-dense); the 2q-row question.

## Round 10 (started 07:05 UTC). Reports `R2/r10_*.md`.
| task | owner / file |
|---|---|
| Heavy-block lemma (unambiguous T8) | R10-A, `R2/r10_heavy.md` |
| Rows #a = 2q: poly-ambiguous L ⊇ Cop agreeing with Q there? | R10-B, `R2/r10_2q.md` |
- R10-A heavy-block (`reports/r10_heavy.md`): NOT proved, no counterexample. Chord form W∈G⁻ ⟺ P(k)+P(n−k)<P(n); pair-model reduction. Two no-gos: Dyck-oriented giant blocks are offset-insensitive, and an injective critical two-tape model with a safe outer walk exists.
  So the contradiction must come from whole-word injectivity at the centre: every critical model seen fails by centre-shift ambiguity (w occurs inside heavy blocks). Search: `scripts/r10_heavy_*`.
- R10-B (`reports/r10_2q.md`): **Theorem N2** gives an explicit PCFL L** (amb ≤ |w|, via parity regions + new grammar G₂) with Cop ⊆ L** and L** ∩ {#a or #b ∈ P∪2P∪2^ℕ} ⊆ Q. This refutes the r9 §5 conjecture, so row-2q arguments are dead for ¬P_cop [proof + computational, |w| ≤ 16, rows 4/6/10/14 up to |w| ≤ 20].
- Equality form (L ∩ row 2q = Q ∩ row 2q) is OPEN. Lemma D (one counter: squares D = 0, q-th powers |D| ∈ q·ℕ⁺) reduces it to H₀ = {D=0}∩NonSq and H₊ = {|D|∈#a·ℕ⁺}∩Not2P. If it fails, Q ∉ PCFL, so this is a sub-problem of ¬P(Q), not of ¬P_cop.

**Round 10 synthesis (root).**
- Heavy-block (`R2/r10_heavy.md`): not proved; no-go 1 (Dyck giant blocks are offset-insensitive) and no-go 2 (natural heavy-tailed constructions become
  ambiguous through centre-word recurrence). Gap: centre-shift rigidity.
- 2q rows (`R2/r10_2q.md`): Theorem N2, an explicit PCFL L** (amb ≤ |w|) with Cop ⊆ L** and L** sound on rows #a or #b ∈ P ∪ 2P ∪ 2^ℕ, refuting
  r9's conjecture and killing row-2q arguments for ¬P_cop. The EQUALITY form (EQ-2q: no PCFL agrees exactly with Q on all rows #a = 2q) is open; it implies ¬P(Q).
  Lemma D reduces it to H₀ (D = 0, non-squares) and H₊ (|D| ∈ #a·ℕ⁺, not 2-periodic) on even #b.

## Round 11 (started 07:28 UTC). Reports `R2/r11_*.md`.
| task | owner / file |
|---|---|
| EQ-2q: prove no PCFL matches Q exactly on rows 2q, or build one | R11-A, `R2/r11_eq2q.md` |
| Centre-shift rigidity (unambiguous T8) | R11-B, `R2/r11_rigid.md` |
- R11-A (`reports/r11_eq2q.md`): EQ-2q still **OPEN**. Lemma S: Q∩row_{2q} = ({D≠0}∩Not2P) ⊔ ({D=0}∩NonSq) [proof + computational, rows 4/6/10/14, |w| ≤ 20]. **Theorem T** [proof]: no *regular* (gap-saturated) sorter works. (C₁∩R₁)∪(C₂∩R₂)∪R₃ with C₁ ⊇ P_q, C₂ ⊇ Sq∩Not2P fails on every single row 2q.
- b-pumping route to ¬EQ-2q: the exact obstruction is P1–P3 (pump partner may contain a's; a pure-b partner in gap j ≢ i mod q is harmless; laminarity allows only O(1) square-neutral pumps, but they are not needed). It never uses ambiguity, so as it stands it would prove Q ∉ CFL. Missing piece: Theorem T (the sorter is not gap-saturated) gives no lower bound on amb(w).
- R11-B rigidity (`reports/r11_rigid.md`): NOT proved. No-go 3 [proof + check n≤16]: G⁻∩even is itself an injective critical heavy-tailed pair model (centre = middle, lazy-walk excursion tokens), so the abstract pair statement is FALSE; the correct target is FSC rigidity (heavy blocks one-tape and substitutable, finite-state coupling).
  Lemma Fac: full entropy ⇒ every w occurs ≥ εℓ times in almost all block words. Centre-count bound: mult ≤ Σ_c N(c), so centre shifts give ≤ n+1 collisions. The poly-ambiguity lift needs two-tape re-tokenisation, not centre shift. Scripts `scripts/r11_rigid_{lazy,mult}.py`.

**Round 11 synthesis (root).** Both targets sharpened; neither closed.
- EQ-2q (`R2/r11_eq2q.md`): Lemma S, an exact characterisation of row-2q primitive words via D (checked ~544k words). Theorem T: no regular sorter
  (restricted class). The pumping attempt never uses the ambiguity bound, so as it stands it would prove Q non-CF; the missing piece is turning T into a tree-count bound.
- Rigidity (`R2/r11_rigid.md`): No-go 3, G⁻ itself is an injective critical heavy-tailed pair model, so the abstract statement is false and only
  CF structure (tape-local block swaps + finite-state coupling) can help: "FSC rigidity". Centre absorption gives ≤ n+1 parses, so no iteration.
- 11 rounds in: the three cores stand as (i) uniform certification of typical words, (ii) P_cop ⊇ (i), (iii) FSC rigidity / EQ-2q tree-count lift.

## Round 12 (started 08:06 UTC).
| task | owner / file |
|---|---|
| FSC rigidity (CF-shaped pair models) | R12-A, `R2/r12_fsc.md` |
| Consolidated research note (rounds 2-11) + RESULTS_INDEX update | R12-B, `round2/RESEARCH_NOTE.md` |
- R12-B (`round2/RESEARCH_NOTE.md`, 831 lines): consolidated note for rounds 2–11 (statements with unchanged labels, three open cores, blocked routes, data, errata incl. 10 name collisions §6.8); `RESULTS_INDEX.md` §11 added (+ pointers in two existing rows). [assessment] no new results.
- R12-A FSC rigidity (`reports/r12_fsc.md`): NOT proved, no counterexample. Lemma SF [proof]: blocks with a realised context are fold-oriented (E⁺/high excursions impossible). Lemma Env+Ori ⇒ No-go 4 [proof + check]: for Dyck-oriented blocks (E, D⁻) substitution ≡ one flat word, so the high/low lever is void and G⁻ sees only block lengths.
  Prop HS [proof + check N≤20]: height-coupled FSC models (e.g. {(bEⁱ,Eʲa)}, No-go 2) are ambiguous via centre slide (≤ n+1 parses). Exact gap: "padding rigidity" for couplings richer than additive height. Script `scripts/r12_fsc_checks.py`.

**Round 12 synthesis (root).** Consolidated note written (`round2/RESEARCH_NOTE.md`, RESULTS_INDEX §11).
FSC rigidity (`R2/r12_fsc.md`): Lemma SF (self-fold) kills blocks with high excursions; No-go 4 (Env + Ori): for Dyck-oriented blocks, G⁻ membership depends
only on block lengths, so swapping high/low excursions cannot violate it; Prop HS: additive-height couplings are ambiguous (≤ n+1 parses, no poly lift).
Exact gap: "padding rigidity" (non-injectivity when the coupling carries more than additive height). T8_unamb still open.

## Round 13 (started 08:16 UTC).
| task | owner / file |
|---|---|
| Padding rigidity | R13-A, `R2/r13_padding.md` |
| Audit: Theorems N, N2; interval-fold Lemma F (r5); Lemma A (r6) | R13-B, `R2/audit_r13.md` |
- R13-B audit (`reports/audit_r13.md`): Thm N + L_P2, Thm N2 (G₂, L**), Lemmas F/M/A all **SURVIVE**. Own exact tree counts for all |w| ≤ 20 and semantic checks on non-primitive words |w| ≤ 40; Lemma M checked for every K with n ≤ 24; Lemma A checked for all words with n ≤ 20. 0 failures. Caveats: N2(c) is vacuous for |w| ≤ 16 (shortest extra has length 18; tested at 20/40); r6 drops the factor n in d_k; ε must be excluded at n = 0; N1 relies on the unaudited U′.
- R13-A padding rigidity (`reports/r13_padding.md`): Thm PR2 [proof mod Denisov–Wachtel cone bound]: under square-root block tails (T½), any critical FSC SCC with "level" blocks on both tapes (e.g. E, D⁻) and L ⊆ G⁻ is ambiguous (avg mult ≥ n^{1/6−ε}). Mechanism = measure squeeze: lag freedom (Lemma MS) ⇒ valley shape ⇒ wedge 3π/4 density n^{−2/3} (num. exp −0.666) vs renewal mass ≥ c√N (Lemma R, U(x) ≥ x/m(x)). PR1 [proof]: one-tape models likewise. One-sided case: sketch.
- R13-A gap: "steep" models (no level block words on either tape) and block tails heavier than ℓ^{−3/2}; T8_unamb still OPEN. No counterexample.

**Round 13 synthesis (root).** Audit: Theorems N, N2, Lemmas F, M, A SURVIVE (`R2/audit_r13.md`).
Padding rigidity (`R2/r13_padding.md`): Thm PR2 (two-sided level blocks), a measure squeeze: valley shape (Lemma MS) + 3π/4 wedge density O(n^{-2/3})
(Lemma K, cites Denisov–Wachtel) vs injective mass ≥ c√N (Lemma R) ⇒ contradiction; also rules out multiplicity O(n^{1/6−ε}). Thm PR1 (one-tape).
Open: steep models, tails heavier than ℓ^{-3/2}, one-sided conditional-moment step. First quantitative step beyond unambiguity on the fold route.

## Round 14 (started 08:32 UTC).
| task | owner / file |
|---|---|
| Gated audit of PR1/PR2 (+ Lemma K citation) | R14-A, `R2/audit_r14.md` |
| Steep models + heavier tails (remaining PR gap) | R14-B, `R2/r14_steep.md` |
- R14-A audit of r13 PR1/PR2: **SURVIVES w/ caveats** (MS lag-free per word OK; wedge 3π/4 exponent 2/3 confirmed by exact DP, m^{2/3}P→0.332; Lemma R/squeeze √N vs N^{1/3} OK; caveat: one-sided case only sketch, "all level-padded excluded" overstated) — `R2/audit_r14.md`
- R14-B steep (`reports/r14_steep.md`): premise "steep ⇒ drift≠0" false (bᵐaᵐ). Lemma PC [proof]: a cycle (v,y) with D(v)≥0, D(v)+D(y)≥0 ⇒ U-level (mirror V). Lemma Bot + Prop HL [proof]: every heavy block contains a critical nonlinear SCC and is U-level, V-level, or log-level on both sides (doubling T_{k+1}=αT_kβT_kγ).
- R14-B: Thm PR2ˡᵒᵍ [proof mod uniform Denisov–Wachtel bound]: PR1/PR2 survive log (even n^γ, γ<1/8) slack. Open: side mismatch (a U-side heavy block that is only V-level), tails ℓ^{-1-2^{-k}} k≥2 (squeeze N^{1/4} vs N^{1/3}), one-sided step. T8_unamb OPEN.

**Round 14 synthesis (root).** PR1/PR2 audited (SURVIVES; wedge exponent 2/3 confirmed independently). Steep gap (`R2/r14_steep.md`): Lemma PC, Lemma Bot
(heavy block ⇒ critical nonlinear SCC), Prop HL (every heavy block is U-, V- or log-level on both sides), PR2^log (log / n^{γ<1/8} slack).
T8_unamb remaining: (1) side mismatch (U-side block only V-level); (2) heavier tails −1−2^{−k} (squeeze N^{1/4} vs N^{1/3} fails); (3) one-sided conditional-moment step.

## Round 15 (started 08:43 UTC): close T8_unamb.
| task | owner / file |
|---|---|
| Side mismatch (zero-drift / cosh-tilt) | R15-A, `R2/r15_side.md` |
| Heavier tails −1−2^{−k} | R15-B, `R2/r15_tails.md` |
| One-sided conditional-moment step | R15-C, `R2/r15_onesided.md` |
- R15-C `reports/r15_onesided.md`: **Thm PR1s** (one-sided padding: U-level block + π(v≠ε)>0 + (T½) + G⁻ ⇒ ambiguous), written proof modulo the same DW survival bound as PR2; the conditional-moment step (Lemma CM, E[(s_m+1);τ_W>m] = O(m^{−1/6}√log m)) is proved by truncation plus Hoeffding, with no DW conditional limit. Also: one-tape U-level-only models (§4).
- R15-C checks: `scripts/r15_onesided_moment.py` (DP m ≤ 128: M1·m^{1/6} → 0.35, J·m^{1/6}K^{1/2} ≈ 0.355, stable); `scripts/r15_onesided_models.py` (3 one-sided families, all (p,w,q) with |·| ≤ 2: each fails by n ≤ 12). Closes r13 §6.3 / audit_r14 C1. T8_unamb is still OPEN.
- R15-A side (`reports/r15_side.md`): **side mismatch CLOSED [written proof]**. Thm SM: if D ≤ M on L(Y) (Y in critical nonlinear SCC), potential h makes every C*-rule slack 0 (slack rule ⇒ radius >½ by PF-strict + Hoeffding), so e=0 is attained; hence U-side heavy ⇒ U-(log-)level, mirror V. Checks: all 18,746 Polish grammars (4 bounded ⇒ D const). Open: one-sided, tails, T8_unamb.
- R15-B tails (`reports/r15_tails.md`): B–D Thm 3 checked (finite-μ ⇒ n^{−1−2^{−k}}); r14 mechanism corrected — heavy tails = k stacked critical NONLINEAR SCCs (Lemma ST; critical linear below finite-μ impossible). Prop S: G⁻∩Valley alone can't squeeze β ≤ 1/3 (n^{−2/3} sharp). Thm PR2^β [proof mod DW]: quadrant phase m^{−1/3}n^{−2/3} ⇒ closes balanced tapes (all k) and k=2 with lighter tape 2^{−1}.
- R15-B OPEN: unbalanced two-tape, heavy 2^{−k} (k≥3) vs lighter 2^{−j}, j<k; k=2 with exponentially light tape is exactly borderline (N^{1/4} vs N^{1/4}). One-tape heavy: PR1 covers all k.

**Round 15 synthesis (root).** T8_unamb narrowed to one case.
- One-sided case CLOSED: Thm PR1s (`R2/r15_onesided.md`, Lemma CM via truncation + Hoeffding, Lemma J; mass O(N^{5/12}√log N) vs c√N).
- Side mismatch CLOSED: Theorem SM (`R2/r15_side.md`, slack argument: positive slack ⇒ subcritical).
- Heavier tails PARTLY (`R2/r15_tails.md`): Banderier–Drmota citation verified; tails come from stacked critical NONLINEAR SCCs (Lemma ST; r14's linear
  mechanism corrected); Thm PR2^β closes all balanced two-tape cases (quadrant phase, Lemma QW, Lemma Bal). Open: unbalanced two-tape (k ≥ 3 vs j < k;
  k = 2 with exponentially light tape is borderline N^{1/4} vs N^{1/4}).

## Round 16 (started 08:53 UTC).
| task | owner / file |
|---|---|
| Unbalanced two-tape tails (last T8_unamb gap) | R16-A, `R2/r16_unbal.md` |
| Gated audit: PR1s, Theorem SM, PR2^β | R16-B, `R2/audit_r16.md` |
- R16-B audit (`reports/audit_r16.md`, `scripts/audit_r16_dp.py`): PR1s SURVIVES (Lemma CM/J recomputed by own DP, M1·m^{1/6}→0.34, E[s;τ>m]·m^{1/6}≈0.32; minor fix for m≤n<4m); Theorem SM SURVIVES (rare/frequent bounds uniform; lower SCCs analytic so non-SCC system fine; Step 3 yields a NEW form with e=0); PR2^β SURVIVES (QW own DP m^{1/3}T^{2/3}P∈[0.82,0.97]; 2^j>2^k−3 bookkeeping correct; ST(i) write-up imprecise, conclusion right). All modulo cited DW.
- R16-A unbal (`reports/r16_unbal.md`): Lemma MS⁺ — r13's MS proof bounds A ≤ C_U, B ≥ −C_V for ALL k ≤ n/2 (not just U/V positions) ⇒ L ⊆ quadrant, density c/n, mass O(log N) ≪ N^{β₀}: Thm PR2⁺ closes ALL two-sided level cases (every k, balanced or not, incl. k=2 borderline), no DW needed.
- R16-A FLAG: one-sided HEAVY (U-level only, q_V>0, β₀ ≤ 1/4) not covered (wedge n^{−2/3} vs N^{β₀}); confirm the T8_unamb reduction handles it or list as open.

**Round 16 synthesis (root).** Audit: PR1s, SM, PR2^β SURVIVE (`R2/audit_r16.md`). Unbalanced tails (`R2/r16_unbal.md`): Lemma MS⁺ (the frozen bound holds at EVERY
k ≤ n/2 ⇒ quadrant {A ≤ C, B ≥ −C}, density ≤ c/n, mass O(log N)) ⇒ Thm PR2⁺ closes ALL two-sided cases, elementary, no Denisov–Wachtel. Last gap of T8_unamb:
one-sided HEAVY models (U-level only, q_V > 0, β₀ ≤ 1/4); PR1s assumes (T½).

## Round 17 (started 09:05 UTC).
| task | owner / file |
|---|---|
| Gated audit of MS⁺ / PR2⁺ (+ T8_unamb assembly) | R17-A, `R2/audit_r17.md` |
| One-sided heavy models (last T8_unamb gap) | R17-B, `R2/r17_oneheavy.md` |

**Round 17 PAUSED by the user** (agents stopped before reporting; audit of MS⁺/PR2⁺ and the one-sided heavy case not done).

## Round 17b (restarted 09:39 UTC, 6 agents in parallel). Reports `R2/r17_*.md`.
| task | owner / file |
|---|---|
| Gated audit MS⁺ / PR2⁺ | A, `R2/audit_r17.md` |
| One-sided heavy: half-plane × chord region (MS⁺ extension) | B, `R2/r17_oh_region.md` |
| One-sided heavy: force the non-level tape to be log-level (SM/HL route) | C, `R2/r17_oh_level.md` |
| One-sided heavy: computational counterexample search | D, `R2/r17_oh_search.md` |
| Lift T8 from unambiguous to polynomial ambiguity | E, `R2/r17_lift.md` |
| Bridge: every poly-ambiguous grammar for Q contains a dense fold-type part? | F, `R2/r17_bridge.md` |
