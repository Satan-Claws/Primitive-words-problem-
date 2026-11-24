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
