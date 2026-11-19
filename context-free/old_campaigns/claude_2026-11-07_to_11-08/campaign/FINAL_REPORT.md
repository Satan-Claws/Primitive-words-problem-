# Is the language of primitive words context-free? Campaign report

**Bottom line: not resolved.** After three rounds (14 agent runs: 12 research and computation runs, 2 audits) neither direction was proved. No PDA with L(P) = Q was found, and no proof that none exists was found. Everything below is partial progress, which the brief explicitly says does not count as a resolution. It is reported here so that the next attempt starts from the right place.

The detailed per-route reports are in `round1/`, `round2/` and `round3/`. The approach registry with every verdict is `REGISTRY.md`. Status labels: **proved** means it passed an independent audit; **claimed** means it has not been audited.

---

## 1. What was established

### 1a. Barrier theorems: methods that provably cannot work

| Result | Status | Consequence |
|---|---|---|
| **Rectangle cover** (G Thm 2/3): Q∩Σⁿ is an exact union of O(n) balanced rectangles contained in Q (≤ 8 for odd n), using non-wrapping windows. | proved (audit K, with fix) | Fooling-set, rectangle-cover and communication-complexity lower bounds on CFG size for Q∩Σⁿ are at most O(n), so they are useless. |
| **Interchange barrier** (B Thm 1): for any R ⊆ Q∩Σⁿ and any window, some Z ⊆ R with \|Z\| ≥ \|R\|/(e(ω(n)+1)) has all cross-swaps primitive. Multi-cut version loses only (8m)^{ω(n)}. | proved | Q satisfies the conclusion of the Ogden–Ross–Winklmann interchange lemma with huge slack. No interchange argument can refute Q. |
| **No fooling pairs** (C Lemmas A, B, Thm 1): distinct non-primitive words of equal length differ in ≥ 2 positions, and in exactly 2 only at distance n/2. For any two primitive words and any scale there is a swap interval keeping both primitive. | proved | Single cross-word subtree swaps cannot refute Q. |
| **Analytic barrier** (D Thm 2): an explicit binary 2-ambiguous CFL has a non-algebraic, non-D-finite GF with the same singular features as Q's. | proved | Petersen-style generating-function arguments cannot pass beyond unambiguous grammars without a new structural lemma. |
| **Closure-chain reduction** (A, repaired by audit K): any chain of permitted operations from Q is a single rational transduction of Q (Q is closed under rotation and reversal). Ogden is preserved by rational transductions. | proved (constant (2s+1)p; the general cyclic-shift claim is withdrawn) | Closure reductions plus Ogden refute Q **iff** Ogden fails on some π⁻¹(Q)∩R. Reductions add only regular annotation. |
| **OG(Q) reformulation** (H Thm 1, 2, 5, Lemma U, Cor 5.3): OG(Q) ⇔ Ogden for Q with colour-loop pumps under arbitrary colourings. Annotation cannot block synchronized partner loops. Rigidity kills every design whose marked pumps sit in periodic runs that have a nearby partner. | proved (with margin fixes) | Pins down where a pumping counterexample would have to live. |
| **Gap G, dense case** (M Thm M1): in a fully marked buffer with no long periodic runs, some colour-loop pump is good. | proved (audit N, with fix) | Most remaining pumping-based designs are dead. |
| **Fixed-run slices satisfy Ogden** (J Thm 5): Q∩(a⁺b)^r satisfies plain Ogden for p ≥ p₀(r). | proved (audit N supplied the antipodal case) | Pumping within a fixed run structure can never refute Q. |

### 1b. Positive results about restricted languages

- **F₆ = Q∩(a⁺b)⁶ is context-free** (I). By Ginsburg–Spanier, this means the exponent set S₆ = ℕ⁶∖(P₂∪P₃) is a finite union of stratified linear sets.
  - The explicit cover has 464 linear sets (`round2/I_bounded_m6_linear_sets.json`).
  - The audit regenerated them independently, proved they avoid P₂∪P₃ on all of ℕ⁶, and checked that their union equals S₆ on [0,12]⁶. **Proved.**
  - The construction is built from a P₃-witness and a P₂-witness nested without crossing, using partial-sum functionals (e.g. {x₁≠x₄ ∧ x₁+x₂≠x₃+x₄}).
