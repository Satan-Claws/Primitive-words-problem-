# r17_bridge.md — R17b-F: the bridge (step 5b), from a grammar for Q to a fold-type part

Script: `scripts/r17_bridge_core.py` → `scripts/r17_bridge_core_out.txt` (exact densities of G⁻ and of its padding-stable core).

## Verdict

1. **Route (1), regular or rational surgery: CLOSED NEGATIVELY** [written proof, Prop NR and Cor NR].
   - Let τ be a finite-valued rational relation with |input| ≤ |output| + c. This covers ∩R for regular R, length-preserving
     transducers and gsm-type maps.
   - No such τ has τ(Q) ⊆ G⁻ with τ(Q) rotation-dense, **at any ambiguity**.
   - The reason is that Q and Σ\* differ by a set of growth √2, which a rational operation cannot see.
2. **Route (2), using G's tree structure on the G⁻-part.** T8 uses "L ⊆ G⁻" in exactly one place: the substitution/padding
   step (MS, MS⁺ and their relatives). There it is used **for every token sequence of a fixed context**, that is, on a cone.
   - The "positive fraction of derivations" weakening is **false for every grammar** [written proof, Lemma Core].
     Padding-stable words lie in the quadrant, which has word mass O(log N). The G⁻-part has mass ≍ √N.
   - The weakest property of the T8 type that still works is **(CONE)**: G has a critical linear SCC and a fixed outer
     context p[·]q such that *all* words of that sub-grammar lie in G⁻.
   - (CONE) is a CF sublanguage of L(G) inside G⁻ with divergent mass. It is exactly the object that T8_μ forbids.
3. **Consequence [assessment, logically exact].** Modulo T8_μ, "L(G) = Q ⇒ (CONE)" is *equivalent* to ¬P(Q). So the bridge is
   not an easier lemma: the whole problem sits in it.
   - L(G) = Q does not imply (CONE) by any argument that uses only soundness. On L(G), soundness is Q-soundness, and the
     padding-stable core of Q is all of Q.
   - The cyclic-closure construction shows that G's trees on G⁻-words need not be aligned with the fold at all (§4).
4. **Where ambiguity enters (F1 check).** In T8 ambiguity enters *only* in the renewal lower bound, via injectivity of the pair
   map. The soundness side (MS⁺ → quadrant) is ambiguity-free.
   - For L(G) = Q, the soundness side gives nothing. The squeeze set is all of Q, of mass ≍ N ≥ N^β.
   - So no ambiguity bound can rescue a T8-type squeeze applied to L(G) directly.
   - A valid bridge must use **completeness** (Q ⊆ L(G)) together with ambiguity to *force* a G⁻-sound cone. No mechanism
     for this is known.

## 1. Route (1): no rational bridge [written proof]

**Prop NR.** Let R be regular with |R_n ∖ G⁻| = o(2ⁿ) along all n (for example ≤ C θⁿ with θ < 2). Then R is not
rotation-dense. In fact |R_n| = O(n^d θ′ⁿ) for some θ′ < 2.

*Proof.*
1. Take a trim DFA for R. If no SCC has spectral radius 2, then |R_n| = O(n^d θ′ⁿ) with θ′ < 2. So |Rot(R)_n| ≤ n|R_n|
   = o(2ⁿ), and R is not rotation-dense.
2. Otherwise some SCC K has radius 2. Each state has ≤ 2 out-edges, and the restricted matrix is irreducible with row sums ≤ 2.
   By Perron–Frobenius, every state of K has **both** transitions inside K. So K is closed under all words.
3. Take u reaching some q ∈ K. For each state s ∈ K fix a word v_s leading to acceptance, and put V = max|v_s|.
   Then R ⊇ {u x v_{q·x} : x ∈ Σ^m}, and on fixed m the map x ↦ u x v_{q·x} is injective (u x is a prefix of fixed length).
4. Fix u and v with |u|, |v| bounded. For uniform x, P(u x v ∈ G⁻) ≤ P(d_k < 0 for |u| + |v| < k ≤ n/2) = O(n^{−1/2})
   (difference walk from a bounded offset). A union over the ≤ |K| choices of v gives P(u x v_{q·x} ∈ G⁻) → 0.
