# Audit: R3-C `r3_i2.md` (Lemma I2 for all N ⇒ G-glob′ (i))

Gated audit, 2026-11-24. Independent script: `round2/scripts/audit_r3_i2_sat.py` (SAT existence check of I2,
no CRT/residue structure used in the check).

**Verdict: SURVIVES (with caveats).** No fatal flaw found.

## Checklist
1. **z ∈ V_k ⇔ y ∈ V_k.** z s-periodic ⇒ w_x := y_x − y_{x+s} satisfies w_x = w_{x+1}, so w ≡ c; summing w over an
   s-class telescopes to 0 = p·c ⇒ c = 0 (any field of char 0, so ℝ vs ℕ is irrelevant). Converse trivial. ✔
2. **CRT model.** x = r + P t; x+1 = (r+1) + P t for r < P−1 and = 0 + P(t+1) for r = P−1 (incl. x = n−1 → 0),
   so F4 (t′ = t + ε·(1,…,1) in CRT coordinates) is exact, and adjacency is decided in ℤ_n positions, not
   residues. Shift by s_k = P·(P/p_k) is t ↦ t + P/p_k, changing only coordinate k and generating ℤ_{p_k} (F1). F2
   (u_r factors through t_{K_r}) ✔. A k-witness exists in R_r iff k ∈ K_r ✔.
3. **Case analysis.** Minimum cover I has |I| ≤ N < P, so adjacent pairs in I form paths, never the full cycle.
   - |I| ≥ 3: minimality ⇒ no adjacent pair covers ⇒ shared free coordinate m; setting (φ_{r+1})_m = (φ_r)_m+ε+1
     makes t′_m ≠ t_m + ε for every chosen pair across the edge, hence non-adjacent positions (F4), valid also for
     p_m = 2 (paths are bipartite; each variable fixed by its unique predecessor). ✔
   - |I| = 2 non-adjacent, |I| = 1: no conflicts ✔. Only predecessor→successor adjacency exists (P ≥ 6).
   - |I| = 2 adjacent (Case B): A_o, B_o non-empty and disjoint; projection count |Π| ≤ 2|B_o| < ∏_{B_o} p fails
     only for B_o = {k: p_k = 2}; both options failing would need A_o = B_o. ✔ (The "both B-sets are the p = 2
     coordinate" scenario is exactly this, and it is impossible by disjointness.)
4. **Probability.** S non-consecutive ⇒ S and N(S) = (S±1)∖S disjoint; Pr[S ⊆ A] = 3^{−|S|}(2/3)^{|N(S)|} ≥
   (1/9)^N (16/81)^N = (16/729)^N ✔. I0: a ≡ b mod s_k ⇒ a+1 ≡ b+1, so μ ⊥ V_k; μ ⊥ L(M) (μ·(e_a+e_{a+1}) = 0
   etc.); μ(y) = z_a − z_b ≠ 0 ✔. Bound is uniform in y (depends only on N) ✔.
5. **Use downstream.** I1 + I2 prove G-glob′ (i) exactly as stated in `gglob.md` §4 (Pr ≥ n^{−O(1)} uniformly over
   y ∉ ⋃V_k): for primorial P, (16/729)^N = n^{−O(1/ln ln n)}; for any squarefree P, N ≤ ½log₂ n gives ≥ n^{−2.76}.

## Independent adversarial search [computational]
SAT (minisat22): one witness pair per k, no two cyclically consecutive points.

| n (primes) | family | primitive instances | I2 failures |
|---|---|---|---|
| 36 (2,3) | **exhaustive**: arbitrary binary u on 2 adjacent residues, all 6 start residues (incl. wrap) | 24 120 | 0 |
| 36 (2,3) | random sparse binary u on runs of 3–6 adjacent residues | 19 384 | 0 |
| 36 (2,3),(3,2); 100 (2,5) | private chains / point masses / random K_r on adjacent runs | 1798, 1851, 1237 | 0 |
| 900 (2,3,5),(3,2,5),(5,3,2) | same | 284, 216, 135 | 0 |

## Caveats (non-fatal)
- **C1 (downstream, not this report's fault).** `gglob.md` says "factor C per halving ⇒ ply n^{O(log C)}". With
  C ≈ 1/Pr = (729/16)^N, log C = Θ(N) and that formula gives n^{Θ(log n/log log n)}, not poly; with the stated
  target n^{−O(1)} it would be n^{O(log n)}. So (i) as stated is now proved, but whether (i) at this strength feeds a
  *polynomial* ply bound is unresolved in gglob.md's interface (how 1/Pr enters the per-halving factor — e.g. via a
  derandomised family of n^{o(1)}·poly size covering all ≤ n^{2N} admissible S — must be spelled out). G-glob′
  overall remains open anyway because of (ii).
- **C2.** 𝒟 needs n even (2 | P) for a perfect matching; the "any squarefree P" remark applies to I2 only.
- **C3.** The script's cover for size ≥ 3 is greedy + inclusion-pruned, not minimum; the proof needs only "no
  adjacent pair of I covers", which the script states it enforces. Computation is corroborative only.
