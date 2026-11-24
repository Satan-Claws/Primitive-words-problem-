# audit_foundations_r9r10.md — R17b gated audit of the T8_unamb foundations (r9 §1–3, r10 §2)

Script: `scripts/audit_found_r9_checks.py` (|G⁻_n|·√n/2ⁿ → 0.3987 ≈ (2π)^{-1/2} at n = 400; nonlinear critical SCC
Y → aYY | b has finite value 1 at z = ½; a 2-state critical linear SCC has ρ(M(½)) = 1 and first-return weight F_XX = 1).

## Verdict: **SURVIVES** with caveats C1–C5. No fatal flaw, no counterexample.

| item | verdict |
|---|---|
| Thm M (i) rotation-dense ⇒ μ = ∞ | SURVIVES (C1) |
| Thm M (ii) exponent −1 impossible | SURVIVES; the right reason is Puiseux, not the BD list (C1) |
| Lemma F (a) critical SCC is linear | SURVIVES; DLW not needed, and its hypotheses are not met as cited (C3) |
| Lemma F (b) ρ(M(½)) = 1 | SURVIVES |
| Lemma Rn (finite-mean renewal ⇒ |L_n| ≥ c2ⁿ i.o.) | SURVIVES (C4) |
| Cor H | SURVIVES. The β ≤ ½ part is labelled heuristic and is not used |
| r10 §2 pair model, (i)–(ii) injectivity | SURVIVES. "Equivalent" is an overstatement (C2) |

## Checks
**(a) Thm M(i).** Distinct conjugacy classes give distinct words of L, so |L_n| ≥ δ2ⁿ/n. Σ1/n = ∞ needs this for all large n, or
for a set of n with Σ1/n = ∞. If "rotation-dense" only means infinitely many n, (i) has to go through (ii); see C1.

**(b) Exponent −1.** No N-algebraic series has coefficients ~ c2ⁿ/n. The natural candidate −log(1−2z) is transcendental. Proof for
*any* algebraic f with f_n ≥ 0 (unambiguous ⇒ algebraic, by Chomsky–Schützenberger):
- Suppose μ = f(½) < ∞. Then f is bounded and continuous on |z| ≤ ½.
- So at each of its finitely many singularities on |z| = ½, the Puiseux expansion is analytic + Σ c(1 − z/ζ)^β with β ∈ ℚ_{>0} \ ℤ.
  It has no log terms.
- Transfer then gives f_n = O(2ⁿ n^{−1−β_min}) = o(2ⁿ/n).
- So μ < ∞ ⇒ |L_n| = o(2ⁿ/n) (all n), and (ii) holds.

The Banderier–Drmota list is not needed. Dominant singularities need not be at roots of unity, but this does not matter.

**(c) Lemma F.**
- (a), elementary proof.
  - The radius of every X is ≥ ½, since a reduced unambiguous G makes each L(X) unambiguous and |L(X)_n| ≤ 2ⁿ.
  - Suppose C is nonlinear, with a rule X₀ → …Y…Z… where Y, Z ∈ C. Fix derivations Y ⇒* αXβ, Z ⇒* α'Xβ' and X ⇒* α''X₀β''.
  - Then for z ∈ [¼, ½), y_X(z) ≥ c·y_X(z)², where c > 0 is uniform (lower values are monotone and positive).
  - So y_X ≤ 1/c, and by monotone convergence μ(X) < ∞.
- (b)
  - M(z) is entrywise continuous on [0, ½], by monotone convergence.
  - For z < ½, y = My + b with b ≥ 0, b ≠ 0, M irreducible and y finite. Perron–Frobenius then gives ρ(M(z)) < 1, so ρ(M(½)) ≤ 1.
  - ρ < 1 would make y(½) finite. Hence ρ = 1. C is a nontrivial SCC, because a trivial one has a finite value.

**(d) Lemma Rn.**
- Injectivity of (return sequence, lower choices) ↦ p u₁…u_r w v_r…v₁ q: distinct ones give distinct trees, hence distinct words.
  This includes the case of two first-return paths giving the same (u, v), which would make the word ambiguous.
- So f is a multiplicity-free word-pair measure, and F_XX = 1 for irreducible ρ = 1 (Seneta).
- f(0) = 0, since a zero-length return is a unit/ε cycle, i.e. infinite ambiguity.
- The mean is finite. Taboo submatrices have ρ < 1, and lower blocks have finite means, so F'(½) < ∞.
- Renewal theorem (period d) ⇒ |L_n|2^{−n} ≥ 2^{−|pwq|}u(n − |pwq|) → c > 0 on a residue class.
- This contradicts |G⁻_n|/2ⁿ ~ (2πn)^{−1/2}, which the script confirms numerically.

**(e) r10 §2.**
- (i) and (ii) follow exactly as in (d).
- The outer-walk lemma is immediate: d_k for k ≤ min(|pU|, |Vq|) reads only pU and Vq.

## Caveats
- **C1.** The definition of rotation-dense must be fixed: for all large n, or i.o.
  - For the i.o. form, Thm M(i) is valid only via (ii).
  - (ii) is valid by the Puiseux argument above.
  - The cited exponent list "−1 − 1/2^k, −1 + m/2^k" is a second-hand paraphrase. Replace it by the Puiseux / no-log argument.
- **C2.** "Equivalence" is overstated.
  - T8_μ ("|L_n| = o(2ⁿ/n)", count form) is *stronger* than T8_unamb (no rotation-dense L), since μ = ∞ does not imply rotation-dense.
  - r9 §1 is correct as stated (count form ⟺ T8_μ).
  - r10 §2's "T8_unamb is equivalent to: no pair model inside G⁻" is only ⇐ for rotation-dense T8. It is ⟺ for T8_μ.
  - A pair model inside G⁻ refutes T8_μ, not T8. The T8 proof uses only the valid direction.
- **C3.** Lemma F(a) cites DLW. DLW needs inputs analytic at the evaluation point, and lower components may have radius exactly ½.
  The citation is therefore inapplicable as written, but the conclusion holds by the elementary bound in (c). Replace the citation.
- **C4.** Lemma Rn and Cor H tacitly use the following facts, all of which hold:
  - G is reduced and cycle-free;
  - each L(X) is unambiguous;
  - ρ < 1 for the taboo matrices, giving the finite mean of the C-internal part.
- **C5.** Cor H's tail/β ≤ ½ statement is heuristic, as labelled. Nothing downstream may use it as proved.

Sanity on T8_μ itself: a bounded-window pair-walk (a regular constraint realisable by a linear grammar) has growth
(2 + 2cos(π/(K+1)))^{n/2} < 2ⁿ, so the obvious attempts to put μ = ∞ inside G⁻ lose exponentially. No counterexample to T8_μ found.
