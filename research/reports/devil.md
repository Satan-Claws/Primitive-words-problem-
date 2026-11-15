# Report of agent "devil" (adversary of the conjecture "Q is not context-free")

**Claim status: I do NOT claim a proof either way.** No CFG/PDA for Q was found. What I have is
(1) rigorous barrier theorems that sink the rectangle / fooling-set / interchange route completely,
(2) a rigorous "no bounded certificate" theorem and several refuted certificate candidates,
(3) reductions and partial results for the bounded-language route.

Notation. Σ = {a,b}; Q = primitive words; Q_n = Q ∩ Σ^n; ω(n) = number of distinct primes dividing n;
positions are 0..n-1; "period d" for a word of length n with d | n means w_i = w_{i+d} for all i (mod n).
Scripts are in `scripts/devil/`. Tags: PROVED / COMPUTER-CHECKED / LITERATURE / CONJECTURED.

Basic fact F0 (PROVED). For |w| = n >= 1: w is not primitive iff w has period n/p for some prime p | n.
(If w = u^k, k >= 2, take a prime p | k: w = (u^{k/p})^p, and p | n. A word of length n with period d | n
equals (w[0,d))^{n/d}.)

---------------------------------------------------------------------------------------------------
## 1. Positive side: what IS context-free

### T1 (PROVED + COMPUTER-CHECKED). For every k >= 2, coPow_k = Σ^* \ {u^k : u ∈ Σ^*} is context-free.
Grammar (X -> a | b):

    S -> N | M
    N -> R_1 | ... | R_{k-1};   R_r -> X^r T;   T -> ε | X^k T          (length not divisible by k)
    M -> A[r,c] B[k-2-r,d]      for 0 <= r <= k-2 and (c,d) ∈ {(a,b),(b,a)}
    A[r,c] -> X^{k-1} A[r,c] X | X^r c        generates { x c y : |x| = (k-1)|y| + r }
    B[s,d] -> X B[s,d] X^{k-1} | d X^s        generates { y d z : |z| = (k-1)|y| + s }

Proof. (i) M generates exactly M' = { x c y d z : c != d, |x|+|z| = (k-1)|y| + k-2 }.
"⊆": concatenating x c y1 and y2 d z gives |x|+|z| = (k-1)(|y1|+|y2|) + r + (k-2-r).
"⊇": given such a word put |y1| = floor(|x|/(k-1)), r = |x| mod (k-1). Since |x| <= (k-1)|y| + k-2 we get
|y1| <= |y|; then |z| = (k-1)(|y|-|y1|) + (k-2-r) with 0 <= k-2-r <= k-2.
(ii) If w ∈ M' then |w| = k(|y|+1) and, with m = |y|+1, w_{|x|} = c != d = w_{|x|+m}; so w has no period m,
so w is not a k-th power. (iii) Conversely if |w| = km, m >= 1, and w is not a k-th power, then w has no
period m, so some i has w_i != w_{i+m}; cut w = x c y d z there: |y| = m-1 and |x|+|z| = km-m-1 = (k-1)|y|+k-2.
(iv) Words of length not divisible by k are not k-th powers; ε = ε^k. Hence L(S) = coPow_k. ∎
Check: `copow_grammar.py k 12` (Earley parser on the literal grammar vs brute force), k = 2,3,4,5,
all 8191 words of length <= 12: equal.

### T2 (PROVED). Q_n = Σ^n ∩ ⋂_{p prime, p | n} coPow_p  (n >= 1).  (Immediate from F0.)
So the whole difficulty is the intersection over the primes of n; see §3 for how bad it is.

### T3 (PROVED, modulo LITERATURE: CFLs are closed under cyclic shift, Oshiba 1972 / Maslov 1973 /
Hopcroft–Ullman Ex. 6.4c). Q is CF iff there is a CF language L ⊆ Q such that every primitive word has a
conjugate in L. (⇐: Cyc(L) is CF, Cyc(L) ⊆ Cyc(Q) = Q and Q ⊆ Cyc(L). ⇒: L = Q.)
So a construction may normalise the word by ANY rotation for free. Example use: Q ∩ {|w|_b = k} is CF
iff Q ∩ (ba^*)^k is CF iff the Kászonyi–Katsura language Q ∩ (ab^*)^k is CF.

