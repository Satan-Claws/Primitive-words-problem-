# Round 4 report of agent "cl1": CL1 is FALSE (explicit CF certificate)

**Claim status: no proof of either resolution.** I REFUTE the candidate lemma CL1 from `periodic.md`. I give
an explicit linear CFG L with F_ins ⊆ L ⊆ Q, and a proof that L ⊆ Q. Scripts are in
`context-free/round4/scripts/cl1/` (`refute.py`, `general.py`; each runs in under 10 s on one core).

Notation as in periodic.md. For w ∈ (a*b)^+ the block vector is x = β(w) = (x_1,…,x_k), indexed
cyclically mod k. **Fact B (periodic.md, PROVED):** w is non-primitive iff x = σ_d x for some 0 < d < k.

## 1. The certificate

P = { p ∈ (a*b)^* : β(p) is a palindrome, i.e. β(p)_i = β(p)_{k+1-i} } (ε ∈ P),  **L = a·P**.

Grammar (linear): T → a S;  S → N b | A b | ε;  N → a N a | b S;  A → a A | ε.
S generates exactly P: N b yields a^n b S a^n b (the outer blocks have equal length), and A b is the
middle block of odd length. COMPUTER-CHECKED: L(T) equals the condition-defined L for all lengths ≤ 16
(`refute.py`, exhaustive over Σ^n).

**F_ins ⊆ L (PROVED).** a(a^m b)^k = a·p with β(p) = (m,…,m), which is a palindrome.

**Theorem 1 (PROVED). L ⊆ Q.**
*Proof.* The word `a` is primitive. Otherwise w = a·p with p ∈ P nonempty, so w ∈ (a*b)^+ and
x = β(w) = z + e_1, where z = β(p) is a palindrome of length k ≥ 1. If k = 1, then w = a^{z_1+1}b is primitive.
Let k ≥ 2 and let R be the reflection (Rv)_i = v_{k+1-i}. Then Rz = z and Re_1 = e_k, so x − Rx = e_1 − e_k ≠ 0.
Suppose w is non-primitive. By Fact B, σ_d x = x with 0 < d < k. Since R σ_d = σ_{−d} R, Rx is also σ_d-invariant,
and so is D = x − Rx = e_1 − e_k. A σ_d-invariant vector is constant on the orbit {1, 1+d, 1+2d, …}, which has
size k/gcd(k,d) ≥ 2. So D takes the value D_1 = 1 at some position other than 1. But D has value +1 only at
position 1. Contradiction. ∎

COMPUTER-CHECKED (`refute.py`):
- all 4094 words of L of length ≤ 22 are primitive;
- all their conjugates are primitive up to length 16;
- all 132 members of F_ins of length ≤ 60 lie in L.

**Corollary (PROVED, using LITERATURE: CFLs are closed under cyclic shift, Hopcroft–Ullman Ex. 6.4).**
Cyc(L) is CF, and Cyc(L) ⊆ Q because Q is closed under conjugation. It contains every word obtained by inserting one
a anywhere in (a^m b)^k. So the "inserted a at any block" variant of CL1 is also false.

## 2. Generalisation and what survives

**Theorem 2 (PROVED, same argument).** Let L_gen = { w ∈ (a*b)^+ : ∃ j with x_j ≥ 1, j ≠ k+1−j, and x − e_j a
palindrome }. Then:
- L_gen is linear CF: use the block-palindrome grammar with a one-bit flag "extra a emitted in a non-central block".
- L_gen ⊆ Q, because x − Rx = e_j − e_{k+1−j} cannot be periodic.
- COMPUTER-CHECKED: all 16388 words of L_gen of length ≤ 20 are primitive (`general.py`).

Cyc(L_gen) is CF and lies in Q. It contains every one-a insertion into u^k (any block, any position) whenever β(u)^k is
reflection-symmetric up to rotation. In particular this holds for every u with at most 2 blocks, and for every u whose
block vector is a cyclic block-palindrome. To use such a u at the central block, use a rotation: every reflection
symmetry R of β(u)^k composed with rotation by |u|_b is again a symmetry and moves the insertion block.

