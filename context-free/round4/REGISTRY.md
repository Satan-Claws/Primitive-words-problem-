# Round 4 registry of approach families

Started 2026-11-18 04:29 UTC. Wave 1: 9 independent agents (one slot kept for audits).

| Family | Agent | Status |
|---|---|---|
| Derivation-tree iteration / Ogden / multi-pump on unbounded slices | ogden | **stalled** (Q satisfies all iteration lemmas tested; ceiling theorem) |
| Bounded slices, Kászonyi–Katsura (n = 210 …) | kk | **stalled** (one-scale obstructions dead for all n) |
| Density of CF subsets of Q | density4 | running |
| Construction of a CFG/PDA (positive direction) | builder | open: reflection-dominance certificate (sound, CF, coverage → 0) |
| Rational-transduction reductions (correct direction) | transduce | **stalled** (barriers T1, T2, Prop D) |
| Uniform-in-M upgrade of the finite-ambiguity slice argument | uniform | **blocked** (barrier) |
| Periodicity / near-power witness families | periodic, cl1 | CL1, CL2 **refuted**; CL3 open |
| Analytic / N-algebraic series obstructions | analytic | running |
| Cross-length context × yield decompositions | crossing | **blocked** (missing step = full problem) |

Entries are filled in from each agent's report (exact aim, strongest lemma, missing step,
counterexamples, strength of missing step, reopen condition).

## uniform (done 1st wave)
1. Aim: turn the finite-ambiguity slice argument into an existence obstruction.
2. Proved: on R = a(ab⁺)*a(ab⁺)* (contains every R_m) every non-primitive word is a square, so
   Q ∩ R = R ∩ coPow₂ is CF (explicit 5-nonterminal grammar). General barrier: if the gcd of root exponents
   of non-primitive words of a regular R is d ≥ 2 then Q ∩ R = R ∩ coPow_d is CF. Identity
   Q ∩ R6 = R6 ∩ coPow₂ ∩ coPow₃ for R6 = (a(ab⁺)⁺)⁶ (exponents {2,3,6}).
3. Missing: a regular R with gcd E(R) = 1 and Q ∩ R not CF (candidate R6).
4. Counterexamples: pump-to-equal-halves, bounded certificate-type counting, single-prime slices.
5. Missing step is stronger than Q ∉ CFL (but sufficient).
6. Reopen: an iteration lemma using square and cube certificates jointly on R6, or a grammar for Q ∩ R6.

## kk (done 1st wave)
1. Aim: find n with Q ∩ (ab*)^n not CF (Kászonyi–Katsura counterexample), or a barrier.
2. Proved: Theorem A (reflection axes + CRT): for every n the near-constant region of E_n is covered by
   stratified linear subsets of E_n (covers n = 210); Theorem B: same for every positive direction h.
   So every one-scale Dickson obstruction (bounded.md L6 / finiteindex F) fails for every n.
3. Missing: a two-scale ("flag") obstruction N·h + M·g + δ with g/h having no reflection axis compatible
   with all primes, plus proof that it implies non-CF; must pass at n = 6 (known CF).
4. Counterexamples: one-scale families for all n; near-constant arrangement search at n = 42, 60.
5. Missing step concerns one n (narrower than Q ∉ CFL), but evidence now favours KK being true,
   which would close the route.
6. Reopen: a two-scale obstruction lemma, sound, that survives n = 6.

## periodic (done 1st wave)
1. Aim: CL1 — every CFL containing F_ins = {a(a^m b)^k : m ≥ 1, k ≥ 2} contains a non-primitive word.
2. Proved: L1 (two distinct non-primitive words of equal length differ in ≥ 2 positions); Fact B
   (word in (a*b)+ is a power iff cyclic block vector is shift-invariant); L2 partially (insertion
   into u^k is primitive; proved for q ≥ 3, k ≥ 6, checked |u^k| ≤ 15); Bar1 (one-parameter slices of F_ins
   lie in regular subsets of Q); Bar2 (no coprime semilinear set covers F_ins counts); Bar3 (classification
   of exact-power pumps; case B only computer-checked); Bar4 (Ogden/Bader–Moura cannot force them);
   'unique longest block' superset not CF.
3. Missing: tree surgery combining derivations of a(a^m b)^k and a(a^{m+1}b)^k forcing a power-producing pump.
4. Counterexamples: B-type merge pumps (odd k), k = 3 cube pump, first-vs-last block supersets contain powers,
   L2 false for |u| = 1.
5. Stronger than Q ∉ CFL.
6. Reopen: cross-derivation parity argument; or a CF L with F_ins ⊆ L ⊆ Q (refutes CL1).

