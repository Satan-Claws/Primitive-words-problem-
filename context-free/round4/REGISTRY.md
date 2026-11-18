# Round 4 registry of approach families

Started 2026-11-18 04:29 UTC. Wave 1: 9 independent agents (one slot kept for audits).

| Family | Agent | Status |
|---|---|---|
| Derivation-tree iteration / Ogden / multi-pump on unbounded slices | ogden | running |
| Bounded slices, Kászonyi–Katsura (n = 210 …) | kk | **stalled** (one-scale obstructions dead for all n) |
| Density of CF subsets of Q | density4 | running |
| Construction of a CFG/PDA (positive direction) | builder | running |
| Rational-transduction reductions (correct direction) | transduce | running |
| Uniform-in-M upgrade of the finite-ambiguity slice argument | uniform | **blocked** (barrier) |
| Periodicity / near-power witness families | periodic | open: candidate lemma CL1 (stronger than goal) |
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

## kk (done 1st wave)
1. Aim: find n with Q ∩ (ab*)^n not CF (Kászonyi–Katsura counterexample), or a barrier.
2. Proved: Theorem A (reflection axes + CRT): for every n the near-constant region of E_n is covered by
   stratified linear subsets of E_n (covers n = 210); Theorem B: same for every positive direction h.
   So every one-scale Dickson obstruction (bounded.md L6 / finiteindex F) fails for every n.
3. Missing: a two-scale ("flag") obstruction N·h + M·g + δ with g/h having no reflection axis compatible
   with all primes, plus proof that it implies non-CF; must pass at n = 6 (known CF).
4. Counterexamples: one-scale families for all n; near-constant arrangement search at n = 42, 60.
5. Missing step concerns one n (narrower than Q ∉ CFL), but evidence now favours KK being true,
   which would close the route.
6. Reopen: a two-scale obstruction lemma, sound, that survives n = 6.

## periodic (done 1st wave)
1. Aim: CL1 — every CFL containing F_ins = {a(a^m b)^k : m ≥ 1, k ≥ 2} contains a non-primitive word.
2. Proved: L1 (two distinct non-primitive words of equal length differ in ≥ 2 positions); Fact B
   (word in (a*b)+ is a power iff cyclic block vector is shift-invariant); L2 partially (insertion
   into u^k is primitive; proved for q ≥ 3, k ≥ 6, checked |u^k| ≤ 15); Bar1 (one-parameter slices of F_ins
   lie in regular subsets of Q); Bar2 (no coprime semilinear set covers F_ins counts); Bar3 (classification
   of exact-power pumps; case B only computer-checked); Bar4 (Ogden/Bader–Moura cannot force them);
   'unique longest block' superset not CF.
3. Missing: tree surgery combining derivations of a(a^m b)^k and a(a^{m+1}b)^k forcing a power-producing pump.
4. Counterexamples: B-type merge pumps (odd k), k = 3 cube pump, first-vs-last block supersets contain powers,
   L2 false for |u| = 1.
5. Stronger than Q ∉ CFL.
6. Reopen: cross-derivation parity argument; or a CF L with F_ins ⊆ L ⊆ Q (refutes CL1).
