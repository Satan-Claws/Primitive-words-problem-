# R2/audit_realise: gated audit of R2/realise.md part (1) (pair facets, bounded data, ply)

**Verdict: SURVIVES** (part (1), as scoped: the near-U S_N region x = tω + δ, δ ∈ ⊕E_k, in tile2's R⁰).
No fatal flaw. Non-fatal caveats below. Re-ran `realise_bounded.py 4 2`: all checks reproduce.

## The crux: does a pair-facet family carve out δ_k ≠ 0?
- A *single* pair facet does not. Its kernel on E_k is a hyperplane: any δ_k whose fibre functions satisfy
  f_a(x_a) = f_a(x_a + c_k) at the chosen x_a = i_a mod p_k has μ_k(δ_k) = 0. This is the same for LAM's facets:
  T2a/LAM's local form is per-facet a half-space, and coverage of ∏(E_k∖0) is a property of the *sampled family*.
- The family does cover. Take δ_k ≠ 0; some f_a is non-constant on ℤ_{p_k}. Since c_k ≠ 0 generates ℤ_{p_k},
  f_a(x) ≠ f_a(x + c_k) for at least 2 residues x, and x_k(i_a) is uniform when i_a is uniform on a window of p_k
  consecutive indices. So q := Pr[some d_a ≠ 0] ≥ 2/p_k. Given that, flipping one ε_a changes u, so Pr[u = 0] ≤ 1/2,
  and by ε-symmetry Pr[u_k(δ_k) > 0] ≥ q/4 ≥ 1/(2p_k) (better than the report's 1/(4p_k)); ≤ 1/2 always.
- Ranges {σ : u_{σ,k}(δ_k) > 0 ∀k} are intersections of N homogeneous half-spaces in E_k (VC dim ≤ d_k + 1), so
  T2a's relative approximation applies: ply_VC = O((β/α)·D·log) = 2^{O(N)}·P·√n·polylog = n^{1+o(1)}. Checked.
- Lemma 1 (⊥ U, V_{p_k}, E_j; ≠ 0 on E_k): correct; each pair is in one fibre on one x_k-line.
- Lemma 2 (Lemma C, all N): correct, and stronger than needed. A fibre with one point in I gives a nonzero
  fibre-sum (U-part); a fibre with both gives f ↦ f(x) − f(x + c_k) ≠ 0 on E_k^{(a)}. Moreover, since b_a and
  b_a + s_k have the same relative order (no wrap), no proper arc has zero U-part, so every non-root edge form is
  nonzero already on U (the audit_tile2 "cluster-cut forms ≡ 0 on U" caveat does not arise).
- With root at a positive vertex (μ = +1), Σ μ_p x_p = τ, the tree system is exactly tile2's TP(m') with
  m'_t = x_t − τ, so Thm A(i)/B(ii) + C1 give q_k = 1. Lemma 3(a)–(e) verified (unimodularity via TU of the bipartite
  incidence + e_t with μ(e_t) = 1; L_σ ⊆ {μ_k ≥ 1 ∀k} needs disjoint supports, which nesting gives).
- Nesting inequality: rechecked exactly; windows of width p_k nest for N = 4..12 (also N = 5, which the report's
  "N = 4 and N ≥ 6" omits), fail at N = 3.

## Non-fatal caveats
1. **N = 3 script family does not cover.** With window width 1, x_a is fixed, so e.g. k = 3 (p = 5) and
   δ_3 = e_{r'} − e_{r''} on one fibre with r', r'' ∉ {r_0, r_0 + c_3} is killed by every facet. The N = 3 exact
   checks are structural only; coverage (Lemma 4) needs width p_k, i.e. N ≥ 4. Say so.
2. **Scope of "blocked".** Coverage is only on R⁰ (x_t > τ_k at the root for every k, near U). Points of W far from U
   (τ_k > max over positive t of x_t) are in no piece of this family; off-W points are untreated. Both are listed in
   §3, but the verdict line "S_N blocked under every per-slice condition" should carry "near U_{>0}, modulo
   realisability and G3**".
3. **ply_VC is n^{1+o(1)}, not √n·polylog**; the 2^N factor and P from α are where the loss comes from. Fine for poly.
4. **Lex walls**: the {0,1} offsets implement S2P §1(b) per edge with one generic η ∈ W; this is consistent because
   every edge form is nonzero on W (Lemma 2), but the report does not spell it out.
5. Lemma 4 is a sketch (constants, VC dimension of the product range space, and the integer-point version of the
   relative approximation are asserted, as in T2a).
6. The unrestricted claim "Lemma C for all N" is for the *pair-facet* family only; Hypothesis H for LAM's μ_k
   (R2/lemmaC.md) is untouched and no longer needed.

## Files
- Audited: `polynomial-ambiguity/round2/reports/realise.md` §1; script `round2/scripts/realise_bounded.py` (`… 4 2` rerun).
