# Report of agent "crossing": cross-length (context × yield) arguments

**Claim: no proof of either resolution.** The result is an exact reformulation and a barrier:
1. With context-free sets, the cross-length "context × yield" cover is **equivalent** to "Q is CF" (Theorem 1).
2. With arbitrary sets, an explicit cover by 18 product classes is valid at all lengths simultaneously. It covers every
   primitive word of length ≤ 19 except a thin near-periodic set U_n (Theorem 3 and its table).
3. Cross-length fooling sets for Q have size 1 for every length up to 14 (Lemma 4 and its computation).

Scripts are in `context-free/round4/scripts/crossing/`. Tags: PROVED / COMPUTER-CHECKED / LITERATURE / CONJECTURED / IDEA.
Notation: Σ = {a,b}; minper(x) = least period of x; for a piece x, mid(x) = x[⌊|x|/2⌋].
A *balanced conjugate factorization* (b.c.f.) of w (|w| = n ≥ 2) is a pair (y,m) with ym a rotation of w and
n/3 < |y| ≤ 2n/3.

---------------------------------------------------------------------------------------------------
## 1. Rotation reformulation: the generalized rectangle is a product L·M ⊆ Q

**Lemma 1 (PROVED).** Let G be a CNF grammar with nonterminals N and L(G) = Q (Q is rotation closed). For A ∈ N put
L_A = {y : A ⇒* y} and M_A = {zx : S ⇒* xAz}. Then:
- (a) L_A·M_A ⊆ Q;
- (b) every w ∈ Q with |w| ≥ 2 has a b.c.f. (y,m) with y ∈ L_A, m ∈ M_A for some A;
- (c) every M_A is CF.

*Proof.* (a) If S ⇒* xAz and A ⇒* y, then xyz ∈ Q, and yzx is a rotation of xyz, so it is also in Q.
(b) The descent of rectangles.md Lemma 1.1 gives a node with yield y, n/3 < |y| ≤ 2n/3; then w = xyz and yzx is a rotation.
(c) Grammar with start symbol ⟨S⟩:
- ⟨S⟩ → ε;
- for every rule B → CD, add ⟨C⟩ → D⟨B⟩ and ⟨D⟩ → ⟨B⟩C (C and D are the original nonterminals).

The context of C under S ⇒* xBz ⇒ xCDz is (x, y_D z), whose rotation is y_D·(zx). The context of D is (x y_C, z), whose
rotation is (zx)·y_C. Induction on the length of the path from S gives ⟨A⟩ = M_A. ∎

**Theorem 1 (PROVED, using LITERATURE: CFLs are closed under cyclic shift, Oshiba/Maslov; = devil T3).** The following are equivalent.
- (i) Q is CF.
- (ii) There are finitely many pairs of CFLs (L_i, M_i) with L_i M_i ⊆ Q such that every primitive word has a b.c.f.
  in some L_i × M_i.
- (iii) Same as (ii), without "balanced".

*Proof.* (i)⇒(ii) is Lemma 1. (ii)⇒(iii) is trivial. (iii)⇒(i): K = ⋃ L_i M_i is CF, K ⊆ Q, and K contains a conjugate of every
primitive word, so Cyc(K) = Q is CF. ∎

**Consequence.** The "context × yield across lengths" mechanism is not a weakening of the problem. With CF sets it *is*
the problem: the missing step of this route is exactly as strong as "Q not CF". Any progress must therefore come from a
lemma about the arbitrary-set relaxation, or from a lemma that uses CF-ness of the L_i, M_i in a specific way. §2–§4 show
that the arbitrary-set relaxation is almost satisfiable.

---------------------------------------------------------------------------------------------------
## 2. Cross-length safe classes (arbitrary sets)

**Lemma 2 (fractional-position mismatch; PROVED).** Let y, m be nonempty, ℓ = |y|, k = |m|, n = ℓ + k, p prime,
1 ≤ j < p. Put
- i_y = ℓ − ⌈jℓ/p⌉ (an index in [0, ℓ−1]);
- i_m = ⌊jk/p⌋ (an index in [0, k−1]).

If p | n, then the positions i_y and ℓ + i_m of ym are at distance exactly jn/p.

*Proof.* The distance is ⌈jℓ/p⌉ + ⌊jk/p⌋. Write jℓ/p = A + f with 0 ≤ f < 1. Since jℓ/p + jk/p = jn/p ∈ ℤ,
jk/p = B + (1 − f) if f > 0 (then the sum is A + 1 + B), and jk/p = B if f = 0. Either way the sum is jn/p. ∎

So if y[i_y] ≠ m[i_m], then ym does not have cyclic period n/p. This holds for **all** lengths ℓ, k at once. For p = 2
these positions are the two middles: the middles of y and m are always at distance n/2, whatever |y| and |m| are. This
is the coPow_2 grammar of devil T1, read as a product.

