# Open problem: is there a polynomially ambiguous grammar for the primitive words?

You are a theoretical computer science researcher working on an open problem in formal language theory.
Work in the repository branch `claude/magical-allen-ch9hzl`. All paths below are relative to its root.

**Path prefixes**
- `PA/` = `polynomial-ambiguity/claude_2026-11-18_to_11-19/reports/` (the previous polynomial-ambiguity campaign)
- `R4/` = `infinite-ambiguity/claude_round4-5_2026-11-18/reports/`
- `RESULTS_INDEX.md` lists every result in the repository with its file and status.

---

## 0. Kickoff (do this first)

After reading this prompt and before launching any agent, reply to the user with:
1. what you understood, in at most 15 lines:
   - the exact target statement;
   - which results you will rely on and their status;
   - the main obstruction;
   - your planned first round of tasks (one line each);
2. any questions, or any files or information you want.

Then **wait for the user's answer**. Do not start the search until the user confirms.

---

## 1. The problem in one paragraph

Does there exist a context-free grammar G whose language is exactly the set of primitive words, and whose
ambiguity is polynomially bounded? Polynomially bounded means every word w has at most C·|w|^k derivation trees,
for constants C and k depending only on G. In other words, G accepts every primitive word and rejects every
non-primitive word.

The conjectured answer is **no**.

The finitely ambiguous case is already settled: **no finitely ambiguous grammar generates the primitive words**
(Lean-checked). The next step is to show that no polynomially ambiguous grammar does either. It is still not
known whether the primitive words are context-free at all.

---

## 2. Notation and definitions

**Words and primitive words**
- Σ = {a, b}. Σ* is the set of finite words, including ε. Σ⁺ = Σ* \ {ε}.
- |w| is the length of w. For u ∈ Σ* and n ≥ 0, uⁿ is u repeated n times.
- w ∈ Σ⁺ is *primitive* if w ≠ uⁿ for every u ∈ Σ⁺ and every n ≥ 2. Exponent 1 is allowed, and ε is not primitive.
- Q is the set of primitive words over Σ.

**Grammars**
- A CFG is G = (V, Σ, R, S).
- G is *cycle-free* if there is no nonterminal A with A ⇒⁺ A.
- A *derivation tree* for w is an ordered tree with root S, internal nodes expanded by rules of R, and frontier w.
- amb_G(w) is the number of derivation trees for w. It is finite for every w when G is cycle-free, and
  amb_G(w) = 0 for w ∉ L(G).
- The *ambiguity function* (Wich) is A_G(n) = max_{|w| ≤ n} amb_G(w).

**Degrees of ambiguity**
- G is *finitely ambiguous* if sup_w amb_G(w) < ∞.
- G is *polynomially ambiguous* if there are constants C > 0 and k ∈ ℕ with amb_G(w) ≤ C·|w|^k for all w ∈ Σ⁺.
  Since ε ∉ Q, amb_G(ε) = 0 for any G with L(G) = Q.
- G is *exponentially ambiguous* if A_G(n) ≥ cⁿ for some c > 1 and infinitely many n.

**Slices**
- A *slice* is Q ∩ L(D) for a DFA D.
- A *bounded slice* is a slice whose regular part is contained in w₁* w₂* ⋯ w_r* for fixed words w_i.
- For a word w ∈ (ab*)ⁿ, written a b^{x_1} a b^{x_2} ⋯ a b^{x_n}, its *exponent vector* is
  exp(w) = (x_1, …, x_n) ∈ ℕⁿ.
- R_m = a(ab⁺)^{m−1} a (ab⁺)^{m−1} is the slice family of `finitely-ambiguous/PROOF.md` §1.

**Anti-misreading clauses**
- The bound is **per word**: amb_G(w) ≤ C|w|^k for each word. It is not a bound on the total, or on the average,
  over words of a given length.
- C and k are **constants of the grammar**. They do not depend on w, on the slice, or on any block count.
- The polynomial is in the **word length |w|**. Polynomial in a slice parameter does not count, unless |w| is
  controlled by that parameter in both directions.
- The statement is **inherent**: it quantifies over all cycle-free G with L(G) = Q. A lower bound for one grammar,
  or for a natural family of grammars, proves nothing.
