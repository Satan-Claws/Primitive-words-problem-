# Report of agent "rectangles": counting / communication-complexity lower bounds for Q

**Claim level: (ii) BARRIER THEOREMS, plus (iii) partial results on ambiguity. No proof of the conjecture.**

Answer to the coordinator's question: the balanced-rectangle cover number of Q ∩ Σ^n is
**at most 2⌈n/3⌉ for every n ≥ 2** (Theorem A, PROVED, and checked exhaustively for n ≤ 22).
It is therefore O(n), far below the g·n² that a grammar with g nonterminals is allowed, and it
is never ω(n²). The fractional version is worse still for the method: every probability
distribution on Q ∩ Σ^n gives mass ≥ 1/4 to some balanced rectangle inside Q. So neither an
integral nor a fractional/distributional rectangle bound can prove the conjecture.

Status tags: **PROVED** (full proof in this file), **COMPUTER-CHECKED** (script named),
**FROM LITERATURE** (cited, not re-proved), **CONJECTURED / OPEN**.

Notation. Σ = {a,b}, a = 0, b = 1, positions 0..n−1. Q_n = Q ∩ Σ^n. P(n) = set of primes
dividing n, ω(n) = |P(n)|, d_p = n/p. A word w ∈ Σ^n is *cyclically d-periodic* (d | n) if
w_i = w_{(i+d) mod n} for all i; a word y has *linear period* d if y_i = y_{i+d} whenever both
indices are in range. Scripts are in `scripts/rectangles/`.

---------------------------------------------------------------------------------------------

## 1. The rectangle-cover lemma and the interchange lemma (task 1)

A *rectangle at span (i, ℓ)* in Σ^n is R = {xyz : (x,z) ∈ O, y ∈ I} with O ⊆ Σ^i × Σ^{n−i−ℓ},
I ⊆ Σ^ℓ. It is *balanced* if n/3 ≤ ℓ ≤ 2n/3.

**Lemma 1.1 (rectangle cover). PROVED.** Let G be a grammar in Chomsky normal form with g
nonterminals and L = L(G). For every n ≥ 2, L ∩ Σ^n is a union of at most g·n² balanced
rectangles, each contained in L. Moreover the inner sets are I = L(A) ∩ Σ^ℓ (A a nonterminal),
so at most g(n/3 + 1) distinct inner sets occur.

*Proof.* Take w ∈ L ∩ Σ^n and a parse tree. Each node has a span (i, ℓ) (its yield is
w[i, i+ℓ)). Start at the root (ℓ = n > 2n/3). While the current node has ℓ > 2n/3 ≥ 4/3, it has
ℓ ≥ 2, so in CNF it is binary; move to a child with the larger span. The first node reached
with ℓ ≤ 2n/3 is the larger child of a node of span > 2n/3, so ℓ > n/3. Let A be its label.
Put O_{A,i,ℓ} = {(x,z) : |x| = i, |z| = n−i−ℓ, S ⇒* xAz} and I_{A,ℓ} = {y ∈ Σ^ℓ : A ⇒* y}.
Then w ∈ R_{A,i,ℓ} := {xyz : (x,z) ∈ O_{A,i,ℓ}, y ∈ I_{A,ℓ}} ⊆ L, because S ⇒* xAz ⇒* xyz.
There are g choices of A and at most n(n/3+1) ≤ n² balanced spans. ∎

**Corollary 1.2 (distributional form). PROVED.** If L is context-free with g CNF nonterminals,
then for every n ≥ 2 and every probability measure μ on L ∩ Σ^n there is a balanced rectangle
R ⊆ L with μ(R) ≥ 1/(g n²). (Pigeonhole.) Hence a sequence μ_n with max_R μ_n(R) = o(n^{-2})
would prove non-context-freeness.

**Lemma 1.3 (interchange lemma, Ogden–Ross–Winklmann 1985). PROVED here.** Let L be as above.
For all n ≥ 2, all R ⊆ L ∩ Σ^n and all m with 2 ≤ m ≤ n there are k ≥ |R|/(g n²) words
z_t = w_t x_t y_t ∈ R with all |w_t| equal, all |y_t| equal, m/2 < |x_t| ≤ m, and
w_s x_t y_s ∈ L for all s, t.

