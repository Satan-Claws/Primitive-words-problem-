# r18_am.md — R18-A: average exit-slide multiplicity (AM)

Status:
- **(AM) is NOT proved.** The survival estimate (a desynchronised follower parse dies geometrically) has no proof in
  general. In particular the giant-block risk is not controlled.
- **New, written proof.** (AM) is replaced by a **weaker summed criterion (AM′)** about the *top-divergence pair mass*
  D₀, together with an exact renewal identity for E_n[m]:
  - AM ⇒ AM′, and AM′ suffices for G-trunk;
  - Σ_k D₀(k) < ∞ is *necessary* for tightness.
- **Numerics: a WARNING against (AM).** These are sanity checks, **not** a proof.
  - Many critical candidates with slides violate IF at depth 15–17, so they are exponentially ambiguous.
  - But SH3 and SH6 (Example S plus Dyck tokens, exactly critical, β₀ = ½) are **IF-clean through depth 19**, and their
    sampled E_n[m] **grows**: SH3 gives 1.23 / 1.40 / 1.90 / 2.88 for n = 50 / 100 / 200 / 400.
  - E_n[m] − 1 roughly doubles per doubling of n, which is faster than the N^{β₀} = n^{1/2} that (AM) allows.
  - **Resolved for SH3: it violates IF at depth 21, so it has C_exp.** Its growth is the exponential-ambiguity
    signature, not a counterexample to (AM).
  - **SH6 is IF-clean through depth 21** (`scripts/r18_am_if21_SH6.txt`), and its E_n[m] grows 1.32 → 3.91 for
    n = 50 → 400. SH6 is therefore a **live candidate counterexample to (AM)**, unless it has a deeper IF violation.
    Deciding whether SH6 has C_exp (by a decision procedure, not bounded search) is the top follow-up.
  - **Pattern.** Every critical candidate with slides tested so far eventually violates IF (depths 15–21), and on
    those E_n[m] grows. This is consistent with Conjecture CR.
- **Caveat on r17 Example S.** Its token masses are Σ2^{−|u|−|v|} = 7/16 < 1, so it is **subcritical** under the true
  measure. The r17 "uniform token law" numerics are not of the problem's form (equal weights 2^{−|W|} per word). In the
  true setting, Example S does not arise as a critical SCC.

Scripts (all in `scripts/`):
- `r18_am_lib.py`:
  - enumeration of trees for X → uXv | w, with sides literal or a prime-Dyck block B (mass 1/2, tail k^{−3/2});
  - an exact sampler conditioned on length n;
  - multiplicity counting by an O(n²) interval DP (B is a bifix code, so each side has at most one block match per
    position);
  - an IF checker.
- `r18_am_search.py`, `r18_am_search2.py` (output `r18_am_search2_out16.txt`): searches for critical IF-clean SCCs.
- `r18_am_num.py`: `if` / `enum` / `samp` modes. Output `r18_am_samp_SH1.txt`.

## 1. Setting
- C is a linear critical SCC; X ∈ C is the root of the pair family 𝒫 with context (p, q) and exit w.
- A **token** is a first-return pumping tree X ⇒* uXv. By IF (r17_gstruct Cor (c)) together with SU, a token is
  determined by its interface (u, v), so T ⊂ Σ*×Σ* with π(u, v) = 2^{−|u|−|v|} and Σ_T π = 1.
- r(j) := Σ{Π π(τᵢ) : token sequences of total length j}, with r(0) = 1. This is the renewal sequence, and
  R(N) := Σ_{j≤N} r(j) ≍ U(N) ≍ N^{β₀}.
- Tree mass at length n: u(n) = κ·r(n − c₀), where κ = 2^{−|p|−|q|−|w|} and c₀ = |p| + |q| + |w|.
- **Top-divergence pair mass.** D₀(k) := Σ 2^{−k} over *ordered* pairs (s, s′) of X-trees with exit w that have the
  same yield of length k and **different first tokens**. "First token" means the first first-return token, or the
  exit if the tree has no token. S₀(N) := Σ_{k≤N} D₀(k).

## 2. Exact identity and the criterion AM′ [written proof]
**Lemma D (decomposition of pairs).** For every n,
  u(n)·(E_n[m] − 1) = 2^{−|p|−|q|} Σ_j r(j) D₀(n − c_ctx − j), where c_ctx = |p| + |q|.

*Proof.*
1. u(n)E_n[m] = Σ_{|t|=n} 2^{−n} m(t) = Σ 2^{−n} over ordered pairs (t, t′) ∈ 𝒫² with W(t) = W(t′) and length n.
2. The diagonal pairs t = t′ contribute u(n).
3. Let t ≠ t′. Their token sequences share a longest common prefix τ₁…τ_d, which may be empty. Both trees then contain
   an X-node at depth d with the same span, because the context is fixed and the shared tokens have fixed lengths.
