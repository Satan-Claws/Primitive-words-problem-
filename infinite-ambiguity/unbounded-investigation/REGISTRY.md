# Unbounded ambiguity investigation

Started 2026-11-17 23:37 UTC. This is a research log, not a proof of the primitive-word conjecture. No claim of novelty or formal verification is made for results developed here.

The target is either an arbitrary CFG obstruction for Q or a CFG/PDA generating exactly Q. Restricted-class results and computational checks do not resolve it.

## Mechanisms being investigated

| Family | Exact target | Established starting point | Missing step | Counterexamples / barriers | Strength of missing step | Reopening evidence |
|---|---|---|---|---|---|---|
| Uniform grammar structure | Every CFG containing Q generates a proper power | Same-nonterminal yields can be substituted in every corresponding context | Force a power by substitutions using one fixed grammar | Q satisfies the ordinary interchange conclusion; single-level rectangles have small covers | Equivalent if asserted without further structure | A restriction connecting several lengths or levels of one grammar |
| Regular slices and bounded geometry | Find regular R with Q intersect R not CFL | On fixed block slices, powers are periodic exponent vectors | Violate stratified semilinearity in a concrete slice | Many slices are CFL; general semilinearity is insufficient | A sufficient special case | Explicit obstruction surviving all permitted period sets |
| Analytic series | Exclude an algebraic noncommutative series with positive coefficients exactly on Q | Parse-count series is algebraic; characteristic series obstruction handles unambiguity | Control unknown unbounded coefficients without replacing them by 0/1 coefficients | Catalan ambiguity on a^+b is compatible with every yield being primitive | Potentially equivalent | A support-sensitive invariant of algebraic series |
| Density | Every positive-density CFL contains a proper power | Established locally for fixed-rate class FR; count-imbalance primitive CFL has full entropy but density zero | Handle arbitrary nonlinear grammars and ambiguity | Entropy alone fails; positive density does not force a positive-density regular subset | Stronger than target | A positive-density structural theorem with valid hypotheses |
| Positive construction | Give finite CFG/PDA for all primitive words | Complement of fixed k-th powers is CFL | Combine all divisors of varying word length within a fixed machine | CFLs not closed under arbitrary intersection; bounded letter certificates fail | Equivalent at full generality | Explicit finite rules or stack algorithm with soundness and completeness |
| Periodicity certificates | Characterize sound certificates uniformly across lengths | For each prime p dividing n, a mismatch mod n/p is necessary and sufficient | Compile simultaneous certificates into a CFG, or show any CFG fails a necessary constraint | At least omega(n)+1 inspected positions needed; this is not a PDA lower bound | Depends on certificate model | New complete certificate family or model-independent necessity theorem |

## Evidence classes

- Published theorems: use only after checking a primary source and exact hypotheses.
- Existing local results: retain the distinction between written proofs, audited proofs, and Lean-checked statements. No Lean work is planned in this investigation.
- Current lemmas: record full proof and independent audit before presenting as established.
- Computation: record scripts, bounds, seeds, and counterexamples; do not treat finite success as a general proof.

## Audit queue

Every serious proposed lemma or construction will be sent to a different agent for an attempt to refute it. Failed steps will be recorded explicitly rather than hidden in a summary.