## transduce (done 1st wave)
1. Aim: rational transduction τ and regular R with τ(Q ∩ R) provably not CF.
2. Proved: T1 equality barrier (via closure.md Prop P): {ww}, {aⁿbⁿcⁿ}, {aⁿbᵐcⁿdᵐ}, MIX, {|w|_a=|w|_b},
   {aⁿbaⁿb} are not images of Q; T2: every bounded image reduces to some Q ∩ B for a finite union of
   bounded slices (generalised KK); Prop D: non-primitive exponent vectors on an r-block merge-free slice
   lie in finitely many affine subspaces of dim ≤ ⌊r/2⌋; DIST3 = {aⁱbʲcᵏ pairwise distinct} and
   CROSS≠ = {aⁱbʲcᵏdˡ : i≠k, j≠l} are not CF (open whether images of Q).
3. Missing: a non-stratifiable merge-free slice (negation of generalised KK), or an unbounded Ogden image argument.
4. Counterexamples: none to claims; boundary example limits Prop D's extension.
5. Bounded missing step implies Q ∉ CFL, believed false; unbounded step not reduced.
6. Reopen: non-stratifiable slice; DIST3 or CROSS≠ shown to be an image of Q.

## ogden (done 1st wave)
1. Aim: Q violates a strong iteration lemma valid for all CFLs.
2. Proved: Theorem A (k nested independently iterable pumps under 2^{kN+1} marks); Theorem A′ (m loops at one
   nonterminal, free monoid of pumpings); Theorem B (ceiling): L CF iff ∃N every word has a tree with ≤ N labels
   whose rule set generates only words of L — so all such lemmas are weakenings of exactly "Q CF".
   Inside unary runs loops can be chosen commuting, so near-powers survive every k; in cube-free regions
   (Thue–Morse) ≥ 3 adjacent loops cannot pairwise commute.
3. Missing: ∃m such that for every Ogden constant p some primitive word + marking defeats every m-free-loop
   decomposition.
4. Counterexamples: none to claims; all tested instances (n ≤ 12, Thue–Morse ≤ 32) satisfied by Q.
5. Stronger than Q ∉ CFL; evidence says false.
6. Reopen: cube-free marked region with loop monoid forced to hit a power; cross-word iteration principle.

## crossing (done 1st wave)
1. Aim: cross-length context × yield (generalised rectangle) obstruction.
2. Proved: Lemma 1 (rotation turns a context × yield rectangle into a product L_A·M_A ⊆ Q, M_A CF);
   Theorem 1: Q CF ⇔ finitely many CF pairs (L_i, M_i) with L_i·M_i ⊆ Q cover a conjugate of every primitive
   word — so the route's missing step equals the full problem; Theorem 3: 18 explicit (non-CF) product classes
   inside Q covering all primitive words ≤ 19 up to conjugacy except ≤ 36 near-periodic classes per length;
   Lemma 4 (cross-length fooling sets ≤ g; computationally max fooling set = 1 for n ≤ 14); Lemma 5.
3. Missing: a structural lemma limiting CF L with L·M ⊆ Q (equal in strength to Q ∉ CFL).
4. Counterexamples: no fooling pair for n ≤ 14; unsound 'predicted letter' class: (abbba)(bbb) = (abbb)².
5. Equal to Q ∉ CFL.
6. Reopen: Conjecture "finitely many arbitrary-set product classes cover Q" fails; or a structural lemma
   restricting CF factors.
Leftover hard words everywhere: near-periodic words (a^{n−1}b, (ab)^k and (aab)^k with a defect).

## builder (done 1st wave)
1. Aim: explicit CFG/PDA for Q (positive resolution), or the obstruction a negative proof must capture.
2. Proved: reflection dominance — if for a reflection τ(i) = c − i of the n-cycle and a half-arc H,
   w_i ≤ w_{τ(i)} on H (a < b) with one strict pair, then w is primitive. CF grammar
   S → Y | XY, X → a|b, Y → aYa | bYb | aZb, Z → aZa | bZb | aZb | X | ε; its cyclic closure is a CF subset of Q
   covering all primitive necklaces of lengths 2–8, 10; misses grow (18.5% at n = 20); coverage → 0 (proved
   bound 2n·2^n·(3/4)^⌊(n−1)/2⌋). Missed family bb a^m bab a^m (all m ≥ 2). Half-imbalance certificate (n/6, tight).
3. Missing: a finite union of CF certificate languages whose cyclic closure covers Q; or the lemma
   'every CF L ⊆ Q misses ≥ ε·2^n conjugacy classes infinitely often' (equivalent to Q ∉ CFL).
4. Counterexamples: sign-pattern variants (ababab, abab, baba); Sturmian decoding rescues few words.
5. Missing lemma equal to Q ∉ CFL (the coverage-→-0 version is stronger).
6. Reopen: a new sound CF certificate type covering a positive share of words of highly composite lengths.

