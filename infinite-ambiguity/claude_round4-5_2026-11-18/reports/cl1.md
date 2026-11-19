# Round 4 report of agent "cl1": CL1 is FALSE (explicit CF certificate)

**Claim status: no proof of either resolution.** I REFUTE the candidate lemma CL1 from `periodic.md`. I give
an explicit linear CFG L with F_ins ⊆ L ⊆ Q, and a proof that L ⊆ Q. Scripts are in
`infinite-ambiguity/claude_round4-5_2026-11-18/scripts/cl1/` (`refute.py`, `general.py`; each runs in under 10 s on one core).

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

---

# CL4 (fourth task): not refuted. Reductions, a covering certificate, and the core family

Scripts: `scripts/cl1/cl4_hs.py`, `scripts/cl1/cl4_O.py`, `scripts/cl1/cl4_O2.py` (each runs in under 3 min).
J = {a·u·u : u ∈ (a*b)^+}. Its block vector is x = c^2 + e_0, with K = 2ℓ blocks and c = β(u) ∈ N^ℓ.
**Result: I could not refute CL4, and I did not prove the single-reflection barrier.** What I have:

**P1 (PROVED). Only odd powers matter.** Every member of J has |w|_a = 2|u|_a + 1, which is odd. So for any CFL L ⊇ J,
the language L ∩ {|w|_a odd} is CF and contains J. Its non-primitive words are v^q with q odd ≥ 3, because an even
power has an even a-count. So CL4 is equivalent to: every CFL containing J contains an odd power v^q, q ≥ 3.
Equivalently, the even powers are killed by a regular condition for free.

