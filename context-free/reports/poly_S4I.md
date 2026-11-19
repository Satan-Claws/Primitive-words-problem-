# poly_S4I: reduction from a known inherently exponentially ambiguous CFL via h^{-1}(·) ∩ R — status: BLOCKED (obstruction PROVED)

Setting. Q ⊆ {a,b}* = primitive words; G a hypothetical cycle-free CFG for Q. Goal was: nonerasing
h: Γ* → {a,b}*, regular R ⊆ Γ*, with L' := h^{-1}(Q) ∩ R an inherently exponentially (or super-
polynomially) ambiguous CFL T (Naji 1998 / Wich 2005 type, e.g. T = X*, X = {a^i b^j c^k : i=j ∨ j=k}).
Result: the transfer lemmas hold (§1), but L' has a rigid "line" structure (§2, Theorem C) that every
Naji/Wich-type target violates (§3). The structural reason is exactly "primitivity is one cyclic
condition": along any pumping line, a single far-out rejection forces the whole line to be periodic.

## 1. Ambiguity-non-increasing operations (PROVED, standard)
(a) DFA intersection. Bar-Hillel triple construction G×D, nonterminals [q,A,q']; a tree of G×D for w is a
tree of G for w plus the (unique) run of D on w. So amb_{G×D}(w) = amb_G(w) for w ∈ L(D), 0 otherwise.
(b) Inverse nonerasing morphism. Let M be the sequential transducer reading Δ = {a,b} with states
{0} ∪ {(c,i) : c ∈ Γ, 1 ≤ i < |h(c)|}: it reads h(c) letter by letter and, on the last letter, emits c and
returns to 0. For output w ∈ Γ*, M accepts exactly the input h(w), with exactly ONE run (the output fixes
the block factorisation of the input). Grammar G': nonterminals [s,A,t]; rules [s,A,t] → [s,B,r][r,C,t]
for A → BC; [s,A,t] → out(s,x,t) for A → x and each transition s -x/out-> t (out ∈ Γ ∪ {ε}); start [0,S,0].
Derivations of w in G' ↔ pairs (G-tree of h(w), the unique M-run with output w), so the ε-ful G' has
amb_{G'}(w) = amb_G(h(w)). Since h is nonerasing, every ε-yielding subtree covers ≥ 1 input letter but
no terminal outside the subtree's output, and removing ε-rules/unit rules in tree form (no cycles: G
cycle-free and each [s,A,t]-cycle would be a G-cycle) can only merge derivations: amb_{G''}(w) ≤ amb_G(h(w)),
L(G'') = h^{-1}(L(G)). (This is the exact transfer of poly_S4M §1 for general nonerasing h.)
(c) Hence: if L' = h^{-1}(Q) ∩ R is inherently f-ambiguous, every grammar for Q has
amb_G(N) ≥ f(N / max|h(c)|). Only EQUALITY L' = T (or L' = T ∩ R with T ∩ R still inherently f-ambiguous)
transfers; mere containment does not (supersets of inherently ambiguous CFLs can be unambiguous).
Wich's Parikh-bounded substitution goes the other direction (builds languages FROM Q's grammar) and does not
produce a target here; not used.

## 2. The line lemma (PROVED)
Lemma A. If P, g ∈ {a,b}*, g ≠ ε, Pg ≠ gP, then P g^m is primitive for every m ≥ |P|/|g| + 2.
Proof. Suppose P g^m = u^k, u primitive, k ≥ 2. Then |u| ≤ (|P| + m|g|)/2 ≤ m|g| − |g| by the bound on m.
The suffix g^m has periods |g| and |u| and length ≥ |u| + |g|, so by Fine–Wilf it has period
d = gcd(|u|,|g|). It contains a length-|u| factor, a conjugate u' of u (hence primitive) with period d | |u|;
so u' = t^{|u|/d} forces d = |u|, i.e. |u| divides |g|. Then g (a suffix of u^k of length divisible by |u|) is
u^{|g|/|u|} and P (prefix of length divisible by |u|) is a power of u, so Pg = gP. Contradiction. ∎

