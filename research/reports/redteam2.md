# redteam2: adversarial review of ambiguity.md and density.md

Agent "redteam2". Scripts: `scratchpad/scripts/redteam2/` (all single-core).
- `mobius_check.py`: Lemma 3.1 by brute force, and the reduced denominators for n ≤ 9.
- `thmC_check.py`: Theorem C. Each grammar is checked separately on ALL words of length ≤ 15/14/13.
- `thmA_random.py`: random CNF grammars × DFA of (ab\*)^2. Checks the Step 1 and Step 2 invariants.
- `thm1_check.py`: density Theorem 1 and Lemma M, independent implementation, plus a mutant control.
- `density_examples.py`: E', O2 and the O3 parity remark.

## 1. ambiguity Theorem A / A′: CONFIRMED (proof correct). Novelty: largely KNOWN.

Each step was checked by hand.

- **Lemma 1.1.**
  - ε-removal: the injection works because a node's rule A→α' can be read back after deleting the empty-yield subtrees.
  - Unit cycles created by ε-removal (e.g. A→AB with B nullable gives A→A): these would give infinitely many G'-trees. Φ is injective, so they would also give infinitely many G-trees. So they are excluded by finite ambiguity. OK.
- **Lemma 1.2.**
  - Annotations are forced. OK.
  - Sink-annotated nonterminals cannot reach state n, so they are useless and disappear on reduction. OK.
- **Step 1 (nonlinear SCC ⇒ Catalan).**
  - With annotations it is cleaner than written. X=(s,·,t) and X ⇒\* uXvXz force t→…→s. States are monotone, so s=t, and everything under X is b-only. The "useless symbols" worry is handled by reduction.
  - "SCC generating finitely many words" cannot happen for a non-trivial SCC: in CNF every cycle adds non-empty material.
  - Distinctness of arrangements holds even for X→XX (|uvz|=0), since 2|w|>|w|.
  - The claim does NOT extend to bounded languages in general as phrased ("only linear SCCs"). Here it relies on the a-counting annotation, which makes nonlinear parts unary. Within the theorem's scope it is correct.
- **Step 2.** The annotation argument gives Z=(t,·,t), resp. (s,·,s), and Y=(s,·,t). OK.
- **Step 3 (Cramer).**
  - Entries of M are univariate rational functions in y_s or y_t with zero constant term.
  - det(I−M)=N/H with N∈ℚ[y_s,y_t] and N(0)=H(0)≠0. adj has univariate denominators. So (I−M)^{-1} ∈ R.
  - Restricting F_Z to one variable is a ring homomorphism on {P/Q : Q(0)≠0}. OK.
- **A′.** Pairs from Y ⊂ [s,r] and Z ⊂ [r,t] cannot cross, because k ≥ r ≥ j. The outer pair (s,t) contains both. OK.
- **Random test (`thmA_random.py`, 300 grammars).**
  - Step 2 invariants (one state pair per SCC; side nonterminals b-only in the correct state) held in every case.
  - All 160 grammars with a useful nonlinear SCC showed superpolynomially growing max-ambiguity (e.g. 1,4,28,240,2288).
  - The 8 rows printed as "bounded?" are a parity artefact of my crude criterion; they too grow.
- **Novelty.**
  - The unambiguous case of A, and the non-crossing refinement A′, are the generating-series form of Ginsburg–Ullian (JACM 1966): unambiguous bounded CFL ⇔ disjoint union of stratified linear sets, and "stratified" means exactly ≤2-coordinate periods that do not cross.
  - Koechlin (FSTTCS 2022, LIPIcs 250:41) explicitly translates Ginsburg–Ullian into generating-series criteria. These are a "3-variable criterion" and an "interlacing" criterion, the latter matching A′.
  - New, as far as I can tell: the extension to *finitely ambiguous* grammars (multiplicity series). It is correct.

## 2. Theorem B: CONFIRMED (correct). Novelty: the n=3 case is KNOWN.

- **Lemma 3.1.**
  - The Möbius sum is Σ_{d | n/s₀} μ(d) = [s₀=n]. OK.
  - A word is non-primitive iff its exponent vector is periodic with a proper divisor period. OK.
  - Brute-force check (`mobius_check.py`): coefficients match primitivity for every vector with entries ≤ 4 (n ≤ 5) or ≤ 2 (n = 6, 7). 0 mismatches.
