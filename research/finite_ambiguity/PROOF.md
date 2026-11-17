# Theorem: the primitive words are not finitely ambiguous

**Claim.** For every cycle-free CFG G over {a,b} with L(G) = Q, sup_w amb_G(w) = ∞.
More precisely, if G is k-ambiguous then L(G) ≠ Q; a witness slice is
R_m = a(ab⁺)^{m−1} a (ab⁺)^{m−1} with m = 2k+1, where some word must have ≥ ⌈m/2⌉ > k trees.

Status: both audits complete — CORRECT WITH FIXES (structure: AUDIT_structure.md, fixes F1–F4 applied inline; geometry: AUDIT_geometry.md, fixes G1–G6 in §7). Not peer-reviewed.

---

## 0. Conventions
Blocks: a word in (ab*)^n is a b^{x_1} a b^{x_2} ⋯ a b^{x_n}; exp(w) = (x_1,…,x_n) ∈ ℕ^n
(block i = the b's read after the i-th a). A *pair* is a set {s,t} ⊆ [n] with s ≤ t (s = t allowed).
Two pairs {s,t},{s',t'} *cross* if s < s' < t < t' or s' < s < t' < t. A family is *laminar* if no two
members cross (shared endpoints allowed).

## 1. The slice (PROVED; brute-force checked, `check_slice.py`)
Let m ≥ 2, n = 2m, M = m−1, R_m = a(ab⁺)^{M} a (ab⁺)^{M} (regular). A word of R_m has exponent vector
(0, x_1,…,x_M, 0, y_1,…,y_M), all x_i, y_i ≥ 1.

**Lemma 1.** w ∈ R_m is primitive iff x ≠ y.

*Proof.* If w = u^k, k ≥ 2, then u begins with a, k | n, and exp(w) is invariant under the cyclic
shift by s = n/k ∈ (0,n). The zero coordinates are exactly positions 1 and m+1, so the shift maps
{1, m+1} to itself: 1+s ≡ m+1, s = m. Invariance under shift m is x = y. Conversely x = y gives
w = u² with u = a(ab^{x_1})⋯(ab^{x_M}). ∎

So exp(Q ∩ R_m) ≅ NE_M := {(x,y) ∈ ℕ_{≥1}^M × ℕ_{≥1}^M : x ≠ y} (dropping the two constant 0 blocks).
Order of coordinates in the word: x_1 < ⋯ < x_M < y_1 < ⋯ < y_M. The "diagonal pairs" {x_i, y_i} cross
each other pairwise.

## 2. Reductions (PROVED; these are Lemmas 1.1, 1.2 of `research/reports/ambiguity.md`, audited)
* Lemma 1.1: a cycle-free G yields a CNF G'' with L(G'') = L(G)∖{ε} and amb_{G''}(w) ≤ amb_G(w).
  (Cycle-freeness guarantees the unit graph after ε-removal is acyclic.)
* Lemma 1.2: product of a CNF grammar with a complete DFA preserves tree counts on L(D), gives 0
  trees off L(D).

So if Q has a k-ambiguous grammar, then Q ∩ R_m has a reduced, state-annotated, k-ambiguous CNF
grammar G_m, with every nonterminal (s,A,t) useful, for every m (same k). [Audit fix F1] Concretely
G_m := ((G'' × D_{R_m}) × D_n), reduced, where D_n is the DFA of (ab*)^n (states 0..n plus sink, b loops
in states 1..n). Lemma 1.2 applied twice keeps all tree counts, and the outer annotation is by D_n,
as Lemma 3 requires.

## 3. Structure lemma for finitely ambiguous grammars inside (ab*)^n (PROVED)

**Lemma 3 (Structure).** Let G be a reduced annotated CNF grammar (product with the DFA D_n of
(ab*)^n), finitely ambiguous, L(G) ⊆ (ab*)^n. Then there is a finite set Σ_G of "skeletons" σ, each
with a vector c_σ ∈ ℕ^n and a list of *linearly independent* vectors v_{σ,1},…,v_{σ,r_σ} ∈ ℕ^n∖{0},
such that
  (i) supp(v_{σ,j}) ⊆ π_{σ,j}, a pair, and the pairs π_{σ,1},…,π_{σ,r_σ} form a laminar family;
  (ii) for every w ∈ (ab*)^n: amb_G(w) = Σ_σ 1[exp(w) ∈ L_σ], where L_σ = c_σ + ℕv_{σ,1} + ⋯ + ℕv_{σ,r_σ}.

*Proof.* Let C range over strongly connected components (SCCs) of the graph X → Y ("Y occurs on a
right side of X"). Call C nontrivial if it contains a cycle.

(a) [Theorem A, Steps 1–2 of ambiguity.md, audited] Inside a nontrivial C every rule has at most one
child in C ("linear"); every child not in C ("side child") of a C-node generates only words in b⁺; all
members of C carry the same annotation (s,·,t), left side children lie in block s, right ones in
block t.

(b) Side subtrees contain no C-node (a C-node below a side child Z would put Z in C).
Because of linearity, in any tree the C-nodes lying below a C-node form a single downward path.

(c) **Unique first-return context.** For X ∈ C a *first-return context* is a tree context κ rooted at
X with a single hole labelled X, of positive size, such that no node strictly between the root and the
hole is labelled X. (One exists since C is nontrivial.) Suppose κ₁ ≠ κ₂ are two of them, with b-yields
(b^{p_j} left, b^{q_j} right). Take a tree of a word of L(G) containing an X-node, written outer∘T_X.
For each ε ∈ {12, 21}^N the tree outer∘κ_{ε_1}∘⋯∘κ_{ε_{2N}}∘T_X has the same yield (the inserted
material is b's in block s and b's in block t, and b-words commute). They are pairwise distinct trees:
by (b) the X-nodes below the top inserted X are on one path, and the hole of a first-return context is
the first of them, so the sequence ε is read off the tree. Hence ≥ 2^N trees for one word, for every
N — contradiction. So each X ∈ C has exactly one first-return context. Consequences: each X ∈ C has
exactly one rule with a child in C (two such rules give two first-return contexts differing at the
root), so C is a simple directed cycle (a ring X_0 → ⋯ → X_{r−1} → X_0); every side child Z has
exactly one derivation tree over all words (two trees give two contexts). [Audit fix F4] Every ring
rule X → (child in C) starts some first-return context: follow a shortest path in C from the child
back to X and fill the side positions with arbitrary trees. [Audit fix F3] A side child's unique tree
contains no node W of a nontrivial SCC C', since inserting one turn of C' at W would give it a second
tree; in particular it repeats no nonterminal on a path. Let v_C ∈ ℕ^n be the yield vector of one full turn of the ring
(p b's in block s, q b's in block t); v_C ≠ 0 (CNF), supp v_C ⊆ {s,t}. [Audit fix F2] If s = 0 (no b
is read in state 0, so p = 0), take the pair π := {t} instead; shrinking a pair cannot create a crossing,
and §5 uses only supports.

(d) **Skeletons.** In a tree, a maximal path of C-nodes enters the ring at some X_i and leaves at some
X_j through an exit rule (both children outside C, or a terminal rule). Its length is
(j−i mod r) + q·r with a unique q ≥ 0. Deleting the q full turns gives a tree; doing so for every such
path gives the *skeleton* σ of the tree, and the tree is determined by (σ, (q_π)_π) where π ranges
over the C-paths of σ; conversely every (σ, q) is a tree. In a skeleton no root-to-leaf path repeats
a nonterminal (SCCs are visited at most once along a path, rings for < r steps, side subtrees are
fixed and repetition-free), so there are finitely many skeletons. exp(yield) = c_σ + Σ_π q_π v_{C(π)}.

(e) **Independence.** If the v_π of one skeleton were linearly dependent, there would be q ≠ q' ∈ ℕ^{r_σ}
with Σ q_π v_π = Σ q'_π v_π, and then the K+1 vectors jq + (K−j)q' (0 ≤ j ≤ K) give K+1 trees of one
word, for all K — contradiction. Hence the parametrization is injective and (ii) holds.

(f) **Laminarity.** Each C-path π of σ consists of nodes annotated (s_π, ·, t_π); the yield of each
such node spans the states s_π … t_π. For two C-paths π, π' either one lies inside the subtree of the
bottom (exit) node of the other — then [s',t'] ⊆ [s,t] — or their top nodes are incomparable — then
their yields are disjoint factors, so t ≤ s' or t' ≤ s. (π' cannot lie in a side subtree of π, which
has no cycles by (c).) In no case do the pairs cross. ∎

## 4. Lemma X (laminar families spanning the diagonal) (PROVED; random test `check_lemmaX.py`)

Work in ℝ^{2M} with coordinates x_1..x_M,y_1..y_M in this order (position i ↔ x_i, M+i ↔ y_i),
W = span{e_i + e_{M+i} : i ≤ M}.

**Lemma 4.1 (non-interleaving).** Let H be a graph on vertices 1..N (points on a line) whose edges are
pairwise non-crossing. If C₁ ≠ C₂ are connected components, there are no p<q<r<s with p,r ∈ C₁, q,s ∈ C₂
(nor with the roles swapped).

*Proof.* A path in C₁ from p to r passes over q (q ∉ C₁): some edge {a,b} of C₁ has a < q < b. Any edge
of C₂ with one end in (a,b) and the other outside [a,b] would cross {a,b} (no shared endpoints across
components), so by connectivity C₂ ⊆ (a,b). Symmetrically, r lies between q, s ∈ C₂, so C₁ ⊆ (c,d) for
some edge {c,d} of C₂. But c,d ∈ (a,b), so a ∉ (c,d) although a ∈ C₁. ∎

**Lemma 4.2 (Lemma X).** Let V ⊂ ℝ^{2M} be a finite set of non-negative vectors with |supp v| ∈ {1,2},
supports pairwise non-crossing. If W ⊆ span V, then dim span V ≥ 2M − 1. Moreover at most one
connected component of the support graph contains a pair {i, M+i}.

*Proof.* Support graph: vertices 1..2M, an edge for each 2-support, a loop for each 1-support. span V
= ⊕_C span V_C over components C. Each C has dim span V_C ≥ |C| − 1 (a spanning tree's edge vectors,
with two positive entries each, are independent); call C *full* if equality fails, i.e. span V_C = ℝ^C.
If C is not full, span V_C = λ^⊥ ∩ ℝ^C for some λ; a loop at p forces λ_p = 0 and an edge vector
a e_p + b e_q (a,b > 0) forces λ_p = 0 ⇔ λ_q = 0, so λ vanishes nowhere on C and e_p ∉ span V for
p ∈ C. Since e_i + e_{M+i} ∈ span V, if i and M+i lie in different components then e_i ∈ span V; so
every non-full component is a union of pairs {i, M+i} (isolated unlooped vertices are non-full
singletons, hence impossible). Two components each containing some {i, M+i} and {j, M+j}, i < j,
would interleave (i < j < M+i < M+j), contradicting 4.1. So at most one non-full component, and
dim span V ≥ 2M − 1. ∎

## 5. The geometric argument

Fix m, M = m−1, and suppose G_m (from §2) is k-ambiguous. By Lemma 3, writing points of ℕ^{2M} as (x,y):
  f(x,y) := Σ_σ 1_{L_σ}(x,y) = amb(word) ∈ [1,k] on NE_M, and f = 0 on Δ = {x = y}.
Periods cannot touch the two constant-0 blocks, so all L_σ live in the 2M coordinates, and the laminar
condition is with respect to the order x_1<⋯<x_M<y_1<⋯<y_M. Since f ≥ 1_{L_σ}, every L_σ ⊆ NE_M,
in particular **L_σ ∩ Δ = ∅**. Write V_σ for the period set, cone(V_σ) its real cone, and
C_σ := {u ∈ ℝ^M : (u,u) ∈ cone(V_σ)}, a closed polyhedral cone.

**Choice of parameters.** Choose ω ∈ ℤ_{≥1}^M outside the (finitely many) boundaries ∂C_σ (a lower-
dimensional C_σ counts as its own boundary); so for each σ either ω ∈ int C_σ or ω ∉ C_σ. Choose N so
large that N! is divisible by every index I_σ = [span V_σ ∩ ℤ^{2M} : ℤV_σ] and by every D_σ = |det|
appearing below, and exceeds every constant listed below. Points:
  P(t,δ) := (tω, tω + N!δ),   t ∈ N!ℤ_{>0},  δ ∈ ℤ^M.
These lie in N!ℤ^{2M}; for δ ≠ 0 and t large they lie in NE_M, so f(P(t,δ)) ≥ 1.
For V_σ a basis of span V_σ, n_v(·) denotes the coordinate functionals; V_{σ,1} := {v : n_v ≡ 0 on W},
V_{σ,0} := V_σ ∖ V_{σ,1}.

**Lattice fact.** If L_σ contains one point P₁ ∈ N!ℤ^{2M} and P ∈ N!ℤ^{2M} ∩ (c_σ + span V_σ), then
P − c_σ ∈ ℤV_σ. (P − P₁ ∈ N!·(span V_σ ∩ ℤ^{2M}) ⊆ I_σ(span V_σ ∩ ℤ^{2M}) ⊆ ℤV_σ.)

**Positivity fact.** If ω ∈ int C_σ then W ⊆ span V_σ and n_v(ω,ω) > 0 for every v ∈ V_{σ,0}.
(n_v ≥ 0 on a W-neighbourhood of (ω,ω); a linear form ≥ 0 near a zero vanishes on W.) Moreover, by
Lemma X applied to V_{σ,0} (which spans ⊇ W), |V_{σ,0}| ≥ 2M−1.

Classify σ:
1. ω ∉ C_σ. If P(t,δ) ∈ L_σ for unboundedly many t (δ in a finite set) then (ω,ω) ∈ cone(V_σ),
   impossible. So for |δ|_∞ ≤ R and t ≥ t₀(R): P(t,δ) ∉ L_σ.
2. ω ∈ int C_σ, dim span V_σ = 2M−1 (the only other possibility, by Lemma X). Then V_{σ,1} = ∅.
   span V_σ = λ^⊥ with λ integral and λ_i = −λ_{M+i} (Lemma 4.2's non-full component), so
   ⟨λ,(u,u)⟩ = 0. If some P(t₁,δ₁) ∈ L_σ then ⟨λ, c_σ⟩ = N!·φ(δ₁) ∈ N!ℤ, hence ⟨λ,c_σ⟩ = 0 (N! >
   |⟨λ,c_σ⟩|), so P₀ = (tω,tω) ∈ c_σ + span V_σ, P₀ − c_σ ∈ ℤV_σ by the lattice fact, and its
   coordinates t·n_v(ω,ω) − n_v(c_σ) are ≥ 0 for t large. So P₀ ∈ L_σ ∩ Δ — contradiction.
   **Such σ contain no point P(t,δ).**
3. ω ∈ int C_σ, V_σ a basis of ℝ^{2M}, V_{σ,1} = ∅: the same argument (no λ needed) puts (tω,tω) in
   L_σ if L_σ has any point P(t,δ). **No points.**
4. ω ∈ int C_σ, V_σ a basis, V_{σ,1} = {v*} (|V_{σ,1}| ≤ 1 by the positivity fact). Put
   ψ_σ(δ) := n_{v*}((0,δ)), a non-zero linear form on ℝ^M with values in (1/D_σ)ℤ on ℤ^M; note
   n_{v*}(P(t,δ)) = N!ψ_σ(δ). Suppose L_σ has some point P(t,δ). Then by the lattice fact, for
   |δ|_∞ ≤ R and t ≥ t₀(R):  P(t,δ) ∈ L_σ ⇔ N!ψ_σ(δ) ≥ γ_σ := n_{v*}(c_σ).
   If γ_σ ≤ 0, δ = 0 qualifies and (tω,tω) ∈ L_σ ∩ Δ — contradiction; so γ_σ > 0 and, since
   N!/D_σ > γ_σ, **P(t,δ) ∈ L_σ ⇔ ψ_σ(δ) > 0.**

Let 𝓗 be the set of σ of type 4 having some point P(t,δ); it does not depend on R. Hence:

  **for every δ ∈ ℤ^M∖{0}:  1 ≤ #{σ ∈ 𝓗 : ψ_σ(δ) > 0} = f(P(t,δ)) ≤ k.**

The closed rational polyhedral cone K = ∩_{σ∈𝓗}{ψ_σ ≤ 0} contains no non-zero integer point, hence
K = {0}. Then the ψ_σ span (ℝ^M)*, and since M linearly independent forms cut out a simplicial cone
≠ {0}, |𝓗| ≥ M+1. Pick δ ∈ ℤ^M with ψ_σ(δ) ≠ 0 for all σ ∈ 𝓗. Then
f(P(t,δ)) + f(P(t,−δ)) = |𝓗| ≥ M+1, so some word of Q ∩ R_m has at least ⌈(M+1)/2⌉ = ⌈m/2⌉ trees.

**Conclusion.** With m = 2k+1 we get a word with ≥ k+1 trees, contradicting k-ambiguity. As k was
arbitrary, Q has no finitely ambiguous grammar. ∎

## 6. Remarks
* The witness words: a·(ab^{x})·a·(ab^{y}) with x = tω, y = tω ± N!δ — the number of b's grows, and the
  number of blocks 2m = 4k+2 grows with k, as §4 of the task requires.
* The bound is per slice: inherent ambiguity of Q ∩ R_m is ≥ ⌈m/2⌉; the natural grammar
  "∃ i: x_i ≠ y_i" gives ≤ m−1 (in fact 2(m−1) half-space pieces, ply m−1).
* No normal-form assumption is imposed on G: Lemma 1.1 converts any cycle-free grammar without
  increasing any tree count.

## 7. Geometry-audit fixes (AUDIT_geometry.md)
* G1 (Lemma 4.2, "Moreover"): the non-interleaving argument of 4.1 applies to *all* components, full or
  not: two components containing {i,M+i} and {j,M+j} would interleave. Only the non-full count is used.
* G2 (§5 notation): n_v, V_{σ,0}, V_{σ,1} are defined only when W ⊆ span V_σ, which holds in cases 2–4
  (positivity fact). In case 2, ⟨λ,c_σ⟩ = 0 gives c_σ ∈ span V_σ, so n_v(c_σ) is defined.
* G3 (case 2): λ_i = −λ_{M+i} follows directly from W ⊆ span V_σ = λ^⊥.
* G4 (choice of N): what is used is I_σ | N!, N! > |⟨λ_σ,c_σ⟩|, and N! > D_σ·γ_σ (all depend only on G_m).
* G5 (thresholds): t₀(R) is the maximum over all σ of the case-wise thresholds, and also t₀(R) > N!·R so
  that P(t,±δ) ∈ NE_M (all coordinates ≥ 1, and y − x = ±N!δ ≠ 0).
* G6: the D_n-annotation interface is fix F1 above.
