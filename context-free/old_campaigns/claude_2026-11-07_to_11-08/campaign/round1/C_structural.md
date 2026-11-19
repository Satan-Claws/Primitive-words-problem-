# Round 1 / Route C: structural (derivation-tree) cross-word exchange arguments

Author: researcher C. Status: **negative for the proposed mechanism.** I prove a rigorous no-go for the mechanism as posed. I also give a stronger no-go for its natural relaxation: it is proved for prime-power lengths and checked by computer elsewhere. The one case left open is a combinatorial lemma, not something of theorem strength. Any structural argument that could still work has to use more than one swap per collision. Once it uses the full closure under grafting, that is the original problem again.

Code and outputs live in
`/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/structural/`
(`lemmaAB.c`, `lemmaB_finite.py`, `uniform.c`, `uniform_mm1.c`, `treesafe.c`, `mixsafe.c`, `mixsafe_s.c`, `t2.c`).

---

## 0. Setup and the swap principle

G is in CNF with L(G) = Q and k nonterminals. Fix a length n. For an interval I = [i,j) ⊆ [0,n), write a word w ∈ Σⁿ as w = x·y·z with |x| = i and |y| = j−i. Here *y is the filler* and *c = (x,z) is the context*. Because Q and every power set are closed under rotation, I treat the context as the cyclic factor z·x, which is contiguous on the cycle Z_n.

**Swap principle.** Suppose the derivation trees of w and w' both have a node labelled A at the same interval I. Then both crossovers c₁(I) = x·y'·z and c₂(I) = x'·y·z' are in L(G) = Q.

**Proposed mechanism.** Every tree has a node whose length lies in [m,2m). There are at most k·n² triples (A,i,j). So a family F ⊆ Q ∩ Σⁿ with |F| > k·n² forces a collision. The prover wants F built so that **every** collision gives a non-primitive crossover. The prover cannot control the interval, so the requirement is a property of pairs:

> (U) for all w ≠ w' ∈ F and every interval I with m ≤ |I| ≤ 2m−1, c₁(I) ∉ Q or c₂(I) ∉ Q.

Notation: D = D(w,w') = {p : w[p] ≠ w'[p]}. Both c₁(I) and c₂(I) depend only on the *trace* I∩D. Moving one D-position into or out of I changes each crossover in exactly one letter.

---

## 1. Two rigidity lemmas for non-primitive words

**Lemma A.** If x ≠ y are non-primitive words of the same length n, then d_H(x,y) ≥ 2.

*Proof.* View x and y as functions on Z_n. x is invariant under a shift α ≠ 0 and y under a shift β ≠ 0 (proper divisors of n). Suppose they differ only at p, with s = x(p) ≠ t = y(p).

- **Case α+β ≢ 0.** None of p+α, p+β, p+α+β equals p, so x and y agree at those positions. Then t = y(p) = y(p+β) = x(p+β) = x(p+α+β) = y(p+α+β) = y(p+α) = x(p+α) = x(p) = s. Contradiction.
- **Case α+β ≡ 0.** Then y is also invariant under α. The difference set {p} is then α-invariant, which is impossible. ∎

**Lemma B.** If x ≠ y are non-primitive of length n and differ in exactly two positions p, q, then n is even and q ≡ p + n/2.

*Proof.* Let δ = q−p ≠ 0. Let x have a proper period d₁ (so it is invariant under H₁ = ⟨d₁⟩, of order a = n/d₁ ≥ 2), and let y have period d₂ (H₂, of order b).

**Step 1 (chain condition).** Take any α ∈ H₁∖0 and β ∈ H₂∖0 with α+β ≠ 0. The chain from the proof of Lemma A must pass through q, so δ ∈ {α, β, α+β}.

**Step 2 (case split).** Let A = H₁∖{0,δ} and B = H₂∖{0,δ}.
- If A = ∅, then H₁ = {0,δ}, so δ = n/2. Done. The same holds if B = ∅.
- Otherwise α+β ∈ {0,δ} for all α ∈ A and β ∈ B. Fixing β gives |A| ≤ 2, so a ≤ 4; likewise b ≤ 4.
  - If g = gcd(a,b) ≥ 2, both words have period n/g. The difference set is then n/g-invariant and has size 2, so g = 2 and δ = n/2.
  - Otherwise (a,b) ∈ {(2,3),(3,2),(3,4),(4,3)}. Split Z_n into the t = n/(ab) residue classes mod t. On each class (a copy of Z_{ab}), x is invariant under +b and y under +a.
    - If p and q lie in different classes, Lemma A applies to each class and gives a contradiction.
    - If they lie in the same class, the problem lives on Z₆ or Z₁₂. Exhaustive check (`lemmaB_finite.py`, alphabets up to d₁+d₂ letters) gives 0 violations. ∎

