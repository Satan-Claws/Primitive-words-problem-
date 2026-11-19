# S4M: morphic self-similarity / amplification (session 4, diverse mechanism)

Status: transfer lemmas **PROVED** [written proof, unaudited]. Amplification **REFUTED** in every
word-uniform form (constant factor, any G-derived G'). The word-dependent form is **equivalent to the target**
(circular, same as T1-P2). Theorem P cannot be bootstrapped this way (it gets worse).

Notation: h(a)=ab, h(b)=abb, R = h(Σ*) = (ab+abb)*, 2|w| ≤ |h(w)| ≤ 3|w|. A_G(L) = max_{|x|≤L} amb_G(x).

## 0. Q ∩ R = h(Q), and h^{-1}(Q) = Q
(⊇) If w = u^k then h(w) = h(u)^k. (⊆) Suppose h(w) = z^k with k ≥ 2. Then h(w) starts with a and ends with b,
so z does too. In h(w) every block contains exactly one a and starts at an a. Each copy of z starts at an a, so
z is a union of whole blocks and z = h(u). Since h is injective (a prefix code), w = u^k. ∎

## 1. Transfer Lemma (exact)
**Lemma T1 (pull-back).** Let G be cycle-free with L(G) = Q. Then there is a cycle-free, ε-free G_h with
L(G_h) = Q and amb_{G_h}(w) = amb_G(h(w)) for all w ∈ Σ⁺. Its size satisfies |G_h| ≤ C·|G| for an absolute C
(an NFA with 4 states, cubed, times the finitely many ε-subtrees).

*Proof.* Take the unambiguous NFA N for R with states 0,1,2,3 and transitions 0-a→1-b→0 (output a on the last
step) and 0-a→2-b→3-b→0 (output b on the last step). It is unambiguous because the block factorisation is
unique.
(i) Bar-Hillel product G×N with nonterminals [p,A,q]. Trees of G×N over x correspond one-to-one to pairs
(G-tree over x, accepting N-run on x). The run is read off the labels, so the count is amb_G(x)·1 for x ∈ R.
(ii) Relabel each terminal rule [p,A,q] → c with the output of the transition (p,c,q), which is a letter or
ε. The yield becomes exactly w, and trees stay in bijection.
(iii) The erasing nonterminals [p,A,q] have G-yields of length ≤ 2, the inside of a single block. They have
finitely many ε-subtrees, because G is cycle-free. Every nonempty N-loop p→p passes through state 0, and
state 0 is entered only by output transitions. So a derivation [p,A,q] ⇒⁺ α[p,A,q]β in which α,β produce no
output would need an output-free N-loop, which does not exist. Hence G×N has no erasing cycles.
(iv) Standard ε-elimination: for each rule and each choice of ε-subtrees for the erased occurrences, create
a fresh unit-routed copy. This is a bijection on trees with nonempty yield. It creates no unit cycles, by (iii).
Finally h^{-1}(Q) = Q by §0. ∎

**Lemma T2 (push-forward).** For any G' for Q, G := h(G') ∪ (G'×DFA(R^c)) generates Q and satisfies
amb_G(h(w)) = amb_{G'}(w), while amb_G = amb_{G'} on Q∖R.

**Consequences.**
- A_{G_h}(L) ≤ A_G(3L), and A_G(L) ≤ A_{G'}(L) for the G built in T2.
- Polynomial degree is preserved in both directions. The same holds for any bounded primitivity-preserving
  prefix code h_N with stretch c_N, giving A_{G_{h_N}}(L) ≤ A_G(c_N L).
- The size blow-up is a constant factor per step, so k steps give C^k|G|.

## 2. Amplification: refuted in uniform form
Here is what would be needed. (AMP) There is a constant m ≥ 2 and a map Φ from grammars for Q to grammars for
Q such that amb_G(h(w)) ≥ m·amb_{Φ(G)}(w) for all G and some word w ∈ Q fixed independently of G. Size does
**not** matter for the iteration, because amb_{Φ^k G}(w) ≥ 1 automatically when L(Φ^k G) = Q.

**Prop R (AMP is false).** Let G_0 be any grammar for Q. Apply T2 to Φ(G_0) to obtain G_1. Then
amb_{G_1}(h(w)) = amb_{Φ(G_0)}(w). Repeating gives
amb_{G_0}(h(w)) ≥ m·amb_{Φ G_0}(w) = m·amb_{G_1}(h(w)) ≥ m²·amb_{Φ G_1}(w) ≥ ⋯ ≥ m^k for every k,
which contradicts finiteness. The same contradiction holds for any m(|w|) > 1 and any family h_N, provided
the word is fixed across the chain. ∎

The "for all w" form is also false. Patching a single word (Q∖{x} through a DFA product, plus S → x) makes
amb = 1 at any chosen x.

**Word-dependent form.** For every G and every k there is a w with amb_G(h^k(w)) ≥ m^k. Because
|h^k w| ≤ 3^k|w|, this is precisely a lower bound L^{log m/log 3} for G on the slice h^k(Σ*). By T1 applied k
times, this is equivalent to a polynomial lower bound for the grammar G_{h^k}, which generates all of Q. So it
**is** the target statement, now on slices (circular, exactly like T1-P2).

**Sums do not arise.** A word x = h(u) = g(v) lying in two images gives two equalities:
amb_G(x) = amb_{G_h}(u) = amb_{G_g}(v). Both count the same trees of G, so the two parses do not add.
Disjoint slices combine under max, not under sum. Additivity would need a partition of G's trees on x into
classes, each of which is itself a full grammar for Q. Prop R kills that whenever the partition is
word-uniform.

## 3. Bootstrapping with Theorem P
Apply Theorem P to G_{h^k}. It has K_k ≤ C^k K, so the bound becomes amb ≥ p at length
3^k·exp(O(p²(log p + k + log K))). This is strictly worse than Theorem P applied to G directly. Also, h does
not preserve the (ab*)^n slices: h(ab^e) = ab(abb)^e changes the block count by Σe. So Lemma 3P's laminar
exponent coordinates are not equivariant under h. **No bootstrap.**

## 4. Exact missing step
A *non-uniform* amplification: for every G there is a sequence w_k (chosen depending on G and k) with
|w_k| ≤ c^k|w_0| and amb_G(w_k) ≥ f(k), where log f(k)/k → ∞ (superpolynomial) or f = m^k (polynomial).
By §2 this cannot come from any word-uniform inequality between grammars. It has to come from G-specific
structure, which is the slice/laminar machinery of Theorem P / Lemma G*. Self-similarity contributes only the
equivalence "slice h^k(Σ*) ≡ whole problem".