- **Lemma 3.2.** Irreducibility of 1−Πy_i holds. The degree-1 argument is fine.
- **Survival of f in the reduced denominator.**
  - f = 1−m_{n/q,1} occurs only in the d=q term, with coefficient μ(q) = −1. All other denominator factors are distinct irreducibles (or linear).
  - The partial-fraction argument (H = Pfg ⇒ f | H) is valid.
  - f ∤ E holds because E is a product of ≤2-variable polynomials and f is prime with q ≥ 3 variables.
  - Independently, sympy factors the reduced denominator for n = 2..9 and finds f present for every odd q | n.
  - The numerator is non-zero at a random rational point of {f=0}, so f is a genuine pole.
  - Factor variable-counts: n=3 [1,1,1,3]; 5 [..,5]; 6 [..,2,2,2,3,3,6]; 7 [..,7]; 9 [..,3,3,3]; n=2,4,8: max 2.
- **Corollary for n=3, and Petersen.** The steps are correct: Q unambiguous ⇒ (Lemma 1.2) L_3 unambiguous ⇒ contradiction.
- **NOVELTY: the n=3 case is known.**
  - Q∩(ab\*)^3 ≅ {a^x b^y c^z : ¬(x=y=z)} via a trivial bounded-language transfer.
  - Inherent ambiguity of {aⁿbᵐcᵏ : n≠m or m≠k} was called a "long-standing open question (Autebert et al.)" and was settled by Makarov (DLT 2021, arXiv 1912.13401, "Bounded languages described by GF(2)-grammars").
  - It was re-derived by Koechlin (FSTTCS 2022) via Ginsburg–Ullian translated to generating series.
  - So the claim "new elementary proof that Q is inherently ambiguous" is best described as: Petersen's theorem follows immediately from Makarov/Koechlin plus Lemma 1.2.
  - Still plausibly new: the general n-with-odd-prime-factor statement, and the self-contained proof. It is a modest extension.
  - The report's "LITERATURE-UNCHECKED" flag should become "n=3 KNOWN (Makarov 2021; Koechlin 2022)".

## 3. Theorem C: CONFIRMED.

- **By hand.**
  - The union argument is correct, including that for prime p, primitive means non-constant.
  - U → bUb | B⁺a | aB⁺ is deterministic: the first and last letters choose the rule.
  - Blocks with a fixed number of a's, each starting with a, factor uniquely.
- **Independent check (`thmC_check.py`).**
  - I rebuilt each grammar from the report's text, binarized it, and counted trees for A1 and A2 SEPARATELY.
  - The test runs on all words over {a,b} of length ≤ 15 (p=3), ≤ 14 (p=5), ≤ 13 (p=7), not just on (ab\*)^p.
  - Every word had exactly ([x∈A1], [x∈A2]) trees, and A1∪A2 = primitive ∩ (ab\*)^p. 0 failures.
- **Inherent degree exactly 2.** This follows from B. CONFIRMED.
- **Novelty.** The decomposition is standard: for p=3 it is the classical "i≠j or j≠k" grammar.

## 4. density Theorem 1 (fixed-rate linear): CONFIRMED.

- **By hand.**
  - Lemma M: Q·f = I, φ is a permutation of I, s·f^j = φ^j(s·κ), and φ^{r!} = id. OK.
  - Step 2: x is a prefix of (u0 v)^∞ that begins at u0, so it has period d.
  - Step 3: pt' ≡ pt (mod d), and pt+|c| ≤ |u0|.
  - Step 5: qt ≤ |u0|, so the right blocks lie in the final copy of u0.
  - Step 6: d ≥ |u0| ≥ t, so (y0X)^m y0 is well defined.
  - Step 7: [Pκ(SXPκ)^{gj}S] = [y0].
  - Degenerate cases p=0 or q=0, and κ=ε (all letters act as permutations; κ is then the identity) are fine.
- **Independent test (`thm1_check.py`, seed 7, 400 random DFAs).**
  - The test covers (p,q) ∈ {(1,0),(0,1),(1,1),(2,1),(1,2),(2,0),(0,2),(3,1),(2,2)}, 2–6 states, and middles of length 0–3. κ is found by random search, with its minimality certified exhaustively up to length 5.
  - Results: 370 ok, 30 with no κ-word, 0 failures. Lemma M also held directly on 5 random Y × 3 values of j per DFA.
  - **Control:** with D=(p+q) instead of (p+q)·r!, 7 of 377 trials FAIL. So the test can detect an exponent that is too small.
