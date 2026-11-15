# Status: primitive words not context-free (Dömösi–Horváth–Ito conjecture)

**Not solved.** Both `sorry`s in `PrimitivePDA_Negative.lean` remain. The conjecture has been open since 1991, and no 2023–2026 resolution was found.

## Verified
- `PrimitivePDA_Negative.lean` compiles against Mathlib (Lean v4.36.0-rc2, built from source) with only the two intended `sorry` warnings. The full `import Mathlib` was replaced by the needed modules for the check.
- The formalization was reviewed by hand and is faithful (finite PDA and Mathlib CFG). It has no loophole that makes it trivially true or false.

## Agent results (unrefereed; see `research/reports/`)
- **scout**: literature map. The Kászonyi–Katsura conjecture (Q ∩ (ab*)^n is CF for all n) is proved for n with at most 3 prime-power factors; n = 210 looks open. Q satisfies Bar-Hillel, Ogden, Bader–Moura and interchange.
- **rectangles**: barrier, proved and exhaustively checked for n ≤ 22. Q ∩ Σ^n is a union of 2⌈n/3⌉ balanced rectangles inside Q, using Fine–Wilf. So rectangle, fooling-set, discrepancy and interchange arguments cannot work. Q ∩ Σ^n has n^{2+o(1)}-state NFAs. In any grammar for Q the number of extra parse trees grows exponentially, which strengthens Petersen.
- **closure**: barrier. Every rational-transduction image of Q has a semilinear Parikh image, so no Parikh-based reduction works.
- **devil**: no CFG for Q found. Barriers against the rectangle and interchange routes, plus a "no bounded certificate" result.
- **bounded**: partial lemmas on E_n (stratified-set structure); no counterexample to Kászonyi–Katsura.

## Remaining routes
Any proof must exploit non-uniformity across lengths n: no single grammar can handle all prime-factor patterns. Concrete targets are Kászonyi–Katsura at n = 210, finite ambiguity, and density statements for CFLs.