## cl1 (done)
CL1 REFUTED (PROVED; coordinator checked the proof). L = a·P, P = words of (a*b)* with palindromic block
vector, is linear CF (T → aS, S → Nb | Ab | ε, N → aNa | bS, A → aA | ε), contains F_ins, and L ⊆ Q because
x − Rx = e_1 − e_k is never shift-invariant. Cyclic closure covers single-a insertions anywhere; Theorem 2:
insertions into any power whose block vector is a palindrome up to rotation.
Lesson: near-power witnesses need a base power with no mirror symmetry.
New candidate CL2: every CFL containing {a·(a^m b a^{m+1} b a^{m+3} b)^k} contains a non-primitive word
(stronger than Q ∉ CFL).

## audit1 (adversarial audit of uniform + kk)
- uniform Lemma 1.1, grammar G* = coPow₂, Prop 2.1 (gcd barrier), Q ∩ R6 identity: CONFIRMED.
- uniform Cor 2.2 wording FALSE: gcd E(R) = 1 does not imply two coprime exponents (E = {6,10,15}).
  Correct form: gcd E(R) = 1 is necessary for a slice proof.
- kk Theorem A, Lemmas A1–A2, Cor A3: CONFIRMED (stratified, inside E_n; 13 003 + 1080 checks).
- kk Theorem B: only "the one-scale criterion never holds" is confirmed; explicit stratified covers for
  non-constant h are NOT built (n = 6 counterexample to the naive piece). Rotation remark: informal GAP.

## analytic (done 1st wave)
1. Aim: an analytic/algebraic obstruction valid for ambiguous CFLs.
2. Proved: supports of N-algebraic series = CFLs (literature), so the supports route is circular; commutative
   images reduce to semilinear data; exact series of Q ∩ (ab*)^+ is Σ_d μ(d) t^d/(1−y^d−t^d) and its pole data is
   matched by a linear CFL; 'every CFL is counting-equivalent to an unambiguous CFL' is FALSE
   (L1 = (a*b)*{a^i b a^j b : i≠j}(a*b)* has 2^{n−1} − d(n) words, non-algebraic series); for every d a binary CFL
   with poles at z^{dj} = 1/2 for almost all j; for regular codes X, series built from L_X have poles of
   modulus 2^{-1/p} for only finitely many primes p.
3. Missing: Conjecture A — a binary CFL with meromorphic series in |z| < 1 has poles of modulus 2^{-1/p}
   for only finitely many primes p. (Q has them for all primes.)
4. Counterexamples: to the counting-equivalence claim; to 'composite radii' and 'ternary' variants of A.
5. Stronger than Q ∉ CFL.
6. Reopen: structure theory for counts of ambiguous grammars; or a binary CFL refuting Conjecture A (kills route).

## density4 (done 1st wave)
1. Aim: every CFL of density 1 (or positive) contains a non-primitive word.
2. Proved: Prop C (positive-density CF L ⊆ Q exists iff a CF L′ ⊆ Q meets ≥ c·2^n/n conjugacy classes per length);
   Theorem P (barrier): any language defined by k-gram counts in a semilinear set with no proper power has
   |L_n| = O(2^n n^{-1/2}), attained by E′. Literature (Koga 2022): density version for CFLs is open and noted to
   imply the conjecture; Sin'ya's {|v|_a ≤ 2|v|_b} has density 1 but no positive-density regular sublanguage.
3. Missing: (K*) every positive-density CFL contains x{t : D | |t|, V_k(t) ∈ full-rank linear set}z; or
   (Q½) every CF L ⊆ Q has |L_n| = O(2^n n^{-1/2}). Both stronger than Q ∉ CFL.
4. Counterexamples: L0 = {Δ(w) ∉ {0,1}} and L5 (DCFL, density → 1) refute 'dense CFL contains x(Σ^D)*z' and
   its k-gram variants.
5. Stronger than Q ∉ CFL.
6. Route dies if a CF L ⊆ Q of positive upper density is found.

## Timeline
- 04:29–04:47 UTC: wave 1 (9 agents) + follow-ups; usage limit hit at ~04:47, all running agents stopped.
- 09:22 UTC: resumed r6, cl1 (CL2), thue, audit2, builder2, poles, dense. Active time so far ≈ 18 min;
  campaign continues to ≥ 1 h active (≈ 10:05 UTC), hard stop at 2 h active (≈ 11:05 UTC).

