# Shared briefing: the primitive-words problem

## Target
Q = set of primitive words over {a,b} (nonempty, not u^k for any k >= 2).
Goal (Lean file `PrimitivePDA_Negative.lean` in this directory): prove Q is NOT context-free.
This is the Dömösi–Horváth–Ito conjecture (1991). It is OPEN; recent sources (2025) still call it open.
A Lean answer either way would be a new research result. Be realistic, be rigorous, be honest.

The formalization was checked by the coordinator: finite PDA (Fintype states/stack, Finset rules,
acceptance by final state after consuming the input), and a Mathlib `Language.IsContextFree`
version. No loophole was found: both statements are faithful to the real open problem.
(A positive answer, i.e. an actual CFG/PDA for Q, would DISPROVE the Lean theorems; that also counts as solving.)

## Known facts (verify before relying on any of them; mark which you verified)
- Q is not regular; Q is not deterministic CF (DCFL closed under complement and co-Q is not CF).
- Q is not unambiguous CF (Petersen 1994/96): by Chomsky–Schützenberger the generating function of an
  unambiguous CFL is algebraic, and sum_n psi(n) z^n with psi(n) = sum_{d|n} mu(d) 2^{n/d} is not.
- Q is reportedly not linear (Horváth), and Q satisfies the standard pumping lemma and Ogden-type
  lemmas, so naive pumping arguments cannot work. (Verify exact statements.)
- Lyndon–Schützenberger: u^m v^n = w^p with m,n,p >= 2 implies u,v,w are powers of a common word.
- Shyr–Yu-type: for uv != vu, u^n v is primitive for all but at most one n (check exact statement).
- Fine–Wilf: periods p,q and length >= p+q-gcd(p,q) => period gcd(p,q).
- For each fixed k, the complement of {w^k} is CF. So Q ∩ (words of length n) is an intersection
  over the primes p | n of CF conditions; the difficulty is entirely in the intersection
  (CFLs are not closed under intersection or complement).
- Bounded route: by Ginsburg's theorem a bounded L ⊆ w1* ... wk* is CF iff its exponent set is a
  finite union of stratified linear sets. Kászonyi–Katsura studied Q_n = Q ∩ (ab*)^n (exponent
  set = primitive integer sequences of length n). They CONJECTURED Q_n is CF for all n and proved it for
  n = p^h, and for n with two (and some three) prime divisors (Dömösi–Ito book, ch. 10, "Kászonyi–Katsura
  theory", DLI-languages). Horváth–Ito: Q ∩ (slender regular / slender CF) stays regular / CF.
- Abelian primitive words are not CF (Domaratzki–Rampersad, arXiv 1006.4104). Lyndon words not CF
  (Berstel–Boasson). Non-ins-robust primitive words not CF (arXiv 1707.01010).
- Coordinator's observation: letter counts certify primitivity cheaply (gcd(|w|_a,|w|_b)=1 => primitive;
  p ∤ |w|_b => not a p-th power). So "hard" instances for any lower bound are words that are abelian
  p-th powers for every prime p | n but are not powers.
- Coordinator's observation (CFG rectangle structure): if a CFG in CNF of size g generates L, every
  w ∈ L of length n has a subtree whose yield y has n/3 <= |y| <= 2n/3. So L ∩ Σ^n is a union of
  at most g·n^2 "rectangles" {x y z : (x,z) ∈ O, y ∈ I} (fixed split positions), each fully inside L.
  A superpolynomial fooling set / a distribution that gives every such rectangle inside Q tiny mass
  would prove non-CF. Parity/counting tricks show single-defect near-powers are NOT a fooling set.

## Rules for every agent
1. Never claim a proof unless every step is written out. No "clearly", no "it is easy to see".
   Mark each step as PROVED / CHECKED BY COMPUTER (give the script) / CONJECTURED / FROM LITERATURE (cite).
2. Valuable outputs, best first: (a) a complete proof either way; (b) a rigorous reduction of the
   conjecture to a cleaner statement; (c) a rigorous BARRIER theorem (a proof that a method cannot work);
   (d) computational evidence with scripts.
3. Write your full report to `reports/<your-agent-name>.md` in this scratchpad directory. Put scripts in
   `scripts/<your-agent-name>/`. Your final message should summarise the report in <= 400 words,
   and say clearly whether you claim a proof.
4. Python 3.13 is available. No Lean toolchain is installed (network blocked). Use up to 2 CPU cores
   per long computation and cap runs at ~20 min each; the machine has 4 cores and 15 GB RAM shared by all agents.
5. Do not edit files outside this scratchpad. Do not touch git.