*Proof.* As in 1.1, but descend while the span exceeds m; the node reached has span in
(m/2, m] (if n = m it is the root). Map each z ∈ R to (A, i, ℓ); there are at most g n² values,
so some class Z has ≥ |R|/(g n²) elements. For z_s, z_t ∈ Z: S ⇒* w_s A y_s and A ⇒* x_t. ∎

So the interchange lemma is exactly the rectangle lemma with a prescribed inner length, applied
to the uniform measure on R.

---------------------------------------------------------------------------------------------

## 2. Main barrier: Q_n is covered by 2⌈n/3⌉ balanced rectangles (tasks 2, 3)

**Lemma 2.1. PROVED.** For n ≥ 2, w ∈ Σ^n is non-primitive iff w is cyclically d_p-periodic
for some p ∈ P(n).
*Proof.* If w = v^m, m ≥ 2, take a prime p | m; then p | n and w = (v^{m/p})^p. Converse clear. ∎

**Lemma 2.2 (extension). PROVED.** Let L' ≥ d_p and y ∈ Σ^{L'}, L' ≤ n. If y has linear period
d_p, there is exactly one cyclically d_p-periodic ŵ ∈ Σ^n with ŵ[0,L') = y, namely
ŵ_i = y_{i mod d_p}. If y does not have linear period d_p there is none.
*Proof.* i mod d_p < d_p ≤ L', so ŵ is defined; it is cyclically d_p-periodic because d_p | n,
and it agrees with y on [0,L') because y has linear period d_p. Uniqueness: a cyclically
d_p-periodic word is determined by its first d_p letters. If some extension exists, its prefix y
inherits linear period d_p. ∎

**Lemma 2.3 (Fine–Wilf collapse). PROVED, using Fine–Wilf (FROM LITERATURE, 1965).**
Let n ≥ 2 and L' ≥ ⌊2n/3⌋. Then
(a) L' ≥ d_p for every p ∈ P(n);
(b) for distinct p, q ∈ P(n): L' ≥ d_p + d_q − gcd(d_p, d_q), and gcd(d_p,d_q) = n/(pq).
*Proof.* (a) d_p ≤ n/2 ≤ ⌊2n/3⌋ for n ≥ 2. (b) Write n = p^a q^b m; then
gcd(n/p, n/q) = p^{a−1}q^{b−1}m = n/(pq), so
d_p + d_q − gcd = n(1 − (1−1/p)(1−1/q)). If {p,q} = {2,3} this equals 2n/3 and 3 | n, so
⌊2n/3⌋ = 2n/3. Otherwise max(p,q) ≥ 5 and min(p,q) ≥ 2, so the value is
≤ n(1 − (1/2)(4/5)) = 3n/5; moreover n ≥ 2·5 = 10, and (2n−2)/3 ≥ 3n/5 iff n ≥ 10, so
⌊2n/3⌋ ≥ (2n−2)/3 ≥ 3n/5. ∎

**Theorem A (unique completion ⇒ linear rectangle cover). PROVED; COMPUTER-CHECKED for
2 ≤ n ≤ 22 (`unique_completion.py`, output `unique_completion_out.txt`).**
Let n ≥ 2, L = ⌊2n/3⌋, s = n − L = ⌈n/3⌉.
1. For every y ∈ Σ^L there is **at most one** z ∈ Σ^s with yz ∉ Q. Call it π(y) (or ⊥).
2. Q_n = ⋃_{0≤j<s, c∈Σ} R_{j,c}, where
   R_{j,c} = { y z : y ∈ Σ^L with π(y) = ⊥ or π(y)_j ≠ c ;  z ∈ Σ^s with z_j = c }.
   These are 2s = 2⌈n/3⌉ balanced rectangles (span (0, L)), each contained in Q.
3. For every probability measure μ on Q_n there is a balanced rectangle R ⊆ Q with μ(R) ≥ 1/4.
   Equivalently, the fractional rectangle-cover number of Q_n at this split is ≤ 4.

*Proof.* (1) Let G(y) = {p ∈ P(n) : y has linear period d_p}. By Lemmas 2.1, 2.2, 2.3(a),
yz ∉ Q iff yz = ŵ_p for some p ∈ G(y), where ŵ_p is the extension of Lemma 2.2. Let p ≠ q be
in G(y). By Lemma 2.3(b) and Fine–Wilf, y has linear period g = n/(pq). Since g | d_p,
(i mod d_p) mod g = i mod g, hence ŵ_p(i) = y_{i mod d_p} = y_{i mod g}; the same holds for q.
So ŵ_p = ŵ_q, and all p ∈ G(y) give the same completion.
(2) By (1), yz ∈ Q iff z ≠ π(y). If y ∈ row set of R_{j,c} and z_j = c then z ≠ π(y), so
R_{j,c} ⊆ Q. Conversely if z ≠ π(y): when π(y) = ⊥ use j = 0, c = z_0; otherwise pick j with
z_j ≠ π(y)_j and c = z_j.
(3) Choose S ⊆ Σ^s uniformly at random and R_S = {y : π(y) = ⊥ or π(y) ∉ S} × S ⊆ Q. A fixed
yz ∈ Q lies in R_S with probability ≥ 1/4 (z ∈ S and π(y) ∉ S are independent events of
probability 1/2, as z ≠ π(y)). So E_S μ(R_S) ≥ 1/4. ∎

The proof only uses that one side of the cut is a cyclic arc of length ≥ ⌊2n/3⌋. Indeed Q is
closed under rotation, and for a span (i, ℓ) the map xyz ↦ y·(zx) is a bijection of Σ^n that
preserves Q and turns a rectangle at span (i, ℓ) into a rectangle at span (0, ℓ) (pairs (x,z)
correspond bijectively to words zx because |x| is fixed). So:

**Corollary 2.4. PROVED; COMPUTER-CHECKED for all spans, n ≤ 18
(`unique_completion_offsets.py`).** For any span (i, ℓ) with ℓ ≤ ⌈n/3⌉ or ℓ ≥ ⌊2n/3⌋, Q_n is a union of
at most 2·min(ℓ, n−ℓ) ≤ 2⌈n/3⌉ rectangles at that span, each inside Q (for ℓ = n: one).

**Corollary 2.5 (no hard distribution; no fooling set). PROVED.** Fooling sets, distributional
bounds, fractional covers and the interchange lemma are all lower bounds on the same quantity,
the balanced cover number, so none can exceed 2⌈n/3⌉. More precisely, for every n ≥ 2 and every
μ on Q_n: max over balanced rectangles R ⊆ Q of μ(R) ≥ 1/4. In particular every fooling set for
Q_n at the split (⌊2n/3⌋ | ⌈n/3⌉) has size ≤ 2⌈n/3⌉, and the hypothesis of the method
("every balanced rectangle has μ_n-mass o(n^{-2})", let alone n^{-ω(1)}) is false for every
choice of μ_n. This includes distributions supported on words that are abelian p-th powers for
all p | n.

**Corollary 2.6 (interchange lemma is satisfied by Q). PROVED.** For all n ≥ 2, R ⊆ Q_n,
2 ≤ m ≤ n there are k ≥ |R|/(2⌈n/3⌉) words z_t = w_t x_t y_t ∈ R with equal |w_t|, equal |y_t|,
m/2 < |x_t| ≤ m and w_s x_t y_s ∈ Q for all s, t. So the conclusion of Lemma 1.3 holds for Q
with c_Q = 1 (indeed with n in place of n²).
*Proof.* If m ≥ 2⌈n/3⌉ take |x| = m ≥ ⌊2n/3⌋. Otherwise take |x| = min(m, ⌈n/3⌉); it is > m/2
and ≤ ⌈n/3⌉. In both cases Corollary 2.4 applies at span (0, |x|); pigeonhole. ∎
(This agrees with Horváth–Kudlek 1996 as reported by the scout, with an explicit constant.)

**Corollary 2.7 (refined, "uniform inner set" version). PROVED.** Lemma 1.1 also bounds the
number of distinct inner sets by g(n/3+1). The cover of Theorem A uses 2⌈n/3⌉ ≤ 2(n/3+1)
distinct inner sets, so Q passes this finer test as well (with "g = 2").

**Proposition 2.8 (tightness). PROVED for even n.** For even n ≥ 4 every rectangle cover of
Q_n at span (0, ⌊2n/3⌋) has ≥ ⌈n/3⌉ rectangles. So the cover number at this split is Θ(n).
*Proof.* π is onto Σ^s: given z, s ≤ n/2, pick u ∈ Σ^{n/2} ending in z; then (uu)[0,L) has
completion z. Column z of the matrix is {y : π(y) ≠ z}; distinct z give distinct columns. In a
cover by t rectangles A_r × B_r, column z equals ⋃_{r : z ∈ B_r} A_r, so 2^t ≥ 2^s. ∎
(FROM LITERATURE, de Caen–Gregory–Pullman 1981: the Boolean rank of J − I_N is
min{t : C(t,⌊t/2⌋) ≥ N}, which would give the exact value s + ½log₂ s + O(1) here.)

**Why the "AND of ω(n) NEQ conditions" never costs anything.** Primitivity is the AND over
p | n of "not d_p-periodic". Once one side of the cut is a contiguous arc of length ≥ 2n/3, that
side has at most one periodic completion *in total* (Fine–Wilf merges all the periods), so the
AND of ω(n) inequality tests is a single inequality test on ⌈n/3⌉ bits. Contiguity of the inner
segment, far from helping the lower bound, is what destroys it. COMPUTER-CHECKED
(`unique_completion_out.txt`): uniqueness holds exactly from prefix length 2n/3 on when 6 | n
(n = 12: lengths 8..11; at length 7 some prefix has 2 completions) and from 3n/5 on for n = 10, 20.

---------------------------------------------------------------------------------------------

## 3. Second barrier: affine covers for every bipartition; small NFAs for the slices

Theorem A needs a long contiguous side. The following works for every cut, including
non-contiguous bipartitions of the positions, and gives small automata.

For p ∈ P(n) let V_p ⊆ GF(2)^n be the cyclically d_p-periodic words (a linear subspace) and
S_p = {s ∈ GF(2)^n : Σ_{t<p} s_{r+t·d_p} = 0 for every r < d_p}.

**Lemma 3.1. PROVED.** (a) If w ∈ V_p then ⟨w,s⟩ = 0 for all s ∈ S_p. (b) If w ∉ V_p then
exactly half of the s ∈ S_p satisfy ⟨w,s⟩ = 1.
*Proof.* (a) ⟨w,s⟩ = Σ_r w_r Σ_t s_{r+t d_p} = 0. (b) Some residue class mod d_p contains
positions i, i' with w_i ≠ w_{i'}; e_i + e_{i'} ∈ S_p and ⟨w, e_i+e_{i'}⟩ = 1, so s ↦ ⟨w,s⟩ is a
nonzero linear functional on S_p. ∎

**Theorem B (affine cover). PROVED; COMPUTER-CHECKED exhaustively for n ≤ 24
(`affine_cover.py`, `run_affine_big.py` → `affine_cover_out.txt`) and by sampling for
n = 30, 210, 2310, 30030 (`sample_large_n.py` → `sample_large_n_out.txt`).**
Let n ≥ 2, k = ω(n). For a tuple (s_p)_{p∈P(n)}, s_p ∈ S_p, put
T = {w ∈ Σ^n : ⟨w, s_p⟩ = 1 for all p ∈ P(n)}. Then
1. T ⊆ Q_n;
2. for w ∈ Q_n and independent uniform s_p ∈ S_p, Pr[w ∈ T] = 2^{-k};
3. Q_n is a union of N ≤ ⌈2^k n ln 2⌉ such affine subspaces.
*Proof.* (1) A non-primitive w lies in some V_p (Lemma 2.1), so ⟨w,s_p⟩ = 0. (2) Lemma 3.1(b)
and independence. (3) With N independent tuples the expected number of uncovered w ∈ Q_n is
|Q_n|(1−2^{-k})^N < 2^n e^{-N/2^k} ≤ 1. ∎

**Corollary 3.2 (every bipartition). PROVED.** Let Y ⊆ {0..n−1} be arbitrary. Each T splits
into 2^k rectangles for the partition (Y, Y^c): fix the k parities of ⟨w|_Y, s_p|_Y⟩. Hence
Q_n is a union of ≤ 2^k⌈2^k n ln 2⌉ ≤ 4^{ω(n)} n ln 2 + 2^{ω(n)} rectangles for (Y, Y^c), and for
every μ on Q_n some rectangle inside Q has μ-mass ≥ 4^{-ω(n)}. Since 4^{ω(n)} ≤ (8/3)n for all n
(maximum of 4^k/(p_1⋯p_k), attained at n = 6) and 2^{ω(n)} ≤ n, the count is ≤ 3n²; since
ω(n) ≤ (1+o(1)) ln n / ln ln n it is n^{1+o(1)}.

**Corollary 3.3 (slices have small NFAs). PROVED.** Q_n is accepted by an NFA with at most
(n+1)·2^k·⌈2^k n ln 2⌉ + 1 = n^{2+o(1)} states (≤ 1.85n³ + 2.85n² + n + 1 for all n): each T is
accepted by a DFA with states (position, parity vector), and the NFA is the union. Hence Q_n has
a right-linear grammar, and a CNF grammar, with n^{2+o(1)} nonterminals and rules.
(n^{o(1)} because ω(n)! ≤ n.) This is unconditional. According to the coordinator, the scout has
an unconditional n^{O(ω(n))} NFA and an n^{2+o(1)} slice grammar conditional on a "non-crossing
mismatch pairs" conjecture; Corollary 3.3 gives n^{2+o(1)} without that conjecture, by a different
(probabilistic, parity-test) construction. I did not examine the scout's conjecture itself.

**Corollary 3.4 (multi-cut products). PROVED.** For any cut positions 0 < i_1 < … < i_t < n,
Q_n is a union of at most ⌈2^k n ln 2⌉·2^{kt} sets S_0 S_1 ⋯ S_t (S_r ⊆ Σ^{i_{r+1}−i_r}), each
inside Q_n (classes = (tuple, parity vectors at the cuts)). So nested or iterated interchange
statements with loss (c n²)^t are also satisfied by Q.

**Remark 3.5 (explicit version). FROM LITERATURE, argument PROVED modulo it.** Write
s_p = r_p + σ^{d_p} r_p with r = (r_p)_p ∈ GF(2)^{kn}. Then ⟨w,s_p⟩ = ⟨w + σ^{-d_p}w, r_p⟩, and
for w ∈ Q_n the k vectors w + σ^{-d_p}w are nonzero and sit in different blocks. If r is drawn
from an ε-biased set D ⊆ GF(2)^{kn} with ε < 2^{-k}, then
Pr[all k bits are 1] ≥ 2^{-k}(1 − (2^k−1)ε) > 0, so Q_n = ⋃_{r∈D} T_r. Explicit ε-biased sets of
size O((kn/ε)²) exist (Alon–Goldreich–Håstad–Peralta 1992), giving explicit covers of size
n^{2+o(1)}.

---------------------------------------------------------------------------------------------

## 4. What the barriers do and do not exclude

**Excluded (PROVED):**
* any integral rectangle/fooling-set bound: the balanced cover number is ≤ 2⌈n/3⌉ (Thm A);
* any fractional/distributional bound: every μ has a balanced rectangle of mass ≥ 1/4 (Thm A.3);
* the ORW interchange lemma in the form of Lemma 1.3, for every R and m (Cor 2.6);
* the finer count of distinct inner sets (Cor 2.7);
* nested / multi-cut versions with polynomial loss (Cor 3.4);
* any argument that would show the CNF-grammar (or even NFA) size of Q_n is ≥ n^{2+ε} (Cor 3.3).

**Residual window (OPEN, stated precisely).** If Q is context-free with g nonterminals, then
Q_n has a CNF grammar with ≤ g·n nonterminals (A, m) and ≤ g'·n² rules. We only show
n^{2+o(1)} for both. So a slice-wise proof would have to show "Q_n needs ω(n) nonterminals" or
"ω(n²) rules". Rectangle arguments cannot do this: a grammar with ρ nonterminals yields
≤ ρ(n/3+1) inner sets, and Theorem A covers Q_n with 2⌈n/3⌉, so they give ρ ≥ O(1). I know of no
other technique for lower bounds on the grammar size of explicit finite languages.
Everything else must use uniformity in n (one grammar for all lengths), which no statement
about a single slice captures.

**Proposition 4.1 (contrast: the method does work for the complement). PROVED.** Let n = 2^a,
μ uniform on the squares uu, |u| = n/2. Every balanced rectangle R ⊆ co-Q has μ(R) ≤ 2^{-n/3}.
Hence co-Q_n needs ≥ 2^{n/3} balanced rectangles and co-Q is not context-free.
*Proof.* Let (i,ℓ) be the span and J the set of inner positions j whose partner j+n/2 mod n is
outer; |J| = min(ℓ, n−ℓ) ≥ n/3, and positions of J are distinct mod n/2. If squares
x₁y₁z₁, x₂y₂z₂ ∈ R differ at j ∈ J, the hybrid h = x₁y₂z₁ ∈ R is non-primitive, hence (n = 2^a)
a square, so h_j = h_{j+n/2}; but h_j = (x₂y₂z₂)_j and h_{j+n/2} = (x₁y₁z₁)_{j+n/2} = (x₁y₁z₁)_j.
So all squares in R agree on J: at most 2^{n/2−n/3} of them. ∎
Thus the rectangle method is complement-sensitive: non-primitive words are a union of ω(n)
subspaces (hard, "OR of EQ"), primitive words are the complement (easy, "AND of NEQ").

---------------------------------------------------------------------------------------------

## 5. Analytic angle: bounded and polynomial ambiguity (task 4)

ψ(n) = |Q_n| = Σ_{d|n} μ(d) 2^{n/d}; ψ(i,j) = number of primitive words with i a's and j b's
= Σ_{d | gcd(i,j)} μ(d) C((i+j)/d, i/d). For a CNF grammar G let d_G(w) be the number of parse
trees of w.

**Proposition 5.1 (counting alone cannot exclude ambiguity 2). PROVED; COMPUTER-CHECKED
(`counting_sandwich.py`: n ≤ 3000, i+j ≤ 400).**
(a) ψ(n) ≤ 2^n ≤ 2ψ(n) for all n ≥ 1.
(b) C(i+j,i) ≤ 2ψ(i,j) for all i, j ≥ 1.
So the unambiguous regular languages Σ^+ and {a,b} ∪ {w : |w|_a,|w|_b ≥ 1} have counting
functions (univariate, resp. by letter content) sandwiched between that of Q and twice it. Any
argument using only "the derivation-counting series of a k-ambiguous grammar is algebraic and
lies between ψ and kψ" is therefore consistent for k ≥ 2 and yields no contradiction; the same
holds a fortiori for polynomial ambiguity.
*Proof.* (a) 2^n − ψ(n) = Σ_{d|n, d<n} ψ(d) < 2^{n/2+1} ≤ 2^{n−1} for n ≥ 4; n ≤ 3 by hand.
(b) If gcd(i,j) = 1 all words are primitive. Otherwise i, j ≥ 2; with m = i+j, X = C(m,i) ≥
C(m,2), and C(m/g, i/g) ≤ X^{1/g}, the number of non-primitive words is
≤ X^{1/2} + (m/2)X^{1/3} (the term g = 2, plus at most gcd(i,j) ≤ m/2 terms with g ≥ 3). Dividing
by X, the ratio X^{-1/2} + (m/2)X^{-2/3} is decreasing in X, and at X = m(m−1)/2 it is decreasing
in m and equals 0.42 at m = 16; so the non-primitive words are fewer than X/2 for m ≥ 16. For
m < 16 (in fact m ≤ 400): computer. ∎

**Theorem 5.2 (exponential excess ambiguity). PROVED, using Chomsky–Schützenberger
(FROM LITERATURE) and finiteness of the singularities of an algebraic function.**
Let G be any CNF grammar with L(G) = Q and e_G(n) = Σ_{w∈Q_n} (d_G(w) − 1). Then
limsup_n e_G(n)^{1/n} > 1.
*Proof.* A(z) = Σ_n (ψ(n)+e_G(n)) z^n is algebraic (Chomsky–Schützenberger). Ψ(z) = Σψ(n)z^n =
Σ_{d≥1} μ(d)·2z^d/(1−2z^d) is meromorphic in |z| < 1 with a simple pole at every z with
z^d = 1/2, d squarefree (for such z only the d-th term is singular, since |z^{d'}| = 2^{-d'/d}),
i.e. infinitely many poles in the open unit disc. Suppose limsup e_G(n)^{1/n} ≤ 1. Then
E = A − Ψ is analytic in the disc, so A = E + Ψ is meromorphic there with infinitely many poles.
But A satisfies an irreducible P(z, A) = 0 (as a power series, hence on the whole disc minus
the poles, by the identity theorem); outside the finite set Ex of zeros of the leading
coefficient and of the discriminant, the roots of P(z,·) are distinct analytic germs, and on a
punctured neighbourhood of a point z₀ ∉ Ex the function A coincides with one of them, hence is
bounded near z₀. So all poles of A lie in Ex, a contradiction. ∎

**Corollaries. PROVED (the last one also uses, FROM LITERATURE, that the commutative image of a
ℤ-algebraic series is algebraic).**
* (Petersen) Q is not unambiguous (e_G ≡ 0 is impossible).
* A grammar for Q of ambiguity degree k has ≥ e_G(n)/(k−1) ambiguous words of length n, so
  exponentially many infinitely often: finite ambiguity cannot be "almost unambiguous".
* If Q = L₁ ∪ … ∪ L_k with unambiguous context-free L_i, then
  Σ_w∈Σ^n (#{i : w ∈ L_i} − 1) grows exponentially along a subsequence.
* The characteristic series of Q is not ℤ-algebraic. The class of languages with ℤ-algebraic
  characteristic series contains the unambiguous CFLs and is closed under complement, disjoint
  union and proper difference; Q (and co-Q) lie outside it. E.g. Q ≠ L₁ \ L₂ with L₂ ⊆ L₁
  unambiguous CFLs, and in a k-ambiguous grammar for Q the level sets {w : d_G(w) ≥ j}, j ≥ 2,
  cannot all have ℤ-algebraic characteristic series.

**What remains OPEN here.** Theorem 5.2 gives no contradiction for ambiguity degree k ≥ 2 nor
for polynomial ambiguity; by Proposition 5.1 no purely enumerative argument can. Hadamard
products of algebraic series are not algebraic, so the level sets cannot be isolated analytically.

---------------------------------------------------------------------------------------------

## 6. Computations (all in `scripts/rectangles/`)

| script | what it checks | result |
|---|---|---|
| `unique_completion.py` → `unique_completion_out.txt` | Theorem A exhaustively, 2 ≤ n ≤ 22: uniqueness of the completion at prefix length ⌊2n/3⌋, exact cover by 2⌈n/3⌉ rectangles; number of completions at every other prefix length | all assertions pass |
| `affine_cover.py`, `run_affine_big.py` → `affine_cover_out.txt` | Theorem B exhaustively, n ≤ 24: T ⊆ Q_n, Pr[w∈T] = 2^{-k}, number of random T needed | e.g. n = 24: 48 random / 42 greedy, bound 67 |
| `sample_large_n.py` → `sample_large_n_out.txt` | Theorem B by sampling, n = 30, 210, 2310, 30030, including primitive abelian powers | ⟨u^p,s_p⟩ = 0 always; hit rate ≈ 2^{-k} |
| `unique_completion_offsets.py` → `unique_completion_offsets_out.txt` | Corollary 2.4 at every admissible span (all offsets), n ≤ 18 | pass |
| `split_lp.py` → `split_lp_out.txt` | exact fractional cover number C* of Q_n at one split, first part of length ℓ (column generation, pricing certified by an exact MILP) | n=4,ℓ=2: 3; n=6,ℓ=2: 3; n=6,ℓ=3: 3.5; n=8,ℓ=4: 3.75; n=9,ℓ=3 and 4: 3.5; n=10,ℓ=4: 3.75; n=10,ℓ=5: 3.875. All ≤ 4; at the splits of Theorem A the value is 4(1−2^{-s}), the value for inequality on s bits. The n = 12 runs were stopped by the time limit and gave no result. The two n = 9 lines in the output file were copied by hand from an earlier run of the same script. The "greedy integer cover" numbers printed there are heuristic upper bounds and are weaker than Theorem A (e.g. 16 versus 8 for n=10, ℓ=4). |
| `counting_sandwich.py` → `counting_sandwich_out.txt` | Proposition 5.1 and the formulas for ψ(n), ψ(i,j) against brute force (n ≤ 16) | pass |

---------------------------------------------------------------------------------------------

## 7. Conclusions for the team

1. The rectangle / fooling-set / interchange-lemma line cannot prove the conjecture. This is a
   theorem, not a heuristic: cover number ≤ 2⌈n/3⌉, fractional cover number ≤ 4.
2. The intended hard instances (abelian p-th powers for all p | n) are not hard: with a
   contiguous side of length 2n/3 there is one forbidden completion in total.
3. Each slice Q_n is even NFA-easy (n^{2+o(1)} states), unlike the slices of palindromes or of
   co-Q. The difficulty of the conjecture is entirely in uniformity across lengths.
4. The only slice-wise statement that would still imply the conjecture is a superlinear lower
   bound on the number of nonterminals (or ω(n²) on the rules) of grammars for Q_n; rectangle
   arguments provably cannot give it.
5. Enumerative arguments stop at ambiguity degree 1, but they do force exponentially many
   excess parse trees in any grammar for Q.
