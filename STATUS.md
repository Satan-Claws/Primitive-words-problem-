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

## Round 3: intermediate theorems (red-teamed in `research/reports/redteam2.md`)
Goal: prove substantial intermediate steps toward the full conjecture.

**Ambiguity (`ambiguity.md`). Confirmed by red team.**
- **Theorem A.** If a finitely ambiguous grammar G has L(G) ⊆ (ab*)^n, then its parse-tree-counting generating function in the block variables y_1..y_n is rational, and every irreducible denominator factor involves at most 2 variables, which are non-crossing (A′). The unambiguous case is known (Ginsburg–Ullian; Koechlin 2022). The finitely ambiguous extension appears new.
- **Theorem B.** If n has an odd prime factor, then Q ∩ (ab*)^n is inherently ambiguous: the denominator has the factor 1 − Π_{i≡1 mod n/q} y_i in q ≥ 3 variables. The case n = 3 is known (Makarov 2021; Koechlin 2022).
- **Theorem C.** For an odd prime p, Q ∩ (ab*)^p is a union of two unambiguous CFLs, so its inherent ambiguity is exactly 2. Slices with prime n can give nothing beyond "not unambiguous".
- **Open target this points to:** the inherent ambiguity of Q ∩ (ab*)^n is unbounded in n. That would make Q not finitely ambiguous.

**Density (`density.md`). Confirmed by red team.**
- **Theorem 1.** Let L have a (p,q)-fixed-rate linear grammar (this includes regular and even-linear languages) with growth rate 2. Then there are u0 ∈ L and D ≥ 1 such that u0(v u0)^{Dj} ∈ L for every word v and every j ≥ 0. So L contains infinitely many non-primitive words. This generalises Sin'ya's regular-language theorem.
- **Theorem 2.** The same holds for the class FR: closures of fixed-rate linear languages under union and concatenation, and ultralinear grammars with fixed rates. Corollary: Q ∉ FR.
- **Limits.** Density does not force any fixed power. Growth rate alone fails outside FR: E' = {|w|_b = |w|_a + 1} is DCF with growth rate 2 and contains only primitive words.
- **Open target:** the same statement for general (mixed-rate) linear CFLs. It reduces to a Boolean-matrix lemma.

**Finite index (`finiteindex.md`). Not red-teamed.**
- Q ∩ (b*a)^m b* is not linear for any m ≥ 2. This re-proves Horváth's non-linearity of Q.
- For prime m, that slice is metalinear of width 2.
- Barrier: every bounded CF slice of Q has finite index. So a proof that Q is not of finite index must show the index grows across slices.

## Novelty check (web search only)
The key papers could not be fetched: Koechlin (FSTTCS 2022) and Koga (Acta Cybernetica 2022) are on hosts blocked by the network policy. Verdicts rest on abstracts and snippets.
- **Ambiguity Theorem A, unambiguous case: KNOWN.** Koechlin's "three-variable criterion" for bounded languages. The finitely ambiguous extension was not found anywhere: **probably new, unconfirmed**.
- **Ambiguity Theorem B: LARGELY COVERED.** Koechlin uses primitive words as an example (Props 14 and 17). n = 3 is Makarov (DLT 2021). The general statement for every n with an odd prime factor may be a routine extension of Koechlin's method. **Weakly new at best.**
- **Ambiguity Theorem C (inherent ambiguity exactly 2 for prime p):** not found. **Probably new, but minor.**
- **Density Theorems 1 and 2 (fixed-rate linear, the class FR):** Sin'ya (regular) and Koga (a dense class Γ(TL), compared with regular and DCF languages) are the nearest. No result for linear or even-linear languages was found. **Probably new, unconfirmed until Koga's Γ(TL) is read.**
- **Closure Theorem B (every rational-transduction image of Q has a semilinear Parikh image):** not found. **Probably new.**
- **Rectangle barrier (2⌈n/3⌉ balanced rectangles via Fine–Wilf):** not found, but it is elementary. **Likely folklore-level.**