4. Below that node the two subtrees have the same yield M′, and their first tokens (or exits) differ, by maximality of
   d.
5. Conversely, a shared prefix plus a top-diverged pair for M′ gives a pair in 𝒫 with t ≠ t′.
6. This decomposition is a bijection, and the weight factorises as 2^{−|p|−|q|}·Π π(τᵢ)·2^{−|M′|}. ∎

(Lemma NR is not needed for the identity. It says only that below the divergence the two trees never share a spine
node.)

**Prop AM′.** If S₀(N) = o(R(N)), then the two-sided level critical SCC is impossible in G⁻. This holds in particular
if D := Σ_k D₀(k) < ∞.

*Proof.*
1. By Cauchy–Schwarz, over the summed measure,
   Σ_{|t|≤N} 2^{−|t|}/m(t) ≥ U(N)² / Σ_{|t|≤N} 2^{−|t|} m(t).
2. By Lemma D the denominator is ≤ U(N) + 2^{−|p|−|q|} R(N) S₀(N) ≤ U(N)(1 + c S₀(N)).
3. So the word mass of 𝒫 up to N is ≥ U(N)/(1 + cS₀(N)), which tends to ∞.
4. This contradicts G-word (word mass ≤ c), exactly as in r17_gtrunk Prop AM. ∎

**Relations.**
- AM ⇒ AM′. Indeed Σ_{n≤N} u(n)E_n[m] ≤ U(N)·max E_n[m] = o(U(N)N^{β₀}) = o(U(N)²), and step 1 above needs exactly
  this.
- AM′ needs neither the max over n nor the per-n conditioning. This removes all regularity issues of E_n.
- **Necessity of D < ∞ for tightness.** Let r be regularly varying with index β₀ − 1 ∈ (−1, 0], so that
  r(n − k) ≥ c·r(n) for k ≤ n/2. Then Lemma D gives E_n[m] − 1 ≥ c′ Σ_{k≤n/2} D₀(k). So sup_n E_n[m] < ∞ ⇒ D < ∞.
  Conversely, D < ∞ is enough for G-trunk via AM′.
- So the natural target is **D < ∞**. In words: the expected number of top-diverged partners, summed over the
  unconditioned (infinite) renewal measure, is finite.

## 3. Toward D < ∞: what is proved and what is missing
**Proved (bookkeeping).**
- D₀(k) ≤ (k + 1)·u_X(k). This is trivial (at most one partner per exit position), and useless: it gives
  S₀ ≲ N^{1+β₀}.
- In a top-diverged pair, the exits have different positions, so |U| ≠ |U′| (otherwise IF + Lemma 1 give s = s′). By
  NR, no X-node span is shared.

**The pair process and the exact gap.**
- Run both parses in parallel: the parse that is behind on the left must spell a "debt" word already committed by the
  other parse, and likewise on the right.
- The state is (debt_L, debt_R, which parse leads on each side).
- Steps that only consume debt have weight factor 1. Fresh letters cost 2^{−1} each. The total weight is 2^{−|M|}.

The missing estimate is:
- **(SURV)**: Σ over paths of desynchronised states < ∞.
- **Finite-debt case, partial.** With finitely many tokens and debts bounded by D, the state space is finite. Then
  D₀(k) ≤ (k + 1)·P_π(an i.i.d. token sequence admits a desync follower for its first ≈k letters).
  - A finite NFA under i.i.d. input survives either with exponentially decaying probability or with positive
    probability forever.
  - In the first alternative, D < ∞ follows (written proof, standard Markov-chain-with-killing argument after
    determinisation).
  - The second alternative ("from some debt state every continuation is followable") could **not** be excluded. The
    counting attempt (IF-injectivity of t ↦ (follower, end state)) fails, because sequences of n ± O(D) letters have
    the same renewal mass. No contradiction comes out of counting alone.
- **Unbounded debt (Example-S-type growing overhang) and giant blocks.** Untreated. A Dyck block re-parsed by light
  tokens creates a debt of length up to the block length on the opposite side. Its survival is not controlled.

## 4. Numerics [scripts; plain sanity checks, not proofs]
**Searches for IF-clean critical SCCs.**
- Random critical literal-only token sets (lengths ≤ 6, `r18_am_search.py`): **0 of 20 000** are IF-clean even to
  depth 11.
- With one Dyck token, 16 of about 10⁴ pass to depth 11, some with slides.
- With Example S plus two Dyck tokens plus a literal fill to exact criticality (`r18_am_search2.py`), several pass at
  depth 13, with E₁₄[m] ≈ 1.03–1.10.

**Deeper IF checks fail.** Every candidate with slides that I re-checked violates IF at depth 15–17, so it has C_exp:
- H1, H2, H3: violations at depth ≤ 15;
- SH1 = S + {(a,B), (B,aa), (ε,bbb), (a,baa)}: violation at 17;
- SH2: violation at 17.
- The violating pairs are explicit in the script output, for example SH1:
  (bb,a)(ab,ab)(a,baa)(ε,ba)(a,baa) vs (ε,ba)(bb,a)(ab,aa)(a,ab)(a,ab)(ε,ba).
