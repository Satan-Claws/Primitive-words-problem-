# r9_packing.md — R9-B: cross-spine packing lemma, unambiguous case (negative side)

Status: final for this round. **T8_unamb is NOT proved, and no counterexample was found.**
New result: an exact reduction of T8_unamb to a single *heavy-block lemma*. It comes from a measure reformulation (Thm M), a
location lemma (Lemma F) and a renewal lemma (Lemma Rn). All three use G⁻ only through |G⁻_n| = o(2ⁿ). That property is
not shared by Q, so the F1 check passes; see §5.
Scripts:
- `scripts/r9_packing_search.py`: random search over 240k small grammars. Output in `r9_packing_search_out.txt`.
- `scripts/r9_packing_counts.py`: exact counts. Output in `r9_packing_counts_out.txt`.

Notation. G is unambiguous and reduced, L = L(G) ⊆ G⁻. For a nonterminal X, μ(X) := Σ_{w∈L(X)} 2^{−|w|} ∈ [0, ∞], which is the
generating function at z = ½. Similarly μ(L) = L(½) = Σ_n |L_n|2^{−n}.

## 1. Theorem M (measure reformulation) [written proof; (ii) uses cited N-algebraic asymptotics]
(i) If L is rotation-dense, then μ(L) = ∞. This is because |L_n| ≥ |Rot(L)_n|/n ≥ δ2ⁿ/n, and Σ 1/n = ∞.
(ii) For unambiguous L, μ(L) < ∞ ⟺ |L_n| = o(2ⁿ/n) on every residue class. The reason is that the coefficients of an
N-algebraic series are C_r ρ^{−n} n^{α_r} on residue classes, and the exponent α = −1 never occurs: a log singularity is not
algebraic (Flajolet–Sedgewick VII.7; Banderier–Drmota 2015, which states the possible exponents are −1 − 1/2^k or −1 + m/2^k).
So there is **no borderline case**. T8_unamb (in the count form "|L_n| < δ2ⁿ/n") is equivalent to:

> **T8_μ.** Every unambiguous CFL L ⊆ G⁻ has finite Bernoulli measure Σ_n P(L_n) < ∞.

Compare G⁻, whose partial measure grows like √(2n/π): Σ_{n≤2000} = 17.35. A counterexample needs an exponent α ∈ (−1, −½]
(dyadic, by the cited classification). The value α = −½ means L is a positive fraction of G⁻.

## 2. Lemma F (where divergence lives) [written proof modulo DLW finiteness of nonlinear critical SCCs]
Suppose μ(L) = ∞, and let C be a lowest strongly connected component of the dependency graph that has μ = ∞. Then:
(a) C is **linear**: every rule of a C-nonterminal has at most one C-occurrence. A nonlinear SCC with finite inputs has a finite
value at its own singularity (Drmota–Lalley–Woods square-root type). A singularity below ½ would contradict |L_n| ≤ 2ⁿ.
(b) The context matrix M_{XY} = Σ_{X→αYβ} μ(α)μ(β) is finite at z = ½, since α and β lie in finite-measure lower components.
Its spectral radius is **exactly 1**:
- ρ < 1 gives y = (I−M)^{−1}b finite;
- ρ > 1 gives radius < ½ by continuity of ρ(M(z)), which is impossible.

## 3. Lemma Rn (finite-mean renewal is impossible inside G⁻) [written proof modulo the Erdős–Feller–Pollard / Markov renewal theorem]
Assume in addition that every lower nonterminal B occurring in a C-rule has finite mean Σ_{w∈L(B)} |w|2^{−|w|} < ∞.
Then limsup |L_n|/2ⁿ > 0, which contradicts L ⊆ G⁻.

*Proof.*
1. Fix X ∈ C, a context S ⇒* pXq and an exit word w ∈ L(X). Each first-return path X ⇒⁺ uXv inside C, with words chosen for the
   lower nonterminals, yields a pair (u, v).
2. By unambiguity, distinct (path, choices) give distinct words p u w v q. Otherwise the same word would have two trees.
3. Let f(ℓ) be the total weight 2^{−ℓ} of first-return pairs with |u| + |v| = ℓ. Then Σf = 1, because ρ(M) = 1 and C is
   irreducible. Also Σ ℓ f(ℓ) < ∞ by the finite-mean assumption.
4. By the renewal theorem, u(ℓ) → d/mean > 0 along a residue class mod the period d, where u is the weight of all return
   pairs of length ℓ.
5. Hence |L_n|2^{−n} ≥ 2^{−|pwq|} u(n − |pwq|) ≥ c > 0 infinitely often. But |G⁻_n|/2ⁿ ~ (2πn)^{−1/2} → 0. ∎

**Corollary H (structure of any counterexample).** Suppose L ⊆ G⁻ is unambiguous with μ(L) = ∞, which holds in particular
when L is rotation-dense. Then G has:
- a critical linear SCC C (ρ(M(½)) = 1), and
- a lower nonterminal B in some C-rule with μ(B) < ∞ and infinite mean.

