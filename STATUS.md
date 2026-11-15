# Status: primitive words not context-free (Dömösi–Horváth–Ito conjecture)

**Not solved.** Both `sorry`s in `PrimitivePDA_Negative.lean` remain. The conjecture has been open since 1991, and no 2023–2026 resolution was found.

## Verified
- `PrimitivePDA_Negative.lean` compiles against Mathlib (Lean v4.36.0-rc2, built from source) with only the two intended `sorry` warnings. The full `import Mathlib` was replaced by the needed modules for the check.
- The formalization was reviewed by hand and is faithful (finite PDA and Mathlib CFG). It has no loophole that makes it trivially true or false.

## Agent results (red-teamed; see `research/reports/`)
- **scout**: literature map.
  - Kászonyi–Katsura conjecture (Q ∩ (ab*)^n is CF for all n): proved for n with at most 3 prime-power factors, and reportedly when Σ1/p < 4/5. n = 210 appears open.
  - Q satisfies Bar-Hillel, Ogden, Bader–Moura and the interchange lemma.
- **rectangles**: two barrier results.
  - Proved: Q ∩ Σ^n is a union of 2⌈n/3⌉ balanced rectangles inside Q (Fine–Wilf, tight). So rectangle, fooling-set, discrepancy and interchange arguments cannot work.
  - Q ∩ Σ^n has NFAs with n^{2+o(1)} states.
  - In any CNF grammar for Q, the number of excess parse trees per length grows exponentially infinitely often (limsup). This strengthens Petersen's unambiguity result.
- **closure**: barrier.
  - Theorem B: every rational-transduction image of Q has a semilinear Parikh image. It may be new; the literature was not checked thoroughly.
  - Consequently no Parikh or closure reduction from Q gives a non-CF language. In particular {a^p : p prime}, {a^n b^m : gcd(n,m)=1} and {a^n b^n} are not obtainable.
- **devil**: no CFG or PDA for Q was found.
  - "No bounded certificate": at least ω(n)+1 letter checks are needed, and a PDA cannot tie two mismatch distances to the length.
  - Independent barriers R1–R5 against the rectangle and interchange routes.
- **bounded**:
  - Lemmas L1–L6: Ginsburg's theorem for arbitrary words, and an obstruction criterion for the stratified structure of E_n.
  - Exact certificates show the obstruction fails for n ≤ 30, which is evidence that Kászonyi–Katsura is true.
  - L7–L9 are sketches only.

## Red-team verdict
An independent red-team agent re-derived the proofs by hand and wrote its own scripts, sharing no code with the authors. It found no counterexample and no broken step in any result marked PROVED. Caveats:
- The parse-tree growth holds only infinitely often (limsup), not for every length.
- bounded L7–L9 are sketches, not complete proofs.
- devil R4 has a wording slip: the inner length is ⌈n/3⌉.

## Remaining routes
Any proof must exploit non-uniformity across lengths n, because each fixed length is "easy". Open targets:
- Kászonyi–Katsura at n = 210 (a counterexample would prove the conjecture);
- finite ambiguity;
- density statements for CFLs (Sin'ya's route).
