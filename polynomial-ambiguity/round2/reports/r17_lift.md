# r17_lift.md — R17b-E: lifting T8_unamb to polynomial ambiguity (T8_poly)

Status: **T8_poly NOT proved.** Both routes the brief proposed reduce to the same polynomial multiplicity loss. Every gap in
the T8_unamb squeezes is polynomial or constant, and none is exponential. A count-level squeeze of the r13/r16 shape has a
hard ceiling: it can never exclude ambiguity ≳ n/log n (§4). New items:
- (L1) the marker-free critical loop lemma, which locates *where* Wich's markers, and hence all multiplicity, can sit;
- (L2) the exact partial result PR2⁺ gives for ambiguous grammars;
- (L3) the observation that the two-sided case has **zero word-level slack**. The quadrant Q_n(C) is a rotation
  cross-section of density ≍ 1/n, so the whole contradiction in PR2⁺ lives in the tree/word ratio.

No scripts were written; everything here is elementary.

Notation as in r16: W = p u w v q, A(k) = P(k), B(k) = P(n) − P(n−k), G⁻ ⟺ A(k) < B(k) for 1 ≤ k ≤ n/2. G is cycle-free
with amb_G(w) ≤ C|w|^k. e_n := #trees of length n.

## 1. What of T8_unamb survives verbatim for any cycle-free G [written proof]
- **Thm M(i)**: rotation-dense ⇒ word mass Σ|L_n|2^{−n} = ∞ ⇒ tree mass Σ e_n 2^{−n} = ∞.
- **Lemma F / Cor H** apply to the **tree** series T(z) = Σ e_n zⁿ. It is N-algebraic for every cycle-free CFG (the
  grammar's own system, with no unambiguity needed). So a critical linear SCC C with ρ(M(½)) = 1 and a heavy lower block
  exist exactly as before.
- **MS⁺ (r16 §1)** is set-level: it uses only "ρ·s is a legal token sequence, so its word is in L ⊆ G⁻". It holds for any
  G, so L_n ⊆ Q_n(C) in the two-sided case.
- **Lemma R** (renewal mass ≥ N^{β₀}) is a statement about **tree/pair** mass. Unambiguity is used exactly once, to turn
  pair mass into word mass (r13 §3 step 1, r16 §3 step 2).

So the reduction to "tree mass ≥ cN^{β₀}, word mass ≤ O(log N)" is ambiguity-free. The caveat is that I did not re-audit
the r10–r12 reduction chain for hidden uses of unambiguity; that is flagged.

## 2. (L2) Quantitative PR2⁺ for ambiguous G [written proof]
Let m_N be the maximal multiplicity of a word of length ≤ N in the pair family of one fixed (p, w, q). Then
  c N^{β₀} ≤ Σ_{n≤N} u(n) ≤ m_N · Σ_{n≤N} |L_n|2^{−n} ≤ m_N · O(log N),
so **m_N ≥ c N^{β₀}/log N**. In the two-sided level case this rules out ambiguity o(n^{β₀}/log n). Here β₀ = 2^{−k_max} ≤ ½
depends on the grammar and can be arbitrarily small. **This does not exclude even linear ambiguity** (it matches r13's
n^{1/6} corollary, improved to n^{β₀}).

## 3. Route (1): the Wich projection [written proof of L1; the route itself fails]
By Wich (MFCS 2001), L = h(L′), where L′ is unambiguous over Σ ∪ Γ and every word has ≤ c markers.

**Lemma L1 (marker-free critical loops).** Let G′ be a reduced unambiguous grammar for L′ and C a strongly connected
component of G′ with a loop. Then:
- no rule of C that contains a C-nonterminal has a marker terminal;
- every nonterminal B occurring in such a rule has L(B) ⊆ Σ*.

*Proof.* Such a rule lies on a loop X ⇒⁺ αXβ, because C is strongly connected. Suppose a marker, or a marker-bearing word
of some L(B), were available in α or β. Pump the loop m times, choose that word each time, and complete with a context and
an exit (the grammar is reduced). This gives a word of L′ with ≥ m markers, which contradicts the Parikh bound. ∎

**Consequence.** The pair model of G′ at the critical SCC is a pair model over Σ alone. Markers sit only in the fixed
p, w, q, or more generally at the *junctions* between pumping components. By unambiguity of L′, the map
token sequence ↦ (u, v) is injective. The only collisions after erasure are re-placements of the junction:
h(p)·u·h(w)·v·h(q) = h(p)·u′·h(w)·v′·h(q) with |u| ≠ |u′|. So the multiplicity is ≤ n + 1 per junction, and ≤ (n+1)^c·|Γ|^c
overall. This is the exact structural form of the n^{O(c)} loss the brief anticipated.

**Why the route fails already at c = 1.** The squeeze tolerates multiplicity only up to n^{β₀}/log n (§2). A single erased
junction costs up to n + 1 > n^{β₀}. Similarly, Lemma Rn (finite mean) gives word density ≥ c/n against the G⁻ density
n^{−½}, which is no contradiction.

The loss is real, not an artefact:
- **Example.** L′ = E*·#·E* (unambiguous: X → EX | #Z, Z → EZ | ε) gives h(L′) = E*. Every word with r excursions has
  multiplicity r + 1, and r ≍ n^{½} typically.
- The erased grammar X → EX | Z, Z → EZ | ε is linearly ambiguous and has no C_exp. By contrast, X → EX | XE is C_exp
  (EXE has two parses).
- So in PCFL the split multiplicity comes from **chains of pumping components in series** with an erased junction. Wich's
  "no C_exp" forbids only the both-sided self-recursion.

Applying T8_unamb "to L′ directly" therefore proves only that L′, with the walk ignoring markers, cannot carry
**pair** mass N^{β₀} inside Q_n(C) **with injective erasure**. It says nothing once the erasure is n-to-1.

## 4. Route (2): which gaps are polynomial, constant, or exponential [written proof for the classification]
| squeeze | lower side | upper side | gap |
|---|---|---|---|
| Thm M exponent (no α = −1) | — | — | holds for T(z) only. For ambiguous L the word counts need not be algebraic (2ⁿ/n = 2ⁿn^{−½}·n^{−½} with mult n^{½}) — **polynomial** |
| Lemma Rn (finite mean) | tree density ≥ c | word density n^{−½} | n^{½}: **polynomial** |
| PR1s / one-sided wedge | N^{β₀} | N^{1/3} (DW) | **polynomial** (and fails for β₀ ≤ 1/3 even when unambiguous) |
| PR2⁺ (two-sided) | tree N^{β₀} | word O(log N) | N^{β₀}/log N: **polynomial** |
| **word level, two-sided** | rotation-dense: \|L_n\| ≥ δ2ⁿ/n | Q_n(C): ≤ c_C 2ⁿ/n | **constant: no gap** (L3) |

**(L3) The quadrant is a rotation cross-section.** In Q_n(C), position 0 is within C of the cyclic maximum of the walk on
both sides. The number of rotations near the maximum is O_C(1) in expectation, and the density ≍ 1/n is exactly the
cross-section density (4/π at C = 0, r16 §2). So MS⁺ alone allows a rotation-dense L at the word level. All the leverage in
PR2⁺ is the ratio of tree mass to word mass, which is exactly what polynomial ambiguity can pay.

**Ceiling lemma (count squeezes cannot reach linear ambiguity).**
- For a fixed (p, w, q), the pair mass satisfies U(N) = Σ_{n≤N} u(n) ≤ N + 1, since u(n) is a renewal probability ≤ 1.
- Only O(1) contexts can be forced by finitely many grammar SCCs.
- Any word-mass upper bound valid for a rotation-dense L is ≥ δ log N.
- So any squeeze of the form "forced pair mass vs word mass" yields at best m_N ≳ N/log N. It can never exclude ambiguity
  Θ(n) or above, and with actual tails it caps at n^{β₀}.

**Amplification fails.**
- *Iterating over SCC depth:* the depth is ≤ |N|, so the product of O(1) polynomial gaps is polynomial.
- *Iterating blocks inside one renewal:* still a mass comparison, so the ceiling lemma applies.
- *Concatenation powers:* G⁻ is not closed under concatenation.
- Every quantity in play is 2ⁿ·n^{O(1)}. The only exponential is 2ⁿ itself, and it is matched by |G⁻_n| ≍ 2ⁿn^{−½} and by
  the cross-section ≍ 2ⁿ/n.
- An exponential gap needs **ω(log n) disjoint locally ambiguous nodes** (newmech Lemma M, criterion W), or Wich's C_exp
  directly. Neither is a count statement (cf. r8 Thm C).

## 5. Exact remaining gap (what would prove T8_poly)
Either of the following would suffice.
- **(G-word) Word-level sharpening, ambiguity-independent.** A closure property of L under token insertions (MS⁺-type,
  set-level) forces |L_n| = o(2ⁿ/n) inside Q_n(C), i.e. a sub-cross-section superset. Because it is set-level, it would
  prove T8 for **all** CFGs in the two-sided case. By L3 it must use more than A ≤ C, B ≥ −C, e.g. junction/split
  information or the G⁻ coupling A < B on top of the quadrant.
- **(G-struct) Structural.** In a polynomially ambiguous G with L ⊆ G⁻ and an L dense in the cross-section, show that the
  split multiplicity at a junction must be realised by a self-overlapping loop pair (am(X, αXβ) > 1, i.e. C_exp). The
  E*#E* example shows chained components evade C_exp in general, so the proof must use G⁻.

## Status
| claim | label |
|---|---|
| Lemma F / Cor H / MS⁺ / quadrant bound hold for any cycle-free G (tree series) | written proof (r10–r12 chain not re-audited for unambiguity uses) |
| PR2⁺ ⇒ ambiguity ≥ cN^{β₀}/log N in the two-sided case | written proof |
| L1: Wich markers never sit on critical loops or their lower blocks; loss = junction re-placement ≤ (n+1)^c\|Γ\|^c | written proof |
| Route (1) (Wich projection) | **fails at c = 1**: the junction loss n > n^{β₀} |
| L3: Q_n(C) is a rotation cross-section, so the word-level gap is constant | proof sketch (cycle-lemma heuristic for the O_C(1) count) + r16 DP |
| Ceiling lemma: count squeezes cannot exclude ambiguity ≥ n/log n | written proof |
| All T8_unamb gaps polynomial or constant; no exponential gap is available | classification (written) |
| T8_poly | **OPEN**; exact gaps (G-word) or (G-struct) in §5 |
