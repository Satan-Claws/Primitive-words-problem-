# Agent "uniform": can the finite-ambiguity method become an existence obstruction?

**Short answer: not on the slices it uses, nor on any slice family of the same kind.** Every slice
family in which all non-primitive words are k-th powers for one fixed k is *uniformly* context-free:
one fixed grammar handles all M at once. This holds however bad the crossing structure is. So (1) the
pump-to-the-diagonal lemma, (2) the counting of certificate types and (3) the variants with more blocks
or k ≥ 3 cannot work on such families. Any slice-based existence proof needs slices whose non-primitive
words have root exponents with gcd 1. The smallest natural one is R6 below, where the problem becomes
"is R6 ∩ coPow_2 ∩ coPow_3 CF?".
**I claim no proof of either resolution.**

Script: `context-free/round4/scripts/uniform/check_square_slice.py` (≈1 min, one core).

---

## 1. The finite-ambiguity slices are uniformly CF (PROVED + COMPUTER-CHECKED)

Let R := a(ab⁺)* a (ab⁺)*. This is regular, and the union of all slices R_m used in `finitely-ambiguous/PROOF.md` is
contained in R (R also allows different block counts in the two halves).

**Lemma 1.1.** Every non-primitive word of R is a square. Hence Q ∩ R = R ∩ coPow_2, where
coPow_2 = Σ* ∖ {uu}.

*Proof.* Count *cyclic* occurrences of `aa`, i.e. indices i with w_i = w_{(i+1) mod n} = a. If
w = z^k, this count is k times the cyclic count of z. Write w = a u a v with u, v ∈ (ab⁺)*.
* The explicit letter a at position 0 is followed by the first letter of u (an a) or, if u = ε, by the
  next explicit a.
* The explicit a at position |u|+1 is followed by the first letter of v (an a) or, if v = ε, cyclically
  by w_0 = a.
* Every other a starts a block ab⁺ and is followed by b.
So the cyclic count is exactly 2. Then 2 = k·c(z) with c(z) ≥ 1, so k = 2 and w is a square. Conversely
every square is non-primitive. ∎

(Exhaustive check: the script verifies Q ∩ R = L(G*) ∩ R
for **all 70 101 words of R of length ≤ 22**, with 0 mismatches.)

**Explicit fixed grammar.** G* (classical non-square grammar):
S → O | A B | B A,  A → X A X | a,  B → X B X | b,  X → a | b,  O → X | X X O.
Here AB derives Σ^i a Σ^{i+j} b Σ^j, an even-length word whose two halves Σ^i a Σ^j and Σ^i b Σ^j
differ. O derives the odd-length words. L(G*) = coPow_2 (devil.md T1), so G* × DFA(R) has fixed size and
generates Q ∩ R = ⋃_m (Q ∩ R_m) ∪ (the words of R with different block counts in the two halves).

**Consequences for the three questions.**

(1) *Pump to the diagonal.* The lemma asked for would say: every tree of a slice word contains a pump
whose iteration (exponent 0 included, or block-moving) yields a word of L(G) with equal halves. **It is
false for G* × DFA(R).** That grammar has L ⊆ Q, so no iterate of any of its pumps is ever
non-primitive. An argument of this shape that uses L(G) = Q only through L(G) ∩ R = Q ∩ R proves a
false statement. A valid argument has to use words outside R.

(2) *Counting certificate types.* No bound on the number of "certificate types" (linear pieces,
half-spaces) in terms of g alone can exist. G* has 5 nonterminals and 11 productions. In the annotated grammar
G* × D_{R_m}, the nonterminals (s, A, t), (s, B, t) are indexed by DFA states. Because of the A → XAX
recursion with X = a, every chain of A-nodes moves through block boundaries. The skeletons therefore
range over all ways of placing the mismatch letter and the half-boundary among the 2M blocks, and their
number grows with m. This is exactly how a fixed grammar produces the ≥ M+1 half-space pieces that
§5 of PROOF.md forces on every grammar for Q ∩ R_m. That bound (|𝓗| ≥ M+1) needs only L_σ ⊆ NE_M and
the covering of NE_M. It therefore transfers to any CFG through Ginsburg's stratified decomposition
(LITERATURE: Ginsburg 1966, bounded CFLs ↔ stratified semilinear sets), refined to independent periods by
the Eilenberg–Schützenberger/Ito decomposition, which uses subsets of the periods and so keeps
laminarity. But G* shows that M+1 pieces cost nothing in grammar size.
Where G* escapes the finite-ambiguity proof: G* is infinitely ambiguous on a single slice. It has one
tree per letter mismatch between the halves, so the number of trees grows with the b-exponents. The
maximum number of trees per length on R is 1,3,3,5,5,7,7,9,9,11 for lengths 4,6,…,22 (COMPUTER-CHECKED).
So the skeleton periods are dependent (Lemma 3(e) fails), and one tree's certificate is a
*length-counting* comparison (|p| = |r|, |q| = |s|), not a positionwise block comparison. The crossing
of the pairs {x_i, y_i} is irrelevant to it.

(3) *Other slice families.* See §2. Slices with more blocks per half, and k-th-power slices with k
prime, are all uniformly CF, however badly their diagonal pairs cross.

## 2. General barrier: one root-exponent prime ⇒ uniformly CF (PROVED)

For a language R let E(R) := { k ≥ 2 : some w ∈ R equals z^k with z primitive }.

**Proposition 2.1.** Let R be regular and d := gcd E(R) ≥ 2 (or E(R) = ∅). Then
Q ∩ R = R ∩ coPow_d (respectively R ∩ Σ⁺), which is context-free.