- **Corollary 1.**
  - The avoidance count gives γ<2.
  - u0≠ε can be arranged, because only finitely many κ-containing y would still leave γ<2.

## 5. density Theorem 2 (class FR) and Corollary 2: CONFIRMED.

- F1, F2 and F3 hold. The F3 identity a u0(bva u0)^k b = U(vU)^k was checked by hand.
- Context case (ii): bounding the number of decompositions by Σ_t #{y avoiding κ}·|M_{n−(p+q)t}| is a valid upper bound, so γ(M)=2, and then ℓMr ⊆ L.
- The SCC-fixed-rate ultralinear languages are in FR. The induction along the SCC DAG is fine.
- **Minor gap (fixable).** "Pumpable" allows u0=ε, which means v^{Dj} ∈ L for all v. Then U=z^D gives U^{Dj+1} = z^{D(Dj+1)} ∈ L. So "u0≠ε can be arranged" holds, but the report does not spell this out.
- Q ∉ FR follows.

## 6. density limits section: CONFIRMED, with one cosmetic error.

- **O4 (E').**
  - Every member is primitive, and |E'_n| = C(n,(n−1)/2) for all n ≤ 16 (brute force).
  - E' is a deterministic one-counter language.
  - E' is not linear: in a^N b^{2N+1} a^N, the linear pumping lemma puts the pumped parts in the outer a-blocks.
  - E' ∉ FR follows from Theorem 2.
- **O1 and O2.** Correct. O2 was brute-force checked for N ∈ {2,3,4,6}, n ≤ 12.
- **O3 side remark: WRONG for odd n.** The parity of #{i ≤ n/2 : w_i ≠ w_{n+1−i}} equals |w|_a mod 2 only for even n; for odd n it is |w|_a + [middle letter = a]. 5461 counterexamples for odd n ≤ 13, 0 for even n. Harmless, because that language is even-linear and so covered by Theorem 1. Just fix the sentence.
- **Lemma 6.1.** Checked by hand: the word identity (u0 v)^m u0 (v u0)^m and the step eMe ∩ J_e = H_e. Correct.

## 7. Other notes
- D2 (every bounded CFL is finitely ambiguous) is literature (Ginsburg–Spanier/Ullian stratified decomposition), correctly labelled.
- Web search worked; arxiv.org and drops.dagstuhl.de fetches are blocked, so I relied on abstracts and talk summaries for Makarov and Koechlin.

## 8. Verdict table

| Claim | Verdict | How |
|---|---|---|
| Lemma 1.1, 1.2 (CNF and DFA product keep ambiguity) | CONFIRMED | by hand; unit cycles from ε-removal handled via injectivity |
| Thm A (finitely ambiguous ⇒ GF ∈ R) | CONFIRMED | by hand (Steps 1–3); random test of the Step 1/2 invariants on 300 grammars |
| Thm A′ (non-crossing) | CONFIRMED | laminarity by hand |
| A/A′ novelty | Unambiguous case KNOWN (Ginsburg–Ullian 1966; Koechlin 2022); finitely ambiguous version apparently new | web search |
| Lemma 3.1, 3.2 | CONFIRMED | brute force (n ≤ 7), by hand |
| Thm B (odd prime factor ⇒ inherently ambiguous) | CONFIRMED | by hand; sympy n ≤ 9 plus a pole test on f=0 |
| B, n=3 / "new proof of Petersen" | CORRECT but KNOWN: equivalent to Makarov 2021 / Koechlin 2022 | web search |
| Thm C (L_p is 2-ambiguous, degree exactly 2) | CONFIRMED | each grammar checked separately on all words of length ≤ 15/14/13 |
| Density Lemma M, Thm 1, Cor 1 | CONFIRMED | by hand; 370 random trials; a mutant control detects a wrong D |
| Thm 2 (FR), Cor 2 (Q ∉ FR) | CONFIRMED | by hand; minor u0=ε gap, fixable in one line |
| O1, O2, O4 (E') | CONFIRMED | brute force n ≤ 16 |
| O3 parity remark | FLAWED (odd n), harmless | 5461 counterexamples |
| Lemma 6.1 | CONFIRMED | by hand |