---------------------------------------------------------------------------------------------------
## 2. BARRIER for route (b): rectangles, fooling sets, discrepancy, interchange lemma

A *split* (k,m) of Σ^n: inner = positions [k,k+m), outer = the other n-m positions (a cyclic interval).
Write a word as (o,x) = (outer, inner). Bad(o) = { x ∈ Σ^m : o∘x ∉ Q }.
A *rectangle* of the split is O×I with O a set of outers and I ⊆ Σ^m; it is "in Q" if o∘x ∈ Q for all pairs.

### R1 (PROVED; COMPUTER-CHECKED n <= 16, `rect_barrier.py 16`).
(a) If n-m >= n/p for every prime p | n (in particular if m <= n/2) then |Bad(o)| <= ω(n) for every outer o.
(b) If n is even and m = n/2+1 then |Bad(o)| <= ω(n)+1.
(c) If m <= ceil(n/3) (i.e. n-m >= floor(2n/3)) and n >= 2 then |Bad(o)| <= 1.
Proof. (a) Fix d = n/p. The outer positions are n-m consecutive residues mod n, and d | n, so they cover
n-m >= d consecutive residues mod d, i.e. all of them; a d-periodic completion is therefore unique.
By F0, x ∈ Bad(o) iff o∘x is d-periodic for one of the ω(n) values d = n/p. (b) For d = n/2 exactly one
residue class mod d is uncovered and it meets the inner part in two positions that must be equal: <= 2
completions; for d <= n/3 and n >= 6 the outer (length n/2-1 >= n/3) covers all residues; n = 2,4 by hand.
(c) Suppose x != x' are both bad, with periods d1 = n/p, d2 = n/q. By (a)'s uniqueness p != q.
The outer, read cyclically, is a factor of a rotation of both powers, so as a linear word of length n-m it
has periods d1 and d2. d1 + d2 - gcd(d1,d2) = n(p+q-1)/(pq) <= 2n/3 (max at {2,3}) and it is an integer, so
it is <= floor(2n/3) <= n-m. Fine–Wilf: the outer has period g = gcd(d1,d2) = n/(pq). o∘x is d1-periodic and
contains a window of d1 consecutive positions (inside the outer) that is g-periodic with g | d1, hence o∘x is
g-periodic (cyclically); same for o∘x'. Two g-periodic words that agree on the outer (which covers all
residues mod g) are equal: x = x'. Contradiction. ∎

### R2 (PROVED). Fooling sets are tiny. Fix a split with m <= n/2. If F ⊆ Q_n is a fooling set for rectangles
of this split (for distinct (o,x),(o',x') ∈ F: o∘x' ∉ Q or o'∘x ∉ Q) then |F| <= 2ω(n)+1.
Proof. Two elements with the same inner word (or the same outer) are not fooling, so inners are pairwise
distinct. Orient each fooling pair i -> j if x_j ∈ Bad(o_i). Out-degree <= |Bad(o_i)| <= ω(n) by R1, and every
unordered pair carries an arc, so |F|(|F|-1)/2 <= ω(n)|F|. ∎
COMPUTER-CHECKED (`fooling_cover.py`): the exact maximum fooling set is 3 for
(n,k,m) ∈ {(6,2,2),(6,1,3),(8,3,3),(10,3,4),(10,2,5),(12,4,4),(12,3,6),(14,5,5)}.

### R3 (PROVED). Small rectangle covers and no discrepancy. Fix a split with m <= n/2, n >= 2.
(a) Q_n is a union of at most 2ω(n)(n+1) rectangles of this single split, each contained in Q_n.
(b) For every probability distribution μ on Q_n there is a rectangle of this split, contained in Q_n,
    with μ-mass >= 1/(4ω(n)).
