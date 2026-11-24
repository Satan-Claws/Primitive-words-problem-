# W1-F: cyclic-closure class mass, gcd ≥ 2

Notation: Q = primitive words over {a,b}; [w] = conjugacy class; g(w) = gcd(#a(w), #b(w)) (a class invariant);
M_G([w]) = Σ_{r∈[w]} amb_G(r) (class mass). Scripts: `round2/scripts/cyclic_thmC.py`, `round2/scripts/cyclic_gcd.py`.

## 0. Summary

| item | status |
|---|---|
| Theorem C (amb_{G′}(w) = Σ_j amb_G(rot_j w), G′ cycle-free) reconstructed | [written proof] + [computational] (independent re-implementation: 10160 pairs, 8691 nonzero, 0 mismatches) |
| L1 Active-prime lemma | [written proof] + [computational] (all w, \|w\| ≤ 16) |
| L2 gcd is monotone under non-erasing morphisms | [written proof] + [computational] |
| T1 P_{≥2} ⇔ full problem (even restricted to balanced classes, g = \|w\|/2) | [written proof] (uses S4N Lemma N2, re-checked \|u\| ≤ 14) |
| L3 Divisor localization on fixed-#a slices | [written proof] |
| O1 coprime sub-problem P_cop is not reducible to/from gcd ≥ 2 by morphic transfers; slice methods are blind to it | [written proof] (blindness) / [conjecture] (that it is the second core) |
| Question (2) (1:1 cycle-lemma replacement) | **blocked**: exact self-reduction, ratio reappears one level down |
| Question (1) (pumping/interchange lower bound) | **gap**: reduces to the S_N ply problem; no new mechanism |
| Citation: Berstel–Boasson, "The set of Lyndon words is not context-free", Bull. EATCS 63 (1997) 139–140 | [published], bibliographic data confirmed (HAL hal-00619462); proof text not read |

## 1. Theorem C (reconstruction)

G in CNF, ε ∉ L(G). G′ has nonterminals N ∪ {[A] : A ∈ N} ∪ {S′}; for each B → A C in G add
[A] → C [B] and [C] → [B] A; add [S] → ε; for each A → x add S′ → x [A]; keep G's rules for the N-symbols.
[A] derives βα exactly when S ⇒* αAβ. A G′-derivation of w is S′ → w_1 [X_m] → … → [X_0 = S] → ε with
sibling subtrees from G; it encodes a unique pair (T, ℓ): a G-tree T and a leaf ℓ of T (the path S = X_0 → … → X_m → w_1
plus siblings, each on the recorded side), and w = rot_j(yield T) where j is the position of ℓ. Conversely each pair (T, ℓ) gives
exactly one G′-derivation, because the root-to-leaf path is unique. Hence **amb_{G′}(w) = Σ_{j<|w|} amb_G(rot_j w)**.
Cycle-freeness: the only ε-rule is [S] → ε. Replace each rule with [S] on the right by a copy that drops it. This is count-preserving, since
[S] ⇒ ε uniquely. The result has no ε-rules and no unit rules except [A] → C with C ∈ N, and those are not on any cycle because
N-symbols never derive [·]-symbols. So G′ is cycle-free. For primitive w the rotations are distinct, so amb_{G′}(w) = M_G([w])
**exactly**. For L(G) ⊆ Q, L(G′) = cyc L(G) ⊆ Q.

## 2. Lemmas

**L1 (active primes).** w is non-primitive ⇔ w = v^p for some prime p | g(w).
*Proof.* w = v^k gives #a(w) = k#a(v) and #b(w) = k#b(v), so k | g. Then take a prime p | k. ∎
So coprime classes are primitive with no witness needed. Only primes dividing g are "active".

**L2 (gcd monotonicity).** For a non-erasing morphism τ: {x,y}* → {a,b}* with Parikh matrix M, Parikh(τ(u)) = M·Parikh(u).
So g(τ(u)) is a multiple of g(u), and if det M = ±1 then g(τ(u)) = g(u). (Example: h(x) = ab, h(y) = abb has det 1.) ∎

**T1 (gcd ≥ 2 is the whole problem).** Let P_{≥2} be the statement: some CFG G with L(G) ⊆ Q meets every primitive class with g ≥ 2
with M_G ≤ C|w|^k. Then P_{≥2} ⇔ Q has a polynomially ambiguous grammar. The same holds with "g ≥ 2" replaced by "#a = #b".
*Proof.* (⇐) Take G = G_Q. Then M ≤ |w|·C|w|^k.
(⇒) Build G′ (Theorem C). Then L(G′) ⊆ Q and amb_{G′}(w) = M_G([w]) for every primitive w with g ≥ 2.
Let σ(x) = ab and σ(y) = aabb. Then σ(u) ∈ Q ⇔ u ∈ Q (S4N Lemma N2), and σ(u) is balanced with g(σ(u)) = |σ(u)|/2 ≥ 2 for u ≠ x.
Take the product of G′ with the DFA for {ab, aabb}*, which preserves counts. Decode with the prefix code σ^{-1}, which is exact
(S4N N3). This gives H with Q∖{x} ⊆ L(H) ⊆ Q and amb_H(u) = amb_{G′}(σ(u)) ≤ C(4|u|)^k. Then add H's start symbol → x. ∎
Note that σ lands in the classes of *maximal* gcd. By L2, no morphic transfer can land in coprime classes.

**L3 (divisor localization on fixed-#a slices).** Fix n and the slice Σ_n = (ab*)^n. Then #a = n, #b = Σx, and
g = gcd(n, Σx) is a regular function of w (count #b mod n). Partition Σ_n into the regular parts Π_d = {g = d}, for d | n.
Then:
- (i) Q ∩ Π_1 = Π_1 is regular and unambiguous.
- (ii) On Π_d, w ∈ Q ⇔ x ∉ V_p for every prime p | d. If p ∤ d then x ∈ V_p is impossible, since p | Σx.
- (iii) The inherent ambiguity of Q ∩ Σ_n is at most Σ_{d|n} (inherent ambiguity of Q ∩ Π_d), and at least the maximum over d.
  The upper bound is a union of grammars; the lower bound is a DFA product.

So superpolynomial ambiguity on Σ_n occurs iff it occurs on a single Π_d, at the cost of a factor τ(n) = n^{o(1)}.
For the S_N program (n = P_N²) the witnesses may be taken with g = d, and only the primes of d are active.
The heuristic ply ∏_k d_k becomes ∏_{p_k | d} d_k. A superpolynomial lower bound therefore needs ω(g(w)) → ∞ on the witnesses:
the witness classes must have gcd with unboundedly many prime factors. This is a necessary condition only, not a proof.

## 3. The two questions

**(2) Upper bound at ratio 1:1: blocked (exact self-reduction).** By S4N N1, a balanced class with m cyclic minima is a
necklace ⟨u_1,…,u_m⟩ over the Dyck-prime code C. The cycle lemma resolves m = 1. For m ≥ 2, "pick a canonical rotation"
is the primitive-necklace problem over C. Its restriction to {ab, aabb} is binary Q, with **arbitrary** inner ratio #x : #y.
So fixing the outer ratio to 1:1 frees the ratio one level down. Any second-level cycle lemma needs the word's own inner ratio,
and the union over ratios is non-CF (S4C §3: ∪L_{p,q} ∩ a*b*a*b* is the multiplicative condition xt > yz).
By T1, a solution here *is* the affirmative. No replacement for the cycle lemma at gcd ≥ 2 exists that does not solve the full problem.

**(1) Lower bound by pumping/interchange: gap, reduces to S_N.**
- Ogden pumping changes |w| and hence the class. It relates different classes and forces no multiplicity within one class.
- Interchange (Ogden–Ross–Winklmann) does preserve length. Applied to R = one L-representative per class of a family F, with
  pigeonholing on rotation offset and defect position (poly(n) loss, so still per-word), a swap w_i x_j y_i lands in L ⊆ Q only
  if it is primitive. A contradiction needs swaps that create p-th powers for an *active* prime p | g (L1).
- For F inside a fixed-block family (a*b*)^r, or any family capped by §6 (fixed-block, R_m, prime-power or squarefree n),
  CF transversals of bounded or linear mass exist (e.g. {a^x b^y a^z b^t : x≠z ∨ y≠t}, mass ≤ 4 on 4-block classes). So the
  argument fails there.
- By L3, F must have ω(g) → ∞, i.e. exactly the S_N regime. Forcing many swaps into p-th powers for many p simultaneously is
  the "for every prime, some witness" ply problem TILE_k + G3** under another name. No new mechanism was found.
- Lyndon non-CF (Berstel–Boasson 1997) concerns the multiplicity-1 transversal with a fixed rotation rule. It does not transfer.

## 4. Open sub-question isolated (O1): the coprime sandwich

P_cop: is there a polynomially ambiguous CFG H with {w : g(w) = 1} ⊆ L(H) ⊆ Q?
Equivalently, by Theorem C, a CF L ⊆ Q meeting every coprime class with polynomial mass.
- The full affirmative implies P_cop, so **¬P_cop would give the negative resolution**.
- By L2, morphic exact transfers cannot move gcd ≥ 2 classes into coprime ones, so P_cop is not known to be equivalent to the full problem.
- Per fixed ratio, P_cop is one-counter and unambiguous (cycle lemma). Per fixed #a it is regular (L3(i)). So every
  fixed-#a slice argument, S_N included, is blind to it.
- The difficulty is pure cross-ratio uniformity: the certificate "s#a − r#b = ±1 for some (r,s)" needs multiplication.
- [conjecture] Problems with any fixed bounded set of active primes (e.g. g a power of 2: primitive ⇔ non-square, with
  non-squares CF) reduce to P_cop-type sandwiches, because excluding the *inactive* primes is the same cross-ratio problem.

So the problem has two cores:
- (A) multi-prime witnesses at fixed ratio (S_N, needs ω(g) → ∞);
- (B) cross-ratio exclusion of inactive primes (P_cop).

The gcd ≥ 2 classes carry (A) and, via T1, everything. P_cop is a possibly strictly weaker affirmative and a strictly stronger negative,
attackable only by non-slice (cross-ratio) arguments.