**Lesson (IDEA, but the mechanism is proved above):** a near-power family is useless as a CL1-type witness if the
base power has a reflection symmetry that moves the perturbation. The CFG checks "x − Rx = fixed small
antisymmetric vector", and that is never periodic. A surviving family must use **chiral** bases: β(u) is not a
rotation of its reversal (e.g. β(u) = (1,2,3)). Then β(u)^k − Rβ(u)^k is a large periodic vector, and the condition
"x − Rx = e_j − e_{Rj}" no longer applies.

**CL2 (CONJECTURED, untested against clever certificates).** Every CFL containing
F_chi = { a·(a^m b a^{m+1} b a^{m+3} b)^k : m ≥ 1, k ≥ 2 } contains a non-primitive word.
Caveat: I have not attacked CL2 seriously. Boundary-local block comparisons fail on it, because a periodic vector with
large period can match any finite set of boundary constraints. Parikh-type certificates fail as in Bar2, since
gcd(|w|_a, |w|_b) = gcd(k(3m+4)+1, 3k) is 3 when k ≡ 2 (mod 3). Neither of these is a proof.

## Registry entry
1. **Aimed at:** refute or prove CL1 (every CFL ⊇ F_ins = {a(a^m b)^k} contains a non-primitive word).
2. **Proved:** CL1 is FALSE. L = a·{block-palindromes} is a linear CFL with F_ins ⊆ L ⊆ Q (Theorem 1). Also:
   - Cyc(L) ⊆ Q covers insertion of a at any position;
   - L_gen (Theorem 2) covers one-a insertions into all reflection-symmetric powers.
3. **Missing step (for the route):** a near-power family with no reflection-type certificate, e.g. CL2 for chiral
   bases. This is a precise conjecture, unproved.
4. **Counterexamples found:** CL1 itself (Theorem 1), and the "any block" variant (Corollary).
5. **Strength:** CL1 was stronger than "Q not CF" and is now dead. CL2 is also stronger than "Q not CF"
   (it implies it).
6. **What would reopen the route:** a family whose base powers are chiral, together with a proof that every CF
   certificate must compare ≥ 2 full periods (copy-type information). Alternatively, a CF certificate for chiral
   families too, which would be evidence for the positive side.

---

# CL2 (second task): CL2 is also FALSE. General theorem and a new obstruction class

Scripts: `scripts/cl1/cl2.py` and `scripts/cl1/cl2_extra.py`. Each runs in under 10 s on one core.

Notation:
- σ_d is the cyclic shift, (σ_d f)_i = f_{i+d}, with indices mod K.
- R is the linear reversal, (Rf)_i = f_{K+1−i}.
- Rσ_d = σ_{−d}R, so if x is σ_d-invariant then so is D := x − Rx.

## 1. Certificate for every one-parameter base

Fix ℓ ≥ 2 and c0 ∈ Z^ℓ. Let F(c0) = { a·(a^{m+c0[0]} b ⋯ a^{m+c0[ℓ−1]} b)^k : k ≥ 2, m ≥ −min c0 }.
CL2 is the case c0 = (0,1,3).
For w ∈ (a*b)^+ with block vector x of length K, define

  **L(c0) = { w : K ≡ 0 (mod ℓ), K ≥ 2ℓ, x − Rx = T }**, where
  T_i = c0[(i−1) mod ℓ] − c0[(−i) mod ℓ] + [i=1] − [i=K].

**Membership (PROVED).** For w ∈ F(c0), x = (m·1 + c0)^k + e_1. Write c = m·1 + c0.
- The m·1 parts cancel in c^k − R(c^k), leaving the ℓ-periodic vector v_i = c0[(i−1) mod ℓ] − c0[(−i) mod ℓ].
  This uses ℓ | K.