Proof. Take t = 2ω(n) colours and a uniformly random colouring χ : Σ^m -> [t]. For a colour c let
I_c = χ^{-1}(c), O_c = { o : Bad(o) ∩ I_c = ∅ }; O_c × I_c is in Q by definition. A word (o,x) ∈ Q_n lies in
O_{χ(x)} × I_{χ(x)} unless some x' ∈ Bad(o) (x' != x since x ∉ Bad(o)) gets the colour of x: probability
<= ω(n)/t = 1/2. (b): expected covered mass >= 1/2, so some colouring covers mass >= 1/2 with t rectangles.
(a): with n+1 independent colourings a fixed word is uncovered with probability <= 2^{-(n+1)}; union bound
over < 2^n words. ∎
COMPUTER-CHECKED (`fooling_cover.py`): explicit covers with 5..24 rectangles for the splits listed in R2.

### R4 (PROVED; COMPUTER-CHECKED n <= 18, `first_letter_split.py 18`). An explicit cover whose inner sides are
"everything". Let n >= 2, m = ceil(n/3). For every w ∈ Q_n there is k ∈ {0,..,m-1} such that, writing
w = u y v with |u| = k, |y| = m, EVERY word u y' v with y' ∈ Σ^m and y'_0 = y_0 is primitive.
Consequently  Q_n = ⋃_{k<m, c∈Σ}  { u c z v : |u| = k, z ∈ Σ^{m-1} arbitrary, (u,v) ∈ O_{k,c} },
a union of 2·ceil(n/3) rectangles with inner length ceil(n/3)-1 whose inner side is ALL of Σ^{m-1}.
Proof. Suppose not. Then for every k < m the split (k,m) has a bad inner word x_k whose first letter is w_k
(by R1(c) it is the unique bad word). P_k := u x_k v is a power and agrees with w on [0,k] ∪ [k+m,n).
P_k and P_{k+1} both agree with w on [0,k] ∪ [k+m+1,n), the outer of the split (k+1,m); by R1(c) that outer
has at most one power completion, so P_k = P_{k+1}. Hence P_0 = ... = P_{m-1} =: P, and P agrees with w on
[m,n) (k = 0) and on [0,m-1] (k = m-1): P = w is a power. Contradiction. ∎
In words: every primitive word has a window of ceil(n/3)-1 consecutive letters, starting among the first
ceil(n/3)+1 positions, that can be overwritten arbitrarily without destroying primitivity.

### R5 (PROVED). Q satisfies the conclusion of the interchange lemma (Ogden–Ross–Winklmann form: for n >= 2,
S ⊆ L ∩ Σ^n, 2 <= m <= n there are Z ⊆ S and z_i = w_i x_i y_i with equal |w_i|, equal |x_i| ∈ (m/2, m],
and w_i x_j y_i ∈ L for all i,j, |Z| >= |S|/(c n^2)) with the much stronger bound |Z| >= |S| / (e(ω(n)+2)).
Proof. Use the split k = 0, m' = floor(m/2)+1 (so m/2 < m' <= m). n odd: n-m' >= (n-1)/2 >= n/3 >= n/p, R1(a).
n even, m <= n-1: m' <= n/2, R1(a). n even, m = n: m' = n/2+1, R1(b). In all cases |Bad(o)| <= ω(n)+1. Put each inner word independently into a random set X' with probability
q = 1/(ω(n)+2), and let Z = { (o,x) ∈ S : x ∈ X', Bad(o) ∩ X' = ∅ }. For i,j ∈ Z: x_j ∈ X' and
Bad(o_i) ∩ X' = ∅, so o_i∘x_j ∈ Q. P[(o,x) ∈ Z] >= q(1-q)^{ω(n)+1} >= 1/(e(ω(n)+2)). ∎

### Consequence for route (b) (PROVED).
The coordinator's bound "a CNF grammar of size g gives <= g n^2 balanced rectangles inside L covering L_n"
can never be violated by Q: covers of size 2·ceil(n/3) exist (R4), fooling sets have size <= 2ω(n)+1 (R2),
every distribution charges some rectangle with mass >= 1/(4ω(n)) (R3b), and the interchange lemma holds (R5).
Any successful counting argument must use more than "one level" of the derivation tree, i.e. it must
exploit that the inner/outer sides themselves come from a FIXED grammar for all n (uniformity), or nested
rectangles at several scales simultaneously.