B is therefore a *full-entropy critical* language: radius exactly ½, finite value, infinite derivative. For example
|L(B)_ℓ| ≍ 2^ℓ ℓ^{−3/2}, which is Dyck-like. With block tail ℓ^{−1−β} the renewal density is n^{β−1}. The bound
|L_n| ≤ |G⁻_n| then forces β ≤ ½ [heuristic for β ≤ ½: strong renewal needs extra regularity].
Example of exactly this shape: the negative meanders (b ∪ E)*, where E is the set of negative excursions. Here μ(b) + μ(E) = ½ + ½ = 1, the blocks
are heavy-tailed, and the density is n^{−½}. This shows the critical heavy-tailed mechanism is real. Meanders are not ⊆ G⁻, though.

## 4. Exact remaining gap: the heavy-block lemma (open)
Here is how §1–3 relate to r8 §4. In a critical heavy-tailed renewal, a typical long word has **one giant block**
b ∈ L(B) of length Θ(n), sitting at an offset that varies with independent blocks of total measure 1. The cross-spine packing
lemma for unambiguous G is therefore equivalent (via Thm M and Corollary H) to:

> **Heavy-block lemma (open).** No critical linear SCC C with a heavy-tailed lower block B can have all of its renewal words
> p·(u-blocks)·w·(v-blocks)·q inside G⁻.

What does not suffice:
- (a) Per-block constraints alone: the negative excursions E (density ℓ^{−3/2}) satisfy p E s ⊆ G⁻ for all p ∈ b*, s ∈ a*
  (r6_nofold Lemma M, up-set).
- (b) Counting contexts rather than words. **Ambiguity-collapse example** [written proof]: take A → EA | AE | bAa | ε and
  L = bAa. Every word lies in G⁻, by a 3-case count of pair letters plus E-partials (≤ 0 in prefixes, ≥ 0 in suffixes). The
  context measure is Σ_k 4 = ∞. But as a word set A = Dyck, so L = the negative excursions, with exponent −3/2 and finite measure. The
  divergence lived entirely in multiplicity, as in G2 of r8. So the polynomially ambiguous case needs a separate word-level argument.

The heavy-block lemma would have to use that the giant block's offset relative to the fold centre is randomised by an
independent measure-1 renewal while every outcome stays in G⁻. That is the only center-sensitive input left.

## 5. F1 check
§1–3 use only |G⁻_n| = o(2ⁿ) and |G⁻_n| ≍ 2ⁿn^{−½}. Q has |Q_n| ~ 2ⁿ, so Lemma Rn gives nothing for Q (Σ* itself is a finite-mean critical example of positive density).
The arguments therefore do not prove Q non-CF. Note that they also do not distinguish G⁻ from any other zero-density
language of density ≥ n^{−½}. The heavy-block lemma must use the fold geometry.

## 6. Computation [exhaustive per grammar to n = 14; exact counts]
- Random search: 240k grammars (3 nonterminals, ≤ 3 rules each, |RHS| ≤ 3). Inclusion in G⁻ was checked to n = 14.
  The best *unambiguous* language found is Catalan, 42 / 132 at n = 12 / 14, i.e. negative-excursion type with α = −3/2.
  Larger languages found were ambiguous and still below 0.1|G⁻_14|.
- Exact counts for E = b D a: |E_n|·n/2ⁿ = 0.0927, 0.0522, 0.0283, 0.0089 at n = 20, 60, 200, 2000, which goes to 0. For G⁻ the
  same quantity is 1.76, 3.08, 5.64, 17.8. Partial measures: E → ½ (finite); G⁻ grows like √n.
- No construction reaching δ2ⁿ/n was found. That is consistent with Corollary H: any construction must contain a critical
  heavy-tailed linear recursion, and none of the small grammars has one inside G⁻.

## Status
| claim | label |
|---|---|
| Thm M: rotation-dense ⇒ μ(L) = ∞; for unambiguous L, T8 ⟺ μ(L) < ∞ (no α = −1) | written proof + cited N-algebraic asymptotics |
| Lemma F: divergence sits in a linear SCC with ρ(M(½)) = 1 | written proof modulo DLW |
| Lemma Rn: finite-mean critical linear SCC impossible in G⁻ | written proof modulo the renewal theorem |
| Cor H: a counterexample needs a heavy-tailed full-entropy block feeding a critical linear SCC; α ∈ (−1, −½] | proof (structure) + heuristic (β ≤ ½) |
| Ambiguity-collapse example (context measure ∞, word measure finite) | written proof |
| Heavy-block lemma ⇒ T8_unamb | OPEN (exact gap) |
| Construction with |L_n| ≥ δ2ⁿ/n | none found (240k-grammar search; best = Catalan) |