5. So ≥ (1 − o(1))2^m words of R ∖ G⁻ have length in [m + |u|, m + |u| + V]. Some single length n therefore carries
   ≥ c·2ⁿ of them. This contradicts the hypothesis. ∎

**Cor NR.** Let τ be a k-valued rational relation with |x| ≤ |y| + c for every (x, y) ∈ τ. If τ(Q) ⊆ G⁻, then τ(Q) is not
rotation-dense. The same holds for L(G) ∩ R with L(G) = Q, and for any τ applied to L(G).

*Proof.*
1. τ(Σ\*) is regular.
2. τ(Σ\*) ∖ G⁻ ⊆ τ(P), where P is the set of powers. So |τ(P)_n| ≤ k Σ_{m ≤ n+c} |P_m| = O(2^{n/2}).
3. By Prop NR, τ(Σ\*) is not rotation-dense, and τ(Q) ⊆ τ(Σ\*) is not either. ∎

*Remark.* The proof never uses ambiguity, so it is a genuine no-go and not an F1 violation. For **CF** operators (L(G) ∩ C
with C a CFL) the statement reduces to ROT-FOLD-BALLOT itself: C would already be a CF set that is almost inside G⁻ and
rotation-dense. So route (1) is either impossible (rational) or circular (CF).

## 2. Audit: where "L ⊆ G⁻" is used in T8 [reading of r10, r13–r16]

| step | uses L ⊆ G⁻? | what it really uses |
|---|---|---|
| Thm M, Lemma F, Rn, Cor H (reduction to a critical linear SCC) | only to get Σ\|L_n\|2^{−n} = ∞ from rotation-density | CF structure of L, plus unambiguity (word count = tree count) |
| Lemma PC, Lemma Bot, Prop HL, Thm SM (block shape) | **no** (`r15_side.md` never mentions G⁻) | pumping inside the lower blocks; Bot uses unambiguity for radius ½ |
| MS / MS⁺ / PR1 / PR1s / PR2 / PR2⁺ (squeeze) | **yes, essentially**: "{pUwVq} ⊆ G⁻ for *all* token sequences" (r10_heavy l.37, r13 l.36, r15_onesided l.28) | the padded word W′ = ρ·s must lie in G⁻ (r16 §1 step 5) |
| quadrant / wedge density | no | elementary random-walk bounds |
| renewal lower bound (Lemma R) | no | i.i.d. tokens over **all** sequences, plus injectivity (**the only place ambiguity enters**) |

So the critical use is a **combination**:
- (i) closure of the sequence set under prepending tokens (renewal), and
- (ii) G⁻-membership of every member.

For L(G) = Q, (i) holds, because L(G) is substitution-closed. But (ii) is replaced by Q-membership, which is vacuous.

## 3. The weakest sufficient property, and why "positive fraction" fails [written proof + exact DP]

**Lemma Core.** Call W *padding-stable* for (C, ρ_U, ρ_V) if W ∈ G⁻ and its U- and V-padded versions W′ (r16 §1) are in G⁻.
Then every padding-stable W lies in Q_n(C′) for a constant C′. So the padding-stable words have word mass
Σ_{n≤N} 2^{−n}|·| = O(log N).

*Proof.* This is r16 §1 steps 3–5, applied to the single word W. Those steps use only W′ ∈ G⁻, never L ⊆ G⁻ for other
words. Then apply r16 §2. ∎

**Consequences.**
- (a) The G⁻-part of any G with L(G) = Q has word mass Σ|G⁻_n|2^{−n} ≍ √N (exact DP: √n·dens(G⁻) → 0.399).
  The padding-stable part has mass O(log N) (n·dens(core, C = 2) ≈ 3.1 at n = 512, bounded).
  So **"a positive fraction of the G⁻-derivations are padding-stable" is false for every grammar**, whatever its ambiguity.
  The fraction is Θ(n^{−1/2}). From `r17_bridge_core_out.txt`: √n·core/G⁻ = 5.0, 6.0, 6.8, 7.4, 7.7 for n = 32…512
  (slowly converging).
- (b) The squeeze contradicts injectivity only if the padding-stable sequences carry renewal mass ≫ log N. Lemma R gives
  renewal mass ≳ N^β only to a set closed under prepending **arbitrary** C-tokens.
  - A set closed only under ρ-padding gains no mass beyond its seed set, and the seed set is itself in the quadrant.
  - So a nonempty padding-stable set that is closed under prepending all C-tokens is needed, i.e. a cone {t·s₀ : t}.
