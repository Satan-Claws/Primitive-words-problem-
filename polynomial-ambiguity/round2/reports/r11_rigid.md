# r11_rigid.md — R11-B: centre-shift rigidity (unambiguous T8)

Status: **centre-shift rigidity NOT proved; the heavy-block lemma and T8_unamb remain OPEN.** What this round adds:
- **No-go 3** [written proof + exhaustive check]: the pair-model statement suggested at the end of r10 is **false** for abstract
  pair sets. G⁻ restricted to even lengths is itself an injective, critical, heavy-tailed pair model. So any proof must use the
  context-free shape of the pair set: heavy blocks lie on **one tape**, coupled to the other tape only through a finite-state path.
- **Lemma Fac** [written proof]: every full-entropy block language contains each fixed word w as a factor, at linearly many
  disjoint positions in almost all of its words. This settles part (a) of the task's "absorption" intuition, but by itself it
  gives no re-splitting.
- **Centre-count bound** [written proof + check]: absorption at the centre gives at most n + 1 parses per word and context.
  So centre-shift **cannot** be the superpolynomial mechanism needed for polynomial ambiguity. That mechanism would have to be
  ambiguity in re-cutting a *fixed* two-tape word into pairs.

Scripts:
- `scripts/r11_rigid_lazy.py` → `r11_rigid_lazy_out.txt` (No-go 3);
- `scripts/r11_rigid_mult.py` → `r11_rigid_mult_out.txt` (centre-count bound on the r10 §4 model).

Notation as in r10_heavy. d_k = #a(pre_k) − #a(suf_k), and W ∈ G⁻ ⟺ d_k < 0 for all 1 ≤ k ≤ n/2.

## 1. No-go 3: G⁻ (even n) is an injective critical heavy-tailed pair model [written proof; checked n ≤ 16]
**Zipped walk.** For |U| = |V| = M, put s_j = [U_j = a] − [V_{M+1−j} = a] ∈ {−1, 0, +1}. Then d_{1+j} = d_1 + s_1 + … + s_j.
Under the uniform measure this is a lazy walk with p(±1) = ¼ and p(0) = ½.

**Tokens.** A token is a pair (u, v) with |u| = |v| = m whose zipped steps form one of the following:
- a single 0-step, (a,a) or (b,b): weight ½;
- a single −1 step, (b,a): weight ¼;
- a lazy negative excursion (first step −1, partial sums ≤ −1, return to 0 at m). There are C_{m−1} of these at length m
  (counts 1, 2, 5, 14, 42, 132), so the total weight is Σ C_{m−1}4^{−m} = ¼·(C(¼) − 1) = ¼, with tail ≍ m^{−3/2}.

So π(u, v) = 2^{−|u|−|v|} has Σπ = ½ + ¼ + ¼ = 1: the model is **critical**, and it is **heavy-tailed** (infinite mean).

Take p = b, q = a, w = ε. A pair sequence (u_1, v_1)…(u_r, v_r) gives W = b·u_1⋯u_r·v_r⋯v_1·a, with |U| = |V|.
- **In G⁻.** d_1 = −1. The concatenated tokens form a weak lazy meander ≤ 0, so d_k ≤ −1 for all k ≤ n/2.
- **Injective.** The split point is the exact middle of W. U and V are then fixed, and the zipped weak meander factors
  uniquely into 0-steps, last-visit −1 steps and excursions.
- **Onto G⁻ ∩ {even n}.** Every even-length W ∈ G⁻ starts with b, ends with a, and has a zipped walk ≤ −1.

Computed check (`r11_rigid_lazy_out.txt`): for every even n ≤ 16, the generated set equals G⁻_n (1, 3, 10, 35, 126, 462, 1716, 6435)
and the maximum multiplicity is 1.

**Consequence.** "Critical + heavy-tailed + every word in G⁻ ⇒ ambiguous" is false for abstract pair sets. Injectivity at the
centre is free when the centre is fixed by lengths (|u| = |v|). Heavy excursions are compatible with G⁻ when each excursion is
coupled **letter by letter** across the two tapes.

**What a CF grammar cannot do.** In the CF pair model of r10 §2, a first-return pair comes from a path in a finite SCC C.
Each rule X → αYβ puts *independent* lower-nonterminal blocks on one tape: α on the U tape and β on the V tape.
So a heavy block x ∈ L(B) is **one-tape and substitutable**: replacing x by any x' ∈ L(B) gives another word of L, and the
other tape is unchanged. The lazy excursion tokens above couple the two tapes through an unbounded counter, which a finite C
cannot carry. This gives the refined target:

> **FSC rigidity (open).** Let 𝒫 come from a finite linear SCC with independent one-tape lower blocks (finite-state coupling),
> be critical, and have a heavy one-tape block B (|B_ℓ| ≍ 2^ℓ ℓ^{−3/2}). If {pUwVq} ⊆ G⁻, then the map is not injective.