**Theorem 3 (PROVED).** Each of the following 18 classes satisfies L·M ⊆ Q, for words of all lengths.
- **Family A (8 classes).** L = {y : minper(y) > |y|/2, y[i_y(2,1)] = c₂, y[i_y(3,j)] = c₃},
  M = {m : minper(m) > |m|/2, m[i_m(2,1)] = c₂', m[i_m(3,j)] = c₃'}.
  The parameters are j ∈ {1,2} and letters with c₂ ≠ c₂', c₃ ≠ c₃'.
- **Family B (2 classes).** L = {y : minper(y) > 2|y|/3, mid(y) = c}, M = {m : minper(m) > 2|m|/3, mid(m) = c'},
  with c ≠ c'.
- **Family G (4 classes, plus the 4 classes with the roles of L and M swapped).**
  L = {y : minper(y) > 2|y|/3, y[0] = c, mid(y) = e},
  M = {m : q := minper(m) ≤ |m|/3, m[|m| − q] = c', mid(m) = e'}, with c ≠ c', e ≠ e'.
  Here m[|m| − q] is the letter that m's own period predicts right after m.

*Proof.* Suppose ym = z^p with p ≥ 2. A non-primitive word with p ≥ 2 has cyclic period n/p for some prime p | n,
so it suffices to rule out prime p.
- **p = 2** (every family). The middle letters differ, so Lemma 2 applies with j = 1.
- **p = 3** (Family A). Lemma 2 applies with j = 3's chosen j.
- **p ≥ 3 in Family B, p ≥ 5 in Family A.** Let x be the longer piece, so |x| ≥ n/2. It is a factor of a rotation of
  z^p, so it has period n/p ≤ 2|x|/p. This contradicts minper(x) > 2|x|/3 (when p ≥ 3) and minper(x) > |x|/2 (when p ≥ 5).
- **Family G, case |z| ≤ |m| − q.** m has periods q and |z|, and q + |z| ≤ |m|. By Fine–Wilf, m has period gcd(q,|z|),
  so q | |z|. The rotation m·y of z^p has period |z|, so y[0] = (my)[|m|] = m[|m| − |z|] = m[|m| − q]. This contradicts c ≠ c'.
- **Family G, case |z| > |m| − q ≥ 2|m|/3, p ≥ 3.** Then 2|m|/3 < n/3, so |m| < |y|, and |z| ≤ n/3 < 2|y|/3.
  y is a factor of a rotation of z^p of length ≥ |z|, so minper(y) ≤ |z| < 2|y|/3. Contradiction.

The p = 2 case is already covered by the middle letters. ∎

COMPUTER-CHECKED (`fracpos.py`, `periodic.py`): no unsound pair for Families A and B with pieces of length ≤ 9, nor for
Family G with pieces of length ≤ 11.
Necessity of the middle-letter constraint in Family G (COMPUTER-CHECKED, counterexample): without it, the class is
unsound even with the extra "predicted previous letter" constraint, e.g. y = abbba, m = bbb, ym = (abbb)².

**Coverage (COMPUTER-CHECKED, `ucount.py` → `ucount_out.txt`).** U_n is the set of conjugacy classes of primitive words of
length n with no b.c.f. in any of the 18 classes.

| n | 4–9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| \|U_n\| | 2 | 4 | 6 | 8 | 8 | 4 | 8 | 24 | 14 | 36 | 16 |
| out of | 3–56 | 99 | 186 | 335 | 630 | 1161 | 2182 | 4080 | 7710 | 14532 | 27594 |

Every word in U_16 has (checked with `list16.py`; other n not checked) a cyclic factor of length ≥ 0.6n with period ≤ 1/3 of its length. Examples: a^{n−1}b, a^{n−2}bb,
(ab)^k with a defect, (aab)^k with a defect (`list16.py`).

**Conjecture R6 (CONJECTURED).** Finitely many arbitrary-set product classes L_i M_i ⊆ Q cover Q by b.c.f.'s.
For example, the 18 classes above plus finitely many classes for "periodic stretch + defect" words.
If R6 holds, then no argument that uses only the product structure (contexts × yields across all lengths, one level of
the tree) can prove the conjecture; it must use CF-ness of L_A, M_A (Theorem 1).

Partial evidence:
- the single family a^{n−1}b is covered by the class {|y|_b = 1} × a^+;
- the two-b family a^s b a^t b is covered either by Family A (centre one b in y) or by a square-free 3-colouring of
  d = j − i (pieces a^i b a^j: a period Δ on a window of length |Δ| would be a square).

**Where CF-ness bites (PROVED).** The Family A sets are not CF. Intersect L (c₂ = c₃ = b, j = 2) with a*ba*ba* ∩ (Σ⁶)*.
For ℓ = 6t the conditions force the word a^{3t} b a^{t−1} b a^{2t−1}. It satisfies minper > 3t, because the b at index 3t
has an 'a' at 3t − d for every d ≤ 3t. This gives a one-parameter family whose three a-blocks grow together, which is not
CF by the pumping lemma.

So two fractional constraints on one piece cannot both live in one CF set. This agrees with devil C2: one distance can be
tied to the length, two cannot. A grammar would have to split this information across nonterminals.

---------------------------------------------------------------------------------------------------
## 3. Cross-length fooling sets

**Lemma 4 (PROVED).** Let L be rotation closed with a CNF grammar of g nonterminals. Suppose F ⊆ L has the property that,
for all distinct w, w' ∈ F and all b.c.f.'s (y,m) of w and (y',m') of w', we have ym' ∉ L or y'm ∉ L. Then |F| ≤ g.

*Proof.* By Lemma 1, each w ∈ F has a b.c.f. in some L_A × M_A. Two words of F assigned the same A would give ym', y'm ∈ L. ∎

This is the cross-length analogue of the fooling-set method. An infinite F would prove that L is not CF.
Test against the known CF example: for E', the maximum F is 1 (as it must be).

**Computation (COMPUTER-CHECKED, `fooling.py` → `fooling_out14.txt`).** Among all conjugacy classes of primitive words of
lengths 2..14 (2536 classes, all pairs and all b.c.f.'s), **there is no fooling pair at all**. The maximum cross-length
fooling set for Q is 1 (also for N = 8, 10, 12). The same holds for E'.

**Conjecture (CONJECTURED).** Any two primitive words have b.c.f.'s with both cross products primitive. This would make
the method useless for Q, cross-length or not.

---------------------------------------------------------------------------------------------------
## 4. Why the NEQ structure does not help across lengths

**Lemma 5 (PROVED, profile principle).** Let D be an infinite set and B ⊆ D×D with B ⊇ {(s,t) : s ≠ t}, B ∩ {(s,s)} = ∅.
Then B is not a finite union of rectangles S_i × T_i ⊆ B.

*Proof.* Assign to each s the finite profile ({i : s ∈ S_i}, {i : s ∈ T_i}). Two elements s ≠ t have the same profile.
If (s,t) ∈ S_i × T_i, then t ∈ T_i, hence s ∈ T_i, so (s,s) ∈ S_i × T_i ⊆ B. Contradiction. ∎

The cross-length obstruction would need a *rigid* NEQ: an infinite family in which each word's admissible b.c.f.'s are
forced into one pair (s,t). Q never provides this, because each word has Θ(n²) b.c.f.'s:
- Lemma 2 turns the p = 2 constraint into a single letter comparison that works at all lengths;
- for the two-b family, the shift structure (d, d+Δ) can be covered with finitely many colours (square-free colouring).

Nothing in Q forces rigidity: the computation of §3 found zero fooling pairs.

---------------------------------------------------------------------------------------------------
## 5. Checks against the known barriers
- **E'** (CF, growth 2, inside Q). Lemma 4 bounds its fooling sets and the computation gives 1. Theorem 1 holds for any
  rotation-closed L (E' is rotation closed).
- **Σ^n slices.** They are finite, so the finite-cover statements are trivial for them; nothing here is single-length.
- **R1–R5 (single-length barriers).** Theorem 3 is a cross-length strengthening of them: one family of 18 classes works
  at all lengths simultaneously, rather than 2⌈n/3⌉ classes per length.

---------------------------------------------------------------------------------------------------
## Registry entry
1. **Statement aimed at.** No finite family of context × yield product classes inside Q covers Q (cross-length interchange).
2. **Strongest lemma proved.**
   - Theorem 1: with CF sets this is *equivalent* to "Q not CF".
   - Lemma 2 and Theorem 3: 18 explicit arbitrary-set classes with L·M ⊆ Q at all lengths.
   - Lemma 4: cross-length fooling bound.
   - Lemma 5: profile principle.
   - A Family A class set is not CF.
3. **Missing step.** "For every finite family of pairs of CFLs (L_i, M_i) with L_i M_i ⊆ Q, some primitive word has no
   conjugate in ⋃ L_i M_i." This is exactly Theorem 1(iii) negated.
4. **Counterexamples found.**
   - Cross-length fooling sets: max = 1 for lengths ≤ 14 (no fooling pairs).
   - The "predicted letter" class without the middle-letter constraint is unsound: (abbba)(bbb) = (abbb)².
   - The 18 classes leave only near-periodic words uncovered, ≤ 36 conjugacy classes per length up to n = 19.
5. **Strength of the missing step.** EQUAL to "Q not CF" (Theorem 1). The arbitrary-set version is (CONJECTURED R6) false,
   so it cannot serve as a strictly weaker route.
6. **What would reopen the route.**
   - A proof that R6 fails: an infinite family of near-periodic words (period q stretch + defect, for unboundedly many q)
     that no finite arbitrary-set cover handles. That would prove Q not CF outright.
   - Or a structural lemma restricting CF sets L with L·M ⊆ Q, e.g. "a CF L whose words all have minper > |y|/2 cannot
     carry two independent fractional-position constraints". The non-CF example in §2 is the seed.
