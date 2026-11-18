# Round 4 registry of approach families

Started 2026-11-18 04:29 UTC. Wave 1: 9 independent agents (one slot kept for audits).

| Family | Agent | Status |
|---|---|---|
| Derivation-tree iteration / Ogden / multi-pump on unbounded slices | ogden | running |
| Bounded slices, Kászonyi–Katsura (n = 210 …) | kk | running |
| Density of CF subsets of Q | density4 | running |
| Construction of a CFG/PDA (positive direction) | builder | running |
| Rational-transduction reductions (correct direction) | transduce | running |
| Uniform-in-M upgrade of the finite-ambiguity slice argument | uniform | **blocked** (barrier) |
| Periodicity / near-power witness families | periodic | running |
| Analytic / N-algebraic series obstructions | analytic | running |
| Cross-length context × yield decompositions | crossing | running |

Entries are filled in from each agent's report (exact aim, strongest lemma, missing step,
counterexamples, strength of missing step, reopen condition).

## uniform (done 1st wave)
1. Aim: turn the finite-ambiguity slice argument into an existence obstruction.
2. Proved: on R = a(ab⁺)*a(ab⁺)* (contains every R_m) every non-primitive word is a square, so
   Q ∩ R = R ∩ coPow₂ is CF (explicit 5-nonterminal grammar). General barrier: if the gcd of root exponents
   of non-primitive words of a regular R is d ≥ 2 then Q ∩ R = R ∩ coPow_d is CF. Identity
   Q ∩ R6 = R6 ∩ coPow₂ ∩ coPow₃ for R6 = (a(ab⁺)⁺)⁶ (exponents {2,3,6}).
3. Missing: a regular R with gcd E(R) = 1 and Q ∩ R not CF (candidate R6).
4. Counterexamples: pump-to-equal-halves, bounded certificate-type counting, single-prime slices.
5. Missing step is stronger than Q ∉ CFL (but sufficient).
6. Reopen: an iteration lemma using square and cube certificates jointly on R6, or a grammar for Q ∩ R6.