- For the negative resolution the violating word may come from any sparse family. For each C and k, a single
  word with amb_G(w) > C|w|^k suffices.

---

## 3. The problem, exactly

Determine whether there is a cycle-free CFG G with L(G) = Q and constants C, k such that amb_G(w) ≤ C|w|^k for
all w ∈ Σ⁺.

**Affirmative resolution.** Give G explicitly. Prove L(G) = Q for every length. Give C and k explicitly, and prove
the bound for every word by an exact count of derivation trees. This would show Q is context-free and refute the
Dömösi–Horváth–Ito conjecture, so it must be audited with that in mind.

**Negative resolution.** For every cycle-free G with L(G) = Q and every C, k, there is w with
amb_G(w) > C|w|^k. By Wich's dichotomy (§4.1), this is equivalent to: every cycle-free grammar for Q is
exponentially ambiguous.

The two resolutions are exact complements. Assume a complete resolution exists, but do not assume in advance
which way it goes.

Do **not** replace the target by:
- "Q is not finitely ambiguous" (already proved);
- "amb_G grows at least like |w|^k for one fixed k";
- "the total excess is exponential";
- "Q is not context-free". That would suffice, but it is a strictly harder open problem and is not the goal.

---

## 4. What is known

Status labels, to be kept in every output:
- **[published]**
- **[Lean-checked]**
- **[audited report]**: written proof plus an independent red-team audit
- **[written proof]**: not audited
- **[computational]**
- **[assessment]**: someone's analysis, not checked
- **[conjecture]**

Nothing from the previous polynomial-ambiguity campaign (`PA/`) has passed a gated audit. Treat every `PA/` item
as [written proof] at best, and reconstruct any step before relying on it.

### 4.1 Published
- **[published]** Petersen (TCS 161, 1996): Q is not an unambiguous CFL. Q is not deterministic CF, and Q is not
  linear (S. Horváth 1995).
- **[published]** Wich, DLT 1999, "Exponential ambiguity of context-free grammars". Read in full; see
  `PA/poly_WE.md`.
  - **Dichotomy.** For cycle-free G, A_G(n) is either 2^{Θ(n)} or O(n^d), with d effective (Thm 4.3, Thm 4.4,
    Cor 6.1).
  - **Criterion C_exp (Def 2.7).** There exist A ∈ N and α, β ∈ (N ∪ Σ)* with am_G(A, αAβ) > 1, where αAβ has
    no useless or ε-symbols. In words: two distinct pumping trees at A with the same interface. G is
    exponentially ambiguous iff C_exp holds.
  - **Sufficient tests.** Cor 3.20: pumping trees with interfaces (α^k, β^l) and (α^m, β^n), lm ≠ kn. Cor 3.21:
    some A is both left- and right-recursive.
- **[published]** Wich, MFCS 2001 (abstract read verbatim): PCFL, the class of languages with a polynomially
  ambiguous grammar, is the closure of the unambiguous CFLs under projections that erase only Parikh-bounded
  symbols.
- **[published]** Flajolet (1987) on transcendental generating series; Koechlin (FSTTCS 2022). Check their
  hypotheses verbatim before use.
- **[published]** Lyndon words are not context-free (Berstel–Boasson 1997, as recalled in `PA/poly_S4C.md`;
  confirm before use).

### 4.2 Main local results

1. **[Lean-checked; audited] No finitely ambiguous CFG generates Q.**
   - Files: `finitely-ambiguous/PROOF.md`, `finitely-ambiguous/lean/FiniteAmbiguity/Main.lean`.
   - On R_m, some word of Q ∩ R_m has at least ⌈m/2⌉ trees. Do not reprove this.
2. **[written proof] No linear grammar generates Q** (`context-free/reports/finiteindex.md`).
3. **[audited report] Q ∉ FR** (fixed-rate metalinear / ultralinear) (`context-free/reports/density.md`, audit
   `redteam2.md`).
4. **[audited report] Exponential total excess.** limsup e_G(n)^{1/n} > 1 (`context-free/reports/rectangles.md`
   Thm 5.2). Under polynomial ambiguity the rate is automatically ≤ 2, so this cannot give a per-word bound.
   **Blocked.**
5. **[written proof] Exponent vectors.** For fixed block count, primitive vectors outside the sum of periodic
   subspaces form a CFL (`context-free/reports/devil.md`).