*Proof.* If w ∈ R is non-primitive, then w = z^k with z primitive and k ∈ E(R), so d | k and
w = (z^{k/d})^d ∉ coPow_d. If w ∈ R is a d-th power with d ≥ 2, it is non-primitive. For ε: ε = ε^d is a
d-th power, so ε is excluded. Finally, coPow_d is CF for every d (devil.md T1, PROVED there with an
explicit grammar), and CFLs are closed under intersection with regular sets. ∎

Instances. Each of the following is CF by one fixed grammar for all sizes:
* R = a(ab⁺)*a(ab⁺)* (§1; E = {2});
* R_p := (a(ab⁺)⁺)^p for p prime: the cyclic `aa` count is p, so E(R_p) ⊆ {p} by the counting argument of
  §1, and Q ∩ R_p = R_p ∩ coPow_p. This is the k-th-power version with p pairwise-crossing
  comparison classes {i, i+n/p, …};
* R_{p^e} := (a(ab⁺)⁺)^{p^e}: E ⊆ {p, …, p^e}, with gcd p;
* any family "two halves with c blocks per half for any c", or "halves separated by any regular marker
  pattern", as long as the only possible root exponent is 2.

**Corollary 2.2 (barrier).** A proof that Q is not CF of the form "Q ∩ R is not CF" must use a regular R
with gcd E(R) = 1, so E(R) contains two coprime exponents, or exponents with coprime parts. More
generally, every existence argument (pumping, tree surgery, counting) must exploit an interaction
between at least two distinct prime exponents. Arguments built only on the "x ≠ y" (one prime) crossing
structure cannot prove non-context-freeness. This matches T2/C2 of devil.md for fixed lengths: here it
is extended to arbitrary regular slices with unboundedly many blocks.

## 3. The minimal uniform target (CONJECTURED open; reduction PROVED)

R6 := (a(ab⁺)⁺)^6, w = z_1⋯z_6 with z_i ∈ a(ab⁺)⁺ (exactly 6 factors `aa`, w ends in b).

**Lemma 3.1.** Every non-primitive w ∈ R6 is z^k with k ∈ {2,3,6}, and both 2 and 3 occur with primitive
root, so gcd E(R6) = 1. Hence Q ∩ R6 = R6 ∩ coPow_2 ∩ coPow_3 = {z_1⋯z_6 : z_1z_2z_3 ≠ z_4z_5z_6 and
¬(z_1z_2 = z_3z_4 = z_5z_6)}.
*Proof.* The cyclic count of `aa` in w is exactly 6, since each z_i contributes its leading a, which is followed by a. So 6 = k·c(z).
The 6th powers are squares. Examples: (z_1z_2z_3)^2 with z_1,z_2,z_3 distinct has a primitive root and
exponent 2, and (z_1z_2)^3 with z_1 ≠ z_2 has exponent 3. ∎ (COMPUTER-CHECKED on 20 000 random words:
root exponents seen are {2,3,6}, and none fails k | 6.)

**Open lemma (target).** *Q ∩ R6 is not context-free.* It implies "Q is not CF" (intersection with a
regular set). It is a sufficient condition that could be false while Q is non-CF, so it is logically
stronger. It is the first place where the "two primes" interaction exists with unboundedly many blocks.
With a fixed number of blocks per z_i, the slice is a Kászonyi–Katsura slice, which is CF by
LITERATURE for small block counts. So any non-CF proof must use the variable block counts. I did not
find a proof or a grammar.

Observation (IDEA). Each single condition is local:
* "z_2z_3 ≠ z_4z_5"-type cube tests on the contiguous factors z_1⋯z_4 or z_3⋯z_6 are copy-complement tests
  of a *factor*.
* The square test is a copy-complement test of the whole word.

A grammar must nest two length-counting certificates, (|p| = |r|, |q| = |s|) for the whole word and
another for a factor. devil.md C2 shows that pinned positions of two mismatches cannot both be verified.
So a grammar for Q ∩ R6 would need unbounded ambiguity about where the mismatches are. The finite-
ambiguity theorem already says this, and it is not an obstruction.

## Registry entry

1. **Aimed at:** an existence obstruction (Q not CF) obtained by making the structural method of the
   finite-ambiguity proof (slices R_m, crossing diagonal pairs, half-space covering) uniform for one
   fixed grammar.
2. **Strongest proved:**
   * Lemma 1.1 + G*: Q ∩ a(ab⁺)*a(ab⁺)* = R ∩ coPow_2 is CF via a fixed grammar (5 nonterminals, 11 productions) (exhaustively
     checked to length 22).
   * Proposition 2.1: for every regular R with gcd E(R) ≥ 2, Q ∩ R = R ∩ coPow_d is CF.
   * Lemma 3.1: Q ∩ R6 = R6 ∩ coPow_2 ∩ coPow_3.
3. **Missing step:** "Q ∩ R6 is not CF" (or the same for some regular R with gcd E(R) = 1). There is no
   candidate proof.
4. **Counterexamples found:** to (1), the pump-to-equal-halves lemma on R_m fails for G* × DFA(R). To (2),
   a g-bounded number of certificate types on R_m fails, because G* (fixed size) has piece counts
   growing with m. To (3), k-th-power slices (p prime) and more-blocks-per-half slices are uniformly CF.
5. **Relation to "Q not CF":** the missing step is sufficient and logically stronger. Everything proved
   here is a barrier: it says where an obstruction can *not* come from.
6. **What would reopen the route:** a structural/pumping lemma for slices with gcd E(R) = 1 that uses the
   interaction of the square and cube certificates in one tree. For example: every tree of a word of
   Q ∩ R6 with large blocks contains a pump whose iterate is a square or a cube. Or a proof that
   Q ∩ R6 (or R6 ∩ coPow_2 ∩ coPow_3) is CF, which would move the difficulty to ≥ 3 primes.
