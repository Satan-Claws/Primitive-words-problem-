# Agent "finiteindex": report

**Claim level: partial results plus barriers. The target (Q not metalinear / not of finite index) is NOT proved.**
Scripts: `scratchpad/scripts/finiteindex/` (they reuse `arr2.py`, copied from `research/scripts/bounded/`).

What is proved:
1. **Structure lemma S (PROVED).** The linear / metalinear-width-k analogue of Ginsburg's theorem for block-bounded
   languages: periods are 2-sparse and their pair supports are NESTED (linear), or nested inside k consecutive
   intervals (width k).
2. **Face criterion F (PROVED).** An L6-type obstruction, valid for any class of period sets.
3. **Theorem 1 (PROVED).** For every m >= 2, K_m := Q ∩ (b*a)^m b* is not linear. For prime m,
   K_m IS metalinear of width 2 (Theorem 2, PROVED). So in these slices "not linear" is exactly the truth.
4. **Barrier B1 (PROVED, modulo LITERATURE L1).** For every bounded regular R, Q ∩ R is either non-context-free
   or of finite index. So no argument confined to one bounded slice can prove "Q not of finite index" without
   proving the full conjecture.
5. **Barriers B2 (COMPUTER-CHECKED).** On the seamless slices Q_n = Q ∩ (ab*)^n, the one-scale Dickson
   families (near-constant; ray; full-dimensional V_e) cannot refute even LINEARITY for n = 6 (all three),
   and for n = 10, 12 (near-constant).
6. **Warning check (VERIFIED, and strengthened).**

Notation. A word with m letters a is w(x) = b^{x_0} a b^{x_1} a ... a b^{x_m}, with x in N^{m+1}. Blocks are
indexed 0..m by the number of a's to their left. For L ⊆ (b*a)^m b* put X(L) = {x : w(x) ∈ L}.
For L ⊆ (ab*)^n, the coordinates are x_1..x_n (block 0 is empty). E_n and V_d are as in bounded.md.

---------------------------------------------------------------------------------------------------
## 0. The coordinator's warning (VERIFIED; strengthened)

(a) PROVED. Let x ∈ E_n have a unique maximum at j*. Then every y with y_i = x_i (i != j*) and y_{j*} > max_{i != j*} x_i
is primitive. If y had period d | n with d < n, then y_{j*+d} = y_{j*} (indices mod n), and j*+d != j* mod n. So
x_{j*+d} = y_{j*} > max_{i!=j*} x_i, a contradiction. Hence pumping a's (or b's) inside the dominant block, both up
and down, is safe as long as the block stays the unique maximum.

(b) PROVED (stronger). Any pumping lemma in which the adversary locates the pumps is satisfied by Q on
near-constant words w = (ab^N)^{n-1} a b^{N+1} with N much larger than the pumping constant K. The adversary can pump
a factor v = b^s a b^r with |v| <= K. Pumping inserts t-1 extra blocks of length < K, among blocks of length >= N - K.
The resulting cyclic block sequence has a run of short blocks occurring exactly once (t-1 consecutive short ones).
A periodic sequence with period < its length repeats every run, so the result is primitive for all t >= 0.
The case t = 0 deletes one a. The block sequence then has one block of length about 2N, which is unique, so it is
primitive by (a).
Consequence: pumping and Ogden-type arguments carry no information here. The semilinear (Dickson) structure must be used.

---------------------------------------------------------------------------------------------------
## 1. Structure lemma S (PROVED)

**Lemma S.** Let G be a linear grammar with L(G) ⊆ (b*a)^m b*. Then X(L(G)) is a finite union of linear sets c + N P.
Every p ∈ P has at most 2 nonzero coordinates. For p, p' ∈ P with supports {i<j} and {i'<j'}, the intervals [i,j]
and [i',j'] are comparable under inclusion ("LIN class").
If instead L = L_1 L_2 ... L_k with each L_r linear, then each P splits as P = P^1 ∪ ... ∪ P^k, with
0 = q_0 <= q_1 <= ... <= q_k = m. Supports of P^r lie in [q_{r-1}, q_r], and the pair supports inside each P^r are
pairwise comparable ("MET_k class"). Finite unions of such languages give finite unions of such sets.
The same holds for L ⊆ (ab*)^n, with blocks 1..n.

