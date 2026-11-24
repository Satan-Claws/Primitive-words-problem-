# r3_nonunif: forbidden-exchange (U2 across slices) as a negative mechanism

R3-B, 2026-11-24. Inputs: `realise.md` §2 (U1–U3), `newmech.md` (Lemmas B, T, M; W-forcing), `thmR_unif.md`,
`recon.md` (Lemma 3P), `PA/poly_A2.md`, prompt §§6–7. Check script (inline, scratch): completion counts, binary,
L ≤ 14, all in-range (i, ℓ), ≤ 256 contexts each: 0 violations of Lemma C1, max 5 completions [computational].

**Mechanism (one line, why not §6).** Use the *cross-slice* exchange U2: the inside sets X_A^{(ℓ)} = L_A ∩ Σ^ℓ
(at most |V| of them per inside length ℓ) must serve contexts from slices of every length n′, and no context C of A
may admit a filler y ∈ X_A^{(ℓ)} with C[y] a proper power ("forbidden exchange"). This is neither a pump (no
a-insertion; `thmR_unif.md`) nor a within-length interchange (Lemma T): it constrains which fillers a shared
nonterminal may carry, over all lengths at once.

**Verdict: COLLAPSES.** The forbidden-exchange data is set-level, so it cannot see ambiguity. One level of exchange
yields multiplicity ≤ |V|·L² for *every* grammar, whatever its ambiguity. A contradiction drawn from it alone would
prove Q non-CF, which is open (§7). Any lower bound has to come from recursion inside a single in_A(x), and that is
exactly the open W-forcing lemma of `newmech.md` §5.

## 1. Formalisation

Let G be a reduced, cycle-free CNF grammar with L(G) = Q.
- Ctx_A = {(u, v) : S ⇒* uAv}. Write C[y] = u y v.
- Comp_ℓ(C) = {y ∈ Σ^ℓ : C[y] ∉ Q}, the fillers that complete C to a proper power.

**(FE) Forbidden exchange.** For every A and every C ∈ Ctx_A: L_A ∩ Comp_{|·|}(C) = ∅.
Cross-slice form: if (C₁, x₁) and (C₂, x₂) are A-occurrences in trees of words of slices n₁ ≠ n₂ with
|x₁| = |x₂|, then C₁[x₂] and C₂[x₁] are primitive. This is U2 with ℓ = ℓ′.

**Lemma FE0 (FE is exactly soundness) [written proof].** For reduced G, (FE) for all A ⇔ L(G) ⊆ Q.
*Proof.*
- (⇐) If S ⇒* uAv and A ⇒* y, then uyv ∈ L(G) ⊆ Q, so y ∉ Comp(C).
- (⇒) Take A = S and C = (ε, ε). ∎

So FE carries no information beyond L(G) ⊆ Q, and it is *downward closed*: shrinking any L_A preserves it.
Coverage (Q ⊆ L(G)) is the only upward pressure.

## 2. The single-defect family, made concrete

Let w = u^p with one letter changed at position d (p ≥ 3, so w is primitive by Fine–Wilf). Let ŷ denote y with
the letter at d restored.

**Lemma D (defect-separating path) [written proof].** In every tree of w, every node v whose yield x_v covers d
satisfies x_v ∈ L_{A_v} and x̂_v ∉ L_{A_v}.
*Proof.* C_v[x̂_v] = u^p ∉ Q. Apply FE. ∎

Lemma D constrains every tree, but it forces no *second* tree.
- It is satisfied by any grammar for any L ⊆ Q, including unambiguous ones such as D1·b (`PA/poly_T3.md`).
- It holds for the one-prime grammars of `uniform.md` restricted to their language.
- Cross-slice, the same A with the same x may occur in slices n and n′. Both occurrences forbid the same x̂, and
  nothing new results. With different fillers x₁ ≠ x₂, FE only forbids x₂ ∈ Comp(C₁).

**Lemma C1 (forbidden sets are tiny) [written proof + check].** Let |C| = L − ℓ with ℓ ∈ (L/3, 2L/3]. Then

  |Comp_ℓ(C)| ≤ τ′(L) + [2 | L, ℓ > L/2]·2^{ℓ − L/2},