**P2 (PROVED sound and CF; coverage partly PROVED, partly COMPUTER-CHECKED). Bounded level-set certificate.**
C_O^B = { w ∈ (a*b)^+ : for some reflection ρ(i) = c − i of Z_K and some value v with |v| ≤ V, the count
s = #{i : x_i − x_{ρ(i)} = v} satisfies 1 ≤ s ≤ B and gcd(s, K) = 1 }.
- **Sound:** this is builder2's Lemma O at block level. If w is a power, every level set of D is a union of orbits of
  size p′ > 1 with p′ | K.
- **CF:** Cyc of a finite union of linear fold grammars, covering both fold types. The finite control holds the count
  capped at B and K mod lcm(1..B).
- **Covers (PROVED):** every a·u·u with c_i − c_{−i} ≠ 1 for all i ≢ 0 (mod ℓ). Use the axis ρ(i) = −i, which maps
  0 to its antipode ℓ. Then {D = 1} = {0}, so s = 1.
- **Data:** soundness is exhaustive for all words of length ≤ 18: 244935 certified words, all primitive. C_O^7 covers
  197–200 of 200 random J members with block lengths in [0,30], [0,8], [0,2] or [1,2] and ℓ ≤ 20.
- **But it does not scale (`cl4_O2.py`).** Take c ∈ {1,2}^ℓ and allow values v ∈ {1,2,3}. When c_0 = 1, so that
  x_0 = 2 is not a unique block value, the smallest coprime level-set size over all axes grows linearly: about 7–13 at
  ℓ = 40, 19–29 at ℓ = 80, 51–63 at ℓ = 160. So no fixed B covers J.

**P3 (PROVED). Reduction to a binary core family.** Let φ be the morphism 0 ↦ ab, 1 ↦ aab, a prefix code. Then
φ(1y0y) = a·u·u with u = φ(0y) (checked in `cl4_hs.py`). φ preserves and reflects primitivity: a root of a word in
φ({0,1}^+) ⊆ (a*b)^+ ends in b, so it is a product of codewords, and φ is injective. CFLs are closed under inverse
morphism. Hence:
- **CL5 ⇒ CL4**, where **CL5:** every CFL containing T = {1y0y : y ∈ {0,1}*} contains a non-primitive word.
- Cyc(T ∪ swap(T)) = HS, the set of words at Hamming distance 1 from a square. HS ⊆ Q by periodic.md L1.
  COMPUTER-CHECKED: the 1023 members with |y| ≤ 9 are primitive.
- CL5 is at least as strong as CL4. The P2 data says T-type members (bounded blocks, c_0 = 1) are exactly the
  members of J that escape bounded certificates. So T, the Hamming-1 neighbours of squares, is the natural core.
- Builder's letter-level dominance covers 771/1023 of T for |y| ≤ 9, but 15/300 at |y| = 20 and 0/300 at |y| = 40.

**What a refutation of CL4 (or CL5) must do (IDEA, consistent with builder2's coprimality barrier).**
- By P1, it must exclude odd powers v^q with q unbounded and q | ℓ.
- On the escaping members, every single-reflection level set of bounded value has size growing linearly in ℓ.
- A single-reflection certificate with finite control can only test such sizes against K modulo fixed numbers. So it
  would need either a CF test of gcd(count, K) = 1 for unbounded counts, or a comparison of antipodal blocks
  i ↔ i + K/2. The latter is a matching that crosses the reflection matching.
- builder2's Lemma S (semilinear sets of coprime pairs are thin) suggests the first is impossible as a Parikh-type
  test. Nothing here is a theorem.

**Why the barrier proof did not close.** The natural class is: label automaton A over pair labels
(exact offset |δ| ≤ B / ≥ δ / ≤ δ / free, residues mod N), plus Cyc and finite unions. This class contains C_O^B, the
L_ℓ, the L(c0) and builder2's RGB. Two strategies failed:
- Building a power y with the same label sequence fails on the residue labels. The J residue vector
  r(z)^2 + e_j is never periodic mod N ≥ 2, by the e_j − e_{j+ℓ} argument.
- Changing labels needs a pumping loop of A that contains the perturbed pair, and pigeonhole does not guarantee one.
A proof would have to choose u so that the label language is forced into a loop around the perturbation. I conjecture
J (and T) escapes the class, but I leave it open.

## Registry entry (CL4)
1. **Aimed at:** refute CL4 (J = {a·u·u}), or prove J escapes single-reflection finite-control certificates.
2. **Proved:**
   - P1: reduction to odd powers.
   - P2: C_O^B is sound and CF, and covers all a·u·u without a mirrored ±1 coincidence.
   - P3: CL5 ⇒ CL4 via the code φ; T and HS (Hamming-1 neighbours of squares) are the core.
3. **Missing step:**
   - Negative side: CL5, or the barrier "no finite union of label-automaton reflection certificates covers T".
   - Positive side: a CF certificate covering T, which would need a coprimality-type or antipodal mechanism.
4. **Counterexamples found:** none to CL4.
   - Bounded level-set certificates cover generic J members; this is proved for the "no mirrored ±1" subfamily.
   - They fail on T-type members, with linear growth (computer data only).
5. **Strength:** CL5 ⇒ CL4 ⇒ "Q not CF". Both are stronger than the target. The barrier would be strictly weaker.
6. **What would reopen the route:**
   - A CF test certifying gcd(s, K) = 1 for an unbounded reflection count s. That would refute CL5 and be strong
     positive-side evidence.
   - A pumping argument showing that every finite-state label run on 1y0y can be re-used on some (v)^q, which would
     prove the barrier.

---

# CL5 (fifth task): not refuted. Antipodal certificates and a closure barrier

Script: `scripts/cl1/cl5.py`, which runs in under 1 min. T = {1y0y : y ∈ {0,1}*} over a binary alphabet.
Write n = |w| (even), m = n/2, and take indices mod n.

**P4 (PROVED; COMPUTER-CHECKED n ≤ 20). The antipodal mismatch kills every period dividing m, and windows
kill short odd roots.** Let

  W_N = { w : n even, w_0 ≠ w_m, and w_j = w_{m+j} for all 0 < |j| < N }.

- **T ⊆ W_N for every N:** in 1y0y every antipodal pair agrees except (0, m).
- **W_N is linear CF.** The grammar pairs position j with n−j (M → cMc′). The outer and inner windows are fixed-size
  (the first/last N−1 letters and the N−1 letters each side of the middle), so they sit in the finite control.
- **Non-primitive words of W_N** are exactly the v^q with q odd ≥ 3, |v| even and |v| ≥ 2N.
  *Proof.* Let w = v^q and d = |v|.
  - If q is even, then d | m and w_0 = w_m. Contradiction. So q is odd, d is even (since n is), and m ≡ d/2 (mod d).
  - If d/2 < N, take j = d/2: w_{d/2} = w_{m+d/2} = w_d = w_0. But w_{d/2} = w_m ≠ w_0. Contradiction.
  - Conversely, the windows can be placed in any v of even length d ≥ 2N. ∎
  - Data (`cl5.py`): for N = 1, 2, 3 the minimum root lengths are exactly 2, 4, 6.

So for each N there is a CF L_N ⊇ T whose only non-primitive words are odd powers with root length ≥ 2N. The
coordinator's remark checks out: a mismatch at one antipodal pair kills all periods dividing n/2. A bounded window
cannot reach the remaining odd powers with long roots.

**P5 (PROVED). The walk.md T-operator cannot produce the balanced core.** T(M) ⊆ {Δ ≠ 0}, where Δ = |w|_1 − |w|_0.
But Δ(1y0y) = 2Δ(y), so T_0 = {1y0y : |y|_0 = |y|_1} is infinite and disjoint from every T(M). Also, T-words never have
Δ = ±1, so they are disjoint from the certificate T(E′). At most T ∖ T_0 could come from a T-operator image.

**Theorem 9 (PROVED). Barrier for antipodal-window + count certificates.**
Let 𝓦 be the class of languages of the form
  { w : n even, ∃p: (n mod M, |w|_1 mod M, w[p−N..p+N], w[p+m−N..p+m+N]) ∈ Rel },
for N, M ≥ 1 and any finite relation Rel. The windows are cyclic, and 𝓦 is closed under finite unions. Then:
- every L ∈ 𝓦 is closed under w ↦ w^q for every odd q ≡ 1 (mod M);
- hence every nonempty L ∈ 𝓦, in particular every L ∈ 𝓦 containing T, contains a non-primitive word.

*Proof.* Let n′ = qn and m′ = qm. Then:
- m′ ≡ m (mod n), because q is odd;
- the windows of w^q at p and p+m′ equal those of w at p and p+m;
- qn ≡ n and q|w|_1 ≡ |w|_1 (mod M).
So w^q satisfies the same Rel tuple. Take q = 2M+1 ≥ 3. ∎

𝓦 contains W_N, all antipodal-mismatch tests at bounded distance from the defect, and all parity or modular letter
counts. So no certificate built only from local antipodal information plus counting works. T forces **global**
information.

**Where the barrier stops (why the mixed class stays open).** The sound certificates known in round 4 all use global
information along one reflection: builder's dominance, builder2's Lemma O level-set counts, and cl1's L_ℓ. Such
conditions are **not** preserved by w ↦ w^q. For example, a level-set count s becomes qs, and "s = 1" is lost. So
Theorem 9 does not extend to "reflection fold-regular ∧ antipodal windows".
- I tried to build, inside T, a word whose fold (along the axis through both defects) equals the fold of some (1y0y)^q.
  Then fold-regularity would transfer membership.
- This fails. The fold of (1y0y)^q is (1,1) Y (0,0) Y (1,1) ⋯ Y (0,0), with Y = fold′(y) (the pairs (y_j, y_{|y|−1−j})).
  Its interior separators alternate in the order (0,0),(1,1),…, while the fold of any T-word must be
  "swap-reverse-symmetric". The separator order breaks that symmetry, so no T-word has this fold. I checked this by
  hand: it is consistent with T ⊆ Q.

**What a refutation of CL5 must look like (IDEA).** Use P4 to kill every period dividing m. Then exclude the odd powers
v^q with long even roots, using reflection-global data that every T-word satisfies. On T-words the fold along the
defect axis is (1,1) fold′(y) (0,0), and fold′(y) is an arbitrary swap-reverse-symmetric pair word. On v^q the fold is
the q-fold alternating concatenation above. So a refutation needs a CF (fold-regular, or more) property of pair words
that:
- holds for every (1,1) Z (0,0) with Z swap-reverse-symmetric;
- fails for every (1,1) Y (0,0) Y (1,1) ⋯ Y (0,0) with q odd ≥ 3, where Y is swap-reverse-symmetric;
- and does the same for every other axis choice.

Pair words of the second kind are themselves swap-reverse-symmetric only when the separator pattern is, so a
*regular* test on the fold would have to tell "one central block" from "q blocks" without counting the blocks. I
conjecture this is impossible, which would be the next barrier. It is not proved.

## Registry entry (CL5)
1. **Aimed at:** refute CL5, or give the strongest barrier.
2. **Proved:**
   - P4: L_N = W_N ⊇ T is linear CF, and its non-primitive words are exactly odd powers with root length ≥ 2N.
   - P5: walk.md's T-operator misses the balanced core T_0.
   - Theorem 9: no certificate built from bounded antipodal windows plus modular counts covers T. The class is closed
     under odd powers ≡ 1 mod M.
3. **Missing step:** extend Theorem 9 to certificates that also impose a fold-regular condition along one reflection.
   The precise target: for every regular M over pair words and every axis family, if M accepts the folds of all
   T-words then it accepts the fold of some odd power. This is open, and I conjecture it is true.
4. **Counterexamples found:** none to CL5.
   - W_N is not ⊆ Q (it contains (v)^3 with |v| = 2N).
   - The fold-transfer attempt fails, as explained above.
5. **Strength:** CL5 ⇒ CL4 ⇒ "Q not CF". The fold-regular barrier would be strictly weaker than CL5.
6. **What would reopen the route:**
   - A proof of the fold-regular barrier, by pumping the fold automaton inside the q-block structure.
   - Or a CF certificate distinguishing one swap-symmetric block from q alternately separated copies. That would refute
     CL5 and kill the near-power program altogether.
