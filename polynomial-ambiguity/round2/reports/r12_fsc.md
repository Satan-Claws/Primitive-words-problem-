# r12_fsc.md — R12-A: FSC rigidity (unambiguous T8, CF-shaped pair models)

Status: **FSC rigidity NOT proved; no counterexample.** The heavy-block lemma and T8_unamb remain **OPEN**. What this round adds:
- **Lemma SF (self-fold)** [written proof + check]: every block with a realised context is itself fold-oriented,
  B_ℓ ⊆ G⁻(δ, K). So the suggested "high versus low excursion" lever **does** work, but only against non-oriented blocks.
  Example: blocks containing positive excursions E⁺ are excluded outright.
- **Lemma Env + Lemma Ori ⇒ No-go 4** [written proof + check]: for oriented, Dyck-type heavy blocks (E, D) the lever is
  provably **void**. Each length class has a unique pointwise-maximal walk, low excursions never hurt, and s·B_ℓ·t ⊆ G⁻ is
  equivalent to a single word s·x̂_ℓ·t ∈ G⁻. So the G⁻ side of the problem sees heavy blocks only through their lengths.
- **Prop HS (height slide)** [written proof for the model + check]: in height-coupled FSC models, the centre slides along
  occurrences of w, and the model is ambiguous. That is FSC rigidity in this subclass. The general coupling case is the exact gap.

Scripts: `scripts/r12_fsc_checks.py` → `scripts/r12_fsc_checks_out.txt`.

Notation is as in r10/r11. P(j) is the centred prefix walk, D(x) = P_x(|x|), and in the chord form
W ∈ G⁻ ⟺ F_W(k) := P(k) + P(n−k) − P(n) < 0 for all 1 ≤ k ≤ n/2.
E = primitive negative excursions (P < 0 inside, ending at 0). D⁻ = bridges with P ≤ 0. E⁺ = the positive mirror of E.

## 0. Precise target (from r11 §1)
**FSC rigidity.** Let C be a critical (ρ = 1) linear SCC with context S ⇒* pXq and exit w. Each first-return pair
(u, v) comes from a finite-state path whose rules X → αYβ put independent lower blocks on one tape: α on U, β on V.
Suppose a heavy lower block B occurs, with |B_ℓ| ≍ 2^ℓ ℓ^{−3/2} (finite μ, infinite mean). If every p U w V q is in G⁻,
then the map (pair sequences) → words is not injective.

The CF input used here is **substitution closure**: if a B-subtree has yield x in a word s x t ∈ L, then s·L(B)·t ⊆ L.
This holds for every CFG, **with or without ambiguity**.

## 1. Lemma SF (self-fold) [written proof; check C]
Let (s, t) be a realised context of B, with i = |s|, τ = |t|, δ = τ − i and K = D(t) − D(s).
Then every x ∈ L(B) with |x| = ℓ ≥ |δ| satisfies

  P_x(j) + P_x(ℓ+δ−j) − D(x) < K  for all integers j with max(0, δ, 1−i) ≤ j ≤ (ℓ+δ)/2.

*Proof.*
1. Put k = i + j. Then n − k = i + (ℓ + δ − j), and k ≤ n/2 ⟺ j ≤ (ℓ+δ)/2.
2. Both k and n − k lie in the x-segment [i, i+ℓ] because 0 ≤ j and ℓ + δ − j ≤ ℓ.
3. So P(k) = D(s) + P_x(j), P(n−k) = D(s) + P_x(ℓ+δ−j) and P(n) = D(s) + D(x) + D(t).
4. Substituting gives F(k) = P_x(j) + P_x(ℓ+δ−j) − D(x) − K, and F(k) < 0 by s x t ∈ L ⊆ G⁻. ∎

**Corollary SF.** Define the fold height h_δ(x) := max_j [P_x(j) + P_x(ℓ+δ−j) − D(x)]. If sup_{x∈L(B)} h_δ(x) = ∞ for the δ of
some realised context, then L ⊄ G⁻. In particular:
- a block whose language contains a^m b^m for infinitely many m is impossible (take j = (ℓ+δ)/2, so h ≥ m − O(|δ|));
- so is any block containing a positive sub-language E⁺·(anything).