6. **[written proof] Theorem P (best unconditional result so far).** For every cycle-free CFG G with L(G) = Q,
   A_G(L) = Ω(√(log L / log log L)).
   - This is conditional in form: *if* a grammar exists, it is at least this ambiguous.
   - It quantifies "not finitely ambiguous". It is far below polynomial.
   - Proof chain: `PA/POLY_FINAL.md` §1.
7. **[written proof] Conditional Theorem P′** (`PA/poly_S3P.md`). If one (2p−1)-pair face has facet heights and
   lattice exponents bounded by (pK)^{O(1)}, then A_G(L) = Ω(log L / log log L).

### 4.3 Structure of a polynomially ambiguous grammar on slices (the core toolkit)

Let G be a cycle-free grammar for Q with amb_G ≤ C|w|^k.

- **Reductions [Lean-checked].** CNF conversion and the product with a DFA never increase tree counts. So for each
  n there is a reduced CNF grammar G_n for Q ∩ (ab*)ⁿ (or any sub-slice), with the same C and k.
  - The grammar constant K = |V''|·2^{4|V''|+2} depends only on G, not on n (`PA/poly_T2b.md` §1).
- **Structure part (c) survives [written proof].** `PA/poly_P.md` §1: two first-return contexts at one nonterminal
  give 2^N trees on one word of length O(N). The argument uses only commuting b-insertions, not finite ambiguity.
  So every nontrivial strongly connected component of G_n is a simple ring, and side subtrees are unique.
- **Lemma 3P [written proof]** (`PA/poly_P.md` §2):

  amb(w) = Σ_σ P_σ(exp(w) − c_σ).

  The terms are as follows.
  - σ ranges over finitely many *skeletons*: at most exp(O(n)) of them, with ‖c_σ‖₁ ≤ nK.
  - P_σ(u) = #{q ∈ ℕ^{V_σ} : Σ q_v v = u} is the vector partition function of the list V_σ of *ring vectors*.
  - Each ring vector has support on a pair {s,t} of blocks (or one block), with ‖v‖₁ ≤ K.
  - The pairs of one skeleton are **laminar**: no two cross in the block order.
  - The degree satisfies d_σ = #V_σ − rank V_σ ≤ k uniformly. By Ito / Eilenberg–Schützenberger refinement one may
    take d_σ = 0 (`PA/poly_S3D.md`).
- **Pieces, covers and ply.**
  - The *piece* of σ is L_σ = c_σ + ℕV_σ.
  - The pieces cover every primitive exponent vector and contain no non-primitive one.
  - The *ply* at x is #{σ : x ∈ L_σ}, and amb ≥ ply.
  - So a negative proof via slices means: on some slices, every such laminar cover has a point of large ply whose
    norm (word length) is small.
- **Lemma C and Lemma G [written proof]** (`PA/poly_G3.md` §1).
  - Lemma C: pieces meeting the witness lattice have c_σ ∈ ℤV_σ.
  - Lemma G: every lattice point of Λ_S = ∩_{σ∈S} ℤV_σ inside ∩_{σ∈S}(c_σ + cone V_σ) has amb ≥ |S|.
- **Lemma F, face restriction [written proof]** (`PA/poly_G4.md`). Fixing all but r diagonal pairs of R_m to 1
  gives a valid cover of a smaller R-slice with the same K.

### 4.4 The live approach to the negative resolution: Lemma G* = TILE_k + G3**

**Why slices with many blocks.** Fixed-block slices, and R_m, can only force about linear ambiguity: each has a
grammar with ambiguity m − 1. Also:
- off W_n = Σ_{p | n} V_p, ambiguity ≤ φ(n) is always achievable (`PA/poly_T1.md` P1);
- when n is a prime power, every slice of (ab*)ⁿ is at most linearly ambiguous.

So large ambiguity must come from primitive vectors inside W_n, for n with many prime factors. Here V_p is the
set of shift-(n/p)-invariant vectors.