## 2. Lemma Fac (full entropy forces every factor) [written proof]
Suppose limsup |B_ℓ|^{1/ℓ} = 2, for instance |B_ℓ| ≥ 2^ℓ ℓ^{−c}. Fix a word w with |w| = t.
- Cut a word of length ℓ into ⌊ℓ/t⌋ aligned windows of length t. The number of words in which fewer than ε·ℓ/t windows
  equal w is at most 2^{ℓ(1−δ)} for some δ = δ(ε, t) > 0 (Chernoff bound, window probability 2^{−t}, ε < 2^{−t}).
- Hence all but a 2^{−δℓ}ℓ^{c} fraction of B_ℓ contain ≥ εℓ/t disjoint occurrences of w. In particular B is not contained
  in any language that avoids w.

This makes rigorous the claim that "Dyck-like languages contain every short word in many positions". It needs no CF
structure, and it is exactly why No-go 2 of r10 is ambiguous.
What it does **not** give is a *re-splitting*. An occurrence of w inside x ∈ L(B) still has to fall at a factorisation
x = x_1 w x_2 such that the two resulting pieces are again valid pair-sequence tapes with matching pair counts. No-go 3 shows
that this step must use the finite-state coupling: in the lazy model, w = ε occurs everywhere and there is still no re-split.

## 3. Centre-count bound and the polynomial-ambiguity lift [written proof + check]
Fix a context and exit (p, w, q). A parse of W is a pair sequence, and it determines the centre c = |pU|.
Two parses with the same c have the same tapes U and V. So

  mult(W) ≤ Σ_c N(c),  where N(c) = #{pair sequences with tapes (W[|p|+1..c], W[c+|w|+1..n−|q|])}.

- In an unambiguous grammar every N(c) ≤ 1.
- *Centre-shift* collisions (distinct c, each with N(c) = 1) therefore number at most n + 1 per word per (context, exit).
- Check on the r10 §4 model with (bb, aab, aa) and n ≤ 21 (`r11_rigid_mult_out.txt`): no two parses ever share a centre, and the
  maximum multiplicity is 1, 1, 2, 2, 3, 3 at n = 11, …, 21, so it grows slowly.

**Answer to the lift question.** Centre absorption **cannot** be iterated across ω(log n) independent blocks of one spine,
because a linear critical SCC has a single spine and hence a single centre. Centre shifts give at most a factor n, which a
polynomial-ambiguity bound n^k already absorbs. A superpolynomial collision count would have to come from N(c) itself:
non-unique re-cutting of a *fixed* pair of tapes into pairs, for example blocks migrating between adjacent pairs on one tape,
or from several independent critical sub-derivations nested inside the blocks.
This is the same multiplicity-only phenomenon as the r9 ambiguity-collapse example (A → EA | AE | bAa | ε).
So the candidate new lower-bound mechanism must be a **two-tape re-tokenisation lemma**, not a centre-shift lemma.
[proof of the reduction; whether re-tokenisation is forced is OPEN]

## 4. Exact gap
1. **Unambiguous case.** Prove FSC rigidity (§1). The only inputs not yet used are:
   - one-tape substitution closure: s·L(B)·t ⊆ L for every realised context (s, t);
   - the finite-state path coupling.
   No-go 3 shows these inputs are *necessary*. Lemma Fac supplies occurrences of the centre in blocks, but the matching of
   pair counts across the centre is the unproved step.
2. **Polynomial case.** Show that a critical heavy-tailed FSC model inside G⁻ forces N(c) ≥ n^{ω(1)} for some split.
   This is open, and centre shifts provably cannot supply it (§3).

F1 check: No-go 3 and §3 are statements about pair models; they prove no non-CF claim about Q. Lemma Fac is
language-agnostic. Nothing here implies Q is non-CF.

## Status
| claim | label |
|---|---|
| No-go 3: G⁻ ∩ even = injective critical heavy-tailed pair model (abstract pair statement false) | written proof + exhaustive check n ≤ 16 |
| CF pair sets are finite-state coupled with one-tape substitutable heavy blocks; FSC rigidity is the correct target | written observation (from r9 Lemma F / r10 §2) |
| Lemma Fac: full entropy ⇒ every w occurs ≥ εℓ times in almost all block words | written proof |
| Centre-count bound mult ≤ Σ_c N(c); centre shifts give ≤ n + 1 collisions per (context, exit) | written proof + check n ≤ 21 |
| Centre-shift rigidity / heavy-block lemma / T8_unamb | **OPEN** (exact gap §4.1) |
| Superpolynomial collisions for the fold route | **OPEN**; must come from two-tape re-tokenisation, not centre shift |