Theorem C. Let h be nonerasing, p, y, s ∈ Γ*, y ≠ ε. If p y^m s ∉ h^{-1}(Q) for SOME
m ≥ |h(sp)|/|h(y)| + 2, then h(sp) and h(y) are powers of one primitive z, and
h(p y^m s) ~ z^{e+mf} (conjugate; e ≥ 0, f ≥ 1) for all m; so p y^m s ∈ h^{-1}(Q) for at most one m ∈ {0,1}.
Proof. Primitivity is conjugation-invariant: h(p y^m s) ~ h(s)h(p)h(y)^m; apply Lemma A with P = h(sp). ∎

Corollary D (line dichotomy). For every pump line ℓ = {p y^m s : m ≥ 0} (y ≠ ε) and every regular R,
L' ∩ ℓ is either co-finite in ℓ (all m beyond |h(sp)|/|h(y)|+2 accepted) or contained in {m ≤ 1}.
In words: L' can reject far along a line only if the whole line is periodic with one root; it can never
"accept exactly at some m ≥ 2 and reject infinitely often", and never reject a line for a LOCAL reason
(a defect at fixed position surviving arbitrary insertions).

## 3. Why Naji/Wich targets cannot equal L' (PROVED for the natural forms)
(i) T = X* (or u X* v, any u, v), R = u(a+b+c+)*v. Take β = a b^2 c (bad: i≠j, j≠k) and good blocks
y1 = abc, y2 = a^2 b^2 c. Lines u β y_i^m v ⊆ R∖T are rejected for all m ⇒ (Thm C) h(vuβ) commutes with
h(y1), h(y2); line u ββ y1^m v ⇒ h(vuββ) too; so h(β), h(vu), h(y1) ∈ z* for one primitive z (commutation is
transitive on non-empty words). But u (abc)^m v ∈ T and h(u(abc)^m v) ~ z^{e+m f}, f ≥ 1, non-primitive
for m ≥ 2. Contradiction. (Already: X* ∋ x, xx, while L' never contains both w and ww.)
(ii) Any R containing one "mixed" line, e.g. a^{m} b^5 c^4 · (context): T accepts exactly at m = 5 and
rejects infinitely often — forbidden by Corollary D. The same holds for the Wich polynomial-degree
families and for {a^i b^j c^k : i=j ∨ j=k}^* restricted to any R in which a block exponent can be pumped
across the equality i=j (or j=k): membership of such languages on exponent lines is "= at one point"
or "≠ cofinitely", and the "= at one point m ≥ 2" pattern is excluded.
(iii) Escaping (ii) requires R to remove every mixed line, i.e. T ∩ R line-wise cofinite or ⊆ {m ≤ 1}.
In the star languages the binary choice "i=j or j=k" in a block is decided precisely by exponent
equalities, i.e. by mixed lines; we do not have a theorem that every such R destroys inherent ambiguity
(that would need a statement about all lower-bound proofs), so (iii) is a heuristic, not a proof.

## 4. Structural summary / shape mismatch
- Naji/Wich: membership = ∀ block ∃ option; complement = ∃ block (local defect), an ideal-like set closed
  under insertion of good blocks. Theorem C: complement of h^{-1}(Q) along any insertion direction is
  periodic-or-finite — a local defect never persists under insertion of a non-commuting factor.
- Primitivity on slices is "∀ prime p | N ∃ mismatch" with ω(N) = O(log N / log log N) conjuncts, so even
  ideal ∀∃-products give at most ∏_p (choices) ≤ N^{ω(N)} = 2^{O(log² N / log log N)}: sub-exponential.
  Exponential ambiguity (2^{Θ(N)}) is the wrong target; the only live superpolynomial shape is S_N's.
- No code h makes primitivity a long conjunction of independent local conditions: by Thm C,
  h(w) non-primitive is a global periodicity, never a local defect.
Status: reduction from inherently EXPONENTIAL CFLs BLOCKED (PROVED for X*, uX*v and any R with a mixed line);
reduction from inherently superpolynomial-subexponential CFLs of the ∀p∃ shape not excluded (= S_N).
Literature used only as background: Naji 1998 / Wich 2005 star languages are inherently exponentially
ambiguous (cited, not re-verified; theorem number not checked); Fine–Wilf; Bar-Hillel.
