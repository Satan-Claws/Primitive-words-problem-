# Round 4 registry of approach families

Started 2026-11-18 04:29 UTC. Wave 1: 9 independent agents (one slot kept for audits).

| Family | Agent | Status |
|---|---|---|
| Derivation-tree iteration / Ogden / multi-pump on unbounded slices | ogden | **stalled** (Q satisfies all iteration lemmas tested; ceiling theorem) |
| Bounded slices, Kászonyi–Katsura (n = 210 …) | kk | **stalled** (one-scale obstructions dead for all n) |
| Density of CF subsets of Q | density4, dense, walk, fold | **Q½ REFUTED** by walk (pending audit); positive density open |
| Construction of a CFG/PDA (positive direction) | builder | open: reflection-dominance certificate (sound, CF, coverage → 0) |
| Rational-transduction reductions (correct direction) | transduce | **stalled** (barriers T1, T2, Prop D) |
| Uniform-in-M upgrade of the finite-ambiguity slice argument | uniform, r6 | **blocked** (barrier; R6 evidence: CF) |
| Periodicity / near-power witness families | periodic, cl1 | CL1–CL3 **refuted**; CL4 ⇐ CL5 open |
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

## builder2 (done)
1. Aim: CF L ⊆ Q with Cyc(L) = Q via generalised reflection certificates.
2. Proved: orbit-count lemma (w d-periodic ⇒ D = w − w∘ρ d-periodic for every reflection ρ); certificate G:
   some axis with gcd(m, n) = 1 (m = number of mismatched mirror pairs) ⇒ primitive; RG on run-lengths;
   CF fragments GB, RGB (contains cl1's languages), RD; Cyc(D ∪ GB ∪ RD ∪ RGB) is a CF subset of Q containing
   EVERY primitive word of length ≤ 17 (misses 57, 4, 50 necklaces at n = 18, 19, 20), but density → 0
   (proved for D, GB; sketched RD, RGB). G itself (non-CF) certifies 100% of samples for n ≥ 36.
   Barrier: coprime semilinear sets are finite unions of points and single-period lines (Lemma S); fixed-cut
   'gcd(mismatch count, n) = 1' is not CF (Prop N).
3. Missing: CF control of the coprimality in G; target 'every CF subset of Q has density → 0'.
4. Counterexamples: all 'for all pairs on a half-arc' dominance variants have density e^{−Ω(n)}.
5. Target is stronger than Q ∉ CFL.
6. Reopen: a CF way to certify gcd(m, n) = 1 for a positive share of words (e.g. lines n = 4m + r).

## cl1 → CL3 (done)
CL3 REFUTED (Theorems 5, 6; checked exhaustively ≤ 20–21 for ℓ ≤ 6). L_ℓ: words of (a*b)^+ with ℓ | K, K ≥ 2ℓ,
D = x − Rx (R a block reflection fixing one or two residue classes mod ℓ) equal to +1/−1 at the inserted block
and its mirror on the fixed class f, 0 on the other fixed class, and sign-constant on each swapped pair of
classes. Linear CF, ⊆ Q, and Cyc(L_ℓ) covers every one-a insertion into u^k with |u|_b = ℓ.
Next family J = {a·u·u : u ∈ (a*b)^+}; Prop 7: no finite union of L_ℓ covers J.
CL4 (conjectured, stronger than goal): every CFL ⊇ J contains a non-primitive word.
Coordinator note: on the bounded slice a⁺b⁺a⁺b⁺, J ∩ B = {a^{p+1}b^q a^p b^q} is covered by the CF set
{a^{p+1}b^q a^p b^r} ⊆ Q, so fixed-shape slices of J do not suffice; any proof needs u with unboundedly many blocks.

## audit3 (cl1 CL2, density4, dense, poles, thue, analytic)
- CONFIRMED: cl1 Theorem 3 (CL2 refutation; K = 2ℓ edge case fine), Theorem 4 (restricted class only);
  density4 Theorem P, Lemma AC, Prop C; dense W soundness + positive density, Theorem P^R (needs λ large so the
  constant lies deep in the cone); poles Lemmas 1–3; thue L-UC, L-UF, L-PS and the exact procedure;
  analytic Theorem 3.2 (2^{n−1} − d(n), non-algebraic).
- GAP repaired: thue L-μ (case e = 2; repaired by odd-cycle 2-colouring argument). Statement true.
- Nit: W should be restricted to Σ⁺.

## r6 (done)
1. Aim: decide whether Q ∩ R6 (two primes 2, 3, unboundedly many blocks) is CF.
2. Proved: Q ∩ R6 is CF IF the Cover Lemma holds (every primitive w ∈ R6 has a count certificate (C) —
   per-segment count tuples neither 2- nor 3-periodic; CF via the n = 6 KK slice (LITERATURE, not re-verified) —
   or a non-crossing two-arc certificate (N)); square and cube mismatch arcs sharing no segment always cross,
   sharing a segment they can be ordered; Cover Lemma proved when all six segments have equal length.
3. Missing: Cover Lemma for unequal segment lengths with both count vectors periodic (0 failures among
   49,332,000 tuples with segment length ≤ 5, and all 26,900 R6 words of length ≤ 26).
4. Counterexamples: own earlier 'triangle' argument wrong (not used); unary-like families need (C).
5. If true, R6 route closed (no step toward Q ∉ CFL).
6. Reopen: counterexample to the Cover Lemma, or three coprime exponents (e.g. (a(ab⁺)⁺)^30).

## f2 (done)
1. Aim: prove CL3 (then CL4) via one grammar uniform in k.
2. Proved: an independent, simpler CL3 refutation — linear 7-rule grammar for
   {∏ a^{P_i} b a^{Q_i} b ab : k ≥ 2, P_1 = P_k + 1, P_i = P_{k+1−i} inner, Q_i free} ⊆ Q (checked ≤ 30);
   marker criterion (one-class certificates primitive iff for every prime r | ℓ the classes divisible by ℓ/r
   contain a marker class — exact for ℓ ≤ 6); adjacent-axis lemma (axes c, c−1 never give crossing chords);
   coordinator's observation (ii) FAILS: power-free stratified realisations exist for every k.
   CL4 barrier: Lemma W + corollary — if u has no unary run of length λ and no period ≤ 2mλ, replacing any
   window of length ≤ m in a·u·u never yields a power; so local surgery needs windows Ω(n / log n).
3. Missing: large-window interchange forcing a power (stronger than goal).
   Coordinator note: single-length interchange is already blocked by rectangles.md (Q ∩ Σ^n is a union of
   2⌈n/3⌉ rectangles inside Q, which also cover J ∩ Σ^n), so this missing step cannot hold at a single length.
4. Counterexamples: to CL3 (second independent one); to observation (ii).
5. Stronger than Q ∉ CFL.
6. Reopen: a cross-length surgery principle for J.

## fold (done, follow-up sent)
1. Aim: CF fold-count line certificates with density ≫ n^{-1/2}.
2. Proved: certificate G re-verified (p divides m_c and n, any parity); exact line targets per n mod 8;
   union over axes U has density → 1 (PROVED for odd n via independence of different axes' mirror-pair
   forests + Chebyshev, P(miss) ≤ C/√n; even n computer-checked: 0.925, 0.959, 0.968 at n = 18, 20, 22, MC ≥ 0.998
   for n = 100..1012); fixed-axis languages Φ_R = {|w| − 4m = R} and F_r are NOT CF (Ginsburg on a^i b^j a^k,
   homogeneity of f = i+j+k − 4 min(j, |i−k|)); even-linear fold languages with bounded matched−mismatched
   have exponentially small density.
3. Missing: is the rotation-closed union U itself CF? (Φ not CF does not imply Cyc(Φ) not CF.) A CF
   L ⊆ Φ_{±1} with density ≥ n^{-1+δ} would already refute Q½.
5. Stronger/equal: U CF ⇒ Q½ false (density route dead); U not CF ⇒ consistent with Q½.

## walk (done) — Q½ REFUTED (pending audit5)
1. Aim: CF variant of the walk-window certificate W with density ≫ n^{-1/2}.
2. Proved: T-operator. P = first-passage pieces z·a (z ∈ B, Dyck with b opening); σ: a ↦ a, b ↦ {z·a : z ∈ B∖ε};
   T(M) = Cyc(σ(M)) ∪ swap(Cyc(σ(M))). Lemma: M CF, M ⊆ Q ⇒ T(M) CF and ⊆ Q (unique first-passage decomposition
   of a word ending at a strict maximum; a power x^p decodes to Φ(x)^p). T(E′) has exact count formula and
   |T(E′)_n| ≥ c·2^n n^{-1/4} for odd n (PROVED). T^k(E′) CF, sound, density ≍ n^{-2^{-(k+1)}} (outline + MC:
   0.135, 0.567, 0.867 at n = 100001 for k = 1, 2, 3). Weighted variant covers even n at n^{-1/4}.
   Consequences: Q½ FALSE; dense.md's CRH FALSE; Theorems P, P^R do not extend to all CF L ⊆ Q.
3. Missing (density route): is there a CF L ⊆ Q with positive upper density? N_∞ (iterate until one letter)
   is sound with heuristic density → 1; CF status open.
5. 'Every CF L ⊆ Q has density o(1)' still implies Q ∉ CFL and is stronger.

## cl1 → CL4 (done)
- P1 (proved): words of J have |w|_a odd, so CL4 ⇔ every CFL ⊇ J contains an odd power v^q (q ≥ 3).
- P2: bounded level-set certificate C_O^B (reflection, level set of size s ≤ B with gcd(s, K) = 1; sound by
  builder2's orbit lemma) covers 197–200 of 200 random J members but no fixed B covers J (needed s grows linearly).
- P3 (proved): φ: 0 ↦ ab, 1 ↦ aab preserves primitivity both ways and φ(1y0y) = a·u·u, so CL5 ⇒ CL4:
  CL5: every CFL containing T = {1y0y : y ∈ {0,1}*} contains a non-primitive word.
  Up to rotation/swap, T = words at Hamming distance 1 from a square (exactly one antipodal mismatch pair).
- Single-reflection finite-control barrier: conjectured, not proved.
Coordinator note: 'exactly one antipodal mismatch' is a sound certificate (an odd power's antipodal mismatch
set is a union of orbits of odd size ≥ 3), but verifying the other n/2 − 1 antipodal equalities is copy-like.

## fold follow-up (done)
- Lemma H (proved): m_c ≤ min(|w|_a, |w|_b), so U ⊆ H = {both counts ≳ n/4}.
- Lemma NC (proved): on every slice (a*b*)^K, every asymptotic direction of H is covered by non-crossing
  2-coordinate periods — the Ginsburg cone argument cannot show U (or Cyc(Φ_R)) non-CF on any bounded slice.
- Computer: on 4- and 6-block slices U agrees with H except for congruence (parity-skip) gaps, which are semilinear.
- Conjectured: U ∩ every bounded slice is CF; deciding U needs an unbounded obstruction. If U is CF it is a
  density-1 CF subset of Q (refutes Q½, not a resolution).