**Candidate slice family S_N [conjecture]** (`PA/poly_T1.md` P4).
- Take n = P_N², where P_N is the product of the first N primes p_1, …, p_N.
- U = ∩_k V_{p_k} is the space of P_N-periodic vectors.
- Choose subspaces E_k ⊆ ∩_{j≠k} V_{p_j} with E_k ∩ V_{p_k} = 0, so that d_k = dim E_k = P_N(p_k − 1).
- Near a positive base point tω (ω ∈ U), a vector x = tω + δ with δ = (δ_1, …, δ_N) ∈ ⊕E_k is primitive
  **iff every δ_k ≠ 0**. This is the "for every prime, some witness" structure.
- The natural cover has ply ∏ d_k ≥ n^{N/2}, which is superpolynomial in n.

**Budget [assessment].**
- Ply ≤ #skeletons ≤ exp(O(n)), and log(n^{N/2}) ≈ N² log N with log n ≈ 2N log N.
- So witness words must have length n^{o(N)} = exp(o(log² n / log log n)).
- Any argument producing witnesses of length exponential in n (such as the N!/determinant trick of `PROOF.md` §5)
  is useless.

Lemma G* (`PA/POLY_FINAL.md` §2) says: on S_N, every valid laminar cover has a point of ply n^{ω(1)} and norm
n^{o(N)}. With Lemma 3P and Lemma G this gives the negative resolution. It splits into two open parts.

**(i) TILE_k: the ply side.** See `PA/poly_LAM.md`, `PA/poly_GLAM.md`, `PA/poly_GLAM2.md`, `PA/poly_S2P.md`,
`PA/poly_S2Y.md`, `PA/poly_S3*.md`.
- **Convex geometry is not enough [written proof].** Ignoring laminarity, the product region ∏(E_k∖0) has a cover
  of ply only √n·polylog n, by VC-dimension sampling (`PA/poly_T2a.md` §2). Laminarity is the only possible source
  of superpolynomial ply.
- **Local form.** Near a base point ω, a laminar piece restricts, for each k, to a half-space {μ_k > 0} on E_k.
  - The facet μ_k is realised by a **non-crossing two-coloured tree T** built from the ring-vector support graph.
  - T is *valid at ω* iff, for every subtree u, the scalar ⟨fold(μ|_{S_u}), ω⟩ has the sign of u's top vertex.
    Here "fold" sums coordinates over residue classes mod P_N, called *fibres*.
  - The set of ω where T is valid is an open polyhedral cone K_T ⊆ U_{>0}. On walls a lexicographic rule applies,
    fixed by c_σ.
- **Proved facts [written proof].**
  - (a) Facets touching ≤ s fibres force ply ≥ (P_N/2s)^N = n^{ω(1)} for bounded s (`PA/poly_LAM.md` §1).
  - (b) A tree valid at *every* ω has single-fibre facets (fold lemma, `PA/poly_GLAM2.md`). So covers made of
    ω-uniform pieces have superpolynomial ply.
  - (c) At *any single* ω, low-ply laminar covers exist (`PA/poly_LAM.md` §2, `PA/poly_S2W.md`).
  - (d) Patching local covers gives ply ≤ ply_VC · ∏_k q_k, where q_k is the maximum number of chosen trees whose
    cones contain one point (`PA/poly_S2P.md`). Walls are not double counted.
  - (e) No tree is valid near two different vertices of the ω-simplex once M ≥ poly(n) (`PA/poly_S3V.md`).
- **Open question TILE_k.** Can one choose finitely many trees whose validity cones K_T cover U_{>0} with every
  point in at most p_k^{O(1)} of them?
  - If yes for all k, S_N is blocked at the geometric level, modulo grammar realisability.
  - If no, the ply side of the candidate holds.
- **Already dead.** Order-cone selection: Q1 is false at n = 36 (exhaustive interval DP, `PA/poly_S3A.md`), and
  abstractly it needs D ∈ {P−1, P} trees (`PA/poly_S3E.md`, `PA/poly_S3L.md`). Numerical tiling tests at n = 36
  were inconclusive (`PA/poly_S2X.md`, `PA/poly_S3T.md`).

**(ii) G3**: the length side.** See `PA/poly_G3.md` §4, `PA/poly_T2b.md`, `PA/poly_S3H.md`, `PA/poly_S2L.md`.
- For a set S of overlapping pieces, three quantities must be at most poly(n)·K, or n^{o(N)}:
  - the **apex** of ∩_S(c_σ + cone V_σ);
  - the **covering radius** of the joint lattice Λ_S;
  - the **inradius** of ∩_S cone V_σ.