- e_1 − Re_1 = e_1 − e_K.
So x − Rx = T.

**CF (PROVED; grammar COMPUTER-CHECKED).** L(c0) is generated by a linear grammar. The pair (i, K+1−i) is emitted as
a^P b ⋯ a^{P−T_i} b, and T_i is a bounded constant. The nonterminals carry three finite pieces of data:
- (number of pairs emitted) mod ℓ;
- a flag for i = 1;
- the number of pairs, capped at ℓ.
At the stop, the grammar checks that 2p or 2p+1 is ≡ 0 (mod ℓ) and that p ≥ ℓ. A middle block is automatically consistent.
`cl2.py` builds this grammar and checks it equals the condition-defined language, exhaustively over Σ^n, for:
- n ≤ 14 for c0 = (0,1,3);
- n ≤ 12 for (0,1), (0,0,1), (0,2,1,5), (1,0,0,2), (0,1,3,2,0).

**Theorem 3 (PROVED). L(c0) ⊆ Q.**
*Proof.* Let w ∈ L(c0), so K = ℓk with k ≥ 2. Suppose w is non-primitive. By Fact B, σ_d x = x for some 0 < d < K, so
D = x − Rx = T is σ_d-invariant. Write T = v + g with v ℓ-periodic and g = e_1 − e_K. Let E := T − σ_ℓT = g − σ_ℓ g.
Then E = e_1 + e_{K−ℓ} − e_K − e_{K+1−ℓ}. These four indices are distinct because 2 ≤ ℓ ≤ K−2. E is σ_d-invariant
because shifts commute.
- The set {i : E_i = +1} = {1, K−ℓ} is a nonempty union of σ_d-orbits. Every orbit has size K/gcd(K,d) ≥ 2, so this
  set is one orbit of size 2. Then σ_d is the shift by K/2, and K−ℓ−1 ≡ K/2 (mod K).
- In the same way, {K, K+1−ℓ} gives 1−ℓ ≡ K/2 (mod K).
Subtracting the two congruences gives K−2 ≡ 0 (mod K), which is impossible because K ≥ 4. ∎

The proof only uses that v is ℓ-periodic, never that it is bounded. Boundedness is needed only for CF-ness.

COMPUTER-CHECKED for c0 = (0,1,3):
- all 1230 words of L(c0) of length ≤ 30 are primitive;
- all 21 members of F_chi of length ≤ 60 are in L(c0).
For the other five c0 listed above, all words of length ≤ 18 are primitive.
Control: without the e_1 − e_K term the language contains the power bbaaab·bbaaab, so the check detects powers.

**So CL2 is false.** Cyc(L(0,1,3)) is CF, lies in Q, and contains F_chi together with all its conjugates.

**Corollary (PROVED).** The same holds for any fixed rotation of the insertion point. Inserting the a at block j of u^k
gives a conjugate of a·(u′)^k with u′ a rotation of u. Take the finite union over the ℓ rotations c0′ of c0 and then
Cyc. More parameters also work: c = c0 + Σ_j m_j s_j, provided each direction s_j satisfies
s_j[(i−1) mod ℓ] = s_j[(−i) mod ℓ], i.e. R fixes s_j^k. Then v is still m-independent. With Cyc, any reflection
axis common to all s_j can be used.

**Chirality was a red herring.** CL2's base (0,1,3) is chiral, but the only parameter direction is 1, which every
reflection fixes. **The correct invariant is the set of parameter directions, not the base vector.**

## 2. A family that defeats every bounded-offset reflection certificate

**Certificate class 𝓡 (precise).** 𝓡 is the set of finite unions of languages Cyc(L′) with
L′ ⊆ { w ∈ (a*b)^+ : x − Rx ∈ 𝒯_K for its K }, where each 𝒯_K is a set of vectors with entries bounded in absolute
value by a constant B that does not depend on K. 𝓡 contains every certificate in this report: L, L_gen, Cyc(L(c0)),
and their rotation unions.

