# r10_heavy.md — R10-A: the heavy-block lemma (unambiguous T8)

Status: **heavy-block lemma NOT proved; no counterexample.** What this round adds:
- an exact reduction of the critical SCC to a two-tape i.i.d. pair model (§2);
- two **no-go results** showing that the suggested route cannot work as stated (§3, §4):
  - offset randomisation alone cannot produce a violation for Dyck-oriented giant blocks;
  - an outer-walk / two-tape argument alone cannot work either, because an injective critical pair model with a safe outer walk exists;
- a localisation of the remaining gap: the contradiction must come from *whole-word* injectivity at the fold centre,
  where every example seen so far fails by commutation of the centre with the blocks;
- a targeted grammar search (§6).

Scripts: `scripts/r10_heavy_search.py` (search), `scripts/r10_heavy_checks.py` (checks of §1–§4).

Notation as in r9_packing. For a word W of length n, put P(j) = #a(W[1..j]) − j/2, the centred prefix walk with P(0) = 0.

## 1. Chord form of G⁻ [written proof]
d_k = #a(pre_k) − #a(suf_k) = P(k) − (P(n) − P(n−k)). Hence

  **W ∈ G⁻ ⟺ P(k) + P(n−k) < P(n) for all 1 ≤ k ≤ n/2.**

This is the Lemma A form of r6 seen from the word itself: the chord from 0 to n must lie strictly above every symmetric pair average.
Two consequences:
- If W = α x β, the giant block x contains both k and n−k, and x is Dyck-oriented (D(x) := P_x(|x|) = 0 and P_x ≤ 0), then
  P(k) + P(n−k) − P(n) ≤ 2P(|α|) − (P(|α|) + D(β)) = P(|α|) − D(β).
  This holds **whatever the position of the centre inside x** (§3).
- Let Safe_n = {W : P(k) ≤ 0 and P(n) − P(n−k) ≥ 0 for all k ≤ n/2}, i.e. two one-sided meanders. Then |Safe_n| = |M_{⌈n/2⌉}|·|M_{⌊n/2⌋}| ≍ 2ⁿ/n.

## 2. Pair model [written proof, from Lemma F / Cor H of r9]
Take a critical linear SCC C, a nonterminal X ∈ C, a context S ⇒* pXq and an exit X ⇒* w. Expand each first-return loop
X ⇒⁺ uXv with terminal words chosen for the lower nonterminals. This gives a set 𝒫 of string pairs (u, v) with
π(u, v) := 2^{−|u|−|v|} and Σ_𝒫 π = 1. A single X is enough, since the first-return weights of an irreducible ρ = 1 matrix sum to 1.

Unambiguity has two consequences:
- (i) π is a genuine probability on string pairs: each pair has multiplicity 1.
- (ii) the map (pairs s_1..s_r) ↦ p u_1⋯u_r w v_r⋯v_1 q is injective over **all r jointly**.

T8_unamb is therefore equivalent to: *no such (𝒫, p, w, q) has all its words in G⁻* (with μ(L) = ∞ ⇐ Σ_r 1 = ∞).

**Outer-walk lemma** [written proof]. For k ≤ min(|pU|, |Vq|), d_k depends only on the pair sequence, not on the centre.
So if some finite pair sequence has d_k ≥ 0 at such a k, then that word is in L \ G⁻.

## 3. No-go 1: offset randomisation does not violate G⁻ for Dyck-oriented blocks [written proof]
The r9 heuristic was that the giant block's offset is randomised by independent measure-1 blocks, so G⁻ fails with positive probability.
By §1 this fails for any giant block x with D(x) = 0 and P_x ≤ 0, such as E = bDa, the heavy block of Cor H (tail ℓ^{−3/2}).
For such x, the centre-region constraint reduces to the single *outer* inequality P(|α|) < D(β), uniformly in the offset.
Any proof must therefore use something other than "the fold centre lands at a random place inside a heavy block".

## 4. No-go 2: the outer walk alone cannot work [written proof + exhaustive check]
Take 𝒫 = {(E, ε)} ∪ {(b, Eᵏa) : k ≥ 0}. Then:
- Σπ = ½ + Σ_k ¼·2^{−k} = 1, so the SCC is critical.
- E is heavy-tailed, and the mean is infinite.
- The two-tape map is injective: U ∈ {b, E}* and V ∈ {Eᵏa}* factor uniquely, and the order of the b-tokens matches the V-blocks.
- Every outer walk is strictly negative: P_U ≤ 0 (a meander) and the suffix excess of V is ≥ ½ > 0.