Check (C): for B = E ∪ E⁺, **no** context with |s|, |t| ≤ 5 keeps s B_ℓ t ⊆ G⁻ for all ℓ ≤ 14.

So every heavy block of a counterexample is **fold-oriented**. Its walks fold below a fixed slack K. This is the rigorous form
of the "high versus low excursions" lever: high excursions are fatal **on their own**, and no compensation from the other tape is
even needed. Note the limitation: SF uses only one context, so it cannot exclude E-type blocks. Those satisfy h ≤ 0 (§2).

## 2. Lemma Env, Lemma Ori and No-go 4 [written proof; checks A, B]
**Lemma Env (monotone reduction).** Fix s, t and ℓ, and let X ⊆ {a,b}^ℓ have constant D on X. Suppose x̂ ∈ X satisfies
P_x ≤ P_x̂ pointwise for all x ∈ X. Then s X t ⊆ G⁻ ⟺ s x̂ t ∈ G⁻.

*Proof.*
1. Replacing x changes P only at positions inside the x-segment. Positions after it shift by D(x), which is the same for all of X.
2. P(n) is therefore unchanged.
3. F(k) = P(k) + P(n−k) − P(n) is non-decreasing in each P(j) with j < n. Hence F_{sxt} ≤ F_{s x̂ t} pointwise. ∎

For a general X, split it by D value and apply the lemma to each class.

**Lemma Ori.** E_{2m} has a unique pointwise maximum, x̂ = b(ba)^{m−1}a. D⁻_{2m} has a unique maximum, (ba)^m.

*Proof.* Use the doubled walk 2P ∈ ℤ, which has the parity of j. Inside an E-word, 2P ≤ −1, so 2P ≤ −1 at odd j and 2P ≤ −2 at
even j. The word x̂ attains both bounds. The argument for D⁻ is the same with bound 0. ∎

Check (A): uniqueness of the maximum, for ℓ ≤ 20. Check (B): all 23 814 triples (s, t, ℓ) with |s|, |t| ≤ 5 and ℓ ≤ 12 give
"s E_ℓ t ⊆ G⁻ ⟺ s x̂ t ∈ G⁻", with 0 mismatches.

**No-go 4** [written proof]. Let 𝒫 be an FSC model in which every heavy block class (B, ℓ, D) has a pointwise maximum.
Examples are E, D⁻, and any block whose walks lie under a barrier and contain the barrier-hugging word.
Let 𝒫̂ replace every heavy block word by its class maximum. Then L(𝒫) ⊆ G⁻ ⟺ L(𝒫̂) ⊆ G⁻.

*Proof.* Apply Env block by block. Blocks are disjoint segments, and Env holds for any fixed rest of the word. ∎

Consequences:
- (i) The lever proposed for this round ("B contains high and low excursions of the same length, and the fixed right tape
  cannot compensate both") is **false for Dyck-oriented blocks**. There is no high E-excursion, every E-block is dominated
  by the flat one, and low excursions never create violations.
- (ii) For such models the G⁻ side of the problem depends only on the **length profile** (and D-class) of heavy blocks,
  together with the light letters. A proof of FSC rigidity must therefore get its contradiction from **injectivity of the
  unflattened words**. 𝒫̂ itself is far from injective, since it has one word per block length.
- (iii) Together with SF: in a counterexample, every heavy block is fold-oriented. If the blocks also have class maxima (as all
  Dyck-type CF blocks seen so far do), membership in G⁻ is decided by 𝒫̂.

## 3. Prop HS (height slide): rigidity for height-coupled models [written proof for the model; check D]
Take the critical model 𝒫 = {(bE^i, E^j a) : i, j ≥ 0}.
- π = ¼·2^{−i−j}, so Σπ = 1. Heavy blocks occur on **both** tapes.
- The tapes are U ∈ (bE*)^r, the strict negative meanders with 2D(U) = −r, and V ∈ (E*a)^r, the strict suffix-positive words
  with 2D(V) = r. Each tape decomposes uniquely (last passage), so the map is injective on pairs of tapes.

**Claim.** Let Z = U w V with D(w) ≥ 0. Suppose w occurs at offset c' in Z with c' ≥ 1 and c' + |w| ≤ |U|, and
r ≥ 1 + max_i 2P_w(i) − 2D(w). Then Z = U'wV' is a second parse.

*Proof.*
1. U' = Z[1..c'] is a prefix of a strict negative meander, so it is one too, and r' := −2D(U') ≥ 1.
2. 2D(V') = 2D(Z) − 2D(U') − 2D(w) = r', because 2D(Z) = −r + 2D(w) + r = 2D(w). So the token counts match.
3. V' is strict suffix-positive: 2P_Z(end) = 2D(w), and before the end of the original U, 2P_Z ≤ −1 ≤ 2D(w) − 1.
   On the original w-segment, 2P_Z ≤ −r + max 2P_w ≤ 2D(w) − 1. After that, the original V gives the bound. ∎