**F_2 = { a·(a^p b a^q b a b)^k : p, q ≥ 1, k ≥ 2 }.** Its block vector is x = (p,q,1)^k + e_1.
- **Members are primitive (PROVED):** the Theorem 3 argument with ℓ = 3 and v = (p,q,1)^k − R(p,q,1)^k, which is
  3-periodic though unbounded.
- **Theorem 4 (PROVED). No language in 𝓡 contains F_2.**
  *Proof.* Fix B. Take w ∈ F_2 with p, q, 1 pairwise differing by more than B+1, and k ≥ 2.
  - Rotating and then applying R amounts to a reflection i ↦ s−i of Z_K. Since 3 | K, it permutes the residue
    classes mod 3. It fixes one class and swaps the other two.
  - The swapped classes carry two different values among p, q, 1, which differ by more than B+1. They contain at least
    k ≥ 2 pairs, and at most two blocks are touched by the e_1 perturbation.
  - So some entry of x′ − Rx′ has absolute value > B, for every rotation x′ of x.
  - Hence w lies in no member of the finite union once B exceeds all the bounds involved. ∎
- **Parikh certificates fail trivially (PROVED).** ψ(a(a^p b a^q b a b)^k) = (k(p+q+1)+1, 3k).
  For p = 2, q = 1, k = 2 the word a(aab ab ab)^2 has Parikh vector (9, 6), with gcd 3.
  So any ψ^{-1}(S) ⊇ F_2 contains the power (aaabb)^3.

**CL3 (CONJECTURED).** Every CFL containing F_2 contains a non-primitive word.
- CL3 implies "Q not CF".
- What I tried and failed to make CF:
  - "x − Rx constant on each swapped residue class": this is a copy-type constraint, needing an unbounded difference
    at every pair.
  - Coupling (1, K) with (4, K−3), "x_1 − x_K = x_4 − x_{K−3} + 1": the a-excess matches cross the pair (2, K−1).
  - Sign-only conditions (x_i ≥ x_{K+1−i}): these are CF, but periodic palindromic-type vectors satisfy them.
- Nothing here is a proof that these attempts are impossible.

## Registry entry (CL2)
1. **Aimed at:** refute CL2, and characterise which near-power families have a CF certificate.
2. **Proved:**
   - CL2 is false, via Theorem 3: L(c0) ⊆ Q is CF for every one-parameter base c0, and it contains a·(m·1+c0)^k.
   - The same holds for any insertion block, and for multi-parameter bases whose directions share a reflection axis.
   - Theorem 4: F_2 escapes the whole class 𝓡 of bounded-offset reflection certificates, and Parikh certificates.
3. **Missing step:** CL3, that every CFL ⊇ F_2 contains a non-primitive word. Even a proof that F_2 escapes all
   "nested-linear" certificates (linear grammars with finite control comparing paired blocks with unbounded
   offsets) is open.
4. **Counterexamples found:** CL2 (Theorem 3), plus every one-parameter near-power insertion family.
5. **Strength:** CL3 is stronger than "Q not CF".
6. **What would reopen the route:** a CF certificate for F_2 (for example one exploiting the fixed '1' blocks as
   markers), which would kill CL3. Or a proof that any CFG covering F_2 must transport an unbounded offset across
   crossing pairs.

---

# CL3 (third task): CL3 is FALSE. Every fixed-period-length insertion family has a CF certificate

Scripts: `scripts/cl1/cl3.py` (runs in 17 s), `scripts/cl1/dom.py`, `scripts/cl1/cl4_probe.py`.
Indices are 0-based and taken mod K, where K is the number of blocks. Block vector x; σ_d is the cyclic shift.

## 1. Certificate L_ℓ (outside class 𝓡: it uses unbounded sign constraints)