### Pumping (PROVED lemma + COMPUTER-CHECKED n <= 16, `pump_letter.py 16`).
Lemma: if c^i s = t^p with p >= 2, c a letter, s ∉ c^*, then i < |s| (else |t| <= i, t ∈ c^*, so s ∈ c^*).
u c^i z is conjugate to c^i (zu), so "the letter at position j can be pumped (all i >= 0)" is decidable by
checking i <= n-1. Result: every primitive word of length 2..16 has at least one pumpable single letter
(the number of non-pumpable letters can be as large as n-2, e.g. a^{k+1} b a^k b). The general statements
(Bar-Hillel, Ogden, Bader–Moura hold for Q) are LITERATURE / the scout's report.

---------------------------------------------------------------------------------------------------
## 3. Certificates of primitivity: what a "local" certificate can and cannot do

A *certificate* for w ∈ Q_n is a set S of positions such that every word of length n agreeing with w on S is
primitive.

### C0 (PROVED). S is a certificate iff for every prime p | n there are i,j ∈ S with i ≡ j (mod n/p) and
w_i != w_j.  (A partial word is consistent with period d iff equal residues mod d carry equal letters.)

### C1 (PROVED) "forest theorem": every certificate has at least ω(n)+1 positions, for EVERY primitive word.
Proof. Choose for each prime p | n a pair e_p = {i_p,j_p} ⊆ S as in C0; j_p - i_p = c_p·n/p with p ∤ c_p
(0 < |j_p-i_p| < n). Claim: the graph on S with edges e_p is a forest. Take a cycle, orient it; the signed
differences sum to 0: Σ_p ±c_p n/p = 0 over the primes on the cycle (each prime labels at most one edge).
Fix a prime p0 on the cycle and reduce modulo p0-adic valuation: every term with p != p0 has valuation
>= v_{p0}(n), the p0-term has valuation v_{p0}(n)-1. Contradiction. A forest with ω(n) edges has >= ω(n)+1
vertices. ∎
Corollary (PROVED): there is NO bounded-size certificate scheme. For n = p_1 p_2 ... p_r every certificate
of every primitive word of length n reads >= r+1 letters and contains >= r mismatch pairs at r pairwise
different distances, each tied to a different divisor n/p_i. (See §3b for the brute-force part.)