- The sweep `r18_am_search2.py 16` (output `r18_am_search2_out16.txt`, stopped early) gave 5 candidates.
  - SH4 and SH5 violate IF at depth 19.
  - **SH3** = S + {(a,B), (B,aa), (a,bb), (ab,bb)} and **SH6** = S + {(a,B), (B,bb), (a,bb), (ab,aa)}, with w = ab, are
    **IF-clean to depth 19**.
  - Sampling (`r18_am_samp_SH3.txt`, `r18_am_samp_SH6.txt`; 300 samples per n), for n = 50 / 100 / 200 / 400:

    | | E_n[m] | P(m ≥ 2) | max m |
    |---|---|---|---|
    | SH3 | 1.23 / 1.40 / 1.90 / 2.88 (±0.14 at 400) | 0.19 → 0.65 | 4 → 16 |
    | SH6 | 1.32 / 1.74 / 2.57 / 3.91 (±0.17 at 400) | 0.29 → 0.80 | 4 → 17 |

  - E_n[m] − 1 grows roughly linearly in n, which is ≫ n^{β₀} = n^{1/2}.
  - **Update: SH3 violates IF at depth 21**:
    (bb,a)(a,ab)³(bb,a)(a,ab)(bb,a) vs (ε,ba)³(bb,a)(ε,ba)(B=aaabbabb, aa).
    So SH3 has C_exp and is not a counterexample. SH6 is IF-clean to depth 21, so it is a live candidate counterexample.
  - Depth-21 IF checks were started: `scripts/r18_am_if21_SH3.txt`, `scripts/r18_am_if21_SH6.txt`. Resolving this is
    the first follow-up. A general C_exp test (Wich's criterion / a pair-automaton argument), not bounded-depth search,
    is needed.

**SH1, which is exponentially ambiguous** (exact enumeration to k = 20; sampling n ≤ 400, 300 samples each):

| quantity | values |
|---|---|
| u(k) | ≈ k^{−1/2} (heavy, β₀ = ½) |
| S₀(20) | 0.022 |
| U(20) | 1.21 |
| word mass | 1.18 ≈ U/(1 + S₀) |
| E_n[m], n = 50 / 100 / 200 / 400 | 1.23 / 1.44 / 2.05 / 3.33 |
| max m | 4 → 53 |

- So E_n[m] **grows** once n is past the IF-violation depth. This fits the expectation that C_exp shows up as growing
  mean multiplicity.
- Small-n enumeration (k ≤ 20) cannot distinguish the cases. Only n ≳ 100 does.

## 5. Conjecture CR (critical rigidity) [conjecture, numerical support only]
In a critical linear SCC (Σ_T 2^{−|u|−|v|} = 1, lower blocks unambiguous), IF-freeness up to all depths forces D < ∞.
Possibly it even forces the exit slides to be confined to a set of trees of finite total mass.
- **Heuristic.** Under exact criticality, a desynchronised follower that survives with positive probability has
  enough token "mass" to close a loop at equal debt state with two distinct t-segments. That would be an IF violation,
  which is what the searches keep finding.
- Subcritical sets (Example S, 7/16) are not covered, and they do have Θ(n) slides. But they cannot be critical SCCs.
- If CR holds, then AM′ holds, G-trunk (two-sided level) closes, and so does the trunk case of T8_poly.

## Status
| claim | label |
|---|---|
| Lemma D: u(n)(E_n[m] − 1) = 2^{−\|p\|−\|q\|}(r ∗ D₀)(n − c_ctx) | written proof |
| Prop AM′: S₀(N) = o(R(N)) ⇒ two-sided level case impossible; AM ⇒ AM′ | written proof (uses G-word, Lemma R) |
| tightness ⇒ D < ∞ (r regularly varying) | written proof |
| finite-debt, finite-token: D < ∞ unless some debt state is "always followable" | written proof of the dichotomy; second branch OPEN |
| r17 Example S is subcritical under the true measure | checked (7/16) |
| critical candidates with slides found so far all violate IF (depth 15–17); SH1 has E_n[m] growing | numerics |
| Conjecture CR (critical + IF-free ⇒ D < ∞) | conjecture; every critical slide-candidate tested so far eventually violates IF (SH3 at depth 21); **SH6 IF-clean to depth 21 with E_n[m] growing: a live threat** |
| SH3/SH6: E_n[m] growing ≈ linearly; SH3 has C_exp (IF violation at depth 21); SH6 IF-clean to depth 21 (live candidate counterexample) | numerics |
| (AM) / (AM′) in general, giant-block re-parse | **OPEN** (exact gap: (SURV), §3) |
