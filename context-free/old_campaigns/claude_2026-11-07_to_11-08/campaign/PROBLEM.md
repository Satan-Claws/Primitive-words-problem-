# Problem: is the language of primitive words context-free?

Σ finite, |Σ| ≥ 2 (primary case Σ = {a,b}). A word w ∈ Σ⁺ is primitive if w ≠ uⁿ for every u ∈ Σ⁺ and n ≥ 2. ε is NOT primitive. Q_Σ = set of primitive words.

Goal: EITHER construct a (nondeterministic, one-stack, one-way) PDA / CFG with L = Q_Σ EXACTLY, for every |Σ| ≥ 2,
OR prove Q_{a,b} is not context-free (this suffices for all larger alphabets by intersection with {a,b}*).

## Exact requirements
- Affirmative: explicit finite grammar/PDA (or explicit finite scheme), proofs of both inclusions Q ⊆ L and L ⊆ Q, every length, ε excluded, all alphabets (or a rigorous transfer), finite exceptions identified and patched.
- Negative: rigorous proof that every PDA P has L(P) ≠ Q. Indirect routes allowed through CF-preserving operations only: ∩ regular, inverse morphism, morphism, gsm / rational transduction, left/right quotient by regular, cyclic shift, reversal, union/concatenation with regular. NOT complement, NOT ∩ with a CF language, NOT infinite intersections.

## Known (usable with correct hypotheses)
- Q is DCSL (linear-time decidable); Q not regular; Q not DCFL; Q not unambiguous CF (Petersen 1994, via non-algebraic generating function — says nothing about inherently ambiguous languages); Q not linear (Horváth 1995).
- Reis–Shyr: Q² = Σ⁺ \ {aⁿ : a ∈ Σ, n ≠ 2}.
- Non-k-th-powers are CF for each fixed k ≥ 2; Σ* \ {ww} is CF.
- Q ∩ Σⁿ = ⋂_{p | n prime} (non-p-th-powers ∩ Σⁿ): unboundedly many CF conditions, depending on n.
- Abelian primitive words not CF; primitive palindromes not CF.

## Known dead ends (must explicitly evade)
- Parikh image of Q is semilinear; length set is ℕ≥1; Q closed under rotation (as are CF langs under cyclic shift).
- Pumping/Ogden/interchange stalled 30+ years: Q has density → 1; non-primitive words of length n number O(|Σ|^{n/2}); a pumping argument must force a pumped word INTO the thin non-primitive set for EVERY decomposition the lemma allows.
- Counting/generating-function arguments refute only unambiguous grammars.
- Communication-complexity size lower bounds are known only for unambiguous CFGs.
- Bounded-language intersections Q ∩ w1*…wk* look CF (thin complement) — likely useless.
- "Guess one mismatch for one period" PDA accepts only the non-p-th-powers for a single p.

## What does not count
Restricted-class impossibility (deterministic/unambiguous/finitely ambiguous/linear…), one inclusion only, correctness on a subset, length-indexed families, non-CF-ness of the complement or of a variant, heuristic/numerical evidence, finite computation, reduction to an unproved statement of comparable strength, unrefereed claims not reconstructed line by line.

## Rules for agents
- Return concrete artifacts: lemmas with proofs, explicit grammars/automata, decompositions, estimates with constants, code + output, counterexamples to sublemmas.
- Be brutally honest: if a route stalls, say exactly at which missing lemma, and whether that lemma is of theorem strength. Never call a gap "routine".
- Do NOT search the web for a solution to this problem. Standard background theorems are fine from memory.
- Write your full report to the file path given in your task, then return a ≤400-word summary.