- (c) The yields of such a cone are the language of the sub-grammar S ⇒\* pXq, X ⇒\* (C-loops)·(s₀'s inner derivation).
  This is a CFL, with ambiguity ≤ that of G, inside G⁻, and with divergent mass (in the unambiguous case).

**(CONE)** [the weakest property of this type]: some critical linear SCC C of G, with some outer context p[·]q and some seed,
generates only words of G⁻.

(CONE) is exactly the T8_μ hypothesis for a sub-grammar. r10_heavy l.37 already states T8_unamb as "no (𝒫, p, w, q) has all
its words in G⁻", which is (CONE)-negation for unambiguous grammars.

**Does L(G) = Q imply (CONE)?** Not by any soundness argument. For L(G) = Q every substitution-reachable word is in L(G) = Q,
so the "padding-stable core relative to Q" is all of Q, and soundness constrains nothing.

And modulo T8_μ (in whatever ambiguity class it gets proved), (CONE) fails for **every** grammar in that class. So
"L(G) = Q ⇒ (CONE)" ⟺ ¬P(Q) for that class. **The bridge is not easier than the problem** [logically exact, given T8_μ].

## 4. Fold alignment is not forced [written proof, via cyclic.md Theorem C]

Let G₀ be any grammar whose language R contains ≥ 1 rotation of every primitive word, with R ⊆ Q (any canonical-rotation set).
- The cyclic closure G = G₀′ has L(G) = Q and amb_G(w) = Σ_j amb_{G₀}(rot_j w).
- Each G-derivation of a G⁻-word w is a G₀-tree of some rotation rot_j w, with a marked leaf.
- The fold centre (position n/2 of w) is an arbitrary position of that G₀-tree.

So "the block/pair structure of G near the fold centre" (the T8 input) is not determined by L(G) = Q. A proof of (CONE) from
L(G) = Q would in particular have to show that every canonical-rotation set R with a poly-ambiguous grammar contains a
G⁻-sound cone after some rotation. That is ROT-FOLD-BALLOT in disguise.

## 5. Exact gap and what a real bridge would need

- **Exact gap.** T8's mechanism needs a renewal-closed family inside G⁻ (CONE). L(G) = Q supplies renewal closure, but only
  Q-soundness. Lemma Core shows that the G⁻-sound part of any grammar has log-mass, so it can never be shown to be a positive
  fraction.
- **What could work instead (suggestion, not a result).** A bridge must use *completeness* (Q ⊆ L(G)) and ambiguity jointly,
  e.g. "covering the tie family / gcd ≥ 2 classes forces ambiguity" (cores (ii)/(iii) of RESEARCH_NOTE §3). It must **not** go
  through a G⁻-sound sub-structure. Equivalently, the fold route is a sufficient obstruction only for grammars that
  *implement* the fold. Step 5b as stated ("every grammar for Q contains a dense fold-type part") is **not a sub-lemma; it is
  equivalent to the whole problem** given T8.
- **F1 check.** Every statement in this file is either a no-go for a construction (Prop NR, Lemma Core: ambiguity-free, and
  correctly so, since they *refute* routes) or an equivalence. Nothing here proves a density bound for all CFLs ⊆ Q.

## Status
| claim | label |
|---|---|
| Prop NR / Cor NR: no finite-valued, length-bounded rational map sends Q into a rotation-dense subset of G⁻ | written proof |
| Audit: G⁻ is used only in the padding/substitution step, on all sequences of a fixed context | reading of r10/r13/r15/r16 |
| Lemma Core: padding-stable ⇒ quadrant; the G⁻-part is never positively padding-stable (fraction Θ(n^{−1/2})) | written proof + exact DP (n ≤ 512) |
| (CONE) is the weakest T8-type property; (CONE) = CF ⊆ G⁻ with divergent mass | written proof (renewal needs prefix-closure) |
| L(G) = Q ⇒ (CONE) ⟺ ¬P(Q), modulo T8_μ | logically exact; **bridge = full problem** |
| Fold alignment not forced (cyclic closure) | written proof (Theorem C) |
| A completeness-based bridge | OPEN; no mechanism |