Proof.
(1) Product construction. Let A be the DFA for (b*a)^m b*: states 0..m, with b-loops and q --a--> q+1. Build G' with
nonterminals [p,X,q] and rules:
- [p,X,q] -> u [p',Y,q'] v whenever X -> uYv is in G, δ(p,u) = p' and δ(q',v) = q;
- [p,X,q] -> u whenever X -> u is in G and δ(p,u) = q.
The start symbol is [0,S,m]. Then L(G') = L(G) ∩ L(A) = L(G), and G' is linear. A derivation tree of G' is a path
(spine) of labels ℓ_1 ... ℓ_h.

(2) Cycles. A segment of the spine from a label X = [p,A,q] to the same label is a derivation X =>+ u X v. Then
δ(p,u) = p and δ(q,v) = q. Since a strictly increases the state, u and v lie in b*. Because the state is monotone
along the spine, every label on the segment has the same (p,q). The contribution of the cycle to x is
|u| e_p + |v| e_q, which has at most 2 nonzero coordinates.

(3) Parikh-type decomposition. Let K be the number of labels of G'.
- Call a spine reduced if no "simple cycle segment" can be removed without shrinking its label set. A simple cycle
  segment is a stretch between consecutive equal labels with no other repetition inside.
- Every window of K+1 consecutive positions contains a simple cycle segment. In a reduced spine, each such segment
  contains a "private" label, one whose occurrences all lie inside the segment.
- Disjoint segments have distinct private labels. Hence a reduced spine has length h <= K(K+1).
- Removing a cycle segment from a spine leaves a valid spine.
So every tree τ gives ψ(τ) = ψ(τ_0) + Σ (contributions of simple cycles with labels in Λ). Here τ_0 is reduced and
Λ = lab(τ_0) = lab(τ).
Conversely, any simple cycle with labels in Λ can be inserted at a node of τ_0 carrying one of its labels. So
X(L) = ∪_{τ_0 reduced} (ψ(τ_0) + N P_Λ), where P_Λ is the finite set of contributions of simple cycles with labels in Λ.

(4) Nesting. All labels of Λ occur on the single spine of τ_0. If X = [p,A,q] lies above Y = [p',B,q'], then the
yield of Y is a factor of the yield of X. Hence p <= p' and q' <= q, so [p',q'] ⊆ [p,q]. A pair support of a cycle
contribution with label (p,q) is exactly {p,q}. So pair supports are pairwise comparable.

(5) Metalinear. Use the rule [0,S,m] -> [0,S_1,q_1][q_1,S_2,q_2]...[q_{k-1},S_k,m] and apply (3) to each of the k
spines jointly (tuples of reduced spines). Labels in spine r have q_{r-1} <= p <= q <= q_r. ∎

**Remark S' (full preimages / "artificial seams", PROVED).** Splitting a block b^x into b^{x'} b^{x''} is
legitimate: it amounts to an inverse homomorphism to letters labelled by position, followed by intersection with a
regular set. Linear and metalinear languages are closed under both (product construction as in (1)). So Lemma S
also holds in fine coordinates, with the full preimage of the exponent set (this is the remark already made in L1).

---------------------------------------------------------------------------------------------------
## 2. Face criterion F (PROVED)

**Lemma F.** Suppose X(L) = ∪_k (c_k + N P^(k)) (finite union). Let H be a rational subspace with X(L) ∩ H = ∅.
Let h* ∈ N^{m+1} ∩ H and δ_0 ∈ Z^{m+1}, and suppose N h* + M δ_0 ∈ X(L) for every integer M >= 1 and every
N >= N_0(M). Then for some k there is P_1 ⊆ P^(k) such that:
- h* is a strictly positive rational combination of all elements of P_1, and
- δ_0 ∉ H + span_Q(P_1).

Proof. Suppose not.
- For every k and every such P_1, fix δ_0 = η + Σ r_p p with η ∈ H and r_p ∈ Q. Let M be a common denominator of
  all the r_p.
