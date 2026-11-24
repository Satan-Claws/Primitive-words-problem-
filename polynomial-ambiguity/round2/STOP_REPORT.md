# Round 2 stop report: polynomial ambiguity of Q

Session 2026-11-24, 00:11–01:36 UTC. Five waves, 22 agents and two gated audits. The task is `prompt.md`; the log is `REGISTRY.md`;
reports are in `reports/` (cited as `R2/`). `PA/` = `../claude_2026-11-18_to_11-19/reports/`.

**The problem is not resolved.** Neither resolution of prompt §3 is proved. No route was unblocked.

The main change this round: the negative programme's candidate S_N (n = P_N²) is now blocked at the per-slice level near U, by an audited result.
Two pieces are still open there: the mixed-type region (G-glob′) and uniformity across n.

## 1. Strongest rigorously proved statements

**Theorem P (unchanged, now reconstructed)** [written proof; foundations reconstructed in `R2/recon.md`].
For every cycle-free CFG G with L(G) = Q, A_G(L) = Ω(√(log L / log log L)).
- Structure (c) without finite ambiguity, and Lemma 3P, are CONFIRMED.
- Lemma F is REPAIRED: face offsets are only ≤ 2mK. Cor F′ gives ply ≥ p at norm 2m + m·exp(O(p² log pK)). Theorem P survives with m = 2p − 1.
- The S3D refinement to d_σ = 0 keeps ply but loses the offset bound.

**Theorem T (TILE_k with ply 1)** [audited report: `R2/tile2.md` + `R2/audit_tile2.md`, SURVIVES with fix C1].
- Hypotheses: μ has zero fold and no identically balanced proper (cyclic) arc.
- Selection rule: non-crossing bichromatic trees that are dual-feasible for the transport cost c_ij = h(|y_i − y_j|), with h increasing and strictly concave, and the root at a positive vertex.
- Conclusion: these trees have validity cones that tile the region with ply exactly 1. Walls follow the lex rule with η ∈ W.

**Theorem BD (bounded-data tiling of S_N near U)** [audited report: `R2/realise.md` part (1) + `R2/audit_realise.md`, SURVIVES near U].
- Facets: pair facets μ_k = (1 − T^{n/p_k})ν_k, one ±1 per fibre in nested windows. These satisfy Lemma C for all N.
- The tiling of Theorem T then uses ring vectors of ℓ¹-norm ≤ 2 (K = 2 for every n), offsets ≤ 2n, and unimodular bases.
- Total ply is ≤ n^{1+o(1)}. The Littlewood–Offord / VC step (Lemma 4) is a sketch.
- Consequence: near U, no per-slice condition known to the programme (Lemma 3P data bounds, ply, laminarity) can separate Q from a polynomially ambiguous grammar on S_N.
- Extension: `R2/global.md` G1 ([written proof], multi-root slack forests) extends this to all of (U ⊕ ⊕E_k) ∩ ℕⁿ.

**Other new results** [written proof unless marked]
- Constructive covers.
  - n = pq: laminar cover of Q ∩ (ab*)^{pq} with ply ≤ n + φ(n) (`R2/construct.md`).
  - n = 36: explicit 72-system cover, ply ≤ 2n + φ(n) (`R2/construct36.md`, Lemma 36). The mechanism grows like n^{N/2}, so this does not extend to S_N.
  - Transfer atoms, Lemma FT: fibre-supported pqr vectors (`R2/construct2.md`).
