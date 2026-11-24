# r17_gtrunk.md — R17b-G′: closing G-trunk? (constant slide multiplicity)

Status:
- **G-trunk is NOT closed.** The brief's two hoped-for facts are both **false**:
  - "only O(1) junction re-placements keep the word in G⁻" fails, because set-level constraints cannot see the centre (§3);
  - "the slide multiplicity is O(1) per word" fails even inside ONE C_exp-free linear SCC with fixed context and fixed
    exit (§4, Example S, worst case Θ(n)).
- **Exact sharpening.** In the two-sided level case, combining G-word (finite word mass) with PR2⁺ reduces G-trunk to an
  **average**-multiplicity statement (AM) about the renewal measure. This uses the identity in §2 (written proof).
  Worst-case bounds are not needed. In Example S, (AM) holds numerically (mean multiplicity ≈ 1.3–2.2, flat in n).
- Two more facts, both with written proofs:
  - the 2-SCC (E*#E*-type) junction slides are frozen in the fixed-exit pair family (§1);
  - single linear SCCs violate the Weber–Seidl "one SCC ⇒ bounded ambiguity" analogue (§4).

Scripts (all in `scripts/`):
- `r17_gtrunk_slide.py`: random search over single-nonterminal linear SCCs;
- `r17_gtrunk_ex.py` → `r17_gtrunk_ex_out.txt`: Example S to depth 14;
- `r17_gtrunk_typ.py` → `r17_gtrunk_typ_out.txt`: typical multiplicity of Example S.

Notation as in r16/r17_gstruct:
- the pair family 𝒫 = 𝒫(p, X, exit) is the set of trees made of a fixed context S ⇒* pXq, a C-spine of i.i.d.
  first-return tokens, and a fixed exit subtree X ⇒* w;
- W(t) = p U w V q is the word of a tree t;
- m(W) := #{t ∈ 𝒫 : W(t) = W} is the multiplicity in the family.

## 1. Where the n-dependence enters [written proof]
**Lemma 1 (fixed-family multiplicity = exit slides inside C).** Let G be C_exp-free and t, t′ ∈ 𝒫 with W(t) = W(t′).
- If the exit node has the same span in t and t′, then t = t′.
- Hence m(W) ≤ #{j : M = U w V with |U| = j and (U, V) a C-interface} ≤ occ_w(M) ≤ n.

*Proof.*
1. The context is a fixed tree, and p, q have fixed lengths. So the top X-node has span [|p|, n − |q|) in both trees.
2. The exit subtree is fixed. If its span agrees too, both spines are pumping trees X ⇒* UXV with the same interface.
3. By IF (r17_gstruct Cor (c), Lemma IF) they coincide. The lower-block subtrees coincide by SU, since they are loop
   sides. ∎

**Consequences.**
- *Trunk junctions outside C cannot slide inside 𝒫.* The other ≤ K − 1 trunk junctions sit in the fixed context or
  in the fixed exit subtree. In particular, the E*#E* slide (X → EX | Z, Z → EZ | ε) is invisible: with the exit
  Z ⇒ ε fixed, E^r has exactly one tree in 𝒫.
- So the hypothesis "every X ∈ C is ambiguous" in G-trunk is irrelevant. All that matters is the **intra-C exit
  slide**.
- The n-dependence enters only through the **position** of the exit node. That position can take ≤ n values, which
  is the source of Wich's factor n per junction. The ℓ^{|N|} of the Trunk Lemma counts junctions, not positions.

## 2. Reduction to average multiplicity [written proof, two-sided level case]
**Identity.** Σ_{W ∈ W(𝒫), |W|≤N} 2^{−|W|} = Σ_{t ∈ 𝒫, |t|≤N} 2^{−|t|}/m(W(t)). This holds because each word is
counted m(W) times with weight 1/m(W).

**Inputs.**
- **G-word** (r17_gword Thm, set-level, any ambiguity): pair words have bounded context (p, q fixed). Using both
  outermost level insertions, they lie in F_n(C₁). So the left side is **≤ c < ∞ for all N**.
- **Renewal**: the tree mass is U(N) = Σ_{n≤N} u(n) ≥ cN^{β₀}, by Lemma R plus the tail bound, with no ambiguity used.
  Write E_n for the uniform law on the trees of 𝒫 of length n (weights 2^{−|t|}).

**Prop AM.** If max_{n≤N} E_n[m] = o(N^{β₀}), then the two-sided level critical SCC is impossible in G⁻. This holds in
particular if the multiplicity is **tight**, i.e. sup_n E_n[m] < ∞.
*Proof.*
1. By Jensen, E_n[1/m] ≥ 1/E_n[m].
2. So the right side of the identity is ≥ U(N)/max_{n≤N}E_n[m], which tends to ∞.
3. This contradicts G-word. ∎

Compared with PR2⁺, which needed the **worst case** m ≤ N^{β₀}/log N, the requirement is now on the **mean** and has
no log. The ceiling lemma (r17_lift §4) does not apply, because it concerns worst-case multiplicity. A
mean-multiplicity bound is a statement about the token process, not a mass squeeze.

*Remark (one-sided, sketch).* The same identity can replace injectivity in Thm OH (r17_oh_level):
- class 1 is a word-level bound;
- class 2 is bounded by tree mass, and 1/m ≤ 1;
- step 1 becomes U(N)/max E[m].

So OH lifts under the condition max_{n≤N}E_n[m] ≤ N^{β₀−3γ/4−ε}. Not written out in detail.

## 3. Set-level constraints are centre-blind [written proof]
**Lemma CI.** Suppose W ∈ F_n(c), W = L·R is any split, and x is any word with |P_x(i)| ≤ K for all i and
|wt x| ≤ K. Then W′ = L x R ∈ F_{n′}(2c + 2K). In particular W′ ∈ Q(2c + 2K).

*Proof.* The prefix walk of W′ is:
- P on L;
- P(|L|) + P_x on x, which is ≤ c + K;
- shifted by wt x on R.

So max P_{W′} ≤ c + K. The endpoint is P(n) + wt x ≥ −c − K, since W ∈ F gives P(n) ≥ max P − c ≥ −c. ∎

So every insertion constraint in the relaxed (additive-constant) form used by MS⁺, MS^in and FR, applied at **any**
candidate centre j, is already implied by W ∈ F. In particular:
- G⁻ plus insertions cannot single out the true centre among the ≤ occ_w(M) candidates;
- any Env/Ori-type monotonicity in the centre is vacuous on F.

This is consistent with r17_gword §4 (centre shifts gain at most constants) and with F1. Any bound on m must come from
the **token process** (grammar structure plus the renewal law), not from G⁻.

## 4. Example S: one C_exp-free linear SCC with Θ(n) exit slides [written proof + check]
The grammar is X → ab X ab | bb X a | X ba | ab, with tokens t₁ = (ab, ab), t₂ = (bb, a), t₃ = (ε, ba) and exit
w = ab. It has a single nonterminal and no lower blocks.

**Θ(n) slides.** For every k, m ≥ 0, the sequence t₃^m t₂ t₁^k has word bb(ab)^{2k+1+m}a. So the word
bb(ab)^{2N+1}a has ≥ N + 1 trees in 𝒫, with centres at 2, 4, …, 2N + 2.
- Script check (`r17_gtrunk_ex_out.txt`): max multiplicity 7 at depth 14.

**C_exp-free.** For a single nonterminal without lower blocks, C_exp ⟺ two distinct token sequences have the same
interface. Suppose they do.
1. *Counts.* Parikh counts give |U| = 2(x₁ + x₂), #a(U) = x₁ and |V| = 2x₁ + x₂ + 2x₃. So the token counts agree.
2. *Order of t₁/t₂.* {ab, bb} is a code, so U fixes the order of the t₁/t₂ subsequence.
3. *Parsing V.* Read rev(V) = rev(v₁)rev(v₂)⋯ with the code t₁ → ba, t₂ → a, t₃ → ab.
   - In a factor bb, the first b is a t₃-b and the second b is a t₁-b. So bb is a forced cut.
   - Each maximal factor between cuts is (ba)^j (all t₁), (ab)^j (all t₃), or a(ba)^j.
   - A factor a(ba)^j parses only as t₃^i t₂ t₁^{j−i}.
4. *Fixing i.* The known t₁/t₂ order fixes the number of t₁ between consecutive t₂'s. The pure factors' contributions
   are forced, so this determines i in each factor.
5. So the parse is unique. ∎
- Script check: 0 IF violations among all 3^{≤14} sequences.

**Typical multiplicity is tight.** Under i.i.d. tokens, E[m] and P(m ≥ 3) are flat in r (`r17_gtrunk_typ_out.txt`,
200 samples each):

| token law | r = 50 | r = 200 | r = 800 |
|---|---|---|---|
| uniform | E[m] = 1.37, P(m ≥ 3) = 0.055 | 1.40 | 1.31 |
| (.6, .2, .2) | 2.22 | 2.17 | 2.12, P(m ≥ 3) = 0.23 |

**Lessons.**
- The worst case Θ(n) is real within one SCC with fixed exit. So there is no worst-case route, consistent with the
  ceiling lemma.
- The Weber–Seidl fact "no EDA in one SCC ⇒ bounded ambiguity" has **no** linear-CFG analogue. Two-sided reading
  lets the overhang grow (the V-side t₃ run versus the t₂ shift).
- The slide requires a long global pattern (here a periodic run), which is rare under the renewal law. That makes
  (AM) plausible.

## 5. Structural lemma toward (AM) [written proof]
**Lemma NR (no resynchronisation).** Let t ≠ t′ ∈ 𝒫 have the same word. List their spine nodes from the top. Suppose
the token sequences first differ at depth d. Then after depth d, no spine node of t has the same (label, span) as a
spine node of t′.

*Proof.* Suppose such a pair of nodes existed. The two segments between the divergence node and that pair would be
distinct pumping trees Z ⇒* U′ Z′ V′ with the same interface, and Z, Z′ are in the same SCC. This contradicts IF in its
SCC form (Cor (c)). ∎

**Consequences.**
- The parses of W form a trie in which branches never re-merge.
- m(W) equals the number of branches that survive to a w-occurrence. Each surviving branch carries a span pair that
  stays permanently out of sync with every other branch.
- (AM) would follow from a **branch-survival estimate**: a desynchronised branch survives r further i.i.d. tokens with
  probability ≤ θ^{r}, θ < 1, uniformly in the overhang. That would give E_n[m] = O(1).
- Example S shows this requires care: the overhang can grow (the t₃ run), and a branch survives along periodic runs.
  But periodic runs of length r have probability ≤ θ^{r} under any non-degenerate token law. This is exactly the
  missing estimate.

## 6. Exact remaining gap
**(G-trunk) ⟸ (AM).** For the critical two-sided level linear SCC C of a C_exp-free grammar, with i.i.d. tokens of
law π (Σπ = 1, heavy U-/V-level blocks), the pair-family multiplicity satisfies max_{n≤N} E_n[m] = o(N^{β₀}). Tightness
sup_n E_n[m] < ∞ would be the natural form.
- (AM) is purely a statement about a C_exp-free linear grammar and its renewal law. G⁻ has already been fully used,
  through G-word.
- (AM) is not a mass squeeze, so the ceiling lemma does not apply.
- Candidate proof: Lemma NR plus a branch-survival bound under the heavy-tailed token law.
- Open risk: a heavy block might be re-parsable as many tokens of an alternative branch, which would make survival
  likely precisely on the giant block. I have no example of this, and it was not tested.

## Status
| claim | label |
|---|---|
| Lemma 1: in 𝒫 only the intra-C exit slides; other trunk junctions frozen; m ≤ occ_w ≤ n | written proof |
| Identity + Prop AM: G-trunk (two-sided level) ⟸ max_{n≤N}E_n[m] = o(N^{β₀}) | written proof (uses G-word, Lemma R) |
| OH lift under a mean bound | sketch |
| Lemma CI: insertion constraints at any centre are implied by F (centre-blind) | written proof |
| "O(1) re-placements keep W in G⁻" | **false** as a set-level route (Lemma CI) |
| Example S: C_exp-free single linear SCC, Θ(n) worst-case slides in 𝒫; mean m ≈ 1.3–2.2, flat in n | written proof + exhaustive (depth 14) + sampling |
| Lemma NR (no resynchronisation of distinct parses) | written proof |
| (AM) / T8_poly trunk case | **OPEN** (exact gap, §6) |
