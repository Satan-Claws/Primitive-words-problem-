# poly_WE notes (agent WE)

## Wich, "Exponential ambiguity of context-free grammars" (DLT 1999), full text read (static.aminer.org PDF)
- Def 2.5: am_G(n) := max_{w∈Σ^{≤n}} am_G(S,w), G cycle-free (no A ⇒+ A).
- Def 2.6: polynomially bounded if am_G(n)=O(n^k); exponentially ambiguous if am_G(n)=2^{Ω(n)}.
- Def 2.7 (C_exp): "∃A ∈ N; α, β ∈ (N ∪ Σ)*: am_G(A, αAβ) > 1 and αAβ contains neither useless nor ε-symbols."
  (am_G(A,β) counts leftskip parses = derivation trees from A with frontier β, nonterminal leaves allowed.)
- Thm 3.18: cycle-free G, C_exp ⇒ am_G(n) = 2^{Ω(n)}.
- Cor 3.20: ∃ pumping trees ϑ1,ϑ2 at A with interfaces (α^k,β^l),(α^m,β^n), α,β∈(N∪Σ)^+, lm≠kn ⇒ C_exp.
- Cor 3.21: a nonterminal both left- and right-recursive (A⇒+αA and A⇒+Aβ) ⇒ exponentially ambiguous.
- Thm 4.3: G not satisfying C_exp ⇒ #trees(w) polynomial in |w|; remark: am_G(n)=O(n^{2c−1}), c=Σ_{k=0}^{|N|−1} l^k, l = max #nonterminals on a RHS.
- Thm 4.4 / Cor 6.1: exponentially ambiguous iff C_exp; otherwise at most polynomially ambiguous.
- Thm 5.2: C_exp undecidable even for "extreme" (unambiguous-or-exponential) grammars.
- §6 table: PCFL closed under ∪ and ·, not *; UCFL closed under none; finite-degree closed under ∪ only.
  Conjecture there: L_pal^{k+1} has ambiguity Θ(n^k).

## Wich, MFCS 2001 (LNCS 2136, pp. 703–714), abstract verbatim (via sciweavers)
"We prove that the class of context-free languages with polynomially bounded ambiguity (PCFL) is the closure of the class of unambiguous languages (UCFL) under projections which deletes Parikh bounded symbols only. A symbol a is Parikh bounded in a language L if there is a constant c such that no word of L contains more than c occurrences of a. Furthermore PCFL is closed under the formally stronger operation of Parikh bounded substitution, i.e., a substitution which is the identity for non Parikh bounded symbols. Finally we prove that the closure of UCFL under union and concatenation is a proper subset of PCFL."
- Thesis (Stuttgart 2005, elib.uni-stuttgart.de/bitstream/11682/2567/1/dissWich.pdf) blocked by bot-protection; search snippet says thesis phrases it as "closure of UCFL under bounded contractions". Theorem numbers NOT verified.

## Task E
rectangles.md Thm 5.2 proves only limsup e_G(n)^{1/n} > 1 (redteam.md §1: along a subsequence). No exact rate in either file. Under poly ambiguity e_G(n) ≤ |Q_n|·C n^k ≤ C n^k 2^n. BLOCKED: rate ≤ 2.