### C2 (PROVED, modulo LITERATURE Ginsburg–Spanier: a bounded CFL has a stratified semilinear exponent set).
Two distances cannot be tied to |w| at marked positions. Let p1 != p2 be primes, 0 < j_t < p_t, and fix any
order type of four (or three, if one endpoint is shared) marked positions forming pairs P1, P2. The language
of words a^{l_0} # a^{l_1} # ... # a^{l_s} in which dist(P_t) = j_t·n/p_t (t = 1,2; n = total length) is
either finite or NOT context-free (it is infinite for every geometrically feasible arrangement, e.g. all
nested and shared-endpoint ones).
Proof. Every period vector v of a linear subset satisfies p_t·dist_t(v) = j_t·|v|, so 0 < dist_t(v) < |v|.
If v = αe_a + βe_b had <= 2 non-zero coordinates, exactly one of them lies inside P1 and exactly one inside P2,
giving j1/p1 ∈ {j2/p2, 1 - j2/p2}; impossible for distinct primes. So stratified linear subsets are single
points, and a finite union of them is finite. ∎ (Concrete instance, by the ordinary pumping lemma: { # a^{2l+1} # a^l # a^{3l+2} } is not CF;
this is exactly "w_j, w_{j+n/3}, w_{j+n/2} marked, j = 0".)
Meaning: a PDA can tie ONE mismatch distance to |w| by counting (T1), but as soon as the positions of two
checks for two different primes are pinned down, no PDA can verify both distances. Any CF construction for
even coPow_2 ∩ coPow_3 would have to be genuinely ambiguous about where its mismatches are.

### C3 (PROVED). The normalised universal-mismatch language is not CF.
L_univ = { w : w_0 != w_{n/p} for all primes p | n }. L_univ ∩ a^+ b a^* b a^* ∩ (Σ^6)^* =
{ a^{2m} b a^{m-1} b a^{3m-1} : m = 2^α 3^β, m >= 1 } (a third prime would need a third b), whose length set
is not semilinear. So this certificate shape is not CF even though T3 allows free rotation.

### C4 (COMPUTER-CHECKED, `universal_mismatch.py`). The "universal mismatch" certificate
(∃ i: w_i != w_{i+n/p} for all p | n, indices mod n) is sound but INCOMPLETE: primitive words without it:
n=12: 24 (e.g. bbaabaabbaaa), n=18: 432, n=20: 120, n=21: 42; none for n = 6,10,14,15,22.

### C5 (COMPUTER-CHECKED, `binary_W.py`). Linear ("one-counter") certificates. Let W_n = Σ_p V_{n/p} be the real
span of the (n/p)-periodic vectors. If some integer linear form L ⊥ W_n has L(w) != 0 (w as a 0/1 vector) then
w is primitive. Binary primitive words lying IN W_n (no linear certificate): n=12: 24, n=18: 432, n=20: 120,
n=24: 5664; none for n = 6,10,14,15,21,22. (Same exceptional words as in C4 for n = 12,18,20.)

---------------------------------------------------------------------------------------------------
## 4. Route (a): bounded languages, E_n = exponent set of Q ∩ (ab^*)^n = primitive vectors of N^n

LITERATURE (not re-proved; the Debrecen server was unreachable): Kászonyi–Katsura: Q ∩ (ab^*)^n is CF for n a
product of two (1997: three) prime powers, and whenever Σ_{p|n} 1/p < 4/5 (Kászonyi 2010). The first n not
obviously covered by the 4/5 rule is 30 (31/30), which is a product of three prime powers.

### B1 (PROVED). For any integer linear form L on N^n, { a b^{x_1} ... a b^{x_n} : L(x) != 0 } is a
deterministic one-counter language (counter = |running sum|, sign in the finite control).
Hence E_n \ W_n is CF for EVERY n (x ∉ W_n iff L(x) != 0 for some L in a finite integer basis of W_n^⊥, and
L ⊥ W_n ⊇ V_{n/p} makes the test sound). For n = p^h, W_n = V_{n/p} and E_n ∩ W_n = ∅: prime powers are trivial.
So the Kászonyi–Katsura conjecture is entirely about E_n ∩ W_n (sums of periodic vectors).

### B2 (PROVED + COMPUTER-CHECKED). Chord certificates are sound and CF but incomplete.
For a set M of pairwise vertex-disjoint, pairwise non-crossing chords of the n-cycle with labels in {<,=,>},
C(M) = { x : x satisfies the labels } is a finite union of stratified linear sets (nested push/pop), and
C(M) ⊆ E_n iff the labels are inconsistent with every period n/p. For n = 6 no diameter {i,i+3} and step-2
chord {j,j+2} are vertex-disjoint and non-crossing (each arc cut off by a diameter has two adjacent vertices),
and `matching_cert.py 6 5` shows: 192 of the 46410 primitive vectors in {0..5}^6 have no sound labelled
non-crossing matching, e.g. (0,3,1,3,0,4). The same 192 fail the "mirror sign pattern" certificate
(`axis_sign.py 6 5`); exact mirror differences would work for n = 6 (`axis_delta.py 6 5 0`) but are not
PDA-checkable, and their truncations fail (`axis_delta.py 6 5 1|2`: 192 / 36 failures). All failures are in W_6.
Sharing a vertex does not help piecewise: {a^i b^j c^k : j > i, j > k} and {j < i, j < k} are not CF
(every period of a stratified linear subset must have 3 non-zero coordinates).
So the known CF-ness of E_6 (LITERATURE) needs "rigid" stratified pieces such as
{ (λ1,λ2,λ3,λ3,λ2,λ1+1) } ⊆ E_6 (PROVED: 3-periodicity forces λ1 = λ3 = λ1+1).

### What this means for route (a)
I could NOT prove a general barrier "Q ∩ R is CF for every bounded regular R"; that would contain the
Kászonyi–Katsura conjecture. The literature shows the route needs at least three distinct primes with
Σ 1/p >= 4/5 in (ab^*)^n-type slices; B1 says the only possible obstruction lives in W_n.

---------------------------------------------------------------------------------------------------
## 5. Route (c): closure properties / Parikh

PROVED: ψ(Q) = {(i,j) : i,j >= 1} ∪ {(1,0),(0,1)} is semilinear (a^i b^j is primitive for i,j >= 1).
PROVED: for regular R, ψ(Q ∩ R) ⊇ { v ∈ ψ(R) : gcd(v) = 1 }, and for a bounded R = w_1^* ... w_k^* with
distinct marker letters the question "is ψ(τ(Q)) semilinear" is exactly "is the exponent set
{ n : w_1^{n_1}...w_k^{n_k} ∈ Q } semilinear".
NOT PROVED (CONJECTURED): for every rational transduction τ, ψ(τ(Q)) is semilinear. I found no
transduction with a non-semilinear image and no proof that none exists; heuristically R1 (each context has
<= ω(n) bad fillings) makes every Parikh class that has two "independent" representatives contain a primitive
one. I make no barrier claim here.

---------------------------------------------------------------------------------------------------
## 3b. Answer to the coordinator's question: is there a bounded-size uniform certificate?

Question: is there a bounded number of nested/sequential mismatch checks, with distances tied to |w| by
counting, that every primitive word passes and no power passes?  **No, on two independent grounds.**

(1) PROVED (C1): any family of letter checks that no power of length n passes contains, for each prime p | n,
its own mismatch pair at a distance c·n/p (p ∤ c); these ω(n) pairs form a forest, so >= ω(n)+1 letters are
inspected. ω(n) is unbounded, so no bound r works: for n = p_1...p_{r} every r-letter check set is passed by
some power of length n. This holds for every word, so no search is needed; brute force only shows the bound
is attained:
COMPUTER-CHECKED (`min_certificate.py`): the exact minimum certificate size equals ω(n)+1
 - for ALL primitive words of length 6, 10, 14, 15, 21, 22 (a "star": one centre j lying in a non-constant
   residue class mod n/p for every p);
 - for all but 24 / 432 / 120 primitive words of length 12 / 18 / 20 (these need 4 = ω+2 letters; they are
   exactly as many as the binary primitive words in W_n of C5, e.g. bbaabaabbaaa);
 - on every sampled primitive word of length 30 (4465 words), 42 (2396), 210 (449): random words, powers
   with 1-3 flipped letters, and xors of periodic words.
A star is trivially non-crossing, so for all those words the scout's non-crossing conjecture holds with a
single centre.

(2) PROVED (C2): already for TWO primes the distances cannot be tied to |w| by counting once the check
positions are pinned down: the marked language is not CF for any arrangement (nested, sequential, crossing
or sharing an endpoint). T1 shows one distance can be tied; two cannot. So even for lengths 2^α 3^β a PDA
accepting coPow_2 ∩ coPow_3 could not work as "guess the two mismatches and verify them".
(I do not claim coPow_2 ∩ coPow_3 is non-CF: the unmarked language is a different object; its bounded slices
with k letters b are Kászonyi–Katsura sets "avoid two periods", which are CF by LITERATURE.)

What a uniform certificate CAN do (PROVED): one mismatch check at distance |w|/k for each k in a fixed finite
set, taken disjunctively (T1); any single linear test on block lengths (B1); and R4-type "free window"
structure. None of these certifies primitivity for lengths with two or more prime factors.

---------------------------------------------------------------------------------------------------
## 6. Summary of claims

No proof of the conjecture and no counterexample (no CFG/PDA for Q) is claimed.
PROVED barriers against route (b): R1-R5 (|Bad| <= ω(n); fooling sets <= 2ω(n)+1; covers by 2·ceil(n/3)
rectangles with full inner side; every distribution has a rectangle of mass >= 1/(4ω(n)); interchange lemma
with |Z| >= |S|/(e(ω(n)+2))).
PROVED obstacles for my own side (constructing a PDA): C1 (no bounded certificate), C2 (two distances cannot
be counted at marked positions), C3 (normalised universal mismatch language is not CF).
Route (a): only reductions (T3, B1) and the negative experiment B2; no general barrier.
Route (c): no barrier proved; semilinearity of all transduction images is only conjectured.