where τ′(L) is the number of proper divisors of L.
*Proof.*
- A proper power of length L has some period d | L with d < L.
- The context occupies a cyclic interval of length L − ℓ ≥ L/3. If d ≤ L − ℓ, every residue class mod d meets the
  context, so the filler is unique.
- Otherwise d > L/3 forces d = L/2, and only ℓ − L/2 classes are free. ∎

The binary check (L ≤ 14) found 0 violations, with at most 5 completions.

Consequence: each context forbids at most poly(L)·2^{ℓ−L/2} of the 2^ℓ fillers. The conflict graph on
(context, filler) pairs that FE induces is sparse, so it cannot force a filler to be shared between two
nonterminals.

## 3. Why no multiplicity can come out (the collapse)

**Prop 1 (one-level blindness) [written proof].** Fix L. By `newmech` Lemma B, every tree of w has exactly one
selected in-range node (A, i, j), and

  amb(w) = Σ_{(A,i,j)} out^top_{A,i,j}(w)·in_A(w[i,j)).

Let Cov(w) = #{(A, i, j) : w ∈ top-rectangle(A, i, j)}. This is the multiplicity of the exchange-rectangle cover
{Ctx^top_{A,i,j} × X_A^{(j−i)}}. For *every* CFG G with L(G) = Q, unambiguous or exponentially ambiguous:
- 1 ≤ Cov(w) ≤ |V|·L²;
- the cover satisfies FE, coverage, and U1–U3.

These are set-level data. So any property P of the exchange data (with or without cross-slice sharing) that fails
for every polynomially ambiguous G also fails for every CFG G with L(G) = Q. Proving P would therefore prove Q
non-CF, which is open (prompt §3, §7).

*Proof.* Cov ≤ number of index triples. The data (L_A, Ctx_A) depend only on the languages, not on tree counts. ∎

**Prop 2 (where ambiguity must live) [written proof, from Lemma B + Lemma T].**
- If amb(w) ≥ L^{ω(1)}, then for some single (A, i, j), in_A(x) or out^top(C) is ≥ L^{ω(1)}/(|V|L²).
- Exchange of x's subtree into other contexts C′ ∈ Ctx_A transfers amb(C′[x]) ≥ in_A(x) (Lemma T). This is
  *upward* transfer of an ambiguity that already exists. FE never creates it, because FE is downward closed
  (Lemma FE0).
- Ambiguity off the skeleton is impossible: by `newmech` Lemma M, off-skeleton nodes have in = 1 in every slice,
  since U2 makes in_A(x) context-independent.

**What survives.** Only the following recursive form, which is `newmech` §5 W-forcing stated across slices.

> **Cross-slice W-forcing (open).** There are words w_n ∈ Q and ω(log n) disjoint intervals I_t such that for every
> G with L(G) = Q, some tree of w_n has nodes v_t spanning I_t with in_{A_{v_t}}(w_n[I_t]) ≥ 2.

U2 helps here only by making in_A(x) slice-independent. It cannot force in_A(x) ≥ 2: L_A is constrained only by
L_A ⊆ ⋂_{C ∈ Ctx_A} (Σ^* ∖ Comp(C)), and Lemma C1 makes that intersection's complement sparse per context.
A grammar can always route the hardness into Ctx_A, i.e. into out, which is symmetric.

## 4. Status

| claim | status |
|---|---|
| FE ⇔ L(G) ⊆ Q (downward closed) | [written proof] |
| Lemma D: defect-separating paths on single-defect words, every tree | [written proof]; forces no 2nd tree |
| Lemma C1: \|Comp_ℓ(C)\| ≤ τ′(L) + 2^{ℓ−L/2}[ℓ > L/2] | [written proof + check L ≤ 14] |
| Prop 1: exchange data (incl. cross-slice U2) is ambiguity-blind, Cov ≤ \|V\|L² for all CFGs | [written proof] ⇒ any FE-only lower bound would prove Q ∉ CFL |
| Uniformity-based superpolynomial lower bound | COLLAPSES to W-forcing (`newmech` §5) / NONUNIF; OPEN |
