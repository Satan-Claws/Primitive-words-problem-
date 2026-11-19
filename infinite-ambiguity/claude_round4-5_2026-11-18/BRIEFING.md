# Round 4 briefing: is Q (primitive words over {a,b}) context-free?

## Target
Q = primitive words over Σ = {a,b} (nonempty, not u^k for k ≥ 2). Decide whether Q is context-free.
Conjectured answer: NO (Dömösi–Horváth–Ito, open since 1991). Exactly one of these must be proved:

* **Negative:** for every CFG G over {a,b}, L(G) ≠ Q.
* **Positive:** an explicit CFG/PDA G with L(G) = Q, proved for every word (both inclusions,
  including ε, unary words, lengths 1 and 2).

## Already established (read the proof files before relying on them)
* **No finitely ambiguous CFG generates Q.** Lean-checked: `finitely-ambiguous/lean/FiniteAmbiguity/Main.lean`,
  written proof `finitely-ambiguous/PROOF.md`, short version `finitely-ambiguous/INTUITIVE_PROOF.md`.
  So any CFG for Q (cycle-free) has unbounded ambiguity. Re-proving ambiguity lower bounds is NOT progress.
* Written local proofs (NOT Lean-checked), in `context-free/reports/`:
  - `finiteindex.md`: Q ∩ (b*a)^m b* is not linear for every m ≥ 2; structure lemma and face criterion for
    bounded linear/metalinear languages; barrier: every bounded CF slice of Q has finite index.
  - `density.md` (+ audit `redteam2.md`): Q ∉ FR (fixed-rate linear/metalinear/ultralinear class);
    E' = {|w|_b = |w|_a + 1} is DCF, growth rate 2, all words primitive (so growth alone is no obstruction).
  - `rectangles.md` (+ `redteam.md`): Q ∩ Σ^n is a union of 2⌈n/3⌉ balanced rectangles inside Q
    (so rectangle/fooling-set/interchange arguments at a single length cannot work); total excess parses
    grow exponentially (limsup) in any CNF grammar for Q.
  - `devil.md`: coPow_k = Σ* \ {u^k} is CF for every k (explicit grammar); Q_n = Σ^n ∩ ⋂_{p | n prime} coPow_p;
    Q is CF iff some CF L ⊆ Q contains a conjugate of every primitive word (CFL closed under cyclic shift);
    "no bounded certificate" barriers; on each bounded slice the primitive exponent vectors outside
    the sum of the periodic subspaces form a CF language.
  - `closure.md`: every rational-transduction image of Q has a semilinear Parikh image (so Parikh-type
    reductions to {a^p : p prime} etc. cannot work).
  - `ambiguity.md`: ambiguity of bounded slices Q ∩ (ab*)^n; Theorem C: for odd prime p, Q ∩ (ab*)^p is a
    union of two unambiguous CFLs.
  - `bounded.md`, `scout.md`: Kászonyi–Katsura conjecture (Q ∩ (ab*)^n CF for all n) known for many n;
    certificates for n ≤ 30; n = 210 apparently open. A counterexample n would prove Q is not CF.
  - `context-free/STATUS.md`, `context-free/PARALLEL_CAMPAIGN_FINDINGS.md`: summary of earlier rounds.

## What does NOT count (common traps)
Restricted-class theorems; ambiguity lower bounds (per word or total); fixed bounded slices shown hard
or ambiguous (many are CF); intersecting with a NON-regular language and calling it closure; transductions
in the wrong direction; counting ψ(n) alone; "a PDA cannot remember enough" without a theorem;
Ogden with marks chosen after the decomposition; pumped words asserted (not proved) primitive/non-primitive
(check exponent 0, conjugacy across block boundaries, Fine–Wilf exact bound p+q−gcd(p,q));
inferring arbitrary-CFG facts from CNF without language preservation; bounded-length computations
presented as proofs; reductions to a lemma as strong as "Q is not CF".

## Rules for every agent
1. Never claim a proof unless every step is written. Tag each claim PROVED / COMPUTER-CHECKED (script) /
   LITERATURE (exact statement + source) / CONJECTURED / IDEA.
2. Acceptable returns: a fully quantified lemma with proof; an explicit infinite witness family with proof;
   a regular slice with exact identity + full non-CF proof; a CFG/PDA with soundness+completeness proofs;
   a valid reduction to a strictly simpler established problem; exact computation refuting/supporting a
   precise lemma; a counterexample; an audit locating the first invalid inference.
3. For your approach, end your report with a registry entry: (1) exact statement aimed at; (2) strongest
   lemma actually proved; (3) missing step, as a precise quantified lemma; (4) counterexamples found;
   (5) is the missing step weaker / equal / stronger than "Q not CF"?; (6) what would reopen the route.
4. Write the report to `infinite-ambiguity/claude_round4-5_2026-11-18/reports/<agent-name>.md`, scripts to
   `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/<agent-name>/`. Final message: ≤ 400 words summary; say plainly whether you
   claim a proof of either resolution.
5. Machine: 4 cores, 15 GB RAM, shared by ~10 agents. Use ONE core per computation, cap each run at
   ~10 minutes. Python 3 is available.
6. Do not edit files outside your report/script paths. Do not run git. Do not search the web for a
   purported solution of this exact problem; web search for exact theorem statements is fine.
7. Time budget: about 50 minutes of work, then write up what you have.