## cl1 → CL2 (done)
CL2 REFUTED (Theorem 3, proved + checked): for any base offset c0 of length ℓ, L(c0) = {(a*b)^+ : ℓ | K, K ≥ 2ℓ,
x − Rx = v(c0) + e_1 − e_K} is linear CF, ⊆ Q, contains a·(m·1 + c0)^k. Generalises to several parameters
whose directions share a reflection axis. Theorem 4 (proved): F_2 = {a(a^p b a^q b a b)^k} defeats the class 𝓡
(finite unions of rotation-closures of 'x − Rx bounded by B') and all Parikh certificates.
CL3 (conjectured, stronger than goal): every CFL ⊇ F_2 contains a non-primitive word.

## dense (done)
1. Aim: CF L ⊆ Q with density ≫ n^{-1/2} (refuting Q½), else extend the n^{-1/2} barrier.
2. Proved: W (cyclic walk-window certificate: D = Δ(w) ≥ 1 and some i with S_t ≤ S_i on (i, i+⌊n/2⌋], mirrored
   for D ≤ −1, strict for D = 0) is sound and has positive density (Donsker; ≈0.66 by Monte Carlo) — but is
   probably NOT CF (unproved). Theorem P^R: R ∩ {k-gram counts ∈ S} power-free ⇒ O(2^n n^{-1/2}), also for subsets.
3. Missing: every CF L ⊆ Q agrees up to O(2^n n^{-1/2}) with a power-free regular ∩ count language
   (stronger than goal). First concrete test: is W, or a positive-density variant of W, CF?
4. Counterexamples: none for Q½; W shows soundness alone does not give n^{-1/2}.
5. Stronger than Q ∉ CFL.
6. A CF positive-density variant of W would kill the density route.

## poles (done)
1. Aim: refute or prove Conjecture A (binary CFL with meromorphic series has poles of modulus 2^{-1/p} for
   only finitely many primes p).
2. Proved: Lemma 1 (seed lemma) — for any binary code X with meromorphic series, primes p giving poles of
   modulus 2^{-1/p} in L_X = X⁺ \ {x^k} already come from X or X⁺ (McMillan: no code has a pole at modulus 1/2);
   Lemma 2: {a^k b v : v ≠ u^k for u ∈ Y} is not CF when Y contains all powers of a primitive word;
   Lemma 3: excess-e words that are e-th powers = {u^t : excess(u) = 1}; series Σ_t E₁(z^t) (branch points).
3. Missing: a theorem that poles of modulus 2^{-1/p} (large p) in any CFG's series come only from repetitions
   over a code / regular block set (≥ A in strength).
4. Counterexamples: none to A; natural candidate killed by Lemma 2.
5. Stronger than Q ∉ CFL.
6. Reopen: structure theory for counting series of ambiguous CFGs; a CF complement for Lemma 3's S.

## audit2 (builder, cl1, crossing, transduce)
- FALSE: cl1.md coverage remark after Theorem 2 ('every one-a insertion into u^k with reflection-symmetric
  block vector up to rotation, in particular ≤ 2 blocks') — counterexamples baabbab, aaabbaabb; 60/60 small
  cases fail. Cause: only reflection i ↦ k+1−i used; fix: also allow i ↦ k−i (not re-verified).
  The CL1 refutation itself (Theorem 1) and Theorem 2's L ⊆ Q are CONFIRMED.
- FALSE as stated: crossing Lemma 4 (fooling bound) — L = Σ⁺, F = {a, b}; correct for words of length ≥ 2.
- GAPs (trivial): crossing Theorem 1(ii) needs length ≥ 2; builder coverage claim omits a, b.
- CONFIRMED: builder Lemma D (reflection dominance) in all cases, grammar = predicate, density bound,
  missed family, n/6 bound; transduce T1 (closure.md Prop P re-audited), T2, Prop D, DIST3/CROSS≠ non-CF;
  crossing Lemmas 1, 2. Cyclic-shift citation: Hopcroft–Ullman 1979 Ex. 6.4(c), Oshiba 1972, Maslov 1973.

## thue (done)
1. Aim: cube-free near-power witnesses defeating the m-free-loop iteration theorem A′.
2. Proved: L-UC (factor occurring once circularly ⇒ primitive), L-UF, L-PAR, L-PS (exact test whether a
   loop-generated word σr can be a power, no length cut-off), L-μ (Thue–Morse morphism preserves primitivity
   both ways).
3. Missing: none attainable — Barrier E (conjectured): every primitive word with enough marks has an escaping
   window with empty x_j, so A′ alone cannot prove Q ∉ CFL.
4. Counterexamples: 19,771 instances (10 roots incl. 5 non-mirror-symmetric, all one-letter defects, all mark
   intervals, m = 3): every instance has a certified escaping window.
5. Missing step stronger than Q ∉ CFL; evidence says false.
6. Reopen: an iteration theorem transplanting loops across words/contexts.