Fix ℓ ≥ 1. Choose the reflection R of Z_K and the classes f, g as follows:
- ℓ odd: R(i) = K−1−i, which fixes the residue class f = (ℓ−1)/2 (mod ℓ).
- ℓ even: R(i) = K−2−i. This pairs the first K−1 blocks in reverse order and leaves the last block fixed. It fixes the
  classes f = ℓ/2−1 and g = ℓ−1.

Let D = x − Rx. **C_ℓ(x)** holds iff all of the following hold:
1. K ≡ 0 (mod ℓ) and K ≥ 2ℓ.
2. On class f: D_i = [i = f] − [i = R(f)] exactly (the perturbed class).
3. On class g, if ℓ is even: D_i = 0.
4. On every other class A: D is single-signed on A. Such classes are swapped in pairs A ↔ B by R, and D_B = −D_A∘R,
   so this is a finite union over 2^{⌊(ℓ−1)/2⌋} sign patterns, each of the form "D ≥ 0 on A".

L_ℓ = { w ∈ (a*b)^+ : C_ℓ(β(w)) }.

**CF (PROVED).** Each sign pattern is a linear grammar that emits the pair (i, R(i)) as a^P b ⋯ a^Q b, with one of:
- P − Q fixed (classes f and g);
- P ≥ Q or P ≤ Q (swapped classes).
The finite control holds three pieces of data:
- i mod ℓ, which also gives the class of R(i), since ℓ | K;
- a flag for i = f;
- a pair counter capped at ℓ.
For ℓ even there is one extra free last block. ℓ = 1 is exactly the CL1 certificate.

**Theorem 5 (PROVED). L_ℓ ⊆ Q.**
*Proof.* Let x satisfy C_ℓ and suppose σ_d x = x with 0 < d < K. Since Rσ_d = σ_{−d}R, D is σ_d-invariant, so
D_{f+d} = D_f = 1 and D_{R(f)+d} = D_{R(f)} = −1. Also R(f) ≡ f (mod ℓ) and R(f) ≠ f because K ≥ 2ℓ.
- If ℓ | d: f+d ≠ f lies in class f, where D takes the value +1 only at f. Contradiction.
- If ℓ ∤ d: f+d and R(f)+d are two positions of the class f+d ≠ f, carrying +1 and −1. That class is either g, where
  D ≡ 0, or a single-signed class. Contradiction. ∎

**Theorem 6 (PROVED). Coverage.** Let I_ℓ be the set of words obtained by inserting one letter a anywhere into u^k,
with |u|_b = ℓ and k ≥ 2. Then I_ℓ ⊆ Cyc(L_ℓ).
*Proof.* Such a word is a conjugate of a word with block vector x = c^k + e_f, where c ∈ N^ℓ: rotate the base and
put the inserted a's block at position f. Then D is as follows:
- on class f, D = e_f − e_{R(f)}, since R preserves class f and the c-parts cancel;
- on g, D = 0;
- on a swapped class A ↔ B, D is the constant c_A − c_B, which is single-signed. ∎

So **CL3 is false**: F_2 ⊆ I_3. The 3-parameter family F_3 = {a(a^p b a^q b a^r b)^k} is covered too. The mechanism:
- the exact constraint on the perturbed class kills every period with ℓ | d;
- the sign constraints on the other classes kill the periods with ℓ ∤ d. Those shifts carry the ±1 pair into a
  single-signed class.

This is builder.md's "translation ∘ reflection" idea, applied per residue class.

COMPUTER-CHECKED (`cl3.py`):
- C_ℓ-words are primitive, exhaustively over all words of length ≤ 20 (≤ 21 for ℓ = 3), for ℓ = 1..6. The counts are
  2026, 3370, 37470, 19921, 20688 and 15895 words.
- Coverage: all single-a insertions into c^k for c ∈ {0..3}^ℓ (ℓ ≤ 5) and k ∈ {2, 3} are covered, plus 3000 random
  instances for each ℓ ≤ 7.
- F_3 with p, q < 10, r < 6, k < 6 is covered.