- **Known [written proof].**
  - Theorem E gives ply ⌈m/2⌉ on R_m only at length exp(O(m² log mK)).
  - Lemma H: the genericity-hyperplane count adds nothing beyond the inradius.
  - Lemma S2T′: polynomial facet heights, quotient exponents and depth constants give polynomial-length witnesses.
  - Ply 2 is always reachable at length 2m + K^{O(1)} (`PA/poly_S3F.md`).
- **Obstacle [written proof].** The laminar chain {e_1} ∪ {e_i + 2e_{i+1}} has lattice index 2^ρ. A fixed grammar
  fragment Y → bYbb realises it on every spaced slice (`PA/poly_R3a.md`). Two laminar pieces can have only
  exponentially large common points: ℕ(1, 2, …, 2^ρ).
- **Open.** Whether a valid cover can force every high-ply point to be exponentially far out
  (`PA/poly_G4.md` §4).

You may pursue this approach, refute it, or replace it. Its definitions are spread over the files cited. Reading
`PA/POLY_FINAL.md` §§1–2 and §§5–7 first, then the cited sections, is the fastest way in. §2 of that file
predates the refutation of G-LAM′, so use §§5–7 for the current form.

---

## 5. Equivalent and related problems

Each item is [written proof] or [published] as marked. Use them to change the viewpoint, not to reprove things.

1. **Wich projection form [published].** A polynomially ambiguous grammar for Q exists iff Q = h(L) for a single
   unambiguous CFL L over Σ ∪ Γ, where every γ ∈ Γ occurs at most c times per word and h erases Γ
   (`PA/poly_M.md`).
2. **Exponential form [published].** Negative ⇔ every cycle-free grammar for Q satisfies C_exp.
3. **Cyclic-closure form [written proof + computational].** Q has a polynomially ambiguous grammar iff some
   CFL L ⊆ Q meets every conjugacy class [w] with polynomial class mass Σ_{r ∈ [w]} amb_L(r)
   (`PA/poly_S4C.md`).
   - The exact construction has amb_{G′}(w) = Σ_j amb_G(rot_j w).
   - Classes with coprime letter counts have an unambiguous one-counter representative language for each fixed
     ratio. Classes with gcd ≥ 2 lead back to the same problem.
4. **Bounded-exponent slice [written proof].** Q ∩ (ab + abb)* = h(Q) for h(a) = ab, h(b) = abb. Pulling back
   along h preserves tree counts exactly, so this slice is the whole problem (`PA/poly_T1.md`, `PA/poly_S4M.md`).