- **F_m for every m ≤ 24 with ≥ 2 prime factors**: covered by "one-turn gap frameworks". This is computer evidence only (ranks mod a prime); m = 30 is unsettled. **Conjecture:** every F_m is CF, so no fixed-block slice refutes Q.
- **Q∩(a⁺b)⁴** has an explicit CFG, checked exactly up to length 18.
- **Q∩(a⁺b)⁺ CF ⇔ Q CF** (proved). So a construction that works uniformly in the number of blocks would be a full resolution.

### 1c. Non-context-freeness of relatives (none transfers to Q)

- **Unbordered words are not CF** (J; proved). **Already known:** Rampersad, Shallit and Wang, "Inverse star, borders, and palstars" (IPL 2011, arXiv:1008.2440), also via Ogden. Not a new result. Ogden on z = a^{p+1}b a^{p+p!}b a^{p+1+p!}b a^p b, with run 1 marked. This kills the most natural transversal route: unbordered words meet every primitive conjugacy class, so their being CF would have given Q CF.
- **MP_c = {min period > n/c} is not CF for 1 < c < 5/4** (L Thm A; claimed). Exhaustive checks found 0 surviving decompositions.
- **L_mid = {no square centred at the middle cut}** meets every primitive class but is not CF (L Thm B; claimed).
- Q ∩ {no border ≤ f(n)} is not CF for every unbounded f (J; claimed).
- Each of these proofs works because the complement contains a full-dimensional piece (words with a long border). Q's complement, the exact powers, has no such piece.

### 1d. Errors caught by the audits

- "c·n ≤ min CNF size of Q∩Σⁿ" was **false**: prime lengths have O(log n)-nonterminal grammars.
- "OG is closed under cyclic shift" (A) had a real gap. It was withdrawn and the conclusion repaired via rotation-closure of Q.
- "π⁻¹(Q)∩R satisfies Bar-Hillel" (M Cor M3) is **flawed**. It breaks at the i = 0 deletion step, where a short run drops out of the skeleton (σ = a¹⁴, T′ = 14, v = a). It is currently unproved.

---

## 2. The common core every route hit

Independent routes (B, E, H, I, L) all stalled at the same configuration:

> a word that, after one local edit per candidate, becomes an exact q-th power for unboundedly many different primes q, together with the Fine–Wilf theorem failing exactly at near-squares.

On the **negative** side, any refutation must use relations **across lengths**, and must handle pumps that change the run structure. Single-length combinatorics is provably dead (§1a), and so is pumping inside a fixed run structure.

On the **affirmative** side, a PDA must refute every prime divisor of n using non-crossing comparisons whose distances cannot be tied to n (E's semilinearity obstruction, I's index-matching obstruction). For each fixed block count this can be done (F₆), but no uniform mechanism was found.

## 3. Open sub-problems isolated (each would advance the main problem)

| Sub-problem | Direction if resolved | Strength |
|---|---|---|
| **Gap G_sp**: Gap G for sparse Ogden markings (unbounded loop lengths). Plus the repair of Cor M3 at i = 0. | Proving it, and so OG(Q), kills every closure + Ogden route. Refuting it proves Q not CF. | Agent M did not claim it is theorem-strength. This is the most concrete open lemma found. |
| **Is MP = {min period > n/2} CF?** | CF ⇒ Q CF (affirmative). | Needs CF certificates for "∀ℓ ∈ (n/4, n/2]: no centred repetition", i.e. crossing translation comparisons. Judged theorem-strength. |
| **MP_c for 5/4 ≤ c < 2.** | Any CF one gives Q CF. | Conjectured not CF. |
| **"Index-mass rigidity"** (I). | Would give a non-CF proof of Q∩(a⁺b)⁺. | Theorem-strength. |
| **F_m for m with ω(m) ≥ 3** (m = 30). | A non-CF F_m proves Q not CF. | Evidence says all are CF. |

## 4. Approaches closed by this campaign

Interchange and fooling sets; rectangle and cover size bounds; single-swap derivation-tree arguments; generating functions beyond unambiguity; closure reductions (reduced exactly to OG(Q)); unbordered and Lyndon transversals; single-functional certificates (cyclotomic barrier); single-marked-mismatch PDAs (semilinearity); Ogden inside fixed run structures; critical-factorization local witnesses; SAT minimum-grammar growth at feasible n (≤ 9), which cannot distinguish Q from the non-cubes.

## 5. Testing guidance for future candidates

Agent I's sound CF family U_K covered every primitive class up to length 21, then failed at length 22 and on scaled words t·x. Testing to length 20 is **not** adequate. Candidates should also be tested on scaled run-length families, long {1,2}-run sequences and near-powers. The tester is `tools/check_grammar.py`.
