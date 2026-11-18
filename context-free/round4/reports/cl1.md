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