5. **Balanced slice [written proof].** Q ∩ {#a = #b} is at least as hard as Q. It is equivalent to primitive
   necklaces over the Dyck-prime code (`PA/poly_S4N.md`).
6. **Two-letter-run slices [written proof].** (a⁺b⁺)ⁿ gives the same covering problem as (ab⁺)^{2n}
   (`PA/poly_S2R.md`).

---

## 6. Traps and blocked routes (do not reopen without a materially new mechanism, stated in one line)

**Counting and analytic**
- **The count sandwich.** Arguments using only q_n ≤ d_n ≤ C n^k q_n, univariate or multivariate, are satisfiable
  (e.g. d_n = 2ⁿ).
- **Total excess** in `rectangles.md`: the rate is ≤ 2.
- **Marker-variable or cut-uniqueness arguments** via Wich's projection (`PA/poly_M.md`, M1, M2). Uniqueness fails
  exactly where transcendence holds.
- **Rank or communication bounds at one split.** Q's matrix at any split has nonnegative rank O(n) with entries in
  [1, n/3] (`PA/poly_S4R.md`). An argument must link different splits.

**Structural**
- **Restricted classes.** Polynomial ambiguity forces no global restriction: D1·b is unambiguous, branching,
  inside Q, not FR and not finite index (`PA/poly_T3.md`).
- **Pumping on letter-count families.** Families such as x^p y lie inside DCFLs {r#a − s#b = ±1} ⊆ Q, so Ogden and
  Lyndon–Schützenberger arguments on them give nothing (`PA/poly_L.md`).
- **Wich Cor 3.20/3.21 on fixed slices.** Primitivity forces proportional loops (`PA/poly_S4W.md`).
- **Forcing high degree d_σ > k.** Ito refinement makes every d_σ = 0 (`PA/poly_S3D.md`).
- **Morphic self-similarity.** Transfer along codes is exact, so it gives no amplification (`PA/poly_S4M.md`).
- **Reduction to known inherently exponentially ambiguous CFLs.** By Fine–Wilf and conjugacy, local defects do not
  survive insertion of a non-commuting factor (`PA/poly_S4I.md`).

**Slices**
- **Fixed-block slices, R_m alone, squarefree n, prime-power n.** All are capped at about linear ambiguity.
- **Nested R_m.** Gives only L^{<1}.
- **Spacers, slice congruences, box averaging** for the length gap (`PA/poly_R3a.md`, `PA/poly_G3.md`).
- **Witnesses of exponential length.** Useless by the budget in §4.4.

**Geometry of the candidate**
- **Pure convex geometry.** It cannot give superpolynomial ply; laminarity must be used.
- **A single symmetric or near-vertex base point.** It forces nothing (`PA/poly_S2W.md`, `PA/poly_S3V.md`).
- **Order-cone selection for TILE_k.** Dead.
- **Lemma X.** It does not extend to residue classes of size > 2 (`PA/poly_T2a.md` §3). Do not assume it.

**Constructive (affirmative)**
- **One witness per prime.** Fails on single-defect words when n has ≥ 2 primes. A canonical laminar choice is
  impossible (Lemma A, `PA/poly_A2.md`).
- **Small grammars.** A SAT search found grammars with ≤ 5 nonterminals match Q only up to length 5
  [computational] (`PA/poly_S4S.md`).
- **Explicit covers.** An n = 6 cover with ply ≤ 5 is known (`PA/poly_S2K.md`). At n = 30, the cube certificate is
  not laminar (`PA/poly_S4T.md`, `PA/poly_S4U.md`).

**Unverified citations**
- Kászonyi–Katsura is cited only second-hand (`context-free/reports/devil.md` §4) as "Q ∩ (ab*)ⁿ is CF when n has
  ≤ 3 prime powers". Verify before relying on it. `R4/kk.md` has the audited near-constant-region result.

**Not done yet**
- The test grammars `R4/walk.md` (first-passage substitution) and `R4/builder3.md` (union 𝒰) were never measured
  for ambiguity growth. They were missing from the previous campaign's branch.

---

## 7. What does not count

- Reproving that Q is not finitely ambiguous, not linear, not unambiguous, or not in FR.
- A lower bound for one fixed k, or finitely many k. Bounds like Theorem P, or Ω(log L), are not the target.
- Total or average ambiguity bounds.
- Lower bounds for one grammar or one natural family.
- Restricted-class results, unless it is proved that every polynomially ambiguous grammar for Q falls in the class.
- Operations not proved to preserve tree counts. Only DFA products, CNF conversion, and the exact transfers listed
  in §5 are allowed.
- Slice families already capped (§6).
- Counting sandwiches.
- PDA run counts without an exact translation to derivation trees.
- For the affirmative: grammars correct only on some lengths, or bounded only on typical words.
- Computation presented as proof.
- Reductions to unproved statements of comparable strength, including non-context-freeness of Q, an unverified form
  of a citation, or Lemma G* itself presented as proved.

---

## 8. Permitted tools

Standard theory, stated with exact hypotheses:
- CFG normal forms and their effect on tree counts;
- the Bar-Hillel product with a DFA;
- pumping, Ogden and interchange lemmas;
- Parikh's theorem and semilinear sets;
- vector partition functions (Sturmfels, Brion–Vergne);
- Chomsky–Schützenberger enumeration and algebraic series;
- Ginsburg–Ullian bounded languages;
- Wich's results as recorded in §4.1;
- combinatorics on words: Lyndon–Schützenberger, Fine–Wilf, conjugacy, Lyndon factorization;
- geometry of numbers: Minkowski, Siegel, small solutions of integer programs.

Local results may be used with their status labels.

Public search may be used only for ordinary mathematical background, standard named theorems, and checking a
citation. Do not search for a solution to this exact problem.

---

## 9. How to use agents

Up to **5** concurrent agents.

**Discipline (overrides any instruction to "use agents aggressively")**
- **Concise, distinct tasks.** Each agent targets one precise lemma, obstruction, construction or audit. Never give
  two agents the same question.
- **No repeated background.** Pass file paths and section references, not file contents or this prompt's
  background.
- **No reopening.** Do not reopen a route in §6 without new evidence, stated in one line.
- **Compact returns.** At most about 250 words plus formulas, in the form
  *claim / status label / proof or exact gap / file refs*. No narrative.
- **Shared registry.** Use one registry file, `polynomial-ambiguity/round2/REGISTRY.md`, holding:
  - approach families and their status;
  - proved lemmas with labels;
  - blocked routes with reasons;
  - computed tables.

  Agents read only the lines relevant to them and append at most a few lines.
- **Reports and scripts.** Each agent writes its report to `polynomial-ambiguity/round2/reports/<task>.md` and its
  scripts to `polynomial-ambiguity/round2/scripts/`. Computational agents return tables and certificates, not
  logs, and results are never recomputed.
- **Selective reading.** Long reports are read once by one agent, who records a short summary in the registry.
- **Early stopping.** An agent that reaches a blocked lemma stops and reports one line.
- **Diversity.** Group approaches by mechanism: structural, ply / covering, length / lattice, analytic,
  reformulation, constructive.
  - If several agents converge on one mechanism, redirect some of them elsewhere.
  - Keep at least one agent on the affirmative or constructive side in every round.
  - Do not tell early agents the favoured approach.
- **Synthesis.** After each round, the root writes at most 15 lines in the registry, then launches the next round.
  Do not stop after one failed wave.
- **Commits.** Commit and push agent outputs after each round.

**Audits are gated**
- Audit only a candidate that claims to close a named gap (TILE_k, G3**, Lemma G*, or the full theorem), and that
  has passed the proposer's own check against the audit list.
- Use one auditor per candidate. Add a second only if the first reports a disputed step.
- Auditors report the first fatal flaw and stop.
- Never audit negative findings, summaries or exploratory computations.

**Audit checklist**
- per-word versus total ambiguity;
- C and k uniform in all parameters;
- polynomial in |w|, not in a slice parameter;
- witness length inside the budget of §4.4;
- cycle-free grammars and exact tree counting;
- only DFA products, CNF and the exact transfers of §5 as reductions;
- the exact form of Wich's results and of local results, with labels;
- laminarity actually used, and Lemma X not over-extended;
- realisability of covers by an actual grammar where it is claimed;
- off-by-one errors, the words aⁿ, and length-1 words;
- computation presented as proof;
- circular use of an equivalent statement (§5);
- unrefereed or second-hand claims used without reconstruction.

**Suggested first-round targets** (choose and adapt; one agent each)
- **TILE_k, lower bound.** Prove that any finite family of tree-validity cones covering U_{>0} has a point in
  P_N^{Ω(1)} cones, using the fold lemma and non-crossing structure. Or construct a p_k^{O(1)} tiling.
- **G3**, upper bound.** Bound apex, covering radius and inradius for the ply-sets that arise on S_N, using the
  specific facets μ_k = (1 − T^{n/p_k}) ∏_{j≠k}(1 − T^{P_N p_j}) ν_k of `PA/poly_LAM.md` §2.
- **Audit-style reconstruction of Theorem P's chain.** This is not a gated audit. Reconstruct Lemma 3P and
  Lemma F, since everything rests on them.
- **Affirmative.** A polynomially ambiguous construction for Q ∩ (ab*)^{30} or the product region of S_2. Or prove
  that none exists with laminar pieces.
- **Test grammars.** Measure `R4/walk.md` and `R4/builder3.md` (task G, never done).
- **A genuinely new mechanism** not listed in §6.

---

## 10. Termination

Return when the problem is completely resolved in the sense of §3 and the argument has survived a gated audit.

Spend at least **30** minutes before considering stopping. If after **1** hour no route has been unblocked, stop
and return:
1. the strongest rigorously proved statement, with proof and status label;
2. the exact remaining gap, as one precise lemma with all notation defined;
3. the registry of approach families, with where and why each stalled;
4. witness families and counterexamples found.

Before that point, do not return partial results, reductions, fixed-k bounds, restricted-class theorems, counting
calculations or summaries.