- **NonPow_p grammar:** for each prime p, {w ≠ u^p} has a uniform CFG with amb(w) = #{i : w[i] ≠ w[i + n/p]}, which is exactly linear (`R2/uniform.md`).
- **Theorem U:** no *unambiguous* CFL L has {gcd(#a,#b) = 1} ⊆ L ⊆ Q (`R2/pcop.md`). This strengthens Petersen; it does not count toward the target.
- **Restricted-class results** (do not count, prompt §7).
  - Theorem W: no CFG exposes one mismatch pair per prime for two primes (`R2/uniform.md`).
  - Theorem R: no CFG marks ≥ 3 positions at fixed fractions of n on an infinite language (`R2/l6.md`).
  - Theorem S: L₆ is not a finite Boolean combination of NonSq/NonCube with regular sets (`R2/l6.md`).
- **Reductions.**
  - T1 (`R2/cyclic.md`): restricted to gcd ≥ 2 classes, or to balanced classes, the problem is the full problem.
  - Lemma D (`R2/finv.md`): asymptotic density of pieces transfers to short witnesses. Ray-asymptotic ply does not (CRT counterexample).
  - Lemma G5 (`R2/gglob.md`): mixed-type certification reduces to the choice of a single non-crossing matching.
  - Theorem S1 (`R2/gglob_ii.md`): the signed forest tiling is a network-flow (TU) problem, giving ply 1 under (H1) ±1 facets and (H2) a connected face graph.

## 2. Exact remaining gap

**For the negative resolution via S_N**, two statements remain. Both would have to FAIL for S_N to survive:

> **G-glob′.** Let n = P_N², V_k = {y ∈ ℝⁿ : y shift-(n/p_k)-invariant}, and, for a non-crossing perfect matching M of ℤ_n,
> L(M) = span{e_p + e_q : pq ∈ M}.
> - **(i)** There is a distribution 𝒟 on non-crossing matchings, depending only on n, with
>   Pr_{M∼𝒟}[∀k: y ∉ V_k + L(M)] ≥ n^{−O(1)} for every primitive y ∈ W_n.
>   - This reduces to Lemma I2 (`R2/gglob_i.md`): some set S of ≤ 2N pairwise non-adjacent positions contains, for every k, a pair a ≡ b (mod n/p_k) with z_a ≠ z_b, where z_x = y_x − y_{x+1}.
>   - Proved for N = 2.
> - **(ii)** The signed slack-forest tiling of `R2/gglob_ii.md` holds without (H2): when the support's face graph in M is disconnected (obstruction O1, a separating chord).

**Uniformity (NONUNIF).** Even if S_N is blocked per slice, a negative proof could still come from showing that no single grammar realises the per-slice covers uniformly in n (`R2/realise.md` U1–U3).
- Theorem R reduces to pumping and gives no such mechanism (`R2/thmR_unif.md`).
- Lemma N: low-span (≤ 2) non-crossing facet trees exist, so fixed-fraction chords are never forced.
- NONUNIF is equivalent to the S_N negative statement, and it is open.

**For the affirmative resolution**, the remaining work is:
- a single grammar that is uniform across all n;
- certification of the second prime without exposing witnesses (L₆ = NonSq ∩ NonCube ∩ Σ^{6ℕ} is open, `R2/l6.md`);
- the off-W_n part, lower strata, and all n, not only P_N².

## 3. Approach families

| family | mechanism | status | where and why it stalled |
|---|---|---|---|
| TILE_k | ply / covering | RESOLVED (ply 1), audited | transport rule; S_N blocked geometrically (`R2/tile2.md`) |
| Bounded data near U | realisability | RESOLVED near U, audited | pair facets K = 2 (`R2/realise.md`) |
| Global / mixed types | ply / covering | OPEN: G-glob′ (i) I2, (ii) H2 | `R2/global.md`, `R2/gglob*.md` |
| Other slice families | ply | BLOCKED | DFA sub-slices, deep prime powers, lower strata and 2-prime defects all reduce to S_N (`R2/newslice.md`) |
| G3** length | length / lattice | REDUCED | Prop BC conditional; refinement kills ply-set arguments; density transfers, ray ply does not (`R2/g3.md`, `R2/finv.md`) |
| KKM / Sperner | topology | BLOCKED | half-open cones (`R2/tile.md`) |
| Multi-split inside/outside | structural | BLOCKED | criterion W suffices, but both branches hit §6 routes (`R2/newmech.md`) |
| Cyclic closure, P_cop | reformulation | REDUCED / OPEN | gcd ≥ 2 = full problem; P_cop not shown equivalent (`R2/cyclic.md`, `R2/pcop.md`) |
| Uniformity (NONUNIF) | uniform realisation | OPEN | ≡ S_N negative; Theorem R collapses to pumping (`R2/realise.md`, `R2/thmR_unif.md`) |
| One-prime / two-prime grammars | constructive | 1 prime done; 2 primes open | Theorems W, R, S (`R2/uniform.md`, `R2/l6.md`) |
| Test grammars (task G) | measurement | DONE | neither generates Q (`R2/testgram.md`) |

## 4. Witness families and counterexamples

- **Audit C1:** N = 2, k = 1, ν = [−30, 24, −3, −17, 44, −44, −1, 50, 39, 25, 26, −19] gives μ_{v₀} = −60. Rooting at v₀ makes every tree invalid.
- **CRT pieces** (`R2/finv.md` §3): chain {2e_j + e_{j+1}} ∪ {e_0 + e_t}, D_t = 2^t − 1. These give large ply far out and small ply near the apex.
- **Stanley refinement** (`R2/g3.md` §3): puts chain pieces with E = h = 2^ρ into every ply-set while f is unchanged.
- **n = 30 fibre vectors** (`R2/construct.md`): x0 = 2e_0 + e_10 + e_15 + e_20. Not covered by conjunctive atoms; covered by a transfer atom.
- **Lemma G6** (`R2/gglob.md`): a primitive y at n = 36 that neither adjacent matching certifies for all k.
- **O1 separating chord** (`R2/gglob_ii.md`): M = {(1,2), (0,3), (4,5)}, μ = z_a − z_b. The points (k+1, 0, k) need infinitely many pieces.
- **walk.md:** C_exp witness K ⇒ YXYX·K, two ways. The repaired grammar has amb ≤ n^{k+1} but L ⊊ Q.
- **builder3:** first misses are two necklaces at n = 26.
- **L₆ partial grammar** C_k: amb ≤ 7n/6 + 1, misses a⁶(bᵏaᵏ)⁶.
