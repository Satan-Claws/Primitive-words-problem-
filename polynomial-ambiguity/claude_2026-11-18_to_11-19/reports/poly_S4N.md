# S4N: the balanced slice Q ∩ {#a = #b} and necklaces over the Dyck-prime code (Session 4)

Status: **(1) PROVED** (exact cyclic factorization, all multiplicities of minima). **(2) Affirmative: NO** — the
infinite alphabet does not help; a 2-letter sub-alphabet already contains the full problem. **(3) PROVED:**
Q reduces to the balanced slice with amb_Q(n) ≤ amb_Bal(4n) (one direction). Analytic handle only rules out
unambiguous grammars; it says nothing about the polynomial question.
Check: `polynomial-ambiguity/claude_2026-11-18_to_11-19/scripts/s4n_bal.py` (all 17576 balanced words of length ≤ 16; σ on all u, |u| ≤ 14; 0 mismatches).

Notation. Bal = {w : #a = #b}, walk h (a = +1, b = −1). D = Dyck language (h ≥ 0 on prefixes, h(w) = 0).
C = aDb = Dyck primes (nonempty Dyck words with no proper nonempty Dyck prefix). D = C* freely (C is a prefix code).

## 1. Exact cyclic factorization (Lemma N1)

Correction to the brief: the number of pieces is m = #(positions where the cyclic walk attains its minimum),
1 ≤ m ≤ g, not g.

Let w ∈ Bal, |w| = n ≥ 2. Let h_0..h_{n−1} be the cyclic walk values (h_i = h(w[:i])), μ = min, and
M = {i : h_i = μ}, |M| = m.
- (a) For i ∈ M, rot_i(w) ∈ D \ {ε}, and its C-factorization has exactly m factors, the cuts being M (shifted).
  *Proof:* after rotating to i, all walk values are ≥ 0 and the zeros are exactly M − i. A Dyck word's
  C-factorization cuts are exactly its interior zeros. ∎
- (b) (Uniqueness / circularity) If w is a cyclic shift of u_1⋯u_r with u_j ∈ C, then {cuts} = M and r = m.
  *Proof:* each u_j has h = 0 and h > 0 strictly inside, so cut values are all equal and strictly below every
  non-cut value; hence cut values = μ and cuts = M. ∎
  So the map [w] ↦ necklace ⟨u_1,…,u_m⟩ over the (infinite) alphabet C is a **bijection** between conjugacy
  classes in Bal \ {ε} and nonempty necklaces over C.
- (c) **w primitive ⇔ the necklace ⟨u_1,…,u_m⟩ is primitive.** (⇐) if u_1⋯u_m = s^k over C, the word is
  (concat s)^k. (⇒) if w ~ v^k, k ≥ 2, then v ∈ Bal and M is invariant under shift by |v|, so the piece
  sequence has period m/k. ∎
- (d) Linear version: a Dyck word x ∈ D is primitive over {a,b} iff its C-word is primitive over C (if x = v^k
  then v ∈ D since h(v) = 0 and h ≥ 0 on prefixes). So **Q ∩ D ≅ Prim(C*)** under the free-monoid
  isomorphism D ≅ C*, and Q ∩ Bal = cyc(Q ∩ D) with class mass exactly m (the m rotations at minima are
  distinct because w is primitive).

Consequences. m = 1 classes (unique minimum) are exactly C up to conjugacy and are all primitive — this is
L_{1,1} of S4C. By S4C Theorem C, a grammar G for Q ∩ D gives cyc with amb_{G′}(w) = m·amb ≤ (n/2)·amb.
So Q ∩ Bal is poly-ambiguous ⇔ Q ∩ D is (up to a factor n; the ⇐ via Theorem C, ⇒ via the D-filter is NOT
automatic, see §4 for what is proved).

## 2. Affirmative direction: does the infinite alphabet help? NO

Lemma N2. Let σ: {x,y}* → {a,b}*, x ↦ ab, y ↦ aabb. Both images are in C, so σ(u) ∈ D and its C-word is u
letter for letter. By N1(d), **σ(u) ∈ Q ⇔ u ∈ Q** (binary primitive words). Also σ(u) ∈ Bal always.

So the "pieces of different lengths break periodicity" idea gives nothing: the restriction of Prim(C*) to the
two letters {ab, aabb} (lengths 2 and 4) is exactly a copy of binary Q. An infinite alphabet only adds
classes. Length heterogeneity is a *letter* distinction in C*, which is the binary problem, not a shortcut.
The unambiguity of C (one-counter) is irrelevant: the difficulty is entirely primitivity over C*.

## 3. Negative direction: the balanced slice is the whole problem (PROVED, one way)

Theorem N3. If G is a cycle-free CFG for Q ∩ Bal (resp. Q ∩ D) with amb ≤ f(n), then Q has a cycle-free CFG
with amb_Q(u) ≤ f(4|u|) (in fact = amb_G(σ(u))).
*Proof:* σ(Q) = Q ∩ Bal ∩ {ab, aabb}* = Q ∩ D ∩ {ab,aabb}* by N2. Intersect G with the DFA for
{ab,aabb}* (product preserves amb exactly), then apply σ^{-1}: {ab, aabb} is a prefix code, so decoding is a
deterministic transducer with a unique run and amb_{σ^{-1}G}(u) = amb_G(σ(u)) (the nonerasing h^{-1}
transfer lemma of poly_S4I.md). |σ(u)| ≤ 4|u|. ∎

So any lower bound for Q transfers to the balanced slice (and to Q ∩ D, Prim(C*)) with n ↦ n/4, and the
balanced slice is at least as hard. Converse (Q poly ⇒ Q ∩ Bal poly): NOT obtained — intersection with the
non-regular Bal is not grammar-preserving, and no primitivity-reflecting rational map from {a,b}* onto Bal
is known to us. It is not needed for hardness.

## 4. Analytic handle (structure only)

Language GF: P(z) = Σ_n |Q ∩ Bal ∩ Σ^{2n}| z^n = Σ_{d sq.free} μ(d) (B(z^d) − 1), B(z) = (1−4z)^{-1/2}
(Möbius over the period; balanced periods are balanced). The d-term is analytic on |z| < 4^{-1/d}; the tail
converges locally uniformly in |z| < 1, so P continues to the unit disk minus slits, with a branch point at
every ζ·4^{-1/d} (ζ^d = 1, d squarefree). Distinct d give distinct moduli, so nothing cancels.
Infinitely many singularities ⇒ **P is not algebraic** ⇒ (Chomsky–Schützenberger) Q ∩ Bal, Q ∩ D and
Prim(C*) have **no unambiguous CFG**. (This is Flajolet's argument for Q, transplanted.)

Limit: for k- or poly-ambiguous grammars only the derivation GF Σ amb(w) z^{|w|} is algebraic. Relating it
to P is a count sandwich, which is BLOCKED. The central-binomial / Catalan structure (C(z) = (1−√(1−4z))/2,
P = Σ μ(d)·(1/(1−C(z^d)) − 1) over the C-alphabet) is just this Möbius formula and gives no
super-unambiguous obstruction. Stronger lower bounds come from N3 plus Theorem P / Petersen:
amb = Ω(√(log n / log log n)) on Q ∩ Bal.

## 5. Exact remaining question

Is Prim(C*) — equivalently Q ∩ D, equivalently (by S4C) Q ∩ Bal — poly-ambiguous? By N3 a yes answer gives
poly-ambiguity of Q. By S4C's ratio decomposition, the gcd ≥ 2 classes of every ratio reduce to Prim(P_{p,q}^*)
over a CF prefix code, so the original problem is equivalent to: **is there a family of polynomially ambiguous
grammars for Prim(X*), X an infinite unambiguous-CF circular code, uniformly over the ratio codes P_{p,q}?**
The single-code question (X = C) is already as hard as Q. Open: the converse Q-poly ⇒ (Q ∩ Bal)-poly.