The case D(w) < 0 is the mirror, with an occurrence inside V. By Lemma Fac (r11 §2), w occurs inside the E-blocks of U for
all but an exponentially small fraction of long words. So **this model is ambiguous for every (p, w, q)**.

The coupling is "pair count = additive height". It is translation-invariant along the walk, so the centre is not pinned.
Check (D), N ≤ 20, 0 G⁻ violations in every case:

| (p, w, q) | words | ambiguous | max mult |
|---|---|---|---|
| (b, ε, a) | 2057 | 2055 | 17 |
| (bb, ab, aa) | 1244 | 562 | 6 |
| (b, b, a) | 2056 | 1429 | 8 |
| (bb, aab, aa) | 562 | 74 | 3 |

So ambiguity grows with N, while G⁻ is never violated. The same mechanism covers No-go 2 of r10 (pairs (E, ε) and (b, E^k a)).

## 4. Exact gap
**Padding rigidity (OPEN).** Let 𝒫 be a critical FSC model with fold-oriented heavy blocks that have class maxima, and let 𝒫̂
be its flattening, with L(𝒫̂) ⊆ G⁻. Show that 𝒫 is not injective.

Prop HS proves this when the finite-state coupling reduces to an additive height, i.e. the centre is located only by
pair count. What remains is a coupling carrying more than height, where the centre is pinned by something like "same path".
In No-go 3 the centre was pinned by |U| = |V|, which needs letter-by-letter zipping. Heavy one-tape blocks destroy length
pinning, but the open question is whether a finite-state path plus walk-passage structure can still pin it.
Note that canonical passage-time splits *are* CF-expressible and unambiguous: for example, E*·a·M⁺ (M⁺ = positive meanders) has a
unique split at the last zero. Such languages are not in G⁻, however.

Two further gaps:
- Blocks without class maxima are not covered by No-go 4. For them, SF bounds the fold height but the flattening is unavailable.
- To finish the proof one must show that the light letters plus flat padding force a height-type coupling, or else an outer
  violation. This is where a proof would have to use the finite SCC (a finite set of light patterns per path).

## 5. Polynomial ambiguity
- SF, Env, Ori and No-go 4 use only substitution closure, so they hold verbatim for **any** CFG.
- Prop HS gives at most n + 1 parses per word (centre slides), consistent with r11's centre-count bound. It gives no
  superpolynomial multiplicity, so it does not lift T8 to polynomial ambiguity.
- The poly case still needs two-tape re-tokenisation (r11 §3).

F1 check: SF, Env and HS use the fold geometry of G⁻ (the chord form) and its zero density. Q has density 1 and no fold
constraint. Nothing here implies Q is non-CF.

## Status
| claim | label |
|---|---|
| Lemma SF: realised blocks are fold-oriented; non-oriented heavy blocks (E⁺, aᵐbᵐ, …) impossible in G⁻ | written proof + check C |
| Lemma Env (monotone reduction) + Lemma Ori (E, D⁻ have unique maxima) | written proof + checks A (ℓ ≤ 20), B (23 814 triples) |
| No-go 4: the high/low substitution lever is void for Dyck-oriented blocks; G⁻ depends only on the length profile | written proof |
| Prop HS: height-coupled FSC models (e.g. {(bEⁱ, Eʲa)}, No-go 2) are ambiguous | written proof (model) + check D, N ≤ 20 |
| FSC rigidity / padding rigidity in general; heavy-block lemma; T8_unamb | **OPEN** (§4) |
| Polynomial-ambiguity lift | **OPEN**; §1–2 transfer, §3 gives only ≤ n + 1 |