- The points y_N = N h* + M δ_0 (N >= N_0(M)) lie in X(L), so infinitely many lie in one c_k + N P^(k).
- By Dickson's lemma there are N < N' whose representations satisfy λ <= λ'. Then Σ (λ'-λ)_p p = (N'-N) h*.
- P_1 := {p : λ'_p > λ_p} satisfies the first condition, so δ_0 has its fixed decomposition with respect to P_1.
- Put μ_p = -M r_p + t(λ'-λ)_p. These are integers, and they are >= 0 for t large.
- Then z = y_N + Σ μ_p p ∈ c_k + N P^(k) ⊆ X(L), and z = (N + t(N'-N)) h* + M η ∈ H.
- This contradicts X(L) ∩ H = ∅. ∎

This is bounded's L6 with V_d replaced by an arbitrary forbidden subspace H and 1 replaced by an arbitrary
h* ∈ H. Combined with Lemma S it gives an obstruction for any restricted class.

---------------------------------------------------------------------------------------------------
## 3. Theorem 1: K_m = Q ∩ (b*a)^m b* is not linear, for every m >= 2 (PROVED)

w(x) is a conjugate of a b^{x_1} a ... a b^{x_{m-1}} a b^{x_m + x_0}. So by bounded L2,
w(x) ∈ Q iff y(x) := (x_1, ..., x_{m-1}, x_m + x_0) ∈ E_m. ("Seam": block 0 and block m merge cyclically.)

Proof.
- Let H = {x : x_1 = ... = x_{m-1} = x_0 + x_m}, the set of x with y(x) constant. Constant sequences of length m >= 2
  are not primitive, so X(K_m) ∩ H = ∅.
- Take h* = (1, 2, ..., 2, 1) ∈ H and δ_0 = e_m. Then y(N h* + M e_m) = (2N, ..., 2N, 2N+M) has exactly one
  coordinate different from the rest. Such a sequence is primitive: a period d < m would give y_{j+d} = y_j at the
  odd coordinate j. So the family lies in X(K_m).
- Suppose K_m is linear. By Lemmas S and F there is a LIN-class P_1 with h* ∈ relint cone(P_1) and e_m ∉ H + span(P_1).
- Then there is a functional f vanishing on H and on every p ∈ P_1, with f_m ≠ 0. H contains (1,1,...,1,0) and
  (0,1,...,1,1); subtracting gives f_0 = f_m ≠ 0.
- Since h*_0 > 0, some p ∈ P_1 has p_0 > 0.
  - supp p = {0} is impossible, since it would give f_0 = 0.
  - So supp p = {0,j}, and p_0 f_0 + p_j f_j = 0. Hence f_j has the sign opposite to f_0 = f_m, so j ≠ m: 0 < j < m.
- In the same way h*_m > 0 gives p' ∈ P_1 with supp p' = {j', m}, 0 < j' < m.
- But [0,j] and [j',m] are not comparable under inclusion, which contradicts the LIN class. ∎

(This re-proves Horváth's theorem through a bounded slice.)

**Theorem 2. For prime m, K_m is metalinear of width 2 (PROVED).**
For prime m, y(x) is non-primitive iff it is constant. So
X(K_m) = ∪_{i=1}^{m-2} ({x_i > x_{i+1}} ∪ {x_i < x_{i+1}}) ∪ {x_0+x_m > x_1} ∪ {x_0+x_m < x_1}.
Proof of the equality: if no consecutive middle pair differs, then x_1 = ... = x_{m-1}, and non-constancy of y
means x_0 + x_m ≠ x_1. The converse inclusion is clear.
- {x_i > x_{i+1}} gives a linear language (one counted pair; the other blocks are b*).
- {x_0 + x_m > x_1} = L_A L_B ∪ L_A' L_B' with:
  - L_A = {b^{i+j} a b^j},
  - L_B = {b^k a b^* a ... a b^* a b^{k+l+1}},
  - L_A' = {b^{i+j+1} a b^j},
  - L_B' = {b^k a b^* ... a b^{k+l}}.
  Check the decomposition with j = min(x_0, x_1), using the second product when x_2... (x_m) = 0 and x_0 > x_1.
- {x_1 > x_0 + x_m} = L_C L_D with L_C = {b^i a b^{i+j+1}} and L_D = {b^k a b^* ... a b^k}.
All factors are linear. ∎
So Theorem 1 is sharp for these slices: the seam forces exactly one extra linear factor.

(Correction to the case split in Theorem 2: use L_A L_B with j = min(x_0, x_1) when x_m >= 1 or x_0 <= x_1. Use
L_A' L_B' with j = x_1 when x_m = 0 and x_0 > x_1.)

---------------------------------------------------------------------------------------------------
## 4. Barrier B1: bounded slices cannot refute finite index (PROVED, uses LITERATURE)

**Claim.** If R ⊆ w_1* ... w_k* and Q ∩ R is context-free, then Q ∩ R has finite index.
(I believe this is in Ginsburg–Spanier, "Derivation-bounded languages", JCSS 2 (1968). That is LITERATURE, not
checked; the following is a self-contained proof.)

Proof.
- By bounded L1 (Ginsburg 5.4.2, LITERATURE), Q ∩ R = h(L'). Here L' ⊆ c_1* ... c_k* has exponent set equal to a
  finite union of stratified linear sets c + N P. Homomorphisms and finite unions preserve finite index, so it
  suffices to treat one set c + N P.
- Split each block c_i into consecutive sub-blocks, one for each pair support with an endpoint at i, ordered from
  outside in. Then the pair supports become pairwise disjoint and non-crossing intervals of sub-blocks. Shared
  endpoints are separated because c_i^{s+t} = c_i^s c_i^t.
- The resulting well-nested family is a forest. It is generated by the grammar with one nonterminal per forest node:
  Z_I -> c^{p_left} Z_I c^{p_right} | (children of I in order, with the singleton and base letters as regular
  pieces in between).
- In a leftmost derivation the sentential forms contain at most (number of forest nodes) + 1 <= |P| + 1
  nonterminals. The block-merging homomorphism then gives c + N P back.
- Intersection with a regular set preserves the index (product construction). ∎

**Consequences.**
(i) A proof that Q is not of finite index via one bounded slice Q ∩ R would prove that Q ∩ R, hence Q, is not CF.
So any finite-index proof must be a uniformity argument: show that ind(Q ∩ R_n) -> ∞. This works because
ind(Q ∩ R) <= ind(Q).
(ii) Metalinearity, by contrast, CAN in principle be refuted inside one bounded CF slice. A stratified forest with
a branching node, e.g. supports (1,6),(2,3),(4,5), is not of metalinear type.

---------------------------------------------------------------------------------------------------
## 5. Barriers B2: one-scale Dickson families are too weak (COMPUTER-CHECKED / PROVED)

Every script below lets the coverer use only some valid structures, while the attacker uses ALL faces of the
structure. So "coverer wins" soundly means that the criterion (Lemma F with that family type) cannot fire.
Arithmetic is mod 2^61-1, as in bounded's arr2.py. These are search results, not exact-Q certificates.

| script | slice / class | family | n or m | result |
|---|---|---|---|---|
| `lin_nc.py n` | (ab*)^n, LIN (nested chains of disjoint ratio-1 pairs + singletons) | near-constant N·1 + δ | 6, 10, 12, 14, 15 | coverer wins (3-7 structures suffice). Outputs: `out_lin_nc_6_10_12.txt`, `out_lin_nc_14_15.txt` |
| `rayfam.py 6 w` | (ab*)^6, LIN | ray N·w + δ, w ∈ {1, (1,2)^3, (2,1)^3, (1,3)^3, (1,2,3)^2, (3,1,2)^2, (1,1,2)^2} | 6 | coverer wins for all. `out_rayfam6.txt` |
| `vefam.py 6 e 1 6` | (ab*)^6, LIN, ratio-1 2-sparse sets with span ⊇ V_e | full-dimensional V_e family (bounded L8) with faces | e = 3, 2 | coverer wins. `out_vefam6.txt` |
| `seam_nc.py m k` | K_m seam slice, MET_k | N(1,2,..,2,1) + δ | m = 2, 3: k=1 attacker survives (matches Thm 1); k=2 coverer wins (matches Thm 2). m = 4, 6: k=2 coverer wins (m=6 after 273 of 1401 structures) | `out_seam_nc.txt` |

So with these families:
- not even NON-LINEARITY of Q_6 = Q ∩ (ab*)^6 can be shown;
- the seam slices only give "not linear".

**Why (PROVED, structural explanation).** By Lemma F the coverer needs, for each d, a functional f^(d) in the
annihilator of span(P_1) with f^(d) ⊥ H_d and f^(d)(δ) ≠ 0. The annihilator is a direct sum of one functional g_C
for each tree component C of the support graph of P_1. So the coverer can add "repair edges" (disjoint ratio-1 pairs
{i,j} with g = e_i - e_j) that fix the class sums mod d separately for each d. Such repairs nest freely inside one
chain.
Example (K_6, δ = e_6), checked by hand: P_1 = {e_0+e_3, e_3+e_6, e_1+e_2, e_4, e_5}. This has components
[0,3] ⊇ [1,2] and [3,6] (MET_2). It satisfies h* ∈ relint, and the certificates are:
- f^(3) = e_0 - e_3 + e_6;
- f^(2) = e_0 + e_1 - e_2 - e_3 + e_6.
Both are ⊥ H_d and nonzero at δ.

**Lesson.** Every obstruction of the form "one family, one Dickson increment, one face" is local: the coverer chooses
P_1 after seeing δ. The width of the certificate needed is at most 2 in every case examined. A width-growth proof must
use several families simultaneously. That needs the finitely many base points c_k across a 2-parameter family
(uniformity), which Lemma F does not exploit.

---------------------------------------------------------------------------------------------------
## 6. Final summary of claims

- PROVED: Lemma S (linear/metalinear Ginsburg structure, nested pair supports), Remark S' (full preimages), Lemma F
  (face criterion).
- PROVED: Theorem 1. K_m = Q ∩ (b*a)^m b* is not linear, for every m >= 2.
- PROVED: Theorem 2. For prime m, K_m is metalinear of width 2.
- PROVED (with LITERATURE L1): Barrier B1. A bounded CF slice of Q always has finite index.
- COMPUTER-CHECKED: Barriers B2 (table in Sec. 5).
- NOT PROVED: Q not metalinear; Q not of finite index; Q not metalinear of width 2.
  No slice was found where width 2 provably fails.
- OPEN, the next step: a two-parameter Dickson argument that uses the finitely many base points c_k uniformly
  (multi-scale). Equivalently, decide whether Q ∩ (ab*)^6 is linear. All one-scale tests say the coverer wins.