*Check:* `lemmaAB.c` enumerates all binary non-primitive words for n ≤ 24. It finds no distance-1 pair, and every distance-2 pair has positions n/2 apart.

---

## 2. Theorem 1: no pair satisfies (U), at any scale

**Theorem 1.** Let n ≥ 3 and 2 ≤ m ≤ n/2, and let w ≠ w' be primitive words of length n. Then some interval I with |I| ∈ {m, m+1} makes **both** crossovers primitive. In particular, no two-element family satisfies (U). This holds even when only the lengths m and m+1 are allowed.

**Path lemma.** Let I₁, I₂, I₃ be intervals, each with a non-primitive crossover. Suppose the traces change by a single D-position p from I₁ to I₂, and by a single D-position q ≠ p from I₂ to I₃. Then |p−q| = n/2.

*Proof of the path lemma.* Without loss of generality c₁(I₁) ∉ Q.
1. c₁(I₂) differs from c₁(I₁) in one letter, so it is primitive by Lemma A. Hence c₂(I₂) ∉ Q.
2. By the same argument c₂(I₃) is primitive, so c₁(I₃) ∉ Q.
3. c₁(I₁) and c₁(I₃) differ exactly at {p,q}. By Lemma B, |p−q| = n/2. ∎

*Proof of Theorem 1.* Suppose every interval of length m or m+1 has a non-primitive crossover. Walk along

  [0,m) → [0,m+1) → [1,m+1) → [1,m+2) → … → [n−m, n).

Each step adds position i+m or removes position i. Over the walk, every position of [m,n) ∪ [0,n−m) = [0,n) is added or removed (this uses m ≤ n/2).

Look at the sequence of steps where the trace actually changes, i.e. steps at D-positions. Any two consecutive such steps either involve the same position or, by the path lemma, positions exactly n/2 apart. So D ⊆ {p₀, p₀+n/2}.

- **|D| = 1.** Then some length-m window misses D, because n > 2m−1. That interval has trace ∅, so its crossovers are w and w', both primitive.
- **|D| = 2 and m < n/2.** The window [p₀+1, p₀+m+1) misses D (trace ∅).
- **|D| = 2 and m = n/2.** The interval [p₀, p₀+n/2+1) has length m+1 and contains all of D, so its crossovers are w' and w.

Each case contradicts the assumption. ∎

*Check:* `uniform.c` does an exhaustive search over all pairs, all m, and all lengths in [m,2m−1] for n ≤ 16. It finds no pair satisfying (U). It also finds none when only lengths m and m+1 are allowed (`uniform_mm1.c`). A sanity run that restricts to the single interval [0,m) does find many such pairs, so the search is not vacuous.

**Corollary 1.** The mechanism as posed ("design F so that every collision is bad") is impossible. It already fails for |F| = 2. In rectangle language: there is no 2-element *fooling set* for middle-scale context×filler rectangles of Q.

---

## 3. The honest relaxation: a labelling game, i.e. rectangle covers

Here is what the swap principle really gives. For every pair (A,I), the words whose tree has an A-node at I form a set whose contexts × fillers lie inside Q. That is a combinatorial rectangle with respect to the split "inside I / outside I".

**Same-interval swap game.**
- The adversary gives each primitive w a binary tree on [0,n) and labels its internal nodes from [K], with K independent of n.
- The adversary **wins** if every same-label, same-interval collision has both crossovers primitive.
- If the prover can beat every adversary with fixed K, then Q is not CF, because a real grammar is such an adversary. This game is exactly the "pigeonhole + cross-word swap" mechanism with every node of every tree available to the prover.

**Proposition 2 (fixed interval: small cliques, large chromatic number).**

Fix I with |I| ≤ n/2, and let G_I be the "bad-swap" graph on Q ∩ Σⁿ.

(a) **Small cliques.** Every clique has fewer than 2τ(n) vertices.

*Proof.* A context (x,z) has length ≥ n/2, and any proper divisor d of n is ≤ n/2. So the context admits at most one completion to a d-periodic word for each such d, i.e. fewer than τ(n) completions in total. Two words with the same filler are never adjacent. Orient each edge of a clique towards the vertex whose filler completes the other's context. Some vertex then has out-degree ≥ (t−1)/2, while every out-degree is less than τ(n). ∎

(b) **Large chromatic number.** The chromatic number is nevertheless unbounded. Take contexts c₁,…,c_t with distinct square completions σ_i, and the words (c_i, σ_j) for i ≠ j. These induce the shift graph of the complete digraph, whose chromatic number is about log₂ t.

So if the adversary were forced to put all words at one interval, the prover would win. The adversary escapes by choosing a tree for each word.

**Theorem 2 (8-letter labelling scheme).** For a node I = [i,j) of w and each prime p | n, let d_p = n/p. The certificates are:

- **C_p**: the context of w has no period d_p.
- **A_p(a)**, for a ∈ {i, j−1}: some o ∉ I with o ≡ a (mod d_p) has w[o] ≠ w[a].
- **F_p**: the yield of w has no period d_p.
- **B_p(b)**, for b ∈ {i−1, j} (mod n): some o ∈ I with o ≡ b (mod d_p) has w[o] ≠ w[b].

A node is **OK** if one of the following holds:
- *C-side*: for some a, every prime p has C_p or A_p(a). The label is (C, which end, w[a]).
- *F-side*: for some b, every prime p has F_p or B_p(b). The label is (F, which end, w[b]).
- The node is a leaf, labelled by its letter, or the root.

Then any two words that share a label at the same interval have both crossovers primitive.

*Proof.* Primitivity is equivalent to having no period d_p for every prime p. Take the C-side case and r = c_w·y_{w'}.
- If C_p holds, r contains w's d_p-aperiodic context, so r has no period d_p.
- If A_p(a) holds, then r[a] = w'[a] = w[a] (same label) and r[o] = w[o] ≠ w[a]. Since o ≡ a (mod d_p), r has no period d_p.

The other crossover, and the F-side case, are symmetric. ∎

So a word that has a tree with every node OK is invisible to the game. The adversary needs only 2·2·|Σ| + |Σ| + 1 labels (11 for binary), for every n.

**Theorem 3 (rigorous for prime powers).** If n = p^e, every primitive word of length n has an all-OK tree.

*Proof.* Since w is primitive, there is a pair u < v, in the same class mod d = n/p, with w[u] ≠ w[v]. Use the tree

  root → [0,u) and [u,n);  [u,n) → [u,v) and [v,n);  arbitrary subtrees below.

- Every node that contains u starts at u and does not contain v, so A_p(u) holds.
- Every node that contains v (and not u) starts at v, and its partner u lies outside it, so A_p(v) holds.
- Every other node avoids both u and v, so C_p holds. ∎

**Computer check for general n** (`mixsafe.c`, exhaustive): all primitive binary words of every length n ≤ 22 have all-OK trees, including n = 6, 10, 12, 14, 15, 18, 20, 21, 22. `mixsafe_s.c` checked 20,000 sampled words for each of n = 30, 42, 60 (three primes). Half the sample is near-powers u^p with 1–2 flips, the hard cases. There are 0 failures.

**Earlier, weaker data.** With only C/F certificates and no anchors (`treesafe.c`), the hard core is still exponential, roughly 2^{0.69n}. For n = 2^k it is exactly the "near-squares" with 1 or 2 mismatched pairs (w[q] ≠ w[q+n/2]). Anchors remove this core entirely.

**Open Lemma S (multi-prime).** Every primitive word has an all-OK tree. This is proved for prime powers and checked as above. The simple "star" trees (all nodes share one endpoint k) do **not** suffice: they fail for some words at n = 12, 18, 20 (`t2.c`), so a proof needs adaptive trees. I rate S as a finite-combinatorics lemma (Fine–Wilf-type), not of theorem strength. Until it is proved, the rigorous no-go covers only prime-power lengths. A prover forced to use n with many prime factors is still not ruled out formally.

---

## 4. Where the argument breaks, and what remains

1. **The literal mechanism is dead (Theorem 1).** It is not merely the pumping-style "decomposition is adversarial" problem. Distinct non-primitive words are at Hamming distance ≥ 2, and distance-2 pairs are rigid (Lemmas A and B). So as one interval endpoint slides, the bad crossover would have to alternate between c₁ and c₂ in a way that cannot be sustained.
2. **The relaxed one-swap game is (almost certainly) won by an 11-label adversary.** This is Theorem 3 plus Lemma S. Pigeonhole collisions are then harmless, whatever family is chosen. Rectangle-cover or fooling-set lower bounds over middle-scale splits therefore cannot work. This matches the known limitation of communication-complexity bounds to unambiguous grammars.
3. **What the adversary's scheme does not survive**, which is where a structural proof would have to live:
   - (i) Swaps between same-label nodes at *different* positions or lengths. The anchors are tied to the endpoints of I, and a length change alters the divisor set.
   - (ii) *Iterated* grafting. A crossover's grafted tree need not be all-OK.
   - (iii) Consistency of productions.

   (ii) together with (iii), in full, is exactly "a CFG generating Q exists". Any argument that uses them must exploit genuinely global grammar structure. Its missing ingredient is of **theorem strength**: a lower bound against covers by "grammar-closed" rectangle systems, which is open even in the communication-complexity setting.
4. **Recommendation.** Do not invest further in single cross-word exchanges at fixed positions, whatever family F is used. If structural routes continue, they should target (i): exchanges that change the length into a highly composite n'.
