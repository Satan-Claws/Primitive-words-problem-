# Report of agent "builder" (positive direction: try to build a CFG/PDA for Q)

**Claim status: I do NOT claim a proof of either resolution.** No CFG/PDA for Q was found.
What I have: one new sound context-free certificate that kills *all* periods at once
(reflection dominance), with a full soundness proof, a literal grammar, exact completeness data
up to n = 20, an explicit infinite missed family, and a proof that it covers a vanishing fraction
of words. I also record which natural extensions are unsound or do not help.
Scripts: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/builder/` (pure Python, one core, each run < 3 min).
Notation: Σ = {a,b}, a < b, positions 0..n-1 taken mod n, Cyc(L) = all conjugates of words of L.

---------------------------------------------------------------------------------------------
## 1. Theorem D (PROVED): reflection dominance certifies primitivity

Let τ(i) = c - i (mod n) be a reflection of Z_n and let H ⊆ Z_n be an arc (consecutive residues)
with H ∩ τH = ∅. Say w ∈ Σ^n is *(τ,H)-dominant* if w_i ≤ w_{τ(i)} for every i ∈ H, with strict
inequality for at least one i ∈ H.

**Lemma D.** Suppose that for every proper divisor d of n, either H contains a complete residue
system mod d, or the special case below holds. Then every (τ,H)-dominant word is primitive.
Special case: n even, c = 0, H = {1,…,n/2-1}, d = n/2.

*Proof.* Suppose w has period d (d | n, d < n), and let i0 ∈ H have w_{i0} = a and w_{τ i0} = b.
Take j ∈ H with j ≡ τ(i0) (mod d). Such j exists if H covers all residues mod d; in the special case
take j = n/2 - i0 ∈ H. Then w_j = w_{τ i0} = b. Also τ(j) = c - j ≡ c - τ(i0) = i0 (mod d), so
w_{τ j} = w_{i0} = a. Hence w_j > w_{τ j} with j ∈ H, which contradicts dominance. ∎

(The idea: a translation symmetry composed with τ is another reflection. It maps a strict "<" pair
to a ">" pair inside H.)

**Grammar.** X → a | b, and

    S → Y | X Y
    Y → a Y a | b Y b | a Z b                 (equal mirror pairs until the first strict pair (a,b))
    Z → a Z a | b Z b | a Z b | X | ε         (afterwards, any pair except (b,a))

L(Y) is the set of words v with v_i ≤ v_{|v|-1-i} for all i < |v|/2, strict somewhere. This is
(τ,H)-dominance with c = n-1 and H = {0..⌊n/2⌋-1}. X·L(Y) is the same with c = 0 and
H = {1..⌊(n-1)/2⌋}.

**Theorem D.** L(S) ⊆ Q, so Cyc(L(S)) ⊆ Q is context-free (LITERATURE: CFLs are closed under cyclic
shift, Oshiba 1972 / Maslov 1973). Cyc(L(S)) is exactly the set of words admitting *some* reflection
of the n-cycle such that all mixed mirror pairs {i,τi} (w_i ≠ w_{τi}) have their b on the same side
of the axis, and at least one mixed pair exists.

*Proof of L(S) ⊆ Q.* We check the hypotheses of Lemma D. Every proper divisor d of n is at most n/2,
and when n is odd it is at most n/3.
- Y with n even: |H| = n/2 ≥ d.
- Y with n odd: |H| = (n-1)/2 ≥ n/3 ≥ d (n ≥ 3).
- XY with n odd: |H| = (n-1)/2 ≥ d, as above.
- XY with n even: |H| = n/2 - 1. If n ≥ 6, this is ≥ n/3 ≥ d for every d < n/2, and d = n/2 is the
  special case. If n = 4, then d = 1 ≤ |H| and d = 2 is the special case. If n = 2, H = ∅ and
  nothing is dominant.
- n = 1: L(Y) contains no word of length < 2, and X·L(Y) none of length < 3. ∎

COMPUTER-CHECKED (`grammar_check.py`):
- the DP on the literal grammar equals the predicate, and L(S) ⊆ Q, for all words of length ≤ 16;
- completeness of Cyc(L(S)), as primitive necklaces missed:

| n | 2–8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| missed | 0 | 2 | 0 | 6 | 12 | 34 | 58 | 156 | 344 | 796 | 1873 | 4228 | 9673 |
| fraction | 0 | .036 | 0 | .032 | .036 | .054 | .050 | .071 | .084 | .103 | .129 | .153 | .185 |

So this one rule covers every primitive word of length ≤ 8 and of length 10. It is a genuinely
length-agnostic certificate: one guess (the axis) excludes all periods n/p for all primes p | n at
once, with no counting tied to n. Given C1/C2 of devil.md, this is the only such mechanism I found
with positive coverage at moderate lengths.

---------------------------------------------------------------------------------------------
## 2. Why Theorem D cannot be the whole answer

**D-density (PROVED).** |Cyc(L(S)) ∩ Σ^n| ≤ 2n · 2^n · (3/4)^{⌊(n-1)/2⌋}, so the fraction → 0.
*Proof.* There are n rotations and 2 rule types. Each rule constrains ⌊n/2⌋ or ⌊(n-1)/2⌋ disjoint
mirror pairs, and allows 3 of the 4 values for each pair. ∎
Since |Q_n|/2^n → 1, almost all primitive words need a different certificate. The data shows the
fraction of misses rising from n = 14 on.

**Missed family F1 (PROVED; COMPUTER-CHECKED for m ≤ 120).** For every m ≥ 2,
w_m = b b a^m b a b a^m (length 2m+5: every odd length ≥ 9, including all primes ≥ 11) is primitive
and has no conjugate in L(S).
*Proof.* The b-positions are S = {0, 1, m+2, m+4}, with n = 2m+5 odd, so every reflection has exactly
one fixed point. Dominance needs ≥1 mixed b and all mixed b's on one side of the axis.
(i) Reflections fixing a b. For each fixed b, τ(S) ∩ S is exactly that b, and the other three b's
are mixed and split 2/1 between the sides:
- fix 0: {1, m+2} | {m+4};
- fix 1: {m+2} | {0, m+4};
- fix m+2: {0, 1} | {m+4};
- fix m+4: {0, 1} | {m+2}.
(ii) Reflections fixing no b, with no matched b-pair: all four b's would lie in an open half-arc of
length m+2. But the smallest arc containing S has length n - m = m+5.
(iii) Reflections fixing no b that match a pair of b's.
- The pairs {0,1} and {m+2,m+4} give the same reflection (c = 1), which fixes S, so there is no
  mixed pair.
- In each of the other four pairs {0,m+2}, {1,m+4}, {0,m+4}, {1,m+2}, the remaining two b's are
  mixed. Each of them lies at distance 1 or 2 from a different end of the matched pair, so it is on
  that end's side, using m ≥ 2. The two are therefore on opposite sides. ∎

F1 is *not* by itself an obstruction: Q ∩ bba*baba* is regular (4 b's and a factor bb, so there is no
square and no 4th power). Its role is to show that the dominance mechanism fails on an explicit
sparse family at prime lengths, where nothing at all needs certifying beyond "non-unary".

---------------------------------------------------------------------------------------------
## 3. Extensions tried and why they fail

(a) **Other sign patterns on the mirror pairs** (`foldgen.py`; signs =,<,> outermost first, all axes).
COMPUTER-CHECKED:
- UNSOUND, with counterexamples:
  - "first and last strict signs are <": ababab;
  - "<'s before >'s": abab;
  - ">'s before <'s": baba;
  - "≤1 '>' and ≥2 '<'": ababab.
- Sound but strictly weaker than D: "first two strict signs are <<, at most one '>'".
Reason (the first sentence is PROVED from the proof of Lemma D; the conclusion is IDEA): a d-periodic word has a sign sequence that is d-periodic
and antisymmetric under i ↦ kd-1-i. Each '<' therefore comes with roughly p/2 forced '>' signs, and a
finite automaton reading the fold cannot tell p, so the only threshold it can use is "zero '>' signs".

(b) **A counting version** (sound, but not usable). For n even, w = xy with |x| = |y|: if
||y|_b - |x|_b| > n/6 then w is primitive.
- PROVED: a p-th power has imbalance 0 when p is even, and at most |u|/2 = n/(2p) ≤ n/6 when p is odd.
- COMPUTER-CHECKED (`imbalance.py`): the bound n/6 is attained, n = 6, 12, 18, 24.
- This has positive density among random words. But it needs |x| = |y| *and* a count comparison at
  the same time. Its slice {a^i b^j a^k b^l : i+j = k+l, j > l} has a cone whose extreme rays include
  the crossing pairs (e1+e3, e2+e4). So it is not CF by Ginsburg's stratification criterion
  (IDEA/sketch, not written in full). The fold that gives |x| = |y| for free uses up the stack.

(c) **Closing under Sturmian decodings** (`depth.py`; used the weaker edge-axis-only version of D).
If a cyclic word avoids bb, decode it by a ↦ x, ab ↦ y, recurse, and accept if some level is
dominant. Each decoding preserves primitivity (prefix-closed code argument, PROVED). Data:
- this rescues only a handful of necklaces (n = 18: 208);
- 4784 of 14532 remain with "∞" (both aa and bb occur cyclically);
- the needed depth grows (depth 3 at n = 18), and a finite union of compositions is required to stay CF.

(d) **Length-agnostic certificates of other kinds**, all PROVED sound and CF, all of density → 0:
- cyclic-additive functionals f (weighted counts of cyclic factors of bounded length, so
  f(u^p) = p f(u)) with f(w) = ±1. These are one-counter languages; P(f = ±1) = O(n^{-1/2}) (local-CLT sketch, for non-degenerate f).
- "some factor of length ≤ K occurs exactly once cyclically". This is regular; for fixed K it has
  density → 0.
A union of finitely many of these together with Cyc(L(S)) still has density → 0.

(e) **The obvious global certificates are not CF.** "The longest a-run is unique" is not CF even
up to conjugation: its slice in a*ba*ba*b needs {k > i, k > j} at a shared vertex, which is non-CF
by devil B2. Lyndon or unbordered conditions need unbounded comparisons.

---------------------------------------------------------------------------------------------
## 4. The obstruction this points to (CONJECTURED)

Every sound CF certificate I can build is of one of three kinds:
- (i) length-agnostic and geometric (reflection dominance), or functional (f = ±1, unique short
  factor). All of these have density 0.
- (ii) tied to the length for ONE prime (T1 / coPow_k). This cannot handle n with two primes at
  pinned positions (devil C2), and needs ω(n)+1 letters (devil C1).
- (iii) regular on bounded slices.

A random word of length n with ω(n) large is primitive "for counting reasons". None of (i)–(iii)
certifies it.
Missing step (precise): **Lemma M.** For every CF L ⊆ Q there are infinitely many n with
|Cyc(L) ∩ Σ^n| ≤ (1-ε)·2^n. Lemma M implies Q is not CF. It is equivalent to "Q not CF"
(⇐: if Q were CF, L = Q violates it), so it is NOT a weaker reduction. The stronger version with
density → 0 along a subsequence would explain all the data above, but I have no proof.

---------------------------------------------------------------------------------------------
## Registry entry
1. **Statement aimed at:** an explicit CF L ⊆ Q with Cyc(L) = Q, which would give Q context-free.
2. **Strongest lemma proved:** Theorem D. The linear-type language L(S) (grammar in §1) satisfies
   L(S) ⊆ Q, so Cyc(L(S)) is a CF subset of Q. It contains every primitive word of length ≤ 8 and of
   length 10. Also proved: the D-density bound, family F1, and that the n/6 half-imbalance
   certificate is sound.
3. **Missing step:** a CF certificate of positive (in fact full) density for words whose length has
   many prime factors. Equivalently, for the negative side, Lemma M (§4).
4. **Counterexamples found:**
   - F1_m = bba^m baba^m (all m ≥ 2) is missed by Cyc(L(S)).
   - Exact miss counts up to n = 20 are in the table in §1.
   - The four sign-pattern variants in §3(a) are unsound, with explicit powers.
5. **Missing step vs "Q not CF":** Lemma M is equivalent to "Q not CF". Its density-0 strengthening
   is stronger.
6. **What would reopen the route:** a length-agnostic sound CF mechanism for random words, i.e. one
   with positive density that is not dominance, not a functional = ±1, and not a single tied
   distance. Or a proof that the n/6-imbalance language (or its cyclic closure) is CF after all.

Scripts:
- `common.py`: Lyndon enumeration and primitivity test.
- `grammar_check.py`: grammar and predicate equality, soundness, completeness table, F1.
- `fold.py`, `fold2.py`: earlier, weaker axis sets.
- `foldgen.py`: sign-pattern variants.
- `fourb.py`: missed words with exactly K b's (source of F1).
- `depth.py`: Sturmian-decoding closure.
- `imbalance.py`: the n/6 bound.
