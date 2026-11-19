# Round 1 / Route G: size lower bounds (rectangle covers) and finite intersections

**Verdict.**

1. **The rectangle / fooling-set route is provably dead.** The slice lemma is stated precisely below (Lemma 1). It shows that a CF grammar forces, for every n, a cover of Q_n := Q ∩ Σⁿ by at most |N|·n² balanced rectangles contained in Q. I prove the reverse direction for Q: **Q_n is an exact union of at most 12(1+|Σ|⌈n/3⌉) balanced rectangles contained in Q, and of at most 8 such rectangles when n is odd** (Theorem 2). The cover is explicit and deterministic. Consequences:
   - every fooling set has size O(|Σ|n);
   - every fractional/distributional rectangle bound is O(|Σ|n);
   - the same holds for nested "k-level boxes" of any depth (Theorem 2′) and for every middle length m, so the Ogden–Ross–Winklmann interchange conclusion holds for Q with loss 1/O(n) (Theorem 4).

   Exhaustive checks: binary alphabet n ≤ 24, ternary n ≤ 12. For 5 ≤ n ≤ 10, no two distinct primitive words are fooled at every balanced interval, so the maximum fooling set has size 1.
   *(This overlaps with Route B's Theorem 1/Cor. 2, which uses random rectangles with O(ω(n)·n log|Σ|) per cut. My cover is explicit and deterministic, it is an exact union, it uses only O(1) window positions, its Y-sides do not depend on position, and the yield side of each rectangle is free apart from at most one letter.)*
2. **What survives of the slice route** is a CFG-size question that one-level arguments cannot touch. The thresholds are precise (Lemma 1, Prop. 5). To refute CF-ness it suffices to show that CNF grammars for Q_n need ω(n) nonterminals, or ω(n²) rules, along infinitely many n. Every lower bound must stay below the upper bound n^{O(ω(n))} = 2^{O(log²n / log log n)}. The problem reduces exactly to "core" period-avoidance languages L(ℓ,E) (Theorem 3). The missing ingredient is a lower-bound technique that uses the recursive structure of contexts and yields. No such technique for general (ambiguous) CFGs is known to me. **This gap is of theorem strength.**
3. **Cross-check with Route B (§7).** B's single-window barrier is correct; I re-derived it. Measures that share nonterminals across lengths, used at one level, also die. This is proved for odd n, using one yield set Σ^ℓ per length. For even n it is verified for n ≤ 20 with 1+2|Σ| fixed regular yield languages. Only fully recursive measures survive, together with cross-length pumping.
4. **Finite intersections (Part 2).** I give an exact reformulation (Q is a k-intersection of CFLs iff N∪{ε} is a union of k co-CF sets) and a sufficient "density lemma". Any proof that Q is not a finite intersection implies that Q is not CF. All the one-level obstructions above apply to it as well. Nothing in Part 2 is proved beyond the reformulations, which is an honest stall.

Code and outputs: `campaign/round1/G_sizebounds_code/` (copied from the scratchpad).

---

## 1. Notation

n ≥ 2. D = D_n = {d : d | n, 1 ≤ d < n}. A word x of length L has period d (1 ≤ d < L) if x_i = x_{i+d} for 0 ≤ i < L−d. A period d ≥ L holds vacuously. We read w ∈ Σⁿ cyclically, with indices mod n. The *window* w⟨t,λ⟩ = w_t w_{t+1} ⋯ w_{t+λ−1} has indices mod n, and J_t = {t,…,t+λ−1} mod n is its arc. Facts used:

- (F0) w is non-primitive ⟺ w has cyclic period d for some d ∈ D. Then every window of w has period d.
- (FW) Fine–Wilf: if x has periods p, q and |x| ≥ p+q−gcd(p,q), then x has period gcd(p,q).
- E := D \ {n/2} (E = D if n is odd). Both D and E are closed under gcd: the gcd of two distinct elements of E is a proper divisor that is ≤ n/3. M1 ≥ M2 denote the two largest elements of E (M2 := 0 if |E| ≤ 1). Bounds: for n even, M1 ≤ n/3 and M2 ≤ n/4. For n odd, M1 ≤ n/3 and M2 ≤ n/5.

## 2. The slice lemmas (precise)

**Lemma 1 (slice grammar).** Let G = (N, Σ, P, S) be in CNF with L(G) = L. For n ≥ 1 define G_n as follows:
- nonterminals (A,ℓ) for A ∈ N and 1 ≤ ℓ ≤ n;
- rules (A,ℓ) → (B,ℓ′)(C,ℓ−ℓ′) for each A→BC ∈ P and 1 ≤ ℓ′ < ℓ;
- rules (A,1) → a for each A→a ∈ P;
- start symbol (S,n).

Then L(G_n) = L ∩ Σⁿ. G_n has ≤ |N|·n nonterminals and ≤ |P|·n² rules.
*Proof.* Induction on ℓ: (A,ℓ) ⇒* y iff A ⇒* y and |y| = ℓ. ∎
So if Q is CF, then for some constant c and **all** n, Q_n has a CNF grammar with ≤ c·n nonterminals and ≤ c·n² rules. A lower bound of ω(n) nonterminals, or ω(n²) rules, along a subsequence would refute CF-ness. A superpolynomial bound is far more than needed.

**Lemma 2 (balanced rectangles).** Let G be as above and n ≥ 2. For A ∈ N, 0 ≤ i, and n/3 < ℓ ≤ 2n/3 put
R(A,i,ℓ) = {xyz ∈ Σⁿ : |x| = i, |y| = ℓ, A ⇒* y, S ⇒* xAz}.
Each R(A,i,ℓ) is a combinatorial rectangle Y_{A,ℓ} × C_{A,i,ℓ}: the positions split into the interval [i,i+ℓ) and its complement. Each is contained in L, and L ∩ Σⁿ is their union. There are ≤ |N|·n² of them.
*Proof.* In a derivation tree of w, walk from the root into the child with the longer yield until the yield is ≤ 2n/3. The node reached has yield ℓ > (parent yield)/2 > n/3. Since S ⇒* xAz and A ⇒* y′ for every y′ ∈ Y_{A,ℓ}, the rectangle lies in L. ∎
Note that Y_{A,ℓ} does not depend on i. This is the only extra structure beyond "a cover by rectangles".

## 3. The obstruction: Q_n has an O(n) balanced cover

**Lemma 3 (period extension).** Suppose X has period d, and a suffix (or prefix) S of X with |S| ≥ d has period g with g | d. Then X has period g.
*Proof.* Let u be the last d letters of X, so u ⊆ S. Then X is a suffix of u^r for some r. Since u has period g and g divides |u|, u = v^{d/g}. Hence u^r = v^{rd/g} has period g, and so does X. The prefix case is symmetric. ∎

**Lemma 4 (cyclic chain lemma).** Let E′ ⊆ D be closed under gcd, with largest elements M1 ≥ M2. Let 1 ≤ λ < n. Let T = {t_0<⋯<t_{r−1}} ⊆ Z_n have all cyclic gaps ≤ s, where λ − s ≥ max(M1+M2−1, M1). If every window w⟨t,λ⟩ with t ∈ T has a period in E′, then w has a cyclic period d ∈ E′, so w is not primitive.
*Proof.* Let d_k be the least E′-period of the window X_k = w⟨t_k,λ⟩. The windows X_k and X_{k+1} overlap in O = w⟨t_{k+1}, λ−g_k⟩, where g_k ≤ s is the gap. O is a suffix of X_k and a prefix of X_{k+1}, |O| ≥ λ−s ≥ M1, and O has periods d_k and d_{k+1}.

If d_k ≠ d_{k+1}, then d_k + d_{k+1} − gcd ≤ M1+M2−1 ≤ |O|. By (FW), O has period g = gcd(d_k,d_{k+1}) ∈ E′. Lemma 3 (|O| ≥ d_k, g | d_k) shows that X_k has period g. Minimality forces g = d_k, so d_k | d_{k+1}. Symmetrically d_{k+1} | d_k, a contradiction. So all d_k equal one value d.

Now take any i. Choose t ∈ T with (i−t) mod n < s. Then (i+d) − t ≤ s−1+M1 ≤ λ−1, so i and i+d lie in the same window, which has period d. Hence w_i = w_{i+d} for all i. ∎

**Theorem 2 (explicit balanced cover).** Let λ = ⌊2n/3⌋, s = λ − max(M1+M2−1, M1) for E, and T = {0, s, 2s, …} ∩ [0,n). Define
- A_t = {w : w⟨t,λ⟩ has no period in D}, for t ∈ T;
- (n even only) B_{t,i,a} = {w : w⟨t,λ⟩ has no period in E, w_i = a, w_{i+n/2} ≠ a}, for t ∈ T, i ∈ J_t with i+n/2 ∉ J_t, and a ∈ Σ.

Then **Q_n = ⋃ A_t ∪ ⋃ B_{t,i,a}** (exact equality). Every piece is a rectangle with respect to the complementary arcs J_t and J̄_t. One of these arcs is a linear interval, of length λ or n−λ = ⌈n/3⌉, both in [n/3, 2n/3]. So every piece has the shape required in Lemma 2. Number of pieces: |T| ≤ 12 (n even), |T| ≤ 8 (n odd), and in total
  ≤ 8 (n odd),   ≤ 12·(1 + |Σ|·⌈n/3⌉) (n even).

*Proof.*
- Soundness of A_t: by (F0), any period in D would show up in the window.
- Soundness of B_{t,i,a}: the window rules out every period in E, and the mismatch at (i, i+n/2) rules out n/2. Since D = E ∪ {n/2}, w is primitive.
- Coverage: let w be primitive. By Lemma 4 with E′ = E, some window w⟨t,λ⟩ has no E-period. If it also has no period n/2 (or n is odd), then w ∈ A_t. Otherwise n is even and the window has period n/2. Since w is not a square, there is a pair {i, i+n/2} with w_i ≠ w_{i+n/2}. Both points cannot lie in J_t: they would sit at linear distance exactly n/2 inside the window and therefore be equal. Both cannot lie in J̄_t either, because |J̄_t| = ⌈n/3⌉ < n/2+1. Name the point in J_t as i; then w ∈ B_{t,i,w_i}.
- Counts: for n even, s ≥ (2n−2)/3 − 7n/12 + 1 > n/12, so |T| = ⌈n/s⌉ ≤ 12. For n odd, s > 2n/15, so |T| ≤ 8. For each t there are exactly n−λ admissible i. ∎

**Corollary 2.1 (all one-level methods fail).**
- Every fooling set F ⊆ Q_n (no balanced Q-rectangle contains two elements of F) has |F| ≤ 12(1+|Σ|⌈n/3⌉).
- For every distribution μ on Q_n, some balanced Q-rectangle has μ-mass ≥ 1/(12(1+|Σ|⌈n/3⌉)).
- Lemma 2 only forbids covers smaller than |N|n²/(something). Q needs only O(n) rectangles, so no argument of the type "each word lies in a large rectangle ⊆ L" can refute CF-ness. For odd n the cover has only 8 pieces.

In particular, the specific plan "choose n = primorial and pick primitive words whose crossings are powers" cannot work. Whatever F is chosen, one of the ≤ 12(1+|Σ|⌈n/3⌉) explicit rectangles contains a 1/O(n) fraction of it. With many prime divisors the mechanism is Fine–Wilf: one window of length 2n/3 certifies all periods ≤ n/3 at once. Only n/2 ever needs a crossing certificate, and that costs one position plus one letter.

**Theorem 2′ (seam variant; yields unconstrained).** Same E, M1, M2, λ, s. Assume also 2λ − n ≥ M1, which holds for all n ≥ 8. Use the starts T = {n−λ, n−λ+s, …} ∪ {0}, so every window contains the seam (n−1, 0). Then the same A/B families still cover Q_n exactly.
*Proof.* Run the chain argument along the path of windows. All least periods equal d, and the union V = w[n−λ..n−1]·w[0..λ−1] (length 2λ) has period d. Since 2λ − n ≥ d, every cyclic pair (i, i+d) occurs inside V. ∎
Now the yield side of each rectangle is the linear interval J̄_t of length ⌈n/3⌉. It is completely free (type A) or has one fixed letter (type B). So for any k, nested "k-level boxes" also give an O(n) cover. Here a k-level box is a product over the shells of nested balanced intervals I_1 ⊋ ⋯ ⊋ I_k. A grammar gives ≤ (|N|n²)^k such boxes: nest the balanced nodes and use the relative contexts {(x′,z′): A ⇒* x′Bz′}. Taking the certificate on the outermost shell and leaving the inner shells free shows that **multi-level box arguments are dead too**. A proof must use the fact that the *context* set (the outer shell) is itself generated along a root-to-node path by nonterminals of the same small grammar.

**Theorem 4 (every middle length; interchange).** Let n ≥ 16 and m ∈ [1,n]. Some ℓ ∈ (m/2, m] has ℓ ≤ 3n/8 or ℓ ≥ 5n/8, or ℓ = n. Put the windows on the long side L = max(ℓ, n−ℓ) ≥ 5n/8; then s ≥ L − 7n/12 + 1 > n/24. The construction of Theorem 2 gives Q_n as a union of ≤ 24(1+|Σ|·3n/8) rectangles whose middle interval has length ℓ. Hence for every R ⊆ Q_n there is Z ⊆ R with |Z| ≥ |R|/(24(1+|Σ|n)) and freely interchangeable middles inside Q. The Ogden–Ross–Winklmann interchange lemma asks only for |R|/(c n²), so it cannot refute Q. (This agrees with Route B, Theorem 1.)

## 4. Computations (exhaustive)

All scripts are in `G_sizebounds_code/`.

- `cover_verify.py` (binary, n = 2…24) and `verify_general.py` (binary n ≤ 20 and ternary n ≤ 12, cyclic and linear versions): the union of the A/B pieces equals Q_n exactly, with soundness and completeness both True in every case. Sample counts: n=24 has 8 windows and 136 rectangles; n=21 has 5 rectangles; for prime n there are 2 rectangles.
- `seam.py`: Theorem 2′ verified for binary 5 ≤ n ≤ 20 and ternary 5 ≤ n ≤ 11.
- `anylen.py`: Theorem 4 verified for n = 16…20 and every long-side length L ∈ [⌈5n/8⌉, n−1].
- `sabotage.py` (control): shrinking λ eventually breaks completeness (n=20, λ=6: 220 primitive words uncovered, e.g. 10101010101010010100). So the check is not vacuous. The Fine–Wilf threshold is sufficient, not necessary.
- `fooled_pairs.py`: for 5 ≤ n ≤ 10 there is **no** pair of distinct primitive words that is fooled at every balanced interval, so the maximum fooling set has size 1. For n = 4 there are 22 such pairs, a small-n artefact. Randomized greedy search (`greedy_fool.py`, n ≤ 16) also never finds a fooling set larger than 1.
- `fooling.py`: for natural candidate sets, the exact maximum number of elements inside one balanced Q-rectangle (max clique over all intervals):

| n | family | \|F\| | max in one rectangle |
|---|---|---|---|
| 12 | near-squares u·flip_j(u) | 18 | 16 |
| 12 | near-p-th powers (all p\|n) | 12 | 11 |
| 18, 24, 30 | near-squares | 27, 36, 45 | all |
| 18, 24, 30 | near-p-th powers | 12, 12, 18 | all |
| 30 | random primitive | 40 | 40 |
| 12 | 2-sparse / 3-sparse | 45 | 31 / 39 |

## 5. What remains of the slice route

**Theorem 3 (exact linear reduction to cores).** Let L(ℓ,E′) = {y ∈ Σ^ℓ : y has no period in E′}. Use non-wrapping windows [t, t+λ) with t ∈ T ⊆ [0, n−λ], 0 ∈ T and n−λ ∈ T, gaps ≤ s, and λ − s ≥ max(M1+M2−1, M1). Then:
- n odd: Q_n = ⋃_{t∈T} Σ^t · L(λ,D) · Σ^{n−λ−t};
- n even: add the terms "window avoids E, with w_i = a, w_{i±n/2} ≠ a" for one endpoint inside the window.

The same lemma with E′ ⊆ [1,ℓ) gives L(ℓ,E′) = ⋃_t Σ^t L(λ′,E′) Σ^{ℓ−λ′−t} whenever λ′ − s ≥ M1+M2−1. (Checked exhaustively in `verify_general.py`, linear mode.) Hence μ(Q_n) ≤ O(n)·(1+|Σ|n) + μ(cores), where μ is the CNF grammar size. The recursion stops at the **cores** L(ℓ*, E′) with ℓ* ≈ M1+M2 (for odd n with 15 | n, ℓ* ≈ 8n/15). At a core, the largest period M1 > ℓ*/2 has to be handled by a mismatch pair (i, i+M1). The next window would need length ≥ M2+M3, but the gap between the pair's endpoints is only M1−1. For consecutive primes p_j < p_{j+1} < p_{j+2} < 2p_j (Bertrand), 1/p_{j+1} + 1/p_{j+2} > 1/p_j, so the window always just fails to fit and must contain an endpoint (a "mark"). Marks can pile up over the ω(n) levels, giving n^{O(ω(n))} again.

**Prop. 5 (quasi-polynomial upper bound).** Q_n has an NFA, and hence a right-linear CFG, with ≤ (n+1)·∏_{p|n}(2+|Σ|n/p) = n^{O(ω(n))} states. For each prime p, the state tracks "not yet guessed", "done", or "pending (letter, countdown)". So the minimal grammar size satisfies c·n ≤ μ(Q_n) ≤ 2^{O(log²n / log log n)}. A refutation needs μ(Q_n) = ω(n) nonterminals for infinitely many n, which must be n with at least 2 distinct prime divisors.

**Laminar witnesses fail (data).** If every primitive w had one mismatch pair per prime with the pairs forming a laminar family, Q_n would have CFGs of size poly(n)·2^{ω(n)}. This fails already for 2 primes: n=6 has 2 bad words (e.g. 001011), n=12 has 20 and n=18 has 144. It holds for all words when n ∈ {10, 14, 15, 20, 21} (`laminar.py`).

**Missing lemma (theorem strength).** One of the following is needed:
- (lower bound) a CFG-size technique for finite languages that goes beyond rectangle covers. It would have to use the fact that context sets are path-generated, and show μ(Q_n) = ω(n);
- (killing the route) a "mark-discharge" lemma: in the core recursion, windows avoiding E′ can always be chosen so that O(1) marks are active at a time. This would give μ(Q_n) = n^{O(1)}. It would still not kill the route formally unless the exponent is ≤ 2 (in rules), but it would make a fine-grained lower bound implausible.

Neither is known. I could neither prove nor refute the mark-discharge lemma.

## 6. Part 2: finite intersections of CFLs

Let N = Σ⁺ \ Q and Pow_p = {u^p : u ∈ Σ*}.

**Prop. 6 (reformulation).** Q = L_1 ∩ ⋯ ∩ L_k with every L_j CF ⟺ N ∪ {ε} = N_1 ∪ ⋯ ∪ N_k with every Σ*\N_j CF. (Take N_j = Σ* \ L_j; then N_j ⊆ N ∪ {ε}.) For k = 1 this is exactly "Q is CF". So proving that Q is not a finite intersection is **at least as hard** as the main problem.

**Prop. 7.** Suppose some CF language L ⊇ Q satisfies L ∩ N ⊆ ⋃_{p∈F} Pow_p for a finite set F of primes. Then Q = L ∩ ⋂_{p∈F} NP_p, where NP_p = Σ* \ Pow_p is CF, so Q is a finite intersection of CFLs.
*Proof.* "⊇" holds because Q ⊆ L and Q ⊆ NP_p. For "⊆": a non-primitive word in L is a p-th power for some p ∈ F, so it is not in NP_p. Also ε ∈ Pow_p. ∎
Contrapositive: if Q is not a finite intersection, then every CF superset of Q contains u^m (u primitive) with arbitrarily large least prime factor of m.

Trivial part: Q is never a finite intersection of the NP_p alone, since u^p (u primitive) lies in NP_q for every q ≠ p. So in any decomposition, some L_j must exclude parts of Pow_p for infinitely many primes p. Pigeonhole: for every pair (p,m), some j omits ≥ 1/k of {u^p : u ∈ Q_m}.

**Density lemma (sufficient, open, at least as strong as non-CF).** *For every CF L ⊇ Q: sup_m |{u ∈ Q_m : u^p ∉ L}| / |Q_m| → 0 as p → ∞.* This implies that Q is not a finite intersection, by the pigeonhole above.

**Obstruction.** Each L_j ⊇ Q_n inherits the O(n) rectangle cover of Q_n. So any one-level or box-type argument fails for intersections as well, because it would already fail for k = 1. The bounded-language and semilinear method of Liu–Weiner is listed as a dead end (Q ∩ w_1*⋯w_k* has a thin complement and looks CF). I found no technique specific to intersections that avoids these barriers.

## 7. Cross-check of Route B's barrier, and which size measures survive

### 7.1 Verification of B's single-window barrier: correct
Claim: for n ≥ 2, any R ⊆ Q_n and any window (a, ℓ), some Z ⊆ R with |Z| ≥ |R|/(e(ω(n)+1)) has all cross-swaps in Q.

- **Bad completions are few.** Suppose ℓ ≤ n/2. Then the context arc has length ≥ n/2 ≥ n/p for every prime p | n. A completion that is n/p-periodic is determined by any n/p consecutive letters, so by the context. Hence each context c has a set B(c) of at most ω(n) "bad" middles. If ℓ > n/2, the middle has length > n/2 and the same argument shows each middle has at most ω(n) bad contexts. ✓
- **Random rectangle.** Put each middle into S independently with probability α = 1/(ω+1). Let C = {c : B(c) ∩ S = ∅}. Then C × S ⊆ Q. For (c, y) ∈ R we have y ∉ B(c), so the two events are independent and Pr[(c, y) ∈ C × S] ≥ α(1−α)^ω ≥ 1/(e(ω+1)). Take the expectation and fix a good outcome. ✓
- **Cover per cut.** Take K = ⌈e(ω+1)·n ln|Σ|⌉ + 1 independent copies. One fixed entry is missed with probability < |Σ|^{−n}. A union bound over the ≤ |Σ|ⁿ entries then shows that some K rectangles cover Q_n at that cut. ✓

So B's Theorem 1 and Cor. 2 hold. They are consistent with, and complementary to, my Theorem 2:
- B works at **every** cut and uses O(ω n log|Σ|) rectangles per cut.
- Mine uses **O(1) cuts** and O(|Σ| n) rectangles in total. It is deterministic and an exact union, and odd n needs only 8 rectangles.

I did not re-derive B's (8m)^{ω(n)} multi-cut bound line by line. For the nested case it is superseded by Theorem 2′, which gives O(n) nested boxes of any depth with no ω-exponent. B's bound also covers non-nested multi-window structures, and those I did not treat.

### 7.2 Measures that share nonterminals across lengths: the one-level versions also die
A fixed grammar adds one constraint that slice covers ignore. The yield set Y_{A,ℓ} is **shared by all positions i and all total lengths n**, so each length ℓ has only |N| = O(1) yield sets available. Contexts remain free, since they depend on (A, i, n). Natural measure: cover Q_n by balanced rectangles whose yield sets come from a fixed finite family per length, independent of n.

- **Odd n (proved).** Theorem 2′ uses the single yield set Σ^{⌈n/3⌉}; the context arc carries the whole certificate. So one yield set per length, namely the yield language Σ*, suffices for every odd n.
- **Even n (verified for 6 ≤ n ≤ 20, binary, `shared_yield.py`).** Q_n is exactly covered using only the yield sets Σ^ℓ, {first letter = a} and {last letter = a}, i.e. 1 + 2|Σ| sets per length. The yield languages are Σ*, aΣ* and Σ*a, all fixed regular languages independent of n. Type A: the context arc has no period in D. Type B: the context arc has no period in E, and the first or last letter of the yield differs from its antipode, which lies in the context. Soundness is proved. Completeness is computational only. The proof gap: an E-avoiding arc must end next to a mismatch endpoint. I have not proved this for all even n, and it is open.

So "nonterminals shared across lengths", used at one level, gives nothing. This is proved for odd n and holds computationally for even n ≤ 20.

### 7.3 What survives
The certificate always ends up in a *context* set or a *window* set of the form "no period in D_n". That set changes with n. A fixed grammar must build it from sub-yields of its own nonterminals, and those sub-yields **are** shared across all n. Only two kinds of argument can still have force:

- **Fully recursive size measures.** These use the fact that the long certificate arc is the concatenation of sibling yields along a root-to-node path, each of which is again a yield of the same |N| nonterminals. The required statement amounts to a lower bound on the CFG complexity of the core period-avoidance languages L(ℓ, E), and it must hold uniformly over lengths, so it combines the recursion with cross-length sharing. No such technique for ambiguous CFGs is known. Proving it is essentially the original problem, so this is of theorem strength.
- **Cross-length (pumping-type) information.** This is Route B's other branch (Bader–Moura). It is not a size measure.

No per-length measure that ignores the recursive structure of contexts survives.