Also (PROVED, by symmetry a ↔ b): inserting one b into u^k with |u|_a = ℓ fixed is covered.

## 2. What the next family must avoid: unbounded blocks per period

By Theorem 6, a witness family made of single-a insertions into powers must have unbounded |u|_b. Builder's
letter-level dominance certificate does not fill the gap. Probe (`cl4_probe.py`): for a·u·u with u random with 7–10
blocks, dominance misses 200/200, and dominance together with L_1..L_4 misses 170–200 of 200.

**J = { a·u·u : u ∈ (a*b)^+ }**, equivalently via Cyc { u a u }.
- Members are primitive: they lie in I_{|u|_b} ⊆ Cyc(L_{|u|_b}).
- J ⊆ ⋃_ℓ Cyc(L_ℓ) ⊆ Q, but that union is infinite.

**Proposition 7 (PROVED).** For every ℓ0, J ⊄ ⋃_{ℓ ≤ ℓ0} Cyc(L_ℓ). Explicitly, a·u·u is not covered when u has
ℓ′ > 4ℓ0 blocks of pairwise distinct lengths.
*Proof.* Suppose a rotation of x = β(a u u) satisfies C_ℓ, with ℓ ≤ ℓ0 and reflection R′ (K = 2ℓ′).
- Class f has K/ℓ = 2ℓ′/ℓ > 8 positions. All but at most 4 of them avoid the two perturbed positions j and R′j and the
  two exact ±1 positions.
- At every other position i of class f the exact condition gives D_i = 0, i.e. c_{i mod ℓ′} = c_{R′i mod ℓ′}.
- Because the lengths are distinct, this forces i ≡ R′i (mod ℓ′), i.e. 2i ≡ s (mod ℓ′) for R′(i) = s − i. That has
  ≤ 2 solutions mod ℓ′, so ≤ 4 positions in Z_K.
- Hence 2ℓ′/ℓ ≤ 8, contradicting ℓ′ > 4ℓ0. ∎

**CL4 (CONJECTURED).** Every CFL containing J = {a·u·u : u ∈ (a*b)^+} contains a non-primitive word.
- CL4 implies "Q not CF".
- J is a "near-square" family. Any certificate must break the period |u| using one inserted letter, at an unbounded
  distance |u| from its copy.
- The obstruction I see: every certificate above checks constraints along ONE reflection pairing. To kill the period
  K/2 with distinct block lengths it would need to compare pair depth j with pair depth K/2−1−j (antipodal pairs).
  That is a second matching, crossing the first.
- I did not turn this into a theorem. The "finite-state labelled single-reflection certificate" class needs a precise
  definition and a proof that it cannot cover J. Proposition 7 is the special case of the families L_ℓ.

## Registry entry (CL3)
1. **Aimed at:** refute CL3 (F_2), then find the next witness family.
2. **Proved:**
   - CL3 is false.
   - Theorem 5: L_ℓ ⊆ Q is CF for each ℓ.
   - Theorem 6: every single-a insertion into u^k with |u|_b = ℓ fixed lies in Cyc(L_ℓ). The same holds for b-insertions
     with |u|_a fixed.
   - Proposition 7: J escapes every finite union of the L_ℓ.
3. **Missing step:** CL4. A weaker open target: J escapes every finite union of single-reflection certificates with
   finite-state position labels and per-pair constraints (exact bounded offset, sign, or free).
4. **Counterexamples found:** CL3, and the F_3 analogue. The parameter-direction criterion from the CL2 section was
   too pessimistic: sign constraints remove it.
5. **Strength:** CL4 is stronger than "Q not CF". The single-reflection barrier would be strictly weaker and is
   plausibly provable.
6. **What would reopen the route:** a CF certificate for J. Its idea would have to compare antipodal blocks through a
   single stack, which would be strong evidence toward Q being CF. Or a proof that any CFG containing J yields, by
   pumping inside one copy of u while the other copy is fixed, a word u′ a u′′ that is a power.