So no pair sequence violates G⁻ in the outer region. The failure is at the whole-word level, and it is **ambiguity, not exclusion**
(`r10_heavy_checks_out.txt`; N ≤ 16; every centre w with |w| ≤ 3; (p, q) ∈ {(ε,ε), (b,a), (bb,aa)}):
- 27 of 45 (p, w, q) choices keep every word in G⁻ up to N = 16.
- **all 45 are ambiguous**. The mechanism is that the centre word w reappears inside E-blocks, so the split U | w | V is not recoverable.
  For example, with p = bb, w = aab, q = aa: bb·(bb)·aab·(baabaa)·aa = bb·(bbaabb)·aab·(aa)·aa.
- The number of ambiguous words grows with N: 2, 20, 125 at n = 15, 17, 19 (`r10_heavy_pairmodel.py bb aab aa 20`). There are no G⁻ violations up to N = 20.

So in this model the contradiction to μ(L) = ∞ comes from unambiguity alone. G⁻ is not needed beyond making the blocks Dyck-like.
The heavy-block lemma is therefore a statement about the **interaction of injectivity with the centre word**. It is not about pair sequences.

## 5. What a proof must show (exact gap, sharpened)
Let ℒ_X be the pair language of a critical SCC fed by a heavy-tailed block. Show that

  {p U w V q : (U, V) ∈ 𝒫*} ⊆ G⁻ ⟹ the map 𝒫* → words is not injective.

Every instance examined fails in one of two ways:
- (a) a G⁻ violation from the self-fold at the centre (r9 search: most grammars);
- (b) a **centre-shift ambiguity** p·U·w·V·q = p·U'·w·V'·q. Here w occurs inside a heavy block, because a full Dyck-type block
  language contains every balanced pattern as a factor. This generalises the ambiguity-collapse example of r9 §4(b) and §4 here.

A proof would need a rigidity statement of the form: G⁻-safety of all centre offsets forces the centre to factor through the
same Dyck-type monoid as the blocks. **[heuristic; not proved]**

F1 check: §1, §3 and §4 use the fold geometry (the chord form) rather than only |G⁻_n| = o(2ⁿ), so they do not apply to Q. §1's Safe bound uses
2ⁿ/n density, which Q (density 1) lacks. No statement here implies Q is non-CF.

## 6. Computation
- `r10_heavy_checks.py` → `r10_heavy_checks_out.txt`:
  - chord identity: 0 failures for n ≤ 14;
  - §4 model: 17577 two-tape contexts, all with multiplicity 1, and 0 outer-walk violations; every (p, w, q) choice is ambiguous;
  - |Safe_n|·n/2ⁿ → 1.27 (n = 2000), i.e. ≍ 2ⁿ/n.
- `r10_heavy_search.py` → `r10_heavy_search_out.txt`: critical (Σμ = 1) linear SCCs X → xXy | w, with x and y made of ≤ 2 tokens from {a, b, E}
  and the 5×7 (p,q), w choices.
  - N = 12: 48967 out of G⁻, 15174 ambiguous, 644 ok.
  - Re-tested at N = 16: 276 out, 348 ambiguous, 20 ok. All 20 use the margin p = bb, q = aa, which only delays failure.
  - `r10_heavy_survivors.py` gives explicit n = 28 violations for the two leading one-sided survivors (X → Xa | XE and its mirror),
    e.g. bbbb·a¹⁰·b⁶a⁶·aa ∉ G⁻.
- No counterexample: every critical heavy-block model tested either leaves G⁻ or is ambiguous.

## Status
| claim | label |
|---|---|
| Chord form; offset-insensitivity of Dyck-oriented giant blocks (no-go 1) | written proof |
| Pair-model reduction of T8_unamb; outer-walk lemma | written proof (from r9 Lemma F / Cor H) |
| No-go 2: injective critical two-tape model with safe outer walk | written proof + exhaustive check (N ≤ 16) |
| Heavy-block lemma / T8_unamb | **OPEN**; gap = centre-shift ambiguity rigidity (§5), heuristic |
| Counterexample | none (search above; small survivors refuted at n = 28) |
